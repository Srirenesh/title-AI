from app.config import Settings, get_settings
from app.schemas import GISearchInput
from app.sources.base import RecordSourceAdapter, RecordSourceResult, SourceUnavailableError
from app.sources.mock_data import is_mock_property, mock_recorder_records


class RecorderAdapter(RecordSourceAdapter):
    source_name = "recorder"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def record_search(
        self, query: GISearchInput, owner_variations: list[str]
    ) -> list[RecordSourceResult]:
        if self.settings.source_mode == "mock":
            return (
                mock_recorder_records()
                if is_mock_property(query.address, query.county, query.state)
                else []
            )
        if not self.settings.recorder_api_key:
            raise SourceUnavailableError("Authorized recorder credentials are not configured")
        raise SourceUnavailableError("Authorized recorder provider implementation is not configured")
