from app.config import Settings, get_settings
from app.schemas import PropertySearchInput
from app.sources.base import PropertySourceAdapter, PropertySourceResult, SourceUnavailableError
from app.sources.mock_data import is_mock_property, mock_property_result


class AssessorAdapter(PropertySourceAdapter):
    source_name = "assessor"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def property_search(self, query: PropertySearchInput) -> PropertySourceResult:
        if self.settings.source_mode == "mock":
            if is_mock_property(query.address, query.county, query.state):
                return mock_property_result("mock-assessor")
            raise SourceUnavailableError("No development fixture exists for this property")
        if not self.settings.assessor_api_key:
            raise SourceUnavailableError("Authorized assessor credentials are not configured")
        raise SourceUnavailableError("Authorized assessor provider implementation is not configured")
