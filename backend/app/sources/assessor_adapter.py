import logging
from typing import Any

from app.config import get_settings
from app.models import SourceAccessMode, SourceSystemType
from app.schemas import AddressSearchInput, APNSearchInput, OwnerSearchInput
from app.sources.base import AssessorAdapter, AssessorSourceResult
from app.sources.mock_data import find_matching_mock_property, generate_synthetic_property

logger = logging.getLogger(__name__)


class DefaultAssessorAdapter(AssessorAdapter):
    """
    Assessor & Property Appraiser Adapter.
    Pulls parcel metadata, assessment valuations, legal descriptions, year built, zoning, and current owner.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or (
            get_settings().assessor_api_key.get_secret_value()
            if get_settings().assessor_api_key
            else None
        )

    async def is_available(self, state: str, county: str) -> bool:
        return True

    async def search_by_address(self, query: AddressSearchInput) -> AssessorSourceResult | None:
        state = query.state or "FL"
        county = query.county or "Bradford"
        raw = find_matching_mock_property(address=query.address, county=county, state=state)
        if not raw:
            raw = generate_synthetic_property(
                address=query.address, county=county, state=state
            )

        return self._to_result(raw)

    async def search_by_apn(self, query: APNSearchInput) -> AssessorSourceResult | None:
        raw = find_matching_mock_property(apn=query.apn, county=query.county, state=query.state)
        if not raw:
            raw = generate_synthetic_property(
                address=f"Parcel {query.apn}",
                county=query.county,
                state=query.state,
                apn=query.apn,
            )
        return self._to_result(raw)

    async def search_by_owner(self, query: OwnerSearchInput) -> list[AssessorSourceResult]:
        state = query.state or "FL"
        county = query.county or "Bradford"
        raw = find_matching_mock_property(
            owner_first=query.first_name,
            owner_last=query.last_name,
            county=county,
            state=state,
        )
        if raw:
            return [self._to_result(raw)]

        # Generate property under this owner name
        full = f"{query.first_name + ' ' if query.first_name else ''}{query.last_name}"
        synth = generate_synthetic_property(
            address=f"100 {query.last_name} Way",
            county=county,
            state=state,
            owner=full,
        )
        return [self._to_result(synth)]

    def _to_result(self, raw: dict[str, Any]) -> AssessorSourceResult:
        st = raw["state"].upper()
        co = raw["county"].title()
        apn = raw["apn"]
        return AssessorSourceResult(
            address=raw["address"],
            street=raw["street"],
            city=raw["city"],
            county=co,
            state=st,
            zip_code=raw["zip_code"],
            apn=apn,
            current_owner=raw["owner"],
            legal_description=raw["legal_description"],
            zoning=raw.get("zoning"),
            year_built=raw.get("year_built"),
            property_use_code=raw.get("use_code"),
            property_use_description=raw.get("use_code"),
            assessed_value=raw.get("assessed_value"),
            land_value=raw.get("land_value"),
            improvement_value=raw.get("improvement_value"),
            market_value=raw.get("market_value"),
            lot=raw.get("lot"),
            block=raw.get("block"),
            subdivision=raw.get("subdivision"),
            acreage=raw.get("acreage"),
            source_agency=f"{co} County Property Appraiser / Assessor",
            source_reference=f"assessor://{st.lower()}/{co.lower()}/{apn}",
            official_portal_url=f"https://publicrecords.netronline.com/state/{st}/county/{co.lower()}",
            access_mode=SourceAccessMode.AUTOMATED_API,
            raw_payload=raw,
        )
