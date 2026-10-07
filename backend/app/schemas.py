import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import DocumentCategory, RecordType, SearchStatus, SourceAccessMode, SourceSystemType


# --- Search Requests ---

class AddressSearchInput(BaseModel):
    address: str = Field(min_length=3, max_length=500, description="Full or partial street address")
    city: str | None = Field(default=None, max_length=150)
    county: str | None = Field(default=None, max_length=150)
    state: str | None = Field(default=None, min_length=2, max_length=2)
    zip_code: str | None = Field(default=None, max_length=20)

    @field_validator("address", "city", "county")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return " ".join(value.split()) if value else value

    @field_validator("state")
    @classmethod
    def uppercase_state(cls, value: str | None) -> str | None:
        if value:
            clean = value.strip().upper()
            if not clean.isalpha() or len(clean) != 2:
                raise ValueError("state must be a two-letter US state code")
            return clean
        return None


class APNSearchInput(BaseModel):
    apn: str = Field(min_length=2, max_length=100, description="Assessor Parcel Number / Folio / Account #")
    county: str = Field(min_length=2, max_length=150, description="County name")
    state: str = Field(min_length=2, max_length=2, description="Two-letter state code")

    @field_validator("apn", "county")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("state")
    @classmethod
    def uppercase_state(cls, value: str) -> str:
        clean = value.strip().upper()
        if not clean.isalpha() or len(clean) != 2:
            raise ValueError("state must be a two-letter US state code")
        return clean


class OwnerSearchInput(BaseModel):
    first_name: str | None = Field(default=None, max_length=150)
    last_name: str = Field(min_length=2, max_length=150)
    full_name: str | None = Field(default=None, max_length=300)
    county: str | None = Field(default=None, max_length=150)
    state: str | None = Field(default=None, min_length=2, max_length=2)
    exact_match: bool = Field(default=False, description="Require exact name matching")

    @field_validator("first_name", "last_name", "full_name", "county")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return " ".join(value.split()) if value else value

    @field_validator("state")
    @classmethod
    def uppercase_state(cls, value: str | None) -> str | None:
        if value:
            clean = value.strip().upper()
            if not clean.isalpha() or len(clean) != 2:
                raise ValueError("state must be a two-letter US state code")
            return clean
        return None


class UnifiedSearchInput(BaseModel):
    query: str = Field(min_length=2, max_length=500, description="Address, APN, or Owner Name")
    search_type: str = Field(default="auto", description="auto, address, apn, owner")
    state: str | None = Field(default=None, max_length=2)
    county: str | None = Field(default=None, max_length=150)


# Backward-compatible request schemas
class PropertySearchInput(BaseModel):
    address: str = Field(min_length=5, max_length=500)
    county: str = Field(min_length=2, max_length=150)
    state: str = Field(min_length=2, max_length=2)
    owner_name: str | None = Field(default=None, min_length=2, max_length=300)

    @field_validator("address", "county", "owner_name")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return " ".join(value.split()) if value else value

    @field_validator("state")
    @classmethod
    def uppercase_state(cls, value: str) -> str:
        clean = value.strip().upper()
        if not clean.isalpha() or len(clean) != 2:
            raise ValueError("state must be a two-letter code")
        return clean


class GISearchInput(PropertySearchInput):
    apn: str | None = Field(default=None, max_length=100)
    legal_description: str | None = Field(default=None, max_length=5000)
    grantor: str | None = Field(default=None, max_length=300)
    grantee: str | None = Field(default=None, max_length=300)
    document_type: RecordType | None = None
    instrument_number: str | None = Field(default=None, max_length=150)
    recording_date_from: date | None = None
    recording_date_to: date | None = None


class ChainBuildInput(BaseModel):
    property_id: uuid.UUID
    search_period_years: int | None = Field(default=None, ge=1, le=100)


# --- Response Models ---

class ParcelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    apn: str
    alternate_apn: str | None = None
    fips_code: str | None = None
    tract: str | None = None
    lot: str | None = None
    block: str | None = None
    subdivision_name: str | None = None
    acreage: float | None = None
    land_square_feet: float | None = None
    building_square_feet: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    gis_polygon_ref: str | None = None


class OwnerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    full_name: str
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    entity_type: str | None = None
    ownership_percentage: float | None = None
    vesting_type: str | None = None
    is_current: bool = True
    acquisition_date: date | None = None


class DeedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    deed_type: str
    grantor: str
    grantee: str
    consideration_amount: float | None = None
    recording_date: date | None = None
    conveyance_date: date | None = None
    instrument_number: str | None = None
    book_page: str | None = None
    is_vesting_deed: bool = False
    legal_notes: str | None = None
    source_agency: str
    official_source_url: str | None = None
    retrieval_timestamp: datetime


class MortgageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    mortgage_type: str
    borrower: str
    lender: str
    trustee: str | None = None
    original_principal_amount: float | None = None
    recording_date: date | None = None
    maturity_date: date | None = None
    instrument_number: str | None = None
    book_page: str | None = None
    status: str
    satisfaction_reference: str | None = None
    legal_notes: str | None = None
    source_agency: str
    official_source_url: str | None = None
    retrieval_timestamp: datetime


class LienOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    lien_type: str
    claimant: str
    debtor: str
    amount: float | None = None
    recording_date: date | None = None
    instrument_number: str | None = None
    book_page: str | None = None
    status: str
    release_date: date | None = None
    legal_notes: str | None = None
    source_agency: str
    official_source_url: str | None = None
    retrieval_timestamp: datetime


class JudgmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    court_name: str
    case_number: str | None = None
    plaintiff: str
    defendant: str
    judgment_amount: float | None = None
    entry_date: date | None = None
    status: str
    satisfaction_date: date | None = None
    legal_notes: str | None = None
    source_agency: str
    official_source_url: str | None = None
    retrieval_timestamp: datetime


class TaxOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    tax_year: int
    jurisdiction: str
    assessed_value: float | None = None
    taxable_value: float | None = None
    total_tax_billed: float | None = None
    amount_paid: float | None = None
    delinquent_amount: float | None = None
    status: str
    due_date: date | None = None
    exemptions: list[str] = []
    source_agency: str
    official_source_url: str | None = None
    retrieval_timestamp: datetime


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    sale_date: date
    sale_price: float | None = None
    seller_grantor: str
    buyer_grantee: str
    deed_reference: str | None = None
    arms_length_flag: bool = True
    source_agency: str
    retrieval_timestamp: datetime


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    document_category: DocumentCategory
    document_type: RecordType
    document_type_raw: str | None = None
    instrument_number: str | None = None
    book_page: str | None = None
    recording_date: date | None = None
    document_date: date | None = None
    grantor: str | None = None
    grantee: str | None = None
    borrower: str | None = None
    lender: str | None = None
    plaintiff: str | None = None
    defendant: str | None = None
    amount: float | None = None
    amount_formatted: str | None = None
    legal_description: str | None = None
    status: str
    source_agency: str
    official_source_url: str | None = None
    document_url: str | None = None
    retrieval_timestamp: datetime
    match_score: float = 1.0


class ChainLinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sequence: int
    from_owner: str
    to_owner: str
    transfer_date: date | None = None
    instrument_type: str = "Deed"
    instrument_number: str | None = None
    confidence: float = 1.0


class ExceptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    message: str
    context: dict[str, Any] = {}
    resolved: bool = False


class DiscoveredSourcesOut(BaseModel):
    state: str
    county: str
    netr_county_directory: str
    netr_state_directory: str
    netr_gis_map: str
    historic_aerials: str
    property_data_store: str
    assessor_portal: str | None = None
    recorder_portal: str | None = None
    treasurer_portal: str | None = None
    gis_portal: str | None = None
    court_portal: str | None = None


class PropertyOverviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    normalized_address: str
    street: str
    city: str
    county: str
    state: str
    zip_code: str
    apn: str | None = None
    current_owner: str | None = None
    legal_description: str | None = None
    zoning: str | None = None
    year_built: int | None = None
    property_use_code: str | None = None
    property_use_description: str | None = None
    assessed_value: float | None = None
    land_value: float | None = None
    improvement_value: float | None = None
    market_value: float | None = None
    official_portal_url: str | None = None
    created_at: datetime


class SourceCoverageSummary(BaseModel):
    assessor: str = "COMPLETED"  # COMPLETED, MANUAL_REQUIRED, SOURCE_UNAVAILABLE, NOT_FOUND
    recorder: str = "COMPLETED"
    treasurer: str = "COMPLETED"
    court: str = "COMPLETED"
    gis: str = "COMPLETED"
    coverage_note: str = "Records gathered from authorized public sources and directories. Non-finding does not certify absence of unrecorded claims."


class AITitleOpinionOut(BaseModel):
    engine: str = "claude-3.7-reasoning-title-ai"
    risk_grade: str = "A+ CLEAR TITLE"
    risk_score: int = 0
    title_status: str = "MARKETABLE"
    executive_legal_opinion: str
    chain_of_title_analysis: str
    encumbrance_analysis: str
    tax_status_analysis: str
    action_items: list[str] = []
    confidence_level: str = "HIGH"
    analyzed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UnifiedPropertyReport(BaseModel):
    property_id: uuid.UUID
    search_job_id: uuid.UUID | None = None
    search_status: SearchStatus
    confidence_score: float = 1.0
    property_overview: PropertyOverviewOut
    parcels: list[ParcelOut] = []
    current_owner: OwnerOut | None = None
    ownership_history: list[OwnerOut] = []
    deeds: list[DeedOut] = []
    mortgages: list[MortgageOut] = []
    liens: list[LienOut] = []
    judgments: list[JudgmentOut] = []
    taxes: list[TaxOut] = []
    sales_history: list[SaleOut] = []
    chain_of_title: list[ChainLinkOut] = []
    all_documents: list[DocumentOut] = []
    discovered_sources: DiscoveredSourcesOut
    source_coverage: SourceCoverageSummary
    ai_title_opinion: AITitleOpinionOut | None = None
    exceptions: list[ExceptionOut] = []
    retrieval_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SearchJobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    search_type: str
    status: SearchStatus
    query_payload: dict[str, Any]
    result_property_id: uuid.UUID | None = None
    confidence_score: float = 0.0
    sources_discovered: dict[str, Any] = {}
    sources_queried: list[str] = []
    sources_unavailable: list[str] = []
    error_log: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


# Backward-compatible response schemas
class PropertyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    address: str
    county: str
    state: str
    apn: str | None = None
    current_owner: str | None = None
    normalized_owner: str | None = None
    legal_description: str | None = None
    property_information: dict[str, Any] = {}
    source_reference: str | None = None
    created_at: datetime


class SourceRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    record_type: RecordType
    source_name: str
    source_reference: str
    instrument_number: str | None = None
    grantors: list[str] = []
    grantees: list[str] = []
    legal_description: str | None = None
    apn: str | None = None
    execution_date: date | None = None
    recording_date: date | None = None
    filing_date: date | None = None
    effective_date: date | None = None
    transfer_date: date | None = None
    judgment_date: date | None = None
    lien_date: date | None = None
    release_date: date | None = None
    match_score: float = 1.0
    review_required: bool = False


class SearchResponse(BaseModel):
    status: SearchStatus
    property: PropertyOut | None = None
    records: list[SourceRecordOut] = []
    chain: list[ChainLinkOut] = []
    exceptions: list[ExceptionOut] = []


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
