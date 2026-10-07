#!/usr/bin/env python3
"""
NETR Online Public Records Complete Scraper
Using BeautifulSoup4 and Requests / ThreadPoolExecutor

Scrapes all states, counties, and municipal public record sources from:
https://publicrecords.netronline.com/

Extracts:
- State Name, State Code, State Directory URL
- State-level portals (State Official Website, UCC Search, Corporation/Sunbiz/SOS search)
- Counties (Name, Slug, NETR County URL, GIS Map URL)
- Public Record Offices per County:
  * Recorder / Clerk of Court / Deed Registry (Office Name, Phone, Direct Portal Search URL)
  * Assessor / Property Appraiser / CAD (Office Name, Phone, Direct Portal Search URL)
  * Tax Collector / Treasurer (Office Name, Phone, Direct Portal Search URL)
  * GIS / Mapping portals
"""

import os
import re
import sys
import json
import csv
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

# Set UTF-8 encoding on Windows standard outputs
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://publicrecords.netronline.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

session = requests.Session()
session.headers.update(HEADERS)


def get_soup(url, max_retries=3, backoff=1.5):
    """Fetch URL with retry logic and return BeautifulSoup object."""
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=20)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            elif response.status_code == 404:
                return None
            time.sleep(backoff * (attempt + 1))
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[Error] Failed fetching {url}: {e}", file=sys.stderr)
                return None
            time.sleep(backoff * (attempt + 1))
    return None


def scrape_all_states():
    """Scrape the root homepage to discover all 50 states + DC."""
    print(f"[*] Fetching homepage: {BASE_URL}")
    soup = get_soup(BASE_URL)
    if not soup:
        raise RuntimeError("Failed to fetch NETR homepage.")

    states = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        match = re.search(r"/state/([A-Za-z]{2})$", href)
        if match:
            state_code = match.group(1).upper()
            state_name = a.get_text(strip=True)
            if state_code not in seen and state_name:
                seen.add(state_code)
                full_url = urljoin(BASE_URL, href)
                states.append({
                    "state_code": state_code,
                    "state_name": state_name,
                    "state_url": full_url
                })

    # Sort states alphabetically by code
    states.sort(key=lambda s: s["state_code"])
    print(f"[+] Found {len(states)} states.")
    return states


def scrape_state_details(state_url):
    """Scrape a state page for state-level links and all county links."""
    soup = get_soup(state_url)
    if not soup:
        return {"state_links": {}, "counties": []}

    state_links = {}
    counties = []
    seen_counties = set()

    # Look for state-level agency links (e.g. UCC, Corporations, Official State Website)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if any(term in text.lower() for term in ["official state website", "ucc", "corporation", "sunbiz", "secretary of state"]):
            state_links[text] = href

    # Look for county links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        county_name = a.get_text(strip=True)
        if "/county/" in href and county_name:
            # Clean county name
            if county_name not in seen_counties:
                seen_counties.add(county_name)
                full_url = urljoin(BASE_URL, href)
                counties.append({
                    "county_name": county_name,
                    "county_url": full_url
                })

    return {
        "state_links": state_links,
        "counties": counties
    }


def scrape_county_details(county_url):
    """Scrape a county page for offices, phone numbers, direct data links, and GIS maps."""
    soup = get_soup(county_url)
    if not soup:
        return {"offices": [], "gis_map_url": None, "historic_aerials_url": None}

    offices = []
    gis_map_url = None
    historic_aerials_url = None

    # Check for Map / Aerials links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True).lower()
        if "map.netronline.com" in href or text == "map":
            gis_map_url = href
        elif "historicaerials.com" in href:
            historic_aerials_url = href

    # Locate the office table rows (.div-table or standard tables)
    rows = soup.find_all("div", class_=lambda c: c and "div-table-row" in c and "responsive" in c)
    if not rows:
        # Fallback to any div-table-row
        rows = soup.find_all("div", class_=lambda c: c and "div-table-row" in c)

    for row in rows:
        cols = row.find_all("div", class_=lambda c: c and "div-table-col" in c)
        if len(cols) >= 3:
            name_col = cols[0].get_text(strip=True)
            phone_col = cols[1].get_text(strip=True)
            online_col = cols[2]

            # Skip header row
            if "name" in name_col.lower() and "phone" in phone_col.lower():
                continue

            # Extract data link if present
            online_link = None
            link_tag = online_col.find("a", href=True)
            if link_tag and link_tag["href"] and link_tag["href"] != "#":
                online_link = link_tag["href"]

            # Classify office type
            name_lower = name_col.lower()
            office_type = "Other"
            if any(k in name_lower for k in ["recorder", "clerk", "deed", "register of deeds", "court"]):
                office_type = "Recorder / Clerk"
            elif any(k in name_lower for k in ["assessor", "appraiser", "cad", "evaluation", "valuation"]):
                office_type = "Assessor / Appraiser"
            elif any(k in name_lower for k in ["tax", "treasurer", "collector"]):
                office_type = "Tax Collector / Treasurer"
            elif any(k in name_lower for k in ["gis", "map", "surveyor"]):
                office_type = "GIS / Mapping"

            if name_col:
                offices.append({
                    "office_name": name_col,
                    "office_type": office_type,
                    "phone": phone_col if phone_col and phone_col != "-" else None,
                    "online_portal_url": online_link
                })

    return {
        "offices": offices,
        "gis_map_url": gis_map_url,
        "historic_aerials_url": historic_aerials_url
    }


def scrape_single_state_full(state_info, delay=0.2):
    """Scrape a single state along with all its counties and offices."""
    state_code = state_info["state_code"]
    state_name = state_info["state_name"]
    state_url = state_info["state_url"]

    print(f"[*] Processing State: {state_name} ({state_code})...")
    state_data = scrape_state_details(state_url)
    state_links = state_data["state_links"]
    counties_list = state_data["counties"]

    scraped_counties = []
    for c in counties_list:
        county_name = c["county_name"]
        county_url = c["county_url"]
        
        c_details = scrape_county_details(county_url)
        scraped_counties.append({
            "county_name": county_name,
            "county_url": county_url,
            "gis_map_url": c_details["gis_map_url"],
            "historic_aerials_url": c_details["historic_aerials_url"],
            "offices": c_details["offices"]
        })
        time.sleep(delay)

    print(f"[✓] Completed {state_name}: {len(scraped_counties)} counties scraped.")
    return {
        "state_code": state_code,
        "state_name": state_name,
        "state_url": state_url,
        "state_links": state_links,
        "total_counties": len(scraped_counties),
        "counties": scraped_counties
    }


def save_results(all_data, json_filepath="netr_scraped_records.json", csv_filepath="netr_scraped_records.csv"):
    """Export the scraped dataset to JSON and CSV formats."""
    # 1. Save JSON
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Saved complete JSON data to: {json_filepath}")

    # 2. Flatten and save CSV
    csv_rows = []
    for state in all_data:
        st_code = state["state_code"]
        st_name = state["state_name"]
        for county in state.get("counties", []):
            co_name = county["county_name"]
            co_url = county["county_url"]
            gis_map = county.get("gis_map_url") or ""
            
            offices = county.get("offices", [])
            if not offices:
                csv_rows.append({
                    "State Code": st_code,
                    "State Name": st_name,
                    "County Name": co_name,
                    "NETR County URL": co_url,
                    "GIS Map URL": gis_map,
                    "Office Name": "",
                    "Office Type": "",
                    "Phone": "",
                    "Online Portal URL": ""
                })
            else:
                for off in offices:
                    csv_rows.append({
                        "State Code": st_code,
                        "State Name": st_name,
                        "County Name": co_name,
                        "NETR County URL": co_url,
                        "GIS Map URL": gis_map,
                        "Office Name": off.get("office_name", ""),
                        "Office Type": off.get("office_type", ""),
                        "Phone": off.get("phone", ""),
                        "Online Portal URL": off.get("online_portal_url", "")
                    })

    if csv_rows:
        with open(csv_filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"[+] Saved flattened CSV data ({len(csv_rows)} records) to: {csv_filepath}")


def main():
    parser = argparse.ArgumentParser(description="Scrape publicrecords.netronline.com using BeautifulSoup")
    parser.add_argument("--state", type=str, help="Specific state code (e.g. FL, TX, CA) to scrape")
    parser.add_argument("--county", type=str, help="Specific county name (e.g. Bradford, Travis)")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent worker threads")
    parser.add_argument("--output", type=str, default="netr_scraped_records.json", help="Output JSON path")
    args = parser.parse_args()

    print("=========================================================")
    print("  NETR Online Public Records BeautifulSoup Scraper")
    print("=========================================================")

    all_states = scrape_all_states()

    if args.state:
        target_state = args.state.upper().strip()
        matched = [s for s in all_states if s["state_code"] == target_state]
        if not matched:
            print(f"[!] State '{target_state}' not found.")
            sys.exit(1)
        all_states = matched

    if args.county and len(all_states) == 1:
        state_info = all_states[0]
        state_data = scrape_state_details(state_info["state_url"])
        matched_counties = [c for c in state_data["counties"] if args.county.lower() in c["county_name"].lower()]
        if not matched_counties:
            print(f"[!] County '{args.county}' not found in {state_info['state_name']}.")
            sys.exit(1)
        
        county_obj = matched_counties[0]
        print(f"[*] Scraping specific county: {county_obj['county_name']} ({state_info['state_code']})")
        c_details = scrape_county_details(county_obj["county_url"])
        
        single_res = {
            "state_code": state_info["state_code"],
            "state_name": state_info["state_name"],
            "state_url": state_info["state_url"],
            "state_links": state_data["state_links"],
            "county_name": county_obj["county_name"],
            "county_url": county_obj["county_url"],
            "gis_map_url": c_details["gis_map_url"],
            "historic_aerials_url": c_details["historic_aerials_url"],
            "offices": c_details["offices"]
        }
        print("\n" + json.dumps(single_res, indent=2))
        return

    # Multithreaded or sequential scraping across states
    results = []
    if args.workers > 1 and len(all_states) > 1:
        print(f"[*] Running concurrent scrape with {args.workers} worker threads...")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_state = {executor.submit(scrape_single_state_full, s): s for s in all_states}
            for future in as_completed(future_to_state):
                state_data = future.result()
                results.append(state_data)
    else:
        for s in all_states:
            res = scrape_single_state_full(s)
            results.append(res)

    # Sort results by state code
    results.sort(key=lambda x: x["state_code"])
    save_results(results, json_filepath=args.output, csv_filepath=args.output.replace(".json", ".csv"))
    print("\n[✓] Scraping process completed successfully!")


if __name__ == "__main__":
    main()
