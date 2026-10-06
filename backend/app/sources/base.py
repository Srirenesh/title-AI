from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from app.models import RecordType
from app.schemas import GISearchInput, PropertySearchInput


class SourceUnavailableError(RuntimeError):
    pass


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
