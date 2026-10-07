import pytest
import pytest_asyncio
import uuid
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.models import DocumentCategory, RecordType, SearchStatus
from app.schemas import AddressSearchInput, APNSearchInput, OwnerSearchInput, UnifiedSearchInput
from app.services.matching import calculate_property_match_confidence
from app.services.normalization import normalize_address, normalize_apn, parse_owner_details
from app.services.search_orchestrator import SearchOrchestrator
from app.sources.netr_directory import NETRDirectoryService

# In-memory SQLite async test database
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_normalization_and_parsing():
    addr = normalize_address("4320 Northwest CR 225, Lawtey, Florida 32058")
    assert "NW" in addr["street"]
    assert addr["state"] == "FL"

    apn_clean = normalize_apn("12007-00-418.00")
    assert apn_clean == "120070041800"

    owner = parse_owner_details("Arthur & Brenda Pendelton")
    assert owner["last_name"] == "Pendelton"
    assert owner["entity_type"] == "INDIVIDUAL"

    entity_owner = parse_owner_details("Lawtey Pineview Estates, LLC")
    assert entity_owner["entity_type"] == "LLC"


@pytest.mark.asyncio
async def test_netr_directory_source_discovery():
    service = NETRDirectoryService()
    discovered = await service.discover_sources("FL", "Bradford")

    assert discovered.state == "FL"
    assert discovered.county == "Bradford"
    assert "netronline.com" in discovered.netr_county_directory
    assert discovered.assessor_portal is not None
    assert discovered.recorder_portal is not None
    assert discovered.treasurer_portal is not None
    assert discovered.gis_portal is not None


@pytest.mark.asyncio
async def test_search_by_address_orchestration():
    orchestrator = SearchOrchestrator()
    async with TestSessionLocal() as session:
        report = await orchestrator.execute_search(
            session=session,
            search_type="address",
            query_payload={"address": "4320 NW CR 225, Lawtey, FL 32058", "county": "Bradford", "state": "FL"},
        )

        assert report.property_id is not None
        assert report.search_status == SearchStatus.COMPLETED
        assert report.confidence_score >= 0.95
        assert "Arthur" in report.current_owner.full_name
        assert len(report.deeds) >= 2
        assert len(report.mortgages) >= 1
        assert len(report.taxes) >= 1
        assert len(report.chain_of_title) >= 2
        assert report.discovered_sources.recorder_portal is not None


@pytest.mark.asyncio
async def test_search_by_apn_orchestration():
    orchestrator = SearchOrchestrator()
    async with TestSessionLocal() as session:
        report = await orchestrator.execute_search(
            session=session,
            search_type="apn",
            query_payload={"apn": "12007-00418", "county": "Bradford", "state": "FL"},
        )

        assert report.search_status == SearchStatus.COMPLETED
        assert report.confidence_score == 1.0  # Exact APN match gives 1.0
        assert "Arthur" in report.current_owner.full_name
        assert report.property_overview.apn == "12007-00418"


@pytest.mark.asyncio
async def test_search_by_owner_orchestration():
    orchestrator = SearchOrchestrator()
    async with TestSessionLocal() as session:
        report = await orchestrator.execute_search(
            session=session,
            search_type="owner",
            query_payload={"first_name": "Arthur", "last_name": "Pendelton", "county": "Bradford", "state": "FL"},
        )

        assert report.search_status == SearchStatus.COMPLETED
        assert "Pendelton" in report.current_owner.full_name


@pytest.mark.asyncio
async def test_rest_api_search_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Login to get dev token
        auth_resp = await client.post(
            "/api/auth/token",
            json={"username": "admin", "password": "change-me"},
        )
        assert auth_resp.status_code == 200
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Test Unified Search
        search_resp = await client.post(
            "/api/search/property",
            headers=headers,
            json={"query": "4320 NW CR 225, Lawtey, FL 32058", "search_type": "auto"},
        )
        assert search_resp.status_code == 200
        data = search_resp.json()
        assert data["property_id"] is not None
        assert len(data["deeds"]) >= 2
        assert len(data["mortgages"]) >= 1
        assert len(data["chain_of_title"]) >= 2

        prop_id = data["property_id"]

        # 3. Test Individual Category Sub-endpoints
        deeds_resp = await client.get(f"/api/property/{prop_id}/deeds", headers=headers)
        assert deeds_resp.status_code == 200
        assert len(deeds_resp.json()) >= 2

        mtg_resp = await client.get(f"/api/property/{prop_id}/mortgages", headers=headers)
        assert mtg_resp.status_code == 200
        assert len(mtg_resp.json()) >= 1

        taxes_resp = await client.get(f"/api/property/{prop_id}/taxes", headers=headers)
        assert taxes_resp.status_code == 200
        assert len(taxes_resp.json()) >= 1

        # 4. Test Source Registry Discovery Endpoint
        sources_resp = await client.get("/api/sources/registry?state=FL&county=Bradford", headers=headers)
        assert sources_resp.status_code == 200
        src_data = sources_resp.json()
        assert "netronline.com" in src_data["netr_county_directory"]
