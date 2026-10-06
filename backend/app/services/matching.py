from dataclasses import dataclass

from app.schemas import GISearchInput
from app.services.normalization import comparable, normalize_owner_name
from app.sources.base import RecordSourceResult


@dataclass(frozen=True, slots=True)
class MatchResult:
    score: float
    review_required: bool
    matched_rules: tuple[str, ...]


def _party_match(owner: str | None, parties: list[str]) -> bool:
    if not owner:
        return False
    target = comparable(normalize_owner_name(owner))
    return any(comparable(normalize_owner_name(party)) == target for party in parties)


def deterministic_match(query: GISearchInput, record: RecordSourceResult) -> MatchResult:
    """Weighted exact/normalized rules. AI is not used for legal matching decisions."""
    score = 0.0
    rules: list[str] = []

    checks = [
        ("apn", 0.30, query.apn and comparable(query.apn) == comparable(record.apn)),
        ("address", 0.20, comparable(query.address) == comparable(record.address)),
        ("county_state", 0.15, comparable(query.county) == comparable(record.county)
         and query.state == record.state),
        ("legal_description", 0.15, query.legal_description
         and comparable(query.legal_description) == comparable(record.legal_description)),
        ("owner_party", 0.15, _party_match(
            query.owner_name, record.grantors + record.grantees
        )),
        ("instrument_number", 0.05, query.instrument_number
         and comparable(query.instrument_number) == comparable(record.instrument_number)),
    ]
    for name, weight, matched in checks:
        if matched:
            score += weight
            rules.append(name)

    if query.document_type and query.document_type == record.record_type:
        score = min(1.0, score + 0.05)
        rules.append("document_type")
    if query.recording_date_from and record.recording_date:
        if record.recording_date < query.recording_date_from:
            score = 0.0
    if query.recording_date_to and record.recording_date:
        if record.recording_date > query.recording_date_to:
            score = 0.0

    score = round(min(score, 1.0), 3)
    return MatchResult(
        score=score,
        review_required=score < 0.65,
        matched_rules=tuple(rules),
    )
