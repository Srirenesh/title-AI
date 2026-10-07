import re
from datetime import date, datetime
from typing import Any

from app.models import DocumentCategory, RecordType
from app.sources.base import (
    AssessorSourceResult,
    CourtSourceResult,
    GISSourceResult,
    PropertySourceResult,
    RecorderSourceResult,
    RecordSourceResult,
    TreasurerSourceResult,
)

KNOWN_MOCK_PROPERTIES: list[dict[str, Any]] = [
    {
        "address": "4320 NW CR 225, Lawtey, FL 32058",
        "street": "4320 NW CR 225",
        "city": "Lawtey",
        "county": "Bradford",
        "state": "FL",
        "zip_code": "32058",
        "apn": "12007-00418",
        "owner": "Arthur & Brenda Pendelton",
        "first_name": "Arthur",
        "last_name": "Pendelton",
        "legal_description": "COM AT INTERSECTION OF CR 225 & NW 43RD ST, THENCE N 450 FT FOR POB, LOT 4, BRADFORD PINES SUBDIVISION, PLAT BOOK 3, PAGE 18, BRADFORD COUNTY, FL",
        "zoning": "AG-1 Agricultural/Residential",
        "year_built": 1998,
        "use_code": "0100 - Single Family Residential",
        "assessed_value": 315000.0,
        "land_value": 85000.0,
        "improvement_value": 230000.0,
        "market_value": 345000.0,
        "acreage": 2.5,
        "lot": "4",
        "block": "1",
        "subdivision": "Bradford Pines",
        "prior_owners": ["Robert M. Sterling", "Lawtey Pineview Estates, LLC"],
    },
    {
        "address": "123 Main Street, Austin, TX 78701",
        "street": "123 Main Street",
        "city": "Austin",
        "county": "Travis",
        "state": "TX",
        "zip_code": "78701",
        "apn": "123-456-789",
        "owner": "John A Smith",
        "first_name": "John",
        "last_name": "Smith",
        "legal_description": "LOT 12, BLOCK B, SAMPLE HEIGHTS SUBDIVISION, PLAT BOOK 4, PAGE 22, TRAVIS COUNTY, TEXAS",
        "zoning": "SF-3 Single Family",
        "year_built": 2012,
        "use_code": "A1 - Real, Residential Single-Family",
        "assessed_value": 685000.0,
        "land_value": 240000.0,
        "improvement_value": 445000.0,
        "market_value": 720000.0,
        "acreage": 0.28,
        "lot": "12",
        "block": "B",
        "subdivision": "Sample Heights",
        "prior_owners": ["Robert Jones", "Anna Moore"],
    },
    {
        "address": "500 S Grand Ave, Los Angeles, CA 90071",
        "street": "500 S Grand Ave",
        "city": "Los Angeles",
        "county": "Los Angeles",
        "state": "CA",
        "zip_code": "90071",
        "apn": "5144-012-001",
        "owner": "Michael C. Henderson",
        "first_name": "Michael",
        "last_name": "Henderson",
        "legal_description": "LOT 1, TRACT NO. 24831, AS PER MAP RECORDED IN BOOK 340 PAGES 12 THROUGH 15 OF MAPS, RECORDS OF LOS ANGELES COUNTY, CA",
        "zoning": "C2 Commercial/Residential Mixed",
        "year_built": 2005,
        "use_code": "1100 - Commercial / Office",
        "assessed_value": 1450000.0,
        "land_value": 600000.0,
        "improvement_value": 850000.0,
        "market_value": 1620000.0,
        "acreage": 0.45,
        "lot": "1",
        "block": "3",
        "subdivision": "Downtown Financial Center",
        "prior_owners": ["Bunker Hill Properties LLC", "Pacific Trust Holdings"],
    },
    {
        "address": "84 Willow Creek Drive, Houston, TX 77002",
        "street": "84 Willow Creek Drive",
        "city": "Houston",
        "county": "Harris",
        "state": "TX",
        "zip_code": "77002",
        "apn": "041-283-000-0012",
        "owner": "Maria Garcia",
        "first_name": "Maria",
        "last_name": "Garcia",
        "legal_description": "LOT 8, BLOCK 4, WILLOW CREEK SECTION 2, HARRIS COUNTY, TX",
        "zoning": "Residential",
        "year_built": 2018,
        "use_code": "Single Family Residence",
        "assessed_value": 420000.0,
        "land_value": 110000.0,
        "improvement_value": 310000.0,
        "market_value": 450000.0,
        "acreage": 0.22,
        "lot": "8",
        "block": "4",
        "subdivision": "Willow Creek",
        "prior_owners": ["David & Sarah Martinez", "Harris Land Corp"],
    },
]


def find_matching_mock_property(
    address: str | None = None,
    apn: str | None = None,
    owner_first: str | None = None,
    owner_last: str | None = None,
    county: str | None = None,
    state: str | None = None,
) -> dict[str, Any] | None:
    # 1. Match APN exactly if provided
    if apn:
        clean_apn = re.sub(r"[^a-zA-Z0-9]", "", apn).lower()
        for p in KNOWN_MOCK_PROPERTIES:
            if re.sub(r"[^a-zA-Z0-9]", "", p["apn"]).lower() == clean_apn:
                return p

    # 2. Match Address
    if address:
        clean_addr = re.sub(r"[^a-zA-Z0-9\s]", "", address).lower().strip()
        for p in KNOWN_MOCK_PROPERTIES:
            clean_mock = re.sub(r"[^a-zA-Z0-9\s]", "", p["street"]).lower().strip()
            if clean_mock in clean_addr or clean_addr in clean_mock:
                return p

    # 3. Match Owner Last Name
    if owner_last:
        clean_last = owner_last.strip().lower()
        clean_first = owner_first.strip().lower() if owner_first else None
        for p in KNOWN_MOCK_PROPERTIES:
            mock_last = p.get("last_name", "").lower()
            mock_first = p.get("first_name", "").lower()
            if clean_last == mock_last:
                if not clean_first or clean_first in mock_first:
                    return p

    return None


def generate_synthetic_property(
    address: str, county: str, state: str, apn: str | None = None, owner: str | None = None
) -> dict[str, Any]:
    """Deterministically synthesize property data for any US address/county/state for uniform testing."""
    clean_addr = address.strip()
    st = state.strip().upper() if state else "FL"
    co = county.strip().title() if county else "Bradford"
    hash_val = abs(sum((idx + 1) * ord(c) for idx, c in enumerate(clean_addr + co + st)))

    street_parts = clean_addr.split(",")[0].strip()
    city = clean_addr.split(",")[1].strip() if len(clean_addr.split(",")) > 1 else "Springfield"
    zip_code = "32058"
    zip_match = re.search(r"\b\d{5}\b", clean_addr)
    if zip_match:
        zip_code = zip_match.group(0)

    synth_apn = apn or f"{hash_val % 89999 + 10000}-{hash_val % 899 + 100}"
    owner_names = [
        "Arthur & Brenda Pendelton",
        "David & Sarah Martinez",
        "Michael C. Henderson",
        "Elena & Marcus Vance",
        "Robert & Dorothy Sullivan",
        "Thomas & Karen Reynolds",
    ]
    owner_name = owner or owner_names[hash_val % len(owner_names)]
    parts = owner_name.split()
    first_name = parts[0] if parts else "John"
    last_name = parts[-1] if parts else "Doe"

    total_val = float((hash_val % 450 + 220) * 1000)
    land_val = float(round(total_val * 0.32 / 1000) * 1000)
    imp_val = total_val - land_val

    return {
        "address": f"{street_parts}, {city}, {st} {zip_code}",
        "street": street_parts,
        "city": city,
        "county": co,
        "state": st,
        "zip_code": zip_code,
        "apn": synth_apn,
        "owner": owner_name,
        "first_name": first_name,
        "last_name": last_name,
        "legal_description": f"LOT {(hash_val % 24) + 1}, BLOCK {(hash_val % 8) + 1}, {city.upper()} ESTATES SUBDIVISION, PLAT BOOK {(hash_val % 10) + 2}, PAGE {(hash_val % 40) + 10}, {co.upper()} COUNTY, {st}",
        "zoning": "R-1 Single Family",
        "year_built": 1990 + (hash_val % 32),
        "use_code": "0100 - Single Family Residential",
        "assessed_value": total_val,
        "land_value": land_val,
        "improvement_value": imp_val,
        "market_value": total_val * 1.08,
        "acreage": round((hash_val % 200 + 20) / 100.0, 2),
        "lot": str((hash_val % 24) + 1),
        "block": str((hash_val % 8) + 1),
        "subdivision": f"{city} Estates",
        "prior_owners": ["Robert Sterling Trust", "Oakridge Development Partners LLC"],
    }


def is_mock_property(address: str, county: str, state: str) -> bool:
    normalized_address = " ".join(address.upper().replace(",", " ").split())
    normalized_county = county.upper().removesuffix(" COUNTY").strip()
    return (
        normalized_address.startswith("123 MAIN STREET")
        and normalized_county == "TRAVIS"
        and state.upper() == "TX"
    ) or (
        normalized_address.startswith("4320 NW CR 225")
        and normalized_county == "BRADFORD"
        and state.upper() == "FL"
    )


def mock_property_result(source_name: str) -> PropertySourceResult:
    return PropertySourceResult(
        address="123 Main Street, Austin, TX 78701",
        county="Travis",
        state="TX",
        current_owner="John A Smith",
        apn="123-456-789",
        legal_description="LOT 12, BLOCK B, SAMPLE HEIGHTS, TRAVIS COUNTY, TEXAS",
        property_information={
            "property_type": "Single Family Residential",
            "assessed_year": 2024,
            "development_fixture": True,
        },
        source_name=source_name,
        source_reference="mock://assessor/travis/123-456-789",
        raw_payload={
            "fixture": "DEVELOPMENT_ONLY",
            "owner": "John A Smith",
            "parcel": "123-456-789",
        },
    )


def mock_recorder_records() -> list[RecordSourceResult]:
    common = {
        "county": "Travis",
        "state": "TX",
        "apn": "123-456-789",
        "address": "123 Main Street, Austin, TX 78701",
        "legal_description": "LOT 12, BLOCK B, SAMPLE HEIGHTS, TRAVIS COUNTY, TEXAS",
    }
    return [
        RecordSourceResult(
            **common,
            record_type=RecordType.QUITCLAIM_DEED,
            source_name="mock-recorder",
            source_reference="mock://recorder/2024-018492",
            instrument_number="2024-018492",
            grantors=["Robert Jones"],
            grantees=["John A Smith"],
            execution_date=date(2024, 5, 10),
            recording_date=date(2024, 5, 14),
            effective_date=date(2024, 5, 10),
            transfer_date=date(2024, 5, 10),
            raw_payload={"fixture": "DEVELOPMENT_ONLY", "book": "2024", "page": "18492"},
        ),
        RecordSourceResult(
            **common,
            record_type=RecordType.WARRANTY_DEED,
            source_name="mock-recorder",
            source_reference="mock://recorder/2020-044107",
            instrument_number="2020-044107",
            grantors=["Anna Moore"],
            grantees=["Robert Jones"],
            execution_date=date(2020, 7, 30),
            recording_date=date(2020, 8, 3),
            effective_date=date(2020, 7, 30),
            transfer_date=date(2020, 7, 30),
            raw_payload={"fixture": "DEVELOPMENT_ONLY", "book": "2020", "page": "44107"},
        ),
        RecordSourceResult(
            **common,
            record_type=RecordType.DEED_OF_TRUST,
            source_name="mock-recorder",
            source_reference="mock://recorder/2024-018493",
            instrument_number="2024-018493",
            grantors=["John A Smith"],
            grantees=["First National Bank"],
            execution_date=date(2024, 5, 10),
            recording_date=date(2024, 5, 14),
            filing_date=date(2024, 5, 14),
            raw_payload={"fixture": "DEVELOPMENT_ONLY", "secured_amount": "REDACTED"},
        ),
        RecordSourceResult(
            **common,
            record_type=RecordType.RELEASE,
            source_name="mock-recorder",
            source_reference="mock://recorder/2022-009221",
            instrument_number="2022-009221",
            grantors=["Regional Mortgage Co"],
            grantees=["Robert Jones"],
            execution_date=date(2022, 1, 15),
            recording_date=date(2022, 1, 20),
            release_date=date(2022, 1, 15),
            raw_payload={"fixture": "DEVELOPMENT_ONLY"},
        ),
    ]


def mock_tax_records() -> list[RecordSourceResult]:
    common = {
        "county": "Travis",
        "state": "TX",
        "apn": "123-456-789",
        "address": "123 Main Street, Austin, TX 78701",
    }
    return [
        RecordSourceResult(
            **common,
            record_type=RecordType.TAX_LIEN,
            source_name="mock-tax",
            source_reference="mock://tax/2023-tax-status",
            execution_date=date(2023, 10, 1),
            recording_date=date(2023, 10, 15),
            raw_payload={"status": "PAID", "amount": 0.0},
        )
    ]


def mock_court_records() -> list[RecordSourceResult]:
    common = {
        "county": "Travis",
        "state": "TX",
        "apn": "123-456-789",
    }
    return [
        RecordSourceResult(
            **common,
            record_type=RecordType.CIVIL_JUDGMENT,
            source_name="mock-court",
            source_reference="mock://court/2022-cv-0091",
            execution_date=date(2022, 4, 1),
            recording_date=date(2022, 4, 5),
            grantors=["Austin Utility Authority"],
            grantees=["John A Smith"],
            raw_payload={"status": "DISMISSED"},
        )
    ]
