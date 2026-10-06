from app.config import Settings, get_settings
from app.schemas import GISearchInput, PropertySearchInput
from app.sources.base import (
    PropertySourceAdapter,
    PropertySourceResult,
    RecordSourceAdapter,
    RecordSourceResult,
    SourceUnavailableError,
)
from app.sources.mock_data import is_mock_property, mock_property_result, mock_recorder_records


class NetrAdapter(PropertySourceAdapter, RecordSourceAdapter):
    """Authorized NETR/data-store boundary. No scraping or access-control bypasses."""

    source_name = "netr"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def property_search(self, query: PropertySearchInput) -> PropertySourceResult:
        if self.settings.source_mode == "mock":
            if is_mock_property(query.address, query.county, query.state):
                return mock_property_result("mock-netr")
            raise SourceUnavailableError("No development fixture exists for this property")
        if not self.settings.netr_api_key:
            raise SourceUnavailableError("Authorized NETR credentials are not configured")
        raise SourceUnavailableError("Authorized NETR provider implementation is not configured")

    async def record_search(
        self, query: GISearchInput, owner_variations: list[str]
    ) -> list[RecordSourceResult]:
        if self.settings.source_mode == "mock":
            return (
                mock_recorder_records()
                if is_mock_property(query.address, query.county, query.state)
                else []
            )
        if not self.settings.netr_api_key:
            raise SourceUnavailableError("Authorized NETR credentials are not configured")
        raise SourceUnavailableError("Authorized NETR provider implementation is not configured")
