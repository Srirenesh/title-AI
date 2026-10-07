from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from app.models import DocumentCategory, RecordType, SourceAccessMode, SourceSystemType
from app.schemas import AddressSearchInput, APNSearchInput, GISearchInput, OwnerSearchInput, PropertySearchInput


class SourceUnavailableError(RuntimeError):
    pass


class SourceRateLimitError(RuntimeError):
    pass


class ManualAccessRequiredError(RuntimeError):
    def __init__(self, message: str, portal_url: str):
        super().__init__(message)
        self.portal_url = portal_url


@dataclass(slots=True)
class DiscoveredDirectorySources:
    state: str
    county: str
    county_slug: str
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
    raw_directory_links: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class AssessorSourceResult:
    address: str
    street: str
    city: str
    county: str
    state: str
    zip_code: str
    apn: str
    current_owner: str
    legal_description: str
    zoning: str | None = None
    year_built: int | None = None
    property_use_code: str | None = None
    property_use_description: str | None = None
    assessed_value: float | None = None
    land_value: float | None = None
    improvement_value: float | None = None
    market_value: float | None = None
    lot: str | None = None
    block: str | None = None
    subdivision: str | None = None
    acreage: float | None = None
    source_agency: str = "County Assessor"
    source_reference: str = ""
    official_portal_url: str | None = None
    access_mode: SourceAccessMode = SourceAccessMode.AUTOMATED_API
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecorderSourceResult:
    document_category: DocumentCategory
    document_type: RecordType
    document_type_raw: str
    source_agency: str
    source_reference: str
    county: str
    state: str
    instrument_number: str | None = None
    book_page: str | None = None
    recording_date: date | None = None
    document_date: date | None = None
    grantors: list[str] = field(default_factory=list)
    grantees: list[str] = field(default_factory=list)
    borrower: str | None = None
    lender: str | None = None
    amount: float | None = None
    amount_formatted: str | None = None
    legal_description: str | None = None
    apn: str | None = None
    address: str | None = None
    status: str = "Recorded"
    satisfaction_reference: str | None = None
    official_source_url: str | None = None
    document_url: str | None = None
    legal_notes: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TreasurerSourceResult:
    tax_year: int
    jurisdiction: str
    assessed_value: float | None = None
    taxable_value: float | None = None
    total_tax_billed: float | None = None
    amount_paid: float | None = None
    delinquent_amount: float | None = 0.0
    status: str = "Paid"
    due_date: date | None = None
    exemptions: list[str] = field(default_factory=list)
    source_agency: str = "County Tax Collector"
    source_reference: str = ""
    official_source_url: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GISSourceResult:
    apn: str
    latitude: float | None = None
    longitude: float | None = None
    acreage: float | None = None
    land_square_feet: float | None = None
    building_square_feet: float | None = None
    fips_code: str | None = None
    gis_polygon_ref: str | None = None
    zoning: str | None = None
    source_agency: str = "County GIS Mapping"
    official_source_url: str | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CourtSourceResult:
    court_name: str
    case_number: str | None = None
    plaintiff: str = ""
    defendant: str = ""
    judgment_amount: float | None = None
    entry_date: date | None = None
    status: str = "Active"
    satisfaction_date: date | None = None
    document_type: RecordType = RecordType.CIVIL_JUDGMENT
    legal_notes: str | None = None
    source_agency: str = "County Court"
    official_source_url: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


# Backward-compatible dataclasses
@dataclass(slots=True)
class PropertySourceResult:
    address: str
    county: str
    state: str
    current_owner: str
    apn: str
    legal_description: str
    property_information: dict[str, Any]
    source_name: str
    source_reference: str
    raw_payload: dict[str, Any]


@dataclass(slots=True)
class RecordSourceResult:
    record_type: RecordType
    source_name: str
    source_reference: str
    county: str
    state: str
    instrument_number: str | None = None
    grantors: list[str] = field(default_factory=list)
    grantees: list[str] = field(default_factory=list)
    legal_description: str | None = None
    apn: str | None = None
    address: str | None = None
    execution_date: date | None = None
    recording_date: date | None = None
    filing_date: date | None = None
    effective_date: date | None = None
    transfer_date: date | None = None
    judgment_date: date | None = None
    lien_date: date | None = None
    release_date: date | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


# --- Abstract Adapter Interfaces ---

class BaseSourceAdapter(ABC):
    source_name: str
    system_type: SourceSystemType

    @abstractmethod
    async def is_available(self, state: str, county: str) -> bool:
        raise NotImplementedError


class NETRDirectoryAdapter(ABC):
    source_name: str = "NETR Public Records Directory"

    @abstractmethod
    async def discover_sources(self, state: str, county: str) -> DiscoveredDirectorySources:
        raise NotImplementedError


class AssessorAdapter(ABC):
    source_name: str = "County Assessor / CAD"
    system_type: SourceSystemType = SourceSystemType.ASSESSOR

    @abstractmethod
    async def search_by_address(self, query: AddressSearchInput) -> AssessorSourceResult | None:
        raise NotImplementedError

    @abstractmethod
    async def search_by_apn(self, query: APNSearchInput) -> AssessorSourceResult | None:
        raise NotImplementedError

    @abstractmethod
    async def search_by_owner(self, query: OwnerSearchInput) -> list[AssessorSourceResult]:
        raise NotImplementedError


class RecorderAdapter(ABC):
    source_name: str = "County Recorder / Clerk"
    system_type: SourceSystemType = SourceSystemType.RECORDER

    @abstractmethod
    async def search_records(
        self,
        apn: str | None,
        address: str | None,
        county: str,
        state: str,
        owner_names: list[str],
    ) -> list[RecorderSourceResult]:
        raise NotImplementedError


class TreasurerAdapter(ABC):
    source_name: str = "County Treasurer / Tax Collector"
    system_type: SourceSystemType = SourceSystemType.TREASURER

    @abstractmethod
    async def get_tax_records(self, apn: str, county: str, state: str) -> list[TreasurerSourceResult]:
        raise NotImplementedError


class GISAdapter(ABC):
    source_name: str = "County / NETR GIS"
    system_type: SourceSystemType = SourceSystemType.GIS

    @abstractmethod
    async def get_parcel_gis(self, apn: str, county: str, state: str) -> GISSourceResult | None:
        raise NotImplementedError


class CourtAdapter(ABC):
    source_name: str = "Circuit Court / General Index"
    system_type: SourceSystemType = SourceSystemType.COURT

    @abstractmethod
    async def search_judgments(
        self, owner_names: list[str], county: str, state: str
    ) -> list[CourtSourceResult]:
        raise NotImplementedError


# Backward-compatible abstract classes
class PropertySourceAdapter(ABC):
    source_name: str

    @abstractmethod
    async def property_search(self, query: PropertySearchInput) -> PropertySourceResult:
        raise NotImplementedError


class RecordSourceAdapter(ABC):
    source_name: str

    @abstractmethod
    async def record_search(
        self, query: GISearchInput, owner_variations: list[str]
    ) -> list[RecordSourceResult]:
        raise NotImplementedError
