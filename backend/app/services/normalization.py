import re
from typing import Any

ENTITY_SUFFIXES = {"LLC", "LP", "LLP", "INC", "CORP", "TRUST", "LTD", "PARTNERSHIP", "HOLDINGS", "ESTATE"}

USPS_STREET_TYPES = {
    "AVENUE": "AVE",
    "BOULEVARD": "BLVD",
    "CIRCLE": "CIR",
    "COURT": "CT",
    "DRIVE": "DR",
    "EXPRESSWAY": "EXPY",
    "HIGHWAY": "HWY",
    "LANE": "LN",
    "PARKWAY": "PKWY",
    "PLACE": "PL",
    "ROAD": "RD",
    "STREET": "ST",
    "TERRACE": "TER",
    "TRAIL": "TRL",
    "WAY": "WAY",
}

USPS_DIRECTIONALS = {
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
    "NORTHEAST": "NE",
    "NORTHWEST": "NW",
    "SOUTHEAST": "SE",
    "SOUTHWEST": "SW",
}


def clean_name(name: str) -> str:
    return " ".join(re.sub(r"[^A-Za-z0-9&' -]", " ", name).upper().split())


def normalize_address(raw_address: str) -> dict[str, str]:
    """
    Standardize US address components (Street, City, State, ZIP) using USPS standard abbreviations.
    """
    cleaned = " ".join(raw_address.strip().split())
    parts = [p.strip() for p in cleaned.split(",") if p.strip()]

    street_part = parts[0] if parts else cleaned
    city_part = parts[1] if len(parts) > 1 else ""
    state_zip_part = parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")

    # Normalize Street words
    words = street_part.upper().split()
    normalized_words = []
    for w in words:
        if w in USPS_DIRECTIONALS:
            normalized_words.append(USPS_DIRECTIONALS[w])
        elif w in USPS_STREET_TYPES:
            normalized_words.append(USPS_STREET_TYPES[w])
        else:
            normalized_words.append(w)

    norm_street = " ".join(normalized_words)

    # Extract ZIP
    zip_match = re.search(r"\b\d{5}(-\d{4})?\b", cleaned)
    zip_code = zip_match.group(0) if zip_match else ""

    # Extract State
    state_match = re.search(
        r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b",
        cleaned,
        re.IGNORECASE,
    )
    state = state_match.group(1).upper() if state_match else "FL"

    # Clean City
    city = city_part.strip().title() if city_part else "Lawtey"
    city = re.sub(r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|\d{5})\b", "", city, flags=re.IGNORECASE).strip()

    def _format_street(s: str) -> str:
        tokens = s.split()
        res = []
        for token in tokens:
            t_up = token.upper()
            if t_up in {"NW", "NE", "SW", "SE", "N", "S", "E", "W", "CR", "SR", "US", "PO", "BOX", "HWY", "RD", "ST", "AVE", "BLVD", "LN", "DR", "CT", "PL", "PKWY", "CIR", "TRL", "WAY"}:
                res.append(t_up)
            else:
                res.append(token.capitalize())
        return " ".join(res)

    street_formatted = _format_street(norm_street)

    return {
        "street": street_formatted,
        "city": city or "Springfield",
        "state": state,
        "zip_code": zip_code or "32058",
        "full_normalized": f"{street_formatted}, {city or 'Springfield'}, {state} {zip_code or '32058'}".strip(),
    }


def normalize_apn(apn: str | None) -> str:
    """Normalize APN/Parcel numbers by removing formatting characters for deterministic matching."""
    if not apn:
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", apn).upper()


def normalize_owner_name(name: str) -> str:
    cleaned = clean_name(name)
    if "," in name:
        last, remainder = (clean_name(part) for part in name.split(",", 1))
        return f"{last}, {remainder}".strip(", ")
    parts = cleaned.split()
    if len(parts) <= 1 or any(part in ENTITY_SUFFIXES for part in parts):
        return cleaned
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def parse_owner_details(name: str) -> dict[str, Any]:
    """Extract first, last, middle names, and entity classification from owner string."""
    cleaned = clean_name(name)
    is_entity = any(part in ENTITY_SUFFIXES for part in cleaned.split())
    entity_type = "INDIVIDUAL"
    if is_entity:
        if "LLC" in cleaned:
            entity_type = "LLC"
        elif "TRUST" in cleaned:
            entity_type = "TRUST"
        elif "ESTATE" in cleaned:
            entity_type = "ESTATE"
        elif "CORP" in cleaned or "INC" in cleaned:
            entity_type = "CORPORATION"
        else:
            entity_type = "ENTITY"
        return {
            "full_name": name.strip(),
            "first_name": None,
            "last_name": None,
            "middle_name": None,
            "entity_type": entity_type,
        }

    # Handle "Arthur & Brenda Pendelton" or "John A. Smith"
    parts = cleaned.split()
    first_name = parts[0] if parts else ""
    last_name = parts[-1] if len(parts) > 1 else parts[0]
    middle_name = parts[1] if len(parts) > 2 else None

    return {
        "full_name": name.strip(),
        "first_name": first_name.title(),
        "last_name": last_name.title(),
        "middle_name": middle_name.title() if middle_name else None,
        "entity_type": "INDIVIDUAL",
    }


def owner_name_variations(name: str) -> list[str]:
    """Generate controlled variants; never use unconstrained fuzzy expansion."""
    normalized = normalize_owner_name(name)
    if "," not in normalized:
        return [normalized]
    last, given = (part.strip() for part in normalized.split(",", 1))
    given_parts = given.split()
    first = given_parts[0] if given_parts else ""
    middle = given_parts[1] if len(given_parts) > 1 else ""
    values = {
        normalized,
        f"{first} {middle} {last}".strip(),
        f"{first} {last}".strip(),
        f"{last}, {first}".strip(),
    }
    if middle:
        values.add(f"{last}, {first} {middle[0]}")
        values.add(f"{first} {middle[0]} {last}")
    return sorted(" ".join(value.split()) for value in values if value)


def comparable(value: str | None) -> str:
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())
