from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChainLink, Property, RecordType, SearchException, SourceRecord
from app.services.normalization import comparable, normalize_owner_name

DEED_TYPES = {RecordType.WARRANTY_DEED, RecordType.QUITCLAIM_DEED}


async def build_chain(
    session: AsyncSession, property_record: Property, search_period_years: int
) -> tuple[list[ChainLink], list[SearchException]]:
    records = list(
        (
            await session.scalars(
                select(SourceRecord).where(
                    SourceRecord.property_id == property_record.id,
                    SourceRecord.record_type.in_(DEED_TYPES),
                )
            )
        ).all()
    )
    await session.execute(delete(ChainLink).where(ChainLink.property_id == property_record.id))
    await session.execute(
        delete(SearchException).where(
            SearchException.property_id == property_record.id,
            SearchException.code.in_(
                {
                    "MISSING_PARTY",
                    "CHAIN_GAP",
                    "CURRENT_OWNER_MISMATCH",
                    "CHAIN_NOT_ESTABLISHED",
                    "SEARCH_PERIOD_INCOMPLETE",
                }
            ),
            SearchException.resolved.is_(False),
        )
    )

    deeds = sorted(
        records,
        key=lambda record: (
            record.transfer_date
            or record.effective_date
            or record.execution_date
            or record.recording_date
            or date.min
        ),
    )
    links: list[ChainLink] = []
    exceptions: list[SearchException] = []
    previous_owner: str | None = None

    for sequence, deed in enumerate(deeds, start=1):
        if not deed.grantors or not deed.grantees:
            exceptions.append(
                SearchException(
                    property_id=property_record.id,
                    code="MISSING_PARTY",
                    message="A deed is missing a grantor or grantee.",
                    context={"record_id": str(deed.id), "instrument_number": deed.instrument_number},
                )
            )
            continue
        grantor = normalize_owner_name(deed.grantors[0])
        grantee = normalize_owner_name(deed.grantees[0])
        if previous_owner and comparable(previous_owner) != comparable(grantor):
            exceptions.append(
                SearchException(
                    property_id=property_record.id,
                    code="CHAIN_GAP",
                    message="The next deed grantor does not match the prior deed grantee.",
                    context={
                        "expected_grantor": previous_owner,
                        "actual_grantor": grantor,
                        "instrument_number": deed.instrument_number,
                    },
                )
            )
        confidence = max(0.0, min(1.0, deed.match_score))
        link = ChainLink(
            property_id=property_record.id,
            record_id=deed.id,
            sequence=sequence,
            from_owner=grantor,
            to_owner=grantee,
            transfer_date=deed.transfer_date or deed.effective_date or deed.execution_date,
            instrument_number=deed.instrument_number,
            confidence=confidence,
        )
        session.add(link)
        links.append(link)
        previous_owner = grantee

    if links and property_record.normalized_owner:
        if comparable(links[-1].to_owner) != comparable(property_record.normalized_owner):
            exceptions.append(
                SearchException(
                    property_id=property_record.id,
                    code="CURRENT_OWNER_MISMATCH",
                    message="Latest deed grantee does not match the assessor current owner.",
                    context={
                        "deed_grantee": links[-1].to_owner,
                        "assessor_owner": property_record.normalized_owner,
                    },
                )
            )

    if not links:
        exceptions.append(
            SearchException(
                property_id=property_record.id,
                code="CHAIN_NOT_ESTABLISHED",
                message="No qualifying deed records were available to establish a chain of title.",
                context={"search_period_years": search_period_years},
            )
        )
    elif links[0].transfer_date:
        cutoff_year = date.today().year - search_period_years
        if links[0].transfer_date.year > cutoff_year:
            exceptions.append(
                SearchException(
                    property_id=property_record.id,
                    code="SEARCH_PERIOD_INCOMPLETE",
                    message="Available deed history does not satisfy the configured search period.",
                    context={
                        "oldest_transfer_date": links[0].transfer_date.isoformat(),
                        "search_period_years": search_period_years,
                    },
                )
            )

    # A quitclaim transfer requires backward continuity. CHAIN_GAP and period checks above
    # explicitly prevent a quitclaim from being treated as a complete root of title.
    for exception in exceptions:
        session.add(exception)
    await session.flush()
    return links, exceptions
