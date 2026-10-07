# Title AI Automation & NETR Online Public Records Suite

An automated title examination and Current Owner Search (COS) platform combining a modern React frontend, FastAPI backend, US Census geocoding, and a real-time BeautifulSoup4 web scraper for NETR Online ([publicrecords.netronline.com](https://publicrecords.netronline.com/)).

---

## Features

- **Address-Driven Public Records Scraping**: Enter any US property address to automatically resolve county/state jurisdictions via the US Census Bureau and scrape direct links for:
  - County Clerk & Recorder / Register of Deeds (Deeds, Mortgages, Liens)
  - County Property Appraiser & Assessor (APN, Valuations, Legal Descriptions)
  - County Tax Collector & Treasurer (Ad Valorem Taxes, Delinquency Status)
  - County GIS Parcel Mapping & Historic Aerials
  - State UCC & Secretary of State Corporate Entity searches
- **Examiner-Assisted Title Search Engine**: Deterministic chain of title assembly, document matching, and review exception management.
- **Modern Responsive Frontend**: React 19, TypeScript, and Tailwind CSS v4 running on Vite.
- **FastAPI Backend**: Asynchronous title processing pipeline with PostgreSQL/SQLAlchemy schemas.

---

## Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # REST endpoints for COS, PI, GI, & Chain-of-Title
│   │   ├── sources/
│   │   │   ├── netr_adapter.py    # Real-time geocoding & BeautifulSoup portal resolver
│   │   │   └── ...
│   │   └── main.py                # FastAPI application entrypoint
│   └── pyproject.toml
├── src/
│   ├── App.tsx                    # Main interactive title examination UI
│   ├── data/statesAndCounties.ts  # 50-state county database & slug resolvers
│   └── services/regridService.ts  # Regrid parcel API integration
├── scrape_by_address.py           # Address-to-NETR title dossier scraper
├── scrape_netr_complete.py        # Complete 50-state batch scraper
├── package.json
└── vite.config.ts
```

---

## Getting Started

### 1. Frontend Development Server

```bash
npm install
npm run dev
```

Preview locally at [http://localhost:8443/](http://localhost:8443/).

### 2. NETR Online Address Scraper CLI

Run with any US property address:

```bash
python scrape_by_address.py --address "4320 NW CR 225, Lawtey, FL 32058"
```

Or run interactive mode:

```bash
python scrape_by_address.py
```

### 3. Complete 50-State NETR Directory Scraper

Scrape an entire state or batch across worker threads:

```bash
# Single state
python scrape_netr_complete.py --state FL --output florida_records.json

# All 50 states (concurrent workers)
python scrape_netr_complete.py --workers 8 --output us_records.json
```

### 4. FastAPI Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Interactive OpenAPI docs: `http://localhost:8000/docs`