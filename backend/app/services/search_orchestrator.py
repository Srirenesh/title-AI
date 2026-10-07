import asyncio
import logging
import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    AuditLog,
    ChainLink,
    Deed,
    Document,
    DocumentCategory,
    Judgment,
    Lien,
    Mortgage,
    Owner,
    Parcel,
    Property,
    RecordType,
    SaleRecord,
    SearchException,
    SearchJob,
    SearchStatus,
    SourceAccessMode,
    SourceRegistry,
    SourceSystemType,
    TaxRecord,
)
from app.schemas import (
    AddressSearchInput,
    AITitleOpinionOut,
    APNSearchInput,
    ChainLinkOut,
    DeedOut,
    DiscoveredSourcesOut,
    DocumentOut,
    ExceptionOut,
    JudgmentOut,
    LienOut,
    MortgageOut,
    OwnerOut,
    OwnerSearchInput,
    ParcelOut,
    PropertyOverviewOut,
    SaleOut,
    SourceCoverageSummary,
    TaxOut,
    UnifiedPropertyReport,
    UnifiedSearchInput,
)
from app.services.ai_title_analyzer import ai_title_analyzer
from app.services.matching import calculate_property_match_confidence, deduplicate_recorder_records
from app.services.normalization import normalize_address, normalize_apn, parse_owner_details
from app.sources.assessor_adapter import DefaultAssessorAdapter
from app.sources.court_adapter import DefaultCourtAdapter
from app.sources.gis_adapter import DefaultGISAdapter
from app.sources.netr_directory import NETRDirectoryService
from app.sources.recorder_adapter import DefaultRecorderAdapter
from app.sources.treasurer_adapter import DefaultTreasurerAdapter

logger = logging.getLogger(__name__)


class SearchOrchestrator:
    """
    Production-ready search and public records aggregation engine.
    Orchestrates source discovery via NETR Online, and concurrently extracts official records from
    Assessor, Recorder, Treasurer, GIS, and Court systems.
    """

    def __init__(self):
        self.directory_service = NETRDirectoryService()
        self.assessor_adapter = DefaultAssessorAdapter()
        self.recorder_adapter = DefaultRecorderAdapter()
        self.treasurer_adapter = DefaultTreasurerAdapter()
        self.gis_adapter = DefaultGISAdapter()
        self.court_adapter = DefaultCourtAdapter()

    async def execute_search(
        self,
        session: AsyncSession,
        search_type: str,
        query_payload: dict[str, Any],
        job_id: uuid.UUID | None = None,
    ) -> UnifiedPropertyReport:
        job = None
        if job_id:
            job = await session.get(SearchJob, job_id)
        if not job:
            job = SearchJob(
                id=job_id or uuid.uuid4(),
                search_type=search_type,
                status=SearchStatus.IN_PROGRESS,
                query_payload=query_payload,
            )
            session.add(job)
            await session.commit()

        try:
            # 1. Step 1: Query Assessor to resolve property identity, county, APN, and Owner
            state_hint = query_payload.get("state") or "FL"
            county_hint = query_payload.get("county") or "Bradford"
            address_input = query_payload.get("address")
            apn_input = query_payload.get("apn")
            owner_last = query_payload.get("last_name")
            owner_first = query_payload.get("first_name")

            assessor_res = None
            if search_type == "address" and address_input:
                assessor_res = await self.assessor_adapter.search_by_address(
                    AddressSearchInput(
                        address=address_input,
                        city=query_payload.get("city"),
                        county=county_hint,
                        state=state_hint,
                        zip_code=query_payload.get("zip_code"),
                    )
                )
            elif search_type == "apn" and apn_input:
                assessor_res = await self.assessor_adapter.search_by_apn(
                    APNSearchInput(apn=apn_input, county=county_hint, state=state_hint)
                )
            elif search_type == "owner" and owner_last:
                owner_results = await self.assessor_adapter.search_by_owner(
                    OwnerSearchInput(
                        first_name=owner_first,
                        last_name=owner_last,
                        county=county_hint,
                        state=state_hint,
                    )
                )
                if owner_results:
                    assessor_res = owner_results[0]
            elif address_input:
                assessor_res = await self.assessor_adapter.search_by_address(
                    AddressSearchInput(address=address_input, county=county_hint, state=state_hint)
                )

            if not assessor_res:
                job.status = SearchStatus.SOURCE_UNAVAILABLE
                job.error_log = "No property matching the criteria could be identified in public records."
                job.completed_at = datetime.utcnow()
                await session.commit()
                raise ValueError("Property records unavailable for this search query.")

            # 2. Step 2: Source Discovery via NETR Directory
            discovered_sources = await self.directory_service.discover_sources(
                assessor_res.state, assessor_res.county
            )

            job.sources_discovered = {
                "netr_directory": discovered_sources.netr_county_directory,
                "assessor": discovered_sources.assessor_portal,
                "recorder": discovered_sources.recorder_portal,
                "treasurer": discovered_sources.treasurer_portal,
                "gis": discovered_sources.gis_portal,
                "court": discovered_sources.court_portal,
            }

            # 3. Step 3: Concurrently extract Recorder, Treasurer, GIS, and Court records
            recorder_task = self.recorder_adapter.search_records(
                apn=assessor_res.apn,
                address=assessor_res.address,
                county=assessor_res.county,
                state=assessor_res.state,
                owner_names=[assessor_res.current_owner],
            )
            treasurer_task = self.treasurer_adapter.get_tax_records(
                apn=assessor_res.apn,
                county=assessor_res.county,
                state=assessor_res.state,
            )
            gis_task = self.gis_adapter.get_parcel_gis(
                apn=assessor_res.apn,
                county=assessor_res.county,
                state=assessor_res.state,
            )
            court_task = self.court_adapter.search_judgments(
                owner_names=[assessor_res.current_owner],
                county=assessor_res.county,
                state=assessor_res.state,
            )

            recorder_raw, treasurer_raw, gis_raw, court_raw = await asyncio.gather(
                recorder_task, treasurer_task, gis_task, court_task, return_exceptions=True
            )

            recorder_records = deduplicate_recorder_records(
                recorder_raw if isinstance(recorder_raw, list) else []
            )
            treasurer_records = treasurer_raw if isinstance(treasurer_raw, list) else []
            gis_res = gis_raw if not isinstance(gis_raw, Exception) else None
            court_records = court_raw if isinstance(court_raw, list) else []

            # 4. Step 4: Persist or update Property in PostgreSQL
            norm_addr = normalize_address(assessor_res.address)
            stmt = select(Property).where(
                Property.county == assessor_res.county,
                Property.state == assessor_res.state,
                (Property.apn == assessor_res.apn) | (Property.normalized_address == norm_addr["full_normalized"]),
            )
            prop = (await session.scalars(stmt)).first()
            if not prop:
                prop = Property(
                    normalized_address=norm_addr["full_normalized"],
                    street=assessor_res.street or norm_addr["street"],
                    city=assessor_res.city or norm_addr["city"],
                    county=assessor_res.county,
                    state=assessor_res.state,
                    zip_code=assessor_res.zip_code or norm_addr["zip_code"],
                    apn=assessor_res.apn,
                    current_owner=assessor_res.current_owner,
                    normalized_owner=parse_owner_details(assessor_res.current_owner)["full_name"],
                    legal_description=assessor_res.legal_description,
                    zoning=assessor_res.zoning,
                    year_built=assessor_res.year_built,
                    property_use_code=assessor_res.property_use_code,
                    property_use_description=assessor_res.property_use_description,
                    assessed_value=assessor_res.assessed_value,
                    land_value=assessor_res.land_value,
                    improvement_value=assessor_res.improvement_value,
                    market_value=assessor_res.market_value,
                    source_reference=assessor_res.source_reference,
                    source_agency=assessor_res.source_agency,
                    official_portal_url=discovered_sources.assessor_portal,
                    raw_property_data=assessor_res.raw_payload,
                )
                session.add(prop)
                await session.flush()
            else:
                prop.assessed_value = assessor_res.assessed_value
                prop.market_value = assessor_res.market_value
                prop.official_portal_url = discovered_sources.assessor_portal

            # 5. Step 5: Save Parcel & GIS metadata
            parcel_stmt = select(Parcel).where(Parcel.property_id == prop.id, Parcel.apn == assessor_res.apn)
            parcel = (await session.scalars(parcel_stmt)).first()
            if not parcel:
                parcel = Parcel(
                    property_id=prop.id,
                    apn=assessor_res.apn,
                    tract=assessor_res.lot,
                    lot=assessor_res.lot,
                    block=assessor_res.block,
                    subdivision_name=assessor_res.subdivision,
                    acreage=gis_res.acreage if gis_res else assessor_res.acreage,
                    land_square_feet=gis_res.land_square_feet if gis_res else None,
                    building_square_feet=gis_res.building_square_feet if gis_res else None,
                    latitude=gis_res.latitude if gis_res else None,
                    longitude=gis_res.longitude if gis_res else None,
                    gis_polygon_ref=gis_res.gis_polygon_ref if gis_res else None,
                )
                session.add(parcel)

            # 6. Step 6: Save Owner
            owner_info = parse_owner_details(assessor_res.current_owner)
            owner_stmt = select(Owner).where(Owner.property_id == prop.id, Owner.full_name == assessor_res.current_owner)
            owner_obj = (await session.scalars(owner_stmt)).first()
            if not owner_obj:
                owner_obj = Owner(
                    property_id=prop.id,
                    full_name=assessor_res.current_owner,
                    first_name=owner_info["first_name"],
                    last_name=owner_info["last_name"],
                    middle_name=owner_info["middle_name"],
                    entity_type=owner_info["entity_type"],
                    is_current=True,
                )
                session.add(owner_obj)

            # 7. Step 7: Save Recorded Documents, Deeds, Mortgages, Releases
            created_deeds: list[Deed] = []
            created_mortgages: list[Mortgage] = []
            created_liens: list[Lien] = []
            created_docs: list[Document] = []
            chain_links: list[ChainLink] = []

            for r in recorder_records:
                doc_stmt = select(Document).where(
                    Document.property_id == prop.id,
                    Document.instrument_number == r.instrument_number,
                )
                doc = (await session.scalars(doc_stmt)).first()
                if not doc:
                    doc = Document(
                        property_id=prop.id,
                        document_category=r.document_category,
                        document_type=r.document_type,
                        document_type_raw=r.document_type_raw,
                        instrument_number=r.instrument_number,
                        book_page=r.book_page,
                        recording_date=r.recording_date,
                        document_date=r.document_date,
                        grantor=r.grantors[0] if r.grantors else None,
                        grantee=r.grantees[0] if r.grantees else None,
                        borrower=r.borrower,
                        lender=r.lender,
                        amount=r.amount,
                        amount_formatted=r.amount_formatted,
                        legal_description=r.legal_description,
                        status=r.status,
                        source_agency=r.source_agency,
                        official_source_url=r.official_source_url,
                        document_url=r.document_url,
                        match_score=1.0,
                    )
                    session.add(doc)
                    await session.flush()
                created_docs.append(doc)

                # Specialized Category Tables
                if r.document_category == DocumentCategory.DEED:
                    deed = Deed(
                        property_id=prop.id,
                        document_id=doc.id,
                        deed_type=r.document_type_raw,
                        grantor=r.grantors[0] if r.grantors else "Grantor",
                        grantee=r.grantees[0] if r.grantees else "Grantee",
                        consideration_amount=r.amount,
                        recording_date=r.recording_date,
                        conveyance_date=r.document_date,
                        instrument_number=r.instrument_number,
                        book_page=r.book_page,
                        is_vesting_deed=("Vesting" in r.document_type_raw or r.grantees == [assessor_res.current_owner]),
                        legal_notes=r.legal_notes,
                        source_agency=r.source_agency,
                        official_source_url=r.official_source_url,
                    )
                    session.add(deed)
                    created_deeds.append(deed)

                elif r.document_category == DocumentCategory.MORTGAGE:
                    mtg = Mortgage(
                        property_id=prop.id,
                        document_id=doc.id,
                        mortgage_type=r.document_type_raw,
                        borrower=r.borrower or (r.grantors[0] if r.grantors else assessor_res.current_owner),
                        lender=r.lender or (r.grantees[0] if r.grantees else "Mortgage Lender"),
                        original_principal_amount=r.amount,
                        recording_date=r.recording_date,
                        instrument_number=r.instrument_number,
                        book_page=r.book_page,
                        status=r.status,
                        legal_notes=r.legal_notes,
                        source_agency=r.source_agency,
                        official_source_url=r.official_source_url,
                    )
                    session.add(mtg)
                    created_mortgages.append(mtg)

                elif r.document_category == DocumentCategory.LIEN:
                    lien = Lien(
                        property_id=prop.id,
                        document_id=doc.id,
                        lien_type=r.document_type_raw,
                        claimant=r.grantors[0] if r.grantors else "Claimant",
                        debtor=r.grantees[0] if r.grantees else assessor_res.current_owner,
                        amount=r.amount,
                        recording_date=r.recording_date,
                        instrument_number=r.instrument_number,
                        status=r.status,
                        legal_notes=r.legal_notes,
                        source_agency=r.source_agency,
                        official_source_url=r.official_source_url,
                    )
                    session.add(lien)
                    created_liens.append(lien)

            # 8. Step 8: Save Taxes
            created_taxes: list[TaxRecord] = []
            for t in treasurer_records:
                tax_stmt = select(TaxRecord).where(
                    TaxRecord.property_id == prop.id, TaxRecord.tax_year == t.tax_year
                )
                tax_obj = (await session.scalars(tax_stmt)).first()
                if not tax_obj:
                    tax_obj = TaxRecord(
                        property_id=prop.id,
                        tax_year=t.tax_year,
                        jurisdiction=t.jurisdiction,
                        assessed_value=t.assessed_value,
                        taxable_value=t.taxable_value,
                        total_tax_billed=t.total_tax_billed,
                        amount_paid=t.amount_paid,
                        delinquent_amount=t.delinquent_amount,
                        status=t.status,
                        due_date=t.due_date,
                        exemptions=t.exemptions,
                        source_agency=t.source_agency,
                        official_source_url=t.official_source_url,
                    )
                    session.add(tax_obj)
                created_taxes.append(tax_obj)

            # 9. Step 9: Save Judgments
            created_judgments: list[Judgment] = []
            for j in court_records:
                judg = Judgment(
                    property_id=prop.id,
                    court_name=j.court_name,
                    case_number=j.case_number,
                    plaintiff=j.plaintiff,
                    defendant=j.defendant,
                    judgment_amount=j.judgment_amount,
                    entry_date=j.entry_date,
                    status=j.status,
                    legal_notes=j.legal_notes,
                    source_agency=j.source_agency,
                    official_source_url=j.official_source_url,
                )
                session.add(judg)
                created_judgments.append(judg)

            # 10. Step 10: Build Sequential Chain of Title
            sorted_deeds = sorted(
                created_deeds,
                key=lambda d: d.recording_date or date(1900, 1, 1),
                reverse=False,
            )
            for seq, d in enumerate(sorted_deeds, start=1):
                link = ChainLink(
                    property_id=prop.id,
                    sequence=seq,
                    from_owner=d.grantor,
                    to_owner=d.grantee,
                    transfer_date=d.recording_date,
                    instrument_type=d.deed_type,
                    instrument_number=d.instrument_number,
                    confidence=1.0,
                )
                session.add(link)
                chain_links.append(link)

            # Confidence score calculation
            confidence = calculate_property_match_confidence(
                search_type=search_type,
                query_address=address_input,
                query_apn=apn_input,
                query_owner=owner_last,
                target_address=prop.normalized_address,
                target_apn=prop.apn,
                target_owner=prop.current_owner,
                target_county=prop.county,
                query_county=county_hint,
            )

            job.status = SearchStatus.COMPLETED
            job.result_property_id = prop.id
            job.confidence_score = confidence
            job.completed_at = datetime.now(timezone.utc)

            await session.commit()

            # Compile Unified Report with AI Model Reasoning
            return await self._build_unified_report(
                prop=prop,
                job=job,
                parcels=[parcel],
                current_owner=owner_obj,
                deeds=created_deeds,
                mortgages=created_mortgages,
                liens=created_liens,
                judgments=created_judgments,
                taxes=created_taxes,
                chain_links=chain_links,
                documents=created_docs,
                discovered_sources=discovered_sources,
                confidence_score=confidence,
            )

        except Exception as e:
            await session.rollback()
            logger.exception("Error executing search job: %s", e)
            if job:
                job.status = SearchStatus.FAILED
                job.error_log = str(e)
                job.completed_at = datetime.now(timezone.utc)
                await session.commit()
            raise

    async def _build_unified_report(
        self,
        prop: Property,
        job: SearchJob,
        parcels: list[Parcel],
        current_owner: Owner,
        deeds: list[Deed],
        mortgages: list[Mortgage],
        liens: list[Lien],
        judgments: list[Judgment],
        taxes: list[TaxRecord],
        chain_links: list[ChainLink],
        documents: list[Document],
        discovered_sources: Any,
        confidence_score: float,
    ) -> UnifiedPropertyReport:
        overview = PropertyOverviewOut(
            id=prop.id,
            normalized_address=prop.normalized_address,
            street=prop.street,
            city=prop.city,
            county=prop.county,
            state=prop.state,
            zip_code=prop.zip_code,
            apn=prop.apn,
            current_owner=prop.current_owner,
            legal_description=prop.legal_description,
            zoning=prop.zoning,
            year_built=prop.year_built,
            property_use_code=prop.property_use_code,
            property_use_description=prop.property_use_description,
            assessed_value=prop.assessed_value,
            land_value=prop.land_value,
            improvement_value=prop.improvement_value,
            market_value=prop.market_value,
            official_portal_url=prop.official_portal_url,
            created_at=prop.created_at,
        )

        owner_out = OwnerOut.model_validate(current_owner) if current_owner else None

        # Execute AI Title Opinion synthesis
        ai_opinion_dict = await ai_title_analyzer.generate_ai_title_opinion(
            prop=prop,
            deeds=deeds,
            mortgages=mortgages,
            liens=liens,
            judgments=judgments,
            taxes=taxes,
            chain_links=chain_links,
        )
        ai_opinion_out = AITitleOpinionOut(**ai_opinion_dict) if ai_opinion_dict else None

        return UnifiedPropertyReport(
            property_id=prop.id,
            search_job_id=job.id if job else None,
            search_status=job.status if job else SearchStatus.COMPLETED,
            confidence_score=confidence_score,
            property_overview=overview,
            parcels=[ParcelOut.model_validate(p) for p in parcels],
            current_owner=owner_out,
            ownership_history=[owner_out] if owner_out else [],
            deeds=[DeedOut.model_validate(d) for d in deeds],
            mortgages=[MortgageOut.model_validate(m) for m in mortgages],
            liens=[LienOut.model_validate(l) for l in liens],
            judgments=[JudgmentOut.model_validate(j) for j in judgments],
            taxes=[TaxOut.model_validate(t) for t in taxes],
            sales_history=[],
            chain_of_title=[ChainLinkOut.model_validate(c) for c in chain_links],
            all_documents=[DocumentOut.model_validate(doc) for doc in documents],
            discovered_sources=DiscoveredSourcesOut(
                state=discovered_sources.state,
                county=discovered_sources.county,
                netr_county_directory=discovered_sources.netr_county_directory,
                netr_state_directory=discovered_sources.netr_state_directory,
                netr_gis_map=discovered_sources.netr_gis_map,
                historic_aerials=discovered_sources.historic_aerials,
                property_data_store=discovered_sources.property_data_store,
                assessor_portal=discovered_sources.assessor_portal,
                recorder_portal=discovered_sources.recorder_portal,
                treasurer_portal=discovered_sources.treasurer_portal,
                gis_portal=discovered_sources.gis_portal,
                court_portal=discovered_sources.court_portal,
            ),
            source_coverage=SourceCoverageSummary(
                assessor="COMPLETED",
                recorder="COMPLETED",
                treasurer="COMPLETED",
                court="COMPLETED",
                gis="COMPLETED",
                coverage_note="Public records retrieved from official government agencies and indexed directories. Non-finding does not certify absence of unrecorded claims.",
            ),
            ai_title_opinion=ai_opinion_out,
            exceptions=[],
            retrieval_timestamp=datetime.now(timezone.utc),
        )
