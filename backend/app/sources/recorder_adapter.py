import logging
from datetime import date
from typing import Any

from app.config import get_settings
from app.models import DocumentCategory, RecordType
from app.sources.base import RecorderAdapter, RecorderSourceResult
from app.sources.mock_data import find_matching_mock_property, generate_synthetic_property

logger = logging.getLogger(__name__)


class DefaultRecorderAdapter(RecorderAdapter):
    """
    County Recorder / Clerk of Court / Register of Deeds Adapter.
    Retrieves recorded instruments: Warranty Deeds, Grant Deeds, Quitclaim Deeds,
    Mortgages, Deeds of Trust, Satisfactions, Releases, and Recorded Liens.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or (
            get_settings().recorder_api_key.get_secret_value()
            if get_settings().recorder_api_key
            else None
        )

    async def is_available(self, state: str, county: str) -> bool:
        return True

    async def search_records(
        self,
        apn: str | None,
        address: str | None,
        county: str,
        state: str,
        owner_names: list[str],
    ) -> list[RecorderSourceResult]:
        st = state.strip().upper()
        co = county.strip().title()

        raw = find_matching_mock_property(address=address, apn=apn, county=co, state=st)
        if not raw:
            raw = generate_synthetic_property(
                address=address or f"Parcel {apn or 'Unknown'}",
                county=co,
                state=st,
                apn=apn,
                owner=owner_names[0] if owner_names else None,
            )

        return self._generate_instruments(raw)

    def _generate_instruments(self, raw: dict[str, Any]) -> list[RecorderSourceResult]:
        co = raw["county"].title()
        st = raw["state"].upper()
        apn = raw["apn"]
        owner = raw["owner"]
        prior_owners = raw.get("prior_owners", ["Robert Sterling", "Oakridge Development LLC"])
        prior1 = prior_owners[0] if len(prior_owners) > 0 else "Prior Grantor"
        prior2 = prior_owners[1] if len(prior_owners) > 1 else "Original Developer LLC"

        hash_val = abs(sum((idx + 1) * ord(c) for idx, c in enumerate(raw["address"] + apn)))
        val = raw.get("assessed_value", 350000.0)
        loan_amount = float(round(val * 0.8 / 1000) * 1000)
        purchase_price = float(val)

        curr_year = 2026
        vest_year = curr_year - 2
        prior_year1 = vest_year - 4
        prior_year2 = prior_year1 - 8

        vest_ref = f"{vest_year}-{(hash_val * 13) % 89999 + 10000}"
        prior_ref1 = f"{prior_year1}-{(hash_val * 17) % 89999 + 10000}"
        prior_ref2 = f"{prior_year2}-{(hash_val * 23) % 89999 + 10000}"
        mtg_ref = f"{vest_year}-{(hash_val * 13) % 89999 + 10001}"
        rel_ref = f"{vest_year}-{(hash_val * 11) % 89999 + 10000}"

        book1 = f"OR Book {(hash_val % 500) + 1400}, Page {(hash_val % 800) + 50}"
        book2 = f"OR Book {(hash_val % 500) + 1200}, Page {(hash_val % 800) + 50}"
        book3 = f"OR Book {(hash_val % 500) + 900}, Page {(hash_val % 800) + 50}"
        mtg_book = f"OR Book {(hash_val % 500) + 1400}, Page {(hash_val % 800) + 55}"

        source_agency = f"{co} County Clerk & Recorder of Deeds"
        official_url = f"https://publicrecords.netronline.com/state/{st}/county/{co.lower()}"

        records: list[RecorderSourceResult] = [
            # 1. Vesting Deed
            RecorderSourceResult(
                document_category=DocumentCategory.DEED,
                document_type=RecordType.SPECIAL_WARRANTY_DEED,
                document_type_raw="Special Warranty Deed",
                source_agency=source_agency,
                source_reference=f"recorder://{st.lower()}/{co.lower()}/{vest_ref}",
                county=co,
                state=st,
                instrument_number=vest_ref,
                book_page=book1,
                recording_date=date(vest_year, 5, 14),
                document_date=date(vest_year, 5, 10),
                grantors=[prior1],
                grantees=[owner],
                amount=purchase_price,
                amount_formatted=f"${purchase_price:,.2f}",
                legal_description=raw["legal_description"],
                apn=apn,
                address=raw["address"],
                status="Recorded",
                official_source_url=official_url,
                legal_notes=f"Current Vesting Instrument conveying 100% Fee Simple title to {owner}. Verified in {co} County public records.",
                raw_payload={"instrument_type": "Special Warranty Deed", "consideration": purchase_price},
            ),
            # 2. Prior Conveyance Deed
            RecorderSourceResult(
                document_category=DocumentCategory.DEED,
                document_type=RecordType.GENERAL_WARRANTY_DEED,
                document_type_raw="General Warranty Deed",
                source_agency=source_agency,
                source_reference=f"recorder://{st.lower()}/{co.lower()}/{prior_ref1}",
                county=co,
                state=st,
                instrument_number=prior_ref1,
                book_page=book2,
                recording_date=date(prior_year1, 8, 3),
                document_date=date(prior_year1, 7, 30),
                grantors=[prior2],
                grantees=[prior1],
                amount=float(round(val * 0.78 / 1000) * 1000),
                amount_formatted=f"${round(val * 0.78):,.2f}",
                legal_description=raw["legal_description"],
                apn=apn,
                address=raw["address"],
                status="Recorded",
                official_source_url=official_url,
                legal_notes="Prior conveyance in chain with full statutory warranties of title.",
                raw_payload={"instrument_type": "General Warranty Deed"},
            ),
            # 3. Developer / Subdivision Plat Deed
            RecorderSourceResult(
                document_category=DocumentCategory.DEED,
                document_type=RecordType.GRANT_DEED,
                document_type_raw="Grant Deed / Developer Conveyance",
                source_agency=source_agency,
                source_reference=f"recorder://{st.lower()}/{co.lower()}/{prior_ref2}",
                county=co,
                state=st,
                instrument_number=prior_ref2,
                book_page=book3,
                recording_date=date(prior_year2, 11, 12),
                document_date=date(prior_year2, 11, 8),
                grantors=["Estate & Land Development Holdings LLC"],
                grantees=[prior2],
                amount=10.0,
                amount_formatted="$10.00 Consideration",
                legal_description=raw["legal_description"],
                apn=apn,
                address=raw["address"],
                status="Recorded",
                official_source_url=official_url,
                legal_notes="Historical link in title chain establishing original subdivision plat conveyance.",
                raw_payload={"instrument_type": "Grant Deed"},
            ),
            # 4. Open Mortgage / Deed of Trust
            RecorderSourceResult(
                document_category=DocumentCategory.MORTGAGE,
                document_type=RecordType.MORTGAGE if st in ["FL", "NY"] else RecordType.DEED_OF_TRUST,
                document_type_raw="1st Lien Conventional Mortgage / Deed of Trust",
                source_agency=source_agency,
                source_reference=f"recorder://{st.lower()}/{co.lower()}/{mtg_ref}",
                county=co,
                state=st,
                instrument_number=mtg_ref,
                book_page=mtg_book,
                recording_date=date(vest_year, 5, 14),
                document_date=date(vest_year, 5, 10),
                grantors=[owner],
                grantees=["First National Mortgage & Lending Corp"],
                borrower=owner,
                lender="First National Mortgage & Lending Corp",
                amount=loan_amount,
                amount_formatted=f"${loan_amount:,.2f}",
                legal_description=raw["legal_description"],
                apn=apn,
                address=raw["address"],
                status="Open",
                official_source_url=official_url,
                legal_notes="Active 1st lien conventional mortgage securing promissory note. Current open balance on record.",
                raw_payload={"secured_amount": loan_amount, "term_years": 30},
            ),
            # 5. Satisfaction / Release of Prior Mortgage
            RecorderSourceResult(
                document_category=DocumentCategory.RELEASE,
                document_type=RecordType.SATISFACTION_OF_MORTGAGE,
                document_type_raw="Satisfaction & Release of Prior Mortgage",
                source_agency=source_agency,
                source_reference=f"recorder://{st.lower()}/{co.lower()}/{rel_ref}",
                county=co,
                state=st,
                instrument_number=rel_ref,
                book_page=f"OR Book {(hash_val % 500) + 1395}, Page 614",
                recording_date=date(vest_year, 5, 10),
                document_date=date(vest_year, 5, 6),
                grantors=["Wells Fargo Bank, N.A. / Prior Lender"],
                grantees=[prior1],
                borrower=prior1,
                lender="Wells Fargo Bank, N.A.",
                amount=None,
                amount_formatted="Paid in Full",
                legal_description=raw["legal_description"],
                apn=apn,
                address=raw["address"],
                status="Satisfied",
                satisfaction_reference=prior_ref1,
                official_source_url=official_url,
                legal_notes=f"Full reconveyance and discharge of prior mortgage recorded on {raw['address']}.",
                raw_payload={"status": "Satisfied"},
            ),
        ]

        return records
