from dataclasses import dataclass
from typing import Any

from app.schemas import GISearchInput
from app.services.normalization import comparable, normalize_apn, normalize_owner_name
from app.sources.base import RecorderSourceResult, RecordSourceResult


@dataclass(frozen=True, slots=True)
class MatchResult:
    score: float
    confidence_tier: str  # HIGH, MEDIUM, LOW, UNMATCHED
    review_required: bool
    matched_rules: tuple[str, ...]


def _party_match(owner: str | None, parties: list[str]) -> bool:
    if not owner:
        return False
    target = comparable(normalize_owner_name(owner))
    return any(comparable(normalize_owner_name(party)) == target for party in parties)


def calculate_property_match_confidence(
    search_type: str,
    query_address: str | None,
    query_apn: str | None,
    query_owner: str | None,
    target_address: str | None,
    target_apn: str | None,
    target_owner: str | None,
    target_county: str | None,
    query_county: str | None,
) -> float:
    """
    Deterministic confidence scoring based on search criteria:
    - Exact APN + County matches: 1.0 (Highest confidence)
    - Normalized Address + County matches: 0.95
    - Exact Owner Name + County matches: 0.80
    - Partial Owner Name matches: 0.65 (Lower confidence; never merge solely on name similarity)
    """
    if query_apn and target_apn and normalize_apn(query_apn) == normalize_apn(target_apn):
        return 1.0

    if query_address and target_address:
        norm_q = comparable(query_address)
        norm_t = comparable(target_address)
        if norm_q and (norm_q in norm_t or norm_t in norm_q):
            return 0.95

    if query_owner and target_owner:
        if comparable(normalize_owner_name(query_owner)) == comparable(normalize_owner_name(target_owner)):
            return 0.80
        # Partial match
        q_parts = set(normalize_owner_name(query_owner).split())
        t_parts = set(normalize_owner_name(target_owner).split())
        if q_parts.intersection(t_parts):
            return 0.65

    return 0.50


def deduplicate_recorder_records(records: list[RecorderSourceResult]) -> list[RecorderSourceResult]:
    """
    Deduplicate recorded instruments using instrument number, recording date, document type,
    parties, book/page and source agency while preserving the original source URL.
    """
    seen_keys: set[str] = set()
    deduped: list[RecorderSourceResult] = []

    for r in records:
        inst = comparable(r.instrument_number)
        rec_date = r.recording_date.isoformat() if r.recording_date else ""
        doc_type = str(r.document_type)
        parties_str = "".join(sorted([comparable(p) for p in (r.grantors + r.grantees)]))
        bp = comparable(r.book_page)
        agency = comparable(r.source_agency)

        # Build composite deduplication fingerprint
        if inst:
            key = f"inst:{inst}:{agency}"
        elif bp:
            key = f"bp:{bp}:{rec_date}:{agency}"
        else:
            key = f"doc:{doc_type}:{rec_date}:{parties_str}:{agency}"

        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(r)

    return deduped


def deterministic_match(query: GISearchInput, record: RecordSourceResult) -> MatchResult:
    """Weighted exact/normalized rules. AI is not used for legal matching decisions."""
    score = 0.0
    rules: list[str] = []

    checks = [
        ("apn", 0.30, query.apn and comparable(query.apn) == comparable(record.apn)),
        ("address", 0.20, comparable(query.address) == comparable(record.address)),
        (
            "county_state",
            0.15,
            comparable(query.county) == comparable(record.county) and query.state == record.state,
        ),
        (
            "legal_description",
            0.15,
            query.legal_description
            and comparable(query.legal_description) == comparable(record.legal_description),
        ),
        ("owner_party", 0.15, _party_match(query.owner_name, record.grantors + record.grantees)),
        (
            "instrument_number",
            0.05,
            query.instrument_number
            and comparable(query.instrument_number) == comparable(record.instrument_number),
        ),
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
    tier = "HIGH" if score >= 0.85 else ("MEDIUM" if score >= 0.65 else "LOW")
    return MatchResult(
        score=score,
        confidence_tier=tier,
        review_required=score < 0.65,
        matched_rules=tuple(rules),
    )
