from datetime import date

from app.models import RecordType
from app.schemas import GISearchInput
from app.services.matching import deterministic_match
from app.services.normalization import normalize_owner_name, owner_name_variations
from app.sources.base import RecordSourceResult


def test_normalizes_person_name() -> None:
    assert normalize_owner_name("John A Smith") == "SMITH, JOHN A"


def test_controlled_variations() -> None:
    values = owner_name_variations("John A Smith")
    assert "SMITH, JOHN A" in values
    assert "JOHN A SMITH" in values
    assert "JOHN SMITH" in values


def test_deterministic_match_prefers_property_identifiers() -> None:
    query = GISearchInput(
        address="123 Main Street, Austin, TX 78701",
        county="Travis",
        state="TX",
        owner_name="John A Smith",
        apn="123-456-789",
        legal_description="LOT 12 BLOCK B",
    )
    record = RecordSourceResult(
        record_type=RecordType.WARRANTY_DEED,
        source_name="test",
        source_reference="test://1",
        county="Travis",
        state="TX",
        apn="123-456-789",
        address="123 Main Street, Austin, TX 78701",
        legal_description="LOT 12 BLOCK B",
        grantors=["Robert Jones"],
        grantees=["John A Smith"],
        recording_date=date(2024, 1, 1),
    )
    result = deterministic_match(query, record)
    assert result.score >= 0.9
    assert result.review_required is False


def test_low_signal_record_requires_review() -> None:
    query = GISearchInput(address="1 Other Road", county="Travis", state="TX")
    record = RecordSourceResult(
        record_type=RecordType.LIEN,
        source_name="test",
        source_reference="test://2",
        county="Dallas",
        state="TX",
    )
    result = deterministic_match(query, record)
    assert result.review_required is True
