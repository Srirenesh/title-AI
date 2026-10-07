import enum
import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, TypeDecorator, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type. Uses PostgreSQL's UUID type, otherwise uses CHAR(36)."""
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value) if isinstance(value, uuid.UUID) else value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


class PortableJSON(TypeDecorator):
    """Platform-independent JSON type. Uses PostgreSQL's JSONB type, otherwise standard JSON."""
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())


class SearchStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    MANUAL_REQUIRED = "MANUAL_REQUIRED"
    FAILED = "FAILED"


class DocumentCategory(str, enum.Enum):
    DEED = "DEED"
    MORTGAGE = "MORTGAGE"
    RELEASE = "RELEASE"
    LIEN = "LIEN"
    JUDGMENT = "JUDGMENT"
    TAX = "TAX"
    ASSIGNMENT = "ASSIGNMENT"
    MODIFICATION = "MODIFICATION"
    UCC = "UCC"
    PLAT_MAP = "PLAT_MAP"
    COURT_FILING = "COURT_FILING"
    OTHER = "OTHER"


class RecordType(str, enum.Enum):
    WARRANTY_DEED = "WARRANTY_DEED"
    GENERAL_WARRANTY_DEED = "GENERAL_WARRANTY_DEED"
    SPECIAL_WARRANTY_DEED = "SPECIAL_WARRANTY_DEED"
    GRANT_DEED = "GRANT_DEED"
    QUITCLAIM_DEED = "QUITCLAIM_DEED"
    DEED_OF_TRUST = "DEED_OF_TRUST"
    MORTGAGE = "MORTGAGE"
    HELOC = "HELOC"
    ASSIGNMENT_OF_MORTGAGE = "ASSIGNMENT_OF_MORTGAGE"
    MODIFICATION_OF_MORTGAGE = "MODIFICATION_OF_MORTGAGE"
    RELEASE_OF_MORTGAGE = "RELEASE_OF_MORTGAGE"
    SATISFACTION_OF_MORTGAGE = "SATISFACTION_OF_MORTGAGE"
    RECONVEYANCE = "RECONVEYANCE"
    TAX_LIEN = "TAX_LIEN"
    MECHANICS_LIEN = "MECHANICS_LIEN"
    HOA_LIEN = "HOA_LIEN"
    MUNICIPAL_LIEN = "MUNICIPAL_LIEN"
    JUDGMENT_LIEN = "JUDGMENT_LIEN"
    CIVIL_JUDGMENT = "CIVIL_JUDGMENT"
    LIS_PENDENS = "LIS_PENDENS"
    LIEN = "LIEN"
    RELEASE = "RELEASE"
    JUDGMENT = "JUDGMENT"
    TAX_ASSESSMENT = "TAX_ASSESSMENT"
    TAX_DEED = "TAX_DEED"
    SHERIFF_DEED = "SHERIFF_DEED"
    PROBATE_DEED = "PROBATE_DEED"
    OTHER = "OTHER"


class SourceSystemType(str, enum.Enum):
    ASSESSOR = "ASSESSOR"
    RECORDER = "RECORDER"
    TREASURER = "TREASURER"
    GIS = "GIS"
    COURT = "COURT"
    DIRECTORY = "DIRECTORY"


class SourceAccessMode(str, enum.Enum):
    AUTOMATED_API = "AUTOMATED_API"
    AUTOMATED_FEED = "AUTOMATED_FEED"
    MANUAL_REQUIRED = "MANUAL_REQUIRED"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    MOCK_DEV = "MOCK_DEV"


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    normalized_address: Mapped[str] = mapped_column(String(500), index=True)
    street: Mapped[str] = mapped_column(String(300), index=True)
    city: Mapped[str] = mapped_column(String(150), index=True)
    county: Mapped[str] = mapped_column(String(150), index=True)
    state: Mapped[str] = mapped_column(String(2), index=True)
    zip_code: Mapped[str] = mapped_column(String(20), index=True)
    apn: Mapped[str | None] = mapped_column(String(100), index=True)
    current_owner: Mapped[str | None] = mapped_column(String(300))
    normalized_owner: Mapped[str | None] = mapped_column(String(300), index=True)
    legal_description: Mapped[str | None] = mapped_column(Text)
    zoning: Mapped[str | None] = mapped_column(String(100))
    year_built: Mapped[int | None] = mapped_column(Integer)
    property_use_code: Mapped[str | None] = mapped_column(String(100))
    property_use_description: Mapped[str | None] = mapped_column(String(300))
    assessed_value: Mapped[float | None] = mapped_column(Float)
    land_value: Mapped[float | None] = mapped_column(Float)
    improvement_value: Mapped[float | None] = mapped_column(Float)
    market_value: Mapped[float | None] = mapped_column(Float)
    source_reference: Mapped[str | None] = mapped_column(String(500))
    source_agency: Mapped[str | None] = mapped_column(String(200))
    official_portal_url: Mapped[str | None] = mapped_column(String(500))
    raw_property_data: Mapped[dict[str, Any]] = mapped_column(PortableJSON(), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    parcels: Mapped[list["Parcel"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    owners: Mapped[list["Owner"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    documents: Mapped[list["Document"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    deeds: Mapped[list["Deed"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    mortgages: Mapped[list["Mortgage"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    liens: Mapped[list["Lien"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    judgments: Mapped[list["Judgment"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    taxes: Mapped[list["TaxRecord"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    sales: Mapped[list["SaleRecord"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    chain_links: Mapped[list["ChainLink"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    exceptions: Mapped[list["SearchException"]] = relationship(back_populates="property", cascade="all, delete-orphan")
    records: Mapped[list["SourceRecord"]] = relationship(back_populates="property", cascade="all, delete-orphan")


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    apn: Mapped[str] = mapped_column(String(100), index=True)
    alternate_apn: Mapped[str | None] = mapped_column(String(100))
    fips_code: Mapped[str | None] = mapped_column(String(10))
    tract: Mapped[str | None] = mapped_column(String(100))
    lot: Mapped[str | None] = mapped_column(String(100))
    block: Mapped[str | None] = mapped_column(String(100))
    subdivision_name: Mapped[str | None] = mapped_column(String(300))
    acreage: Mapped[float | None] = mapped_column(Float)
    land_square_feet: Mapped[float | None] = mapped_column(Float)
    building_square_feet: Mapped[float | None] = mapped_column(Float)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    gis_polygon_ref: Mapped[str | None] = mapped_column(String(200))
    gis_raw_metadata: Mapped[dict[str, Any]] = mapped_column(PortableJSON(), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="parcels")


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    full_name: Mapped[str] = mapped_column(String(300), index=True)
    first_name: Mapped[str | None] = mapped_column(String(150), index=True)
    last_name: Mapped[str | None] = mapped_column(String(150), index=True)
    middle_name: Mapped[str | None] = mapped_column(String(100))
    entity_type: Mapped[str | None] = mapped_column(String(50))
    ownership_percentage: Mapped[float | None] = mapped_column(Float, default=100.0)
    vesting_type: Mapped[str | None] = mapped_column(String(150))
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    acquisition_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="owners")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    document_category: Mapped[DocumentCategory] = mapped_column(Enum(DocumentCategory), index=True)
    document_type: Mapped[RecordType] = mapped_column(Enum(RecordType), index=True)
    document_type_raw: Mapped[str | None] = mapped_column(String(200))
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    book_page: Mapped[str | None] = mapped_column(String(100))
    recording_date: Mapped[date | None] = mapped_column(Date, index=True)
    document_date: Mapped[date | None] = mapped_column(Date)
    grantor: Mapped[str | None] = mapped_column(String(300))
    grantee: Mapped[str | None] = mapped_column(String(300))
    borrower: Mapped[str | None] = mapped_column(String(300))
    lender: Mapped[str | None] = mapped_column(String(300))
    plaintiff: Mapped[str | None] = mapped_column(String(300))
    defendant: Mapped[str | None] = mapped_column(String(300))
    amount: Mapped[float | None] = mapped_column(Float)
    amount_formatted: Mapped[str | None] = mapped_column(String(50))
    legal_description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="Recorded")
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    document_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    match_score: Mapped[float] = mapped_column(Float, default=1.0)
    raw_metadata: Mapped[dict[str, Any]] = mapped_column(PortableJSON(), default=dict)

    property: Mapped[Property] = relationship(back_populates="documents")


class Deed(Base):
    __tablename__ = "deeds"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("documents.id", ondelete="SET NULL")
    )
    deed_type: Mapped[str] = mapped_column(String(100), index=True)
    grantor: Mapped[str] = mapped_column(String(300))
    grantee: Mapped[str] = mapped_column(String(300))
    consideration_amount: Mapped[float | None] = mapped_column(Float)
    recording_date: Mapped[date | None] = mapped_column(Date)
    conveyance_date: Mapped[date | None] = mapped_column(Date)
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    book_page: Mapped[str | None] = mapped_column(String(100))
    is_vesting_deed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_notes: Mapped[str | None] = mapped_column(Text)
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="deeds")


class Mortgage(Base):
    __tablename__ = "mortgages"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("documents.id", ondelete="SET NULL")
    )
    mortgage_type: Mapped[str] = mapped_column(String(100))
    borrower: Mapped[str] = mapped_column(String(300))
    lender: Mapped[str] = mapped_column(String(300))
    trustee: Mapped[str | None] = mapped_column(String(300))
    original_principal_amount: Mapped[float | None] = mapped_column(Float)
    recording_date: Mapped[date | None] = mapped_column(Date)
    maturity_date: Mapped[date | None] = mapped_column(Date)
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    book_page: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="Open")
    satisfaction_reference: Mapped[str | None] = mapped_column(String(200))
    legal_notes: Mapped[str | None] = mapped_column(Text)
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="mortgages")


class Lien(Base):
    __tablename__ = "liens"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("documents.id", ondelete="SET NULL")
    )
    lien_type: Mapped[str] = mapped_column(String(100), index=True)
    claimant: Mapped[str] = mapped_column(String(300))
    debtor: Mapped[str] = mapped_column(String(300))
    amount: Mapped[float | None] = mapped_column(Float)
    recording_date: Mapped[date | None] = mapped_column(Date)
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    book_page: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="Active")
    release_date: Mapped[date | None] = mapped_column(Date)
    legal_notes: Mapped[str | None] = mapped_column(Text)
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="liens")


class Judgment(Base):
    __tablename__ = "judgments"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("documents.id", ondelete="SET NULL")
    )
    court_name: Mapped[str] = mapped_column(String(200))
    case_number: Mapped[str | None] = mapped_column(String(150), index=True)
    plaintiff: Mapped[str] = mapped_column(String(300))
    defendant: Mapped[str] = mapped_column(String(300))
    judgment_amount: Mapped[float | None] = mapped_column(Float)
    entry_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="Active")
    satisfaction_date: Mapped[date | None] = mapped_column(Date)
    legal_notes: Mapped[str | None] = mapped_column(Text)
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="judgments")


class TaxRecord(Base):
    __tablename__ = "taxes"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    tax_year: Mapped[int] = mapped_column(Integer, index=True)
    jurisdiction: Mapped[str] = mapped_column(String(200))
    assessed_value: Mapped[float | None] = mapped_column(Float)
    taxable_value: Mapped[float | None] = mapped_column(Float)
    total_tax_billed: Mapped[float | None] = mapped_column(Float)
    amount_paid: Mapped[float | None] = mapped_column(Float)
    delinquent_amount: Mapped[float | None] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="Paid")
    due_date: Mapped[date | None] = mapped_column(Date)
    exemptions: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
    source_agency: Mapped[str] = mapped_column(String(200))
    official_source_url: Mapped[str | None] = mapped_column(String(500))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="taxes")


class SaleRecord(Base):
    __tablename__ = "sales"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    sale_date: Mapped[date] = mapped_column(Date, index=True)
    sale_price: Mapped[float | None] = mapped_column(Float)
    seller_grantor: Mapped[str] = mapped_column(String(300))
    buyer_grantee: Mapped[str] = mapped_column(String(300))
    deed_reference: Mapped[str | None] = mapped_column(String(200))
    arms_length_flag: Mapped[bool] = mapped_column(Boolean, default=True)
    source_agency: Mapped[str] = mapped_column(String(200))
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="sales")


class SourceRegistry(Base):
    __tablename__ = "source_registry"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    state: Mapped[str] = mapped_column(String(2), index=True)
    county: Mapped[str] = mapped_column(String(150), index=True)
    county_slug: Mapped[str] = mapped_column(String(150), index=True)
    system_type: Mapped[SourceSystemType] = mapped_column(Enum(SourceSystemType), index=True)
    agency_name: Mapped[str] = mapped_column(String(250))
    portal_url: Mapped[str] = mapped_column(String(500))
    directory_url: Mapped[str | None] = mapped_column(String(500))
    access_mode: Mapped[SourceAccessMode] = mapped_column(Enum(SourceAccessMode), default=SourceAccessMode.MANUAL_REQUIRED)
    search_capabilities: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=30)
    requires_captcha: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_auth: Mapped[bool] = mapped_column(Boolean, default=False)
    last_verified: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SearchJob(Base):
    __tablename__ = "search_jobs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    search_type: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[SearchStatus] = mapped_column(Enum(SearchStatus), index=True, default=SearchStatus.PENDING)
    query_payload: Mapped[dict[str, Any]] = mapped_column(PortableJSON())
    result_property_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="SET NULL")
    )
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    sources_discovered: Mapped[dict[str, Any]] = mapped_column(PortableJSON(), default=dict)
    sources_queried: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
    sources_unavailable: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
    error_log: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ChainLink(Base):
    __tablename__ = "chain_links"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    sequence: Mapped[int] = mapped_column()
    from_owner: Mapped[str] = mapped_column(String(300))
    to_owner: Mapped[str] = mapped_column(String(300))
    transfer_date: Mapped[date | None] = mapped_column(Date)
    instrument_type: Mapped[str] = mapped_column(String(100), default="Deed")
    instrument_number: Mapped[str | None] = mapped_column(String(150))
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    property: Mapped[Property] = relationship(back_populates="chain_links")


class SearchException(Base):
    __tablename__ = "search_exceptions"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    search_job_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    code: Mapped[str] = mapped_column(String(80), index=True)
    message: Mapped[str] = mapped_column(Text)
    context: Mapped[dict[str, Any]] = mapped_column(PortableJSON(), default=dict)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    property: Mapped[Property] = relationship(back_populates="exceptions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    actor: Mapped[str] = mapped_column(String(150), index=True)
    action: Mapped[str] = mapped_column(String(50))
    resource: Mapped[str] = mapped_column(String(500))
    search_job_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    property_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    status_code: Mapped[int] = mapped_column(Integer)
    ip_address: Mapped[str | None] = mapped_column(String(64))
    request_id: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SourceRecord(Base):
    __tablename__ = "source_records"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("properties.id", ondelete="CASCADE"), index=True
    )
    record_type: Mapped[RecordType] = mapped_column(Enum(RecordType), index=True)
    source_name: Mapped[str] = mapped_column(String(150))
    source_reference: Mapped[str] = mapped_column(String(500), unique=True)
    instrument_number: Mapped[str | None] = mapped_column(String(150), index=True)
    grantors: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
    grantees: Mapped[list[str]] = mapped_column(PortableJSON(), default=list)
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
    review_required: Mapped[bool] = mapped_column(Boolean, default=False)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(PortableJSON())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    property: Mapped[Property] = relationship(back_populates="records")


# Backwards compatibility aliases
SearchRun = SearchJob
PropertyRecord = SourceRecord
TitleChainEntry = ChainLink

