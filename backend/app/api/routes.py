import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.database import get_db
from app.models import Property, SearchStatus, SourceRecord
from app.schemas import (
    ChainBuildInput,
    ChainLinkOut,
    GISearchInput,
    PropertyOut,
    PropertySearchInput,
    SearchResponse,
    SourceRecordOut,
    TokenRequest,
    TokenResponse,
)
from app.security import authenticate_dev_user, create_access_token, require_roles
from app.services.chain import build_chain
from app.services.search import run_cos_search, run_gi_search, run_pi_search, to_response

router = APIRouter(prefix="/api")
DbSession = Annotated[AsyncSession, Depends(get_db)]
Examiner = Annotated[dict, Depends(require_roles("admin", "examiner"))]


async def get_property_or_404(
    session: AsyncSession, property_id: uuid.UUID, load_related: bool = False
) -> Property:
    statement = select(Property).where(Property.id == property_id)
    if load_related:
        statement = statement.options(
            selectinload(Property.records),
            selectinload(Property.chain_links),
            selectinload(Property.exceptions),
        )
    property_record = await session.scalar(statement)
    if not property_record:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_record


@router.post("/auth/token", response_model=TokenResponse, tags=["security"])
async def issue_development_token(payload: TokenRequest) -> TokenResponse:
    if not authenticate_dev_user(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(
        access_token=create_access_token(payload.username, ["admin", "examiner"])
    )


@router.post("/cos/search", response_model=SearchResponse, tags=["search"])
async def cos_search(payload: PropertySearchInput, session: DbSession, user: Examiner):
    return await run_cos_search(session, payload)


@router.post("/pi/search", response_model=SearchResponse, tags=["search"])
async def pi_search(payload: PropertySearchInput, session: DbSession, user: Examiner):
    property_record, _ = await run_pi_search(session, payload)
    if not property_record:
        return to_response(None, SearchStatus.SOURCE_UNAVAILABLE)
    property_record = await get_property_or_404(session, property_record.id, load_related=True)
    return to_response(property_record, SearchStatus.COMPLETED)


@router.post("/gi/search", response_model=SearchResponse, tags=["search"])
async def gi_search(payload: GISearchInput, session: DbSession, user: Examiner):
    property_record, _ = await run_pi_search(session, payload)
    if not property_record:
        return to_response(None, SearchStatus.SOURCE_UNAVAILABLE)
    await run_gi_search(session, payload, property_record)
    property_record = await get_property_or_404(session, property_record.id, load_related=True)
    status = (
        SearchStatus.REVIEW_REQUIRED
        if any(record.review_required for record in property_record.records)
        else SearchStatus.COMPLETED
    )
    return to_response(property_record, status)


@router.post("/chain-of-title/build", response_model=SearchResponse, tags=["chain"])
async def chain_of_title_build(payload: ChainBuildInput, session: DbSession, user: Examiner):
    property_record = await get_property_or_404(session, payload.property_id, load_related=True)
    await build_chain(
        session,
        property_record,
        payload.search_period_years or get_settings().search_period_years,
    )
    await session.commit()
    property_record = await get_property_or_404(session, property_record.id, load_related=True)
    status = (
        SearchStatus.REVIEW_REQUIRED
        if any(not item.resolved for item in property_record.exceptions)
        else SearchStatus.COMPLETED
    )
    return to_response(property_record, status)


@router.get("/properties/{property_id}", response_model=PropertyOut, tags=["properties"])
async def get_property(property_id: uuid.UUID, session: DbSession, user: Examiner):
    return await get_property_or_404(session, property_id)


@router.get(
    "/properties/{property_id}/records",
    response_model=list[SourceRecordOut],
    tags=["properties"],
)
async def get_property_records(property_id: uuid.UUID, session: DbSession, user: Examiner):
    await get_property_or_404(session, property_id)
    return list(
        (
            await session.scalars(
                select(SourceRecord)
                .where(SourceRecord.property_id == property_id)
                .order_by(SourceRecord.recording_date.desc().nullslast())
            )
        ).all()
    )


@router.get(
    "/properties/{property_id}/chain",
    response_model=list[ChainLinkOut],
    tags=["properties"],
)
async def get_property_chain(property_id: uuid.UUID, session: DbSession, user: Examiner):
    property_record = await get_property_or_404(session, property_id, load_related=True)
    return sorted(property_record.chain_links, key=lambda link: link.sequence)
