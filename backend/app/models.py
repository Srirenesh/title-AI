import enum
import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SearchStatus(str, enum.Enum):
    COMPLETED = "COMPLETED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"


class RecordType(str, enum.Enum):
    WARRANTY_DEED = "WARRANTY_DEED"
    QUITCLAIM_DEED = "QUITCLAIM_DEED"
    MORTGAGE = "MORTGAGE"
    DEED_OF_TRUST = "DEED_OF_TRUST"
    ASSIGNMENT = "ASSIGNMENT"
    RELEASE = "RELEASE"
    SATISFACTION = "SATISFACTION"
    JUDGMENT = "JUDGMENT"
    LIEN = "LIEN"
    TAX = "TAX"
    OTHER = "OTHER"


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address: Mapped[str] = mapped_column(String(500), index=True)
    county: Mapped[str] = mapped_column(String(150), index=True)
    state: Mapped[str] = mapped_column(String(2), index=True)
    apn: Mapped[str | None] = mapped_column(String(100), index=True)
    current_owner: Mapped[str | None] = mapped_column(String(300))
    normalized_owner: Mapped[str | None] = mapped_column(String(300), index=True)
    legal_description: Mapped[str | None] = mapped_column(Text)
    property_information: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    source_reference: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    records: Mapped[list["SourceRecord"]] = relationship(
        back_populates="property", cascade="all, delete-orphan"
    )
    chain_links: Mapped[list["ChainLink"]] = relationship(
        back_populates="property", cascade="all, delete-orphan"
    )
    exceptions: Mapped[list["SearchException"]] = relationship(
        back_populates="property", cascade="all, delete-orphan"
    )


class SearchRun(Base):
    __tablename__ = "search_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="SET NULL")
    )
    search_type: Mapped[str] = mapped_column(String(30))
    status: Mapped[SearchStatus] = mapped_column(Enum(SearchStatus))
    query: Mapped[dict[str, Any]] = mapped_column(JSONB)
    source_summary: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SourceRecord(Base):
    __tablename__ = "source_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    record_type: Mapped[RecordType] = mapped_column(Enum(RecordType), index=True)
    source_name: Mapped[str] = mapped_column(String(150))
    source_reference: Mapped[str] = mapped_column(String(500), unique=True)
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    grantors: Mapped[list[str]] = mapped_column(JSONB, default=list)
    grantees: Mapped[list[str]] = mapped_column(JSONB, default=list)
    legal_description: Mapped[str | None] = mapped_column(Text)
    apn: Mapped[str | None] = mapped_column(String(100), index=True)
    address: Mapped[str | None] = mapped_column(String(500))
    county: Mapped[str] = mapped_column(String(150))
    state: Mapped[str] = mapped_column(String(2))
    execution_date: Mapped[date | None] = mapped_column(Date)
    recording_date: Mapped[date | None] = mapped_column(Date)
    filing_date: Mapped[date | None] = mapped_column(Date)
    effective_date: Mapped[date | None] = mapped_column(Date)
    transfer_date: Mapped[date | None] = mapped_column(Date)
    judgment_date: Mapped[date | None] = mapped_column(Date)
    lien_date: Mapped[date | None] = mapped_column(Date)
    release_date: Mapped[date | None] = mapped_column(Date)
    match_score: Mapped[float] = mapped_column(Float, default=0)
    review_required: Mapped[bool] = mapped_column(default=False)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="records")


class ChainLink(Base):
    __tablename__ = "chain_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("source_records.id", ondelete="CASCADE")
    )
    sequence: Mapped[int] = mapped_column()
    from_owner: Mapped[str] = mapped_column(String(300))
    to_owner: Mapped[str] = mapped_column(String(300))
    transfer_date: Mapped[date | None] = mapped_column(Date)
    instrument_number: Mapped[str | None] = mapped_column(String(150))
    confidence: Mapped[float] = mapped_column(Float)
    property: Mapped[Property] = relationship(back_populates="chain_links")


class SearchException(Base):
    __tablename__ = "search_exceptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    code: Mapped[str] = mapped_column(String(80), index=True)
    message: Mapped[str] = mapped_column(Text)
    context: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    resolved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    property: Mapped[Property] = relationship(back_populates="exceptions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor: Mapped[str] = mapped_column(String(150), index=True)
    action: Mapped[str] = mapped_column(String(30))
    resource: Mapped[str] = mapped_column(String(500))
    status_code: Mapped[int] = mapped_column()
    ip_address: Mapped[str | None] = mapped_column(String(64))
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
