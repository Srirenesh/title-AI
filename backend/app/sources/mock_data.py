from datetime import date

from app.models import RecordType
from app.sources.base import PropertySourceResult, RecordSourceResult

MOCK_ADDRESS = "123 MAIN STREET"
MOCK_COUNTY = "TRAVIS"
MOCK_STATE = "TX"


def is_mock_property(address: str, county: str, state: str) -> bool:
    normalized_address = " ".join(address.upper().replace(",", " ").split())
    normalized_county = county.upper().removesuffix(" COUNTY").strip()
    return (
        normalized_address.startswith(MOCK_ADDRESS)
        and normalized_county == MOCK_COUNTY
        and state.upper() == MOCK_STATE
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
            execution_date=date(2022, 2, 10),
            recording_date=date(2022, 2, 15),
            release_date=date(2022, 2, 10),
            raw_payload={"fixture": "DEVELOPMENT_ONLY"},
        ),
    ]


def mock_court_records() -> list[RecordSourceResult]:
    return []


def mock_tax_records() -> list[RecordSourceResult]:
    return [
        RecordSourceResult(
            record_type=RecordType.TAX,
            source_name="mock-tax",
            source_reference="mock://tax/travis/123-456-789/2024",
            county="Travis",
            state="TX",
            instrument_number=None,
            grantees=["John A Smith"],
            apn="123-456-789",
            address="123 Main Street, Austin, TX 78701",
            effective_date=date(2024, 1, 1),
            raw_payload={
                "fixture": "DEVELOPMENT_ONLY",
                "tax_year": 2024,
                "status": "CURRENT",
            },
        )
    ]
