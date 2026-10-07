import logging
import re
import urllib.parse
import httpx
from bs4 import BeautifulSoup

from app.sources.base import DiscoveredDirectorySources, NETRDirectoryAdapter

logger = logging.getLogger(__name__)


def slugify_county(text: str) -> str:
    """Normalize county name to NETR Online URL slug format."""
    clean = re.sub(r"(?i)\s+(county|parish|borough|city|census area)\b", "", text).strip()
    return re.sub(r"[^a-zA-Z0-9]+", "_", clean).lower().strip("_")


# Curated official government portals for major counties across the US
KNOWN_COUNTY_PORTALS: dict[str, dict[str, str]] = {
    "bradford_fl": {
        "recorder": "https://www.bradfordclerk.com/",
        "assessor": "https://www.bradfordappraiser.com/",
        "treasurer": "https://www.bradfordtaxcollector.com/",
        "gis": "https://map.netronline.com/fl-bradford",
        "court": "https://www.bradfordclerk.com/court-records/",
    },
    "travis_tx": {
        "recorder": "https://www.traviscountytx.gov/county-clerk",
        "assessor": "https://www.traviscad.org/",
        "treasurer": "https://tax-office.traviscountytx.gov/",
        "gis": "https://map.netronline.com/tx-travis",
        "court": "https://www.traviscountytx.gov/district-clerk",
    },
    "harris_tx": {
        "recorder": "https://www.cchctx.org/",
        "assessor": "https://hcad.org/property-search.html",
        "treasurer": "https://www.hctax.net/",
        "gis": "https://map.netronline.com/tx-harris",
        "court": "https://www.cchctx.org/records",
    },
    "dallas_tx": {
        "recorder": "https://www.dallascounty.org/government/county-clerk/",
        "assessor": "https://www.dallascad.org/",
        "treasurer": "https://www.dallascounty.org/departments/tax/",
        "gis": "https://map.netronline.com/tx-dallas",
        "court": "https://www.dallascounty.org/government/courts/",
    },
    "los_angeles_ca": {
        "recorder": "https://lavote.gov/home/records",
        "assessor": "https://portal.assessor.lacounty.gov/",
        "treasurer": "https://ttc.lacounty.gov/",
        "gis": "https://map.netronline.com/ca-los_angeles",
        "court": "https://www.lacourt.org/",
    },
    "miami_dade_fl": {
        "recorder": "https://www.miamidadeclerk.gov/clerk/official-records.page",
        "assessor": "https://www.miamidade.gov/pa/",
        "treasurer": "https://miamidade.county-taxes.com/",
        "gis": "https://map.netronline.com/fl-miami_dade",
        "court": "https://www.miamidadeclerk.gov/clerk/civil.page",
    },
    "orange_fl": {
        "recorder": "https://myorangeclerk.com/",
        "assessor": "https://ocpafl.org/",
        "treasurer": "https://octaxcol.com/",
        "gis": "https://map.netronline.com/fl-orange",
        "court": "https://myorangeclerk.com/",
    },
    "cook_il": {
        "recorder": "https://www.cookcountyclerkil.gov/recordings",
        "assessor": "https://www.cookcountyassessor.com/",
        "treasurer": "https://www.cookcountytreasurer.com/",
        "gis": "https://map.netronline.com/il-cook",
        "court": "https://www.cookcountyclerkofcourt.org/",
    },
    "maricopa_az": {
        "recorder": "https://recorder.maricopa.gov/",
        "assessor": "https://mcassessor.maricopa.gov/",
        "treasurer": "https://treasurer.maricopa.gov/",
        "gis": "https://map.netronline.com/az-maricopa",
        "court": "https://www.clerkofcourt.maricopa.gov/",
    },
    "king_wa": {
        "recorder": "https://kingcounty.gov/en/dept/records-licensing/records-and-licensing-services/recorders-office",
        "assessor": "https://kingcounty.gov/en/dept/assessors",
        "treasurer": "https://kingcounty.gov/en/dept/finance-business-operations/treasury-operations",
        "gis": "https://map.netronline.com/wa-king",
        "court": "https://kingcounty.gov/en/dept/superior-court-clerk",
    },
    "fulton_ga": {
        "recorder": "https://www.fultonclerk.org/",
        "assessor": "https://fultonassessor.org/",
        "treasurer": "https://www.fultoncountytaxes.org/",
        "gis": "https://map.netronline.com/ga-fulton",
        "court": "https://www.fultonclerk.org/",
    },
    "new_castle_de": {
        "recorder": "https://www.newcastlede.gov/175/Recorder-of-Deeds",
        "assessor": "https://www.newcastlede.gov/181/Assessment-Division",
        "treasurer": "https://www.newcastlede.gov/188/Treasury-Division",
        "gis": "https://map.netronline.com/de-new_castle",
        "court": "https://courts.delaware.gov/",
    },
}


class NETRDirectoryService(NETRDirectoryAdapter):
    """
    Production service for public record source discovery.
    Uses NETR Online (https://publicrecords.netronline.com/) as a source discovery directory,
    not as a centralized database.
    """

    def __init__(self, timeout_seconds: float = 6.0):
        self.timeout_seconds = timeout_seconds
        self.base_url = "https://publicrecords.netronline.com"

    async def discover_sources(self, state: str, county: str) -> DiscoveredDirectorySources:
        st = state.strip().upper()
        slug = slugify_county(county)
        key = f"{slug}_{st.lower()}"

        netr_county_dir = f"{self.base_url}/state/{st}/county/{slug}"
        netr_state_dir = f"{self.base_url}/state/{st}"
        netr_gis = f"https://map.netronline.com/{st.lower()}-{slug}"
        historic_aerials = "https://www.historicaerials.com/"
        data_store = "https://datastore.netronline.com/"

        # Start with curated known portal mappings
        portals = KNOWN_COUNTY_PORTALS.get(key, {})
        assessor_portal = portals.get("assessor", netr_county_dir)
        recorder_portal = portals.get("recorder", netr_county_dir)
        treasurer_portal = portals.get("treasurer", netr_county_dir)
        gis_portal = portals.get("gis", netr_gis)
        court_portal = portals.get("court", netr_county_dir)
        raw_links: dict[str, str] = {}

        # Attempt live directory discovery from NETR directory page if not already in known portals
        if not portals:
            try:
                async with httpx.AsyncClient(timeout=self.timeout_seconds, follow_redirects=True) as client:
                    resp = await client.get(
                        netr_county_dir,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        },
                    )
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "lxml")
                        for a in soup.find_all("a", href=True):
                            href = a["href"].strip()
                            text = a.get_text().strip().lower()
                            if not href.startswith("http"):
                                continue
                            if "netronline.com" in href or "google.com" in href:
                                continue

                            raw_links[text] = href

                            if any(w in text for w in ["assessor", "appraiser", "cad", "property search", "evaluation"]):
                                assessor_portal = href
                            elif any(w in text for w in ["recorder", "clerk", "register of deeds", "records search"]):
                                recorder_portal = href
                            elif any(w in text for w in ["tax", "treasurer", "tax collector", "tax office"]):
                                treasurer_portal = href
                            elif any(w in text for w in ["gis", "parcel map", "mapping", "arcgis"]):
                                gis_portal = href
                            elif any(w in text for w in ["court", "circuit", "docket", "civil index"]):
                                court_portal = href
            except Exception as e:
                logger.warning("Live NETR directory discovery timed out or failed for %s, %s: %s", county, state, e)

        return DiscoveredDirectorySources(
            state=st,
            county=county,
            county_slug=slug,
            netr_county_directory=netr_county_dir,
            netr_state_directory=netr_state_dir,
            netr_gis_map=netr_gis,
            historic_aerials=historic_aerials,
            property_data_store=data_store,
            assessor_portal=assessor_portal,
            recorder_portal=recorder_portal,
            treasurer_portal=treasurer_portal,
            gis_portal=gis_portal,
            court_portal=court_portal,
            raw_directory_links=raw_links,
        )
