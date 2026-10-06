from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models import (
    Property,
    RecordType,
    SearchException,
    SearchRun,
    SearchStatus,
    SourceRecord,
)
from app.schemas import GISearchInput, PropertySearchInput, SearchResponse
from app.services.chain import build_chain
from app.services.matching import deterministic_match
from app.services.normalization import normalize_owner_name, owner_name_variations
from app.sources import AssessorAdapter, CourtAdapter, NetrAdapter, RecorderAdapter, TaxAdapter
from app.sources.base import PropertySourceResult, RecordSourceResult, SourceUnavailableError


async def _load_property(session: AsyncSession, property_id) -> Property | None:
    return await session.scalar(
        select(Property)
        .where(Property.id == property_id)
        .options(
            selectinload(Property.records),
            selectinload(Property.chain_links),
            selectinload(Property.exceptions),
        )
    )


def _sources(property_record: Property | None) -> list[dict]:
    if not property_record:
        return []
    values: dict[str, dict] = {}
    if property_record.source_reference:
        values[property_record.source_reference] = {
            "source": "property",
            "reference": property_record.source_reference,
        }
    for record in property_record.records:
        values[record.source_reference] = {
            "source": record.source_name,
            "reference": record.source_reference,
        }
    return list(values.values())


def to_response(property_record: Property | None, status: SearchStatus) -> SearchResponse:
    records = sorted(
        property_record.records if property_record else [],
        key=lambda value: value.recording_date or value.execution_date or datetime.min.date(),
        reverse=True,
    )
    return SearchResponse(
        property=property_record,
        current_owner=property_record.normalized_owner if property_record else None,
        apn=property_record.apn if property_record else None,
        records=records,
        mortgages=[
            record
            for record in records
            if record.record_type in {RecordType.MORTGAGE, RecordType.DEED_OF_TRUST}
        ],
        judgments=[record for record in records if record.record_type == RecordType.JUDGMENT],
        liens=[record for record in records if record.record_type == RecordType.LIEN],
        chain_of_title=sorted(
            property_record.chain_links if property_record else [], key=lambda link: link.sequence
        ),
        exceptions=[
            exception for exception in (property_record.exceptions if property_record else [])
            if not exception.resolved
        ],
        sources=_sources(property_record),
        search_status=status,
    )


async def run_pi_search(
    session: AsyncSession, query: PropertySearchInput
) -> tuple[Property | None, list[dict]]:
    source_attempts: list[dict] = []
    result: PropertySourceResult | None = None
    for adapter in (AssessorAdapter(), NetrAdapter()):
        try:
            result = await adapter.property_search(query)
            source_attempts.append({"source": adapter.source_name, "status": "AVAILABLE"})
            break
        except SourceUnavailableError as error:
            source_attempts.append({
                "source": adapter.source_name,
                "status": "SOURCE_UNAVAILABLE",
                "detail": str(error),
            })

    run = SearchRun(search_type="PI", status=SearchStatus.IN_PROGRESS, query=query.model_dump())
    session.add(run)
    if not result:
        run.status = SearchStatus.SOURCE_UNAVAILABLE
        run.source_summary = {"attempts": source_attempts}
        run.completed_at = datetime.now(timezone.utc)
        await session.commit()
        return None, source_attempts

    property_record = await session.scalar(
        select(Property).where(
            Property.apn == result.apn,
            Property.county == result.county,
            Property.state == result.state,
        )
    )
    if not property_record:
        property_record = Property(
            address=result.address,
            county=result.county,
            state=result.state,
            apn=result.apn,
        )
        session.add(property_record)
    property_record.address = result.address
    property_record.current_owner = result.current_owner
    property_record.normalized_owner = normalize_owner_name(result.current_owner)
    property_record.legal_description = result.legal_description
    property_record.property_information = {
        **result.property_information,
        "raw_source_payload": result.raw_payload,
    }
    property_record.source_reference = result.source_reference
    await session.flush()
    run.property_id = property_record.id
    run.status = SearchStatus.COMPLETED
    run.source_summary = {"attempts": source_attempts}
    run.completed_at = datetime.now(timezone.utc)
    await session.commit()
    return property_record, source_attempts


async def run_gi_search(
    session: AsyncSession, query: GISearchInput, property_record: Property
) -> list[dict]:
    owner = query.owner_name or property_record.current_owner or ""
    variations = owner_name_variations(owner) if owner else []
    enriched_query = query.model_copy(
        update={
            "owner_name": owner or None,
            "apn": query.apn or property_record.apn,
            "legal_description": query.legal_description or property_record.legal_description,
        }
    )
    source_attempts: list[dict] = []
    results: list[RecordSourceResult] = []
    for adapter in (RecorderAdapter(), CourtAdapter(), TaxAdapter()):
        try:
            source_records = await adapter.record_search(enriched_query, variations)
            results.extend(source_records)
            source_attempts.append({
                "source": adapter.source_name,
                "status": "AVAILABLE",
                "record_count": len(source_records),
            })
        except SourceUnavailableError as error:
            source_attempts.append({
                "source": adapter.source_name,
                "status": "SOURCE_UNAVAILABLE",
                "detail": str(error),
            })

    run = SearchRun(
        property_id=property_record.id,
        search_type="GI",
        status=SearchStatus.IN_PROGRESS,
        query={**enriched_query.model_dump(mode="json"), "owner_variations": variations},
    )
    session.add(run)
    for source_record in results:
        existing = await session.scalar(
            select(SourceRecord).where(
                SourceRecord.source_reference == source_record.source_reference
            )
        )
        match = deterministic_match(enriched_query, source_record)
        if existing:
            existing.match_score = match.score
            existing.review_required = match.review_required
            continue
        record = SourceRecord(
            property_id=property_record.id,
            record_type=source_record.record_type,
            source_name=source_record.source_name,
            source_reference=source_record.source_reference,
            instrument_number=source_record.instrument_number,
            grantors=source_record.grantors,
            grantees=source_record.grantees,
            legal_description=source_record.legal_description,
            apn=source_record.apn,
            address=source_record.address,
            county=source_record.county,
            state=source_record.state,
            execution_date=source_record.execution_date,
            recording_date=source_record.recording_date,
            filing_date=source_record.filing_date,
            effective_date=source_record.effective_date,
            transfer_date=source_record.transfer_date,
            judgment_date=source_record.judgment_date,
            lien_date=source_record.lien_date,
            release_date=source_record.release_date,
            match_score=match.score,
            review_required=match.review_required,
            raw_payload={
                **source_record.raw_payload,
                "deterministic_match_rules": list(match.matched_rules),
            },
        )
        session.add(record)
    run.status = (
        SearchStatus.COMPLETED if results else SearchStatus.SOURCE_UNAVAILABLE
    )
    run.source_summary = {"attempts": source_attempts}
    run.completed_at = datetime.now(timezone.utc)
    await session.commit()
    return source_attempts


async def run_cos_search(session: AsyncSession, query: PropertySearchInput) -> SearchResponse:
    property_record, _ = await run_pi_search(session, query)
    if not property_record:
        return to_response(None, SearchStatus.SOURCE_UNAVAILABLE)
    gi_query = GISearchInput(**query.model_dump())
    await run_gi_search(session, gi_query, property_record)
    property_record = await _load_property(session, property_record.id)
    assert property_record is not None
    await build_chain(session, property_record, get_settings().search_period_years)

    low_confidence = [record for record in property_record.records if record.review_required]
    for record in low_confidence:
        exists = await session.scalar(
            select(SearchException).where(
                SearchException.property_id == property_record.id,
                SearchException.code == "AMBIGUOUS_RECORD",
                SearchException.context["record_id"].astext == str(record.id),
            )
        )
        if not exists:
            session.add(
                SearchException(
                    property_id=property_record.id,
                    code="AMBIGUOUS_RECORD",
                    message="A source record did not meet the deterministic match threshold.",
                    context={"record_id": str(record.id), "match_score": record.match_score},
                )
            )
    await session.commit()
    property_record = await _load_property(session, property_record.id)
    assert property_record is not None
    status = (
        SearchStatus.REVIEW_REQUIRED
        if any(not item.resolved for item in property_record.exceptions)
        else SearchStatus.COMPLETED
    )
    return to_response(property_record, status)
