from app.config import Settings, get_settings
from app.schemas import PropertySearchInput
from app.sources.base import PropertySourceAdapter, PropertySourceResult
from app.sources.netr_adapter import NetrAdapter


class AssessorAdapter(PropertySourceAdapter):
    source_name = "assessor"

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.netr = NetrAdapter(self.settings)

    async def property_search(self, query: PropertySearchInput) -> PropertySourceResult:
        res = await self.netr.property_search(query)
        res.source_name = self.source_name
        return res

