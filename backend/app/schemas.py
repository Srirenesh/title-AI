import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import RecordType, SearchStatus


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
        if not value.isalpha():
            raise ValueError("state must be a two-letter code")
        return value.upper()


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


class SourceRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    record_type: RecordType
    source_name: str
    source_reference: str
    instrument_number: str | None
    grantors: list[str]
    grantees: list[str]
    legal_description: str | None
    apn: str | None
    execution_date: date | None
    recording_date: date | None
    filing_date: date | None
    effective_date: date | None
    transfer_date: date | None
    judgment_date: date | None
    lien_date: date | None
    release_date: date | None
    match_score: float
    review_required: bool


class ChainLinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sequence: int
    from_owner: str
    to_owner: str
    transfer_date: date | None
    instrument_number: str | None
    confidence: float


class ExceptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str
    message: str
    context: dict[str, Any]
    resolved: bool


class PropertyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    address: str
    county: str
    state: str
    apn: str | None
    current_owner: str | None
    normalized_owner: str | None
    legal_description: str | None
    property_information: dict[str, Any]
    source_reference: str | None
    created_at: datetime


class SearchResponse(BaseModel):
    property: PropertyOut | None
    current_owner: str | None
    apn: str | None
    records: list[SourceRecordOut]
    mortgages: list[SourceRecordOut]
    judgments: list[SourceRecordOut]
    liens: list[SourceRecordOut]
    chain_of_title: list[ChainLinkOut]
    exceptions: list[ExceptionOut]
    sources: list[dict[str, Any]]
    search_status: SearchStatus


class TokenRequest(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=1, max_length=300)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
