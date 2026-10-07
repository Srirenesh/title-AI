from app.config import Settings, get_settings
from app.schemas import GISearchInput
from app.sources.base import RecordSourceAdapter, RecordSourceResult
from app.sources.netr_adapter import NetrAdapter


class RecorderAdapter(RecordSourceAdapter):
    source_name = "recorder"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.netr = NetrAdapter(self.settings)

    async def record_search(
        self, query: GISearchInput, owner_variations: list[str]
    ) -> list[RecordSourceResult]:
        records = await self.netr.record_search(query, owner_variations)
        for r in records:
            r.source_name = self.source_name
        return records

