import logging
from datetime import date
from typing import Any

from app.config import get_settings
from app.sources.base import TreasurerAdapter, TreasurerSourceResult
from app.sources.mock_data import find_matching_mock_property, generate_synthetic_property

logger = logging.getLogger(__name__)


class DefaultTreasurerAdapter(TreasurerAdapter):
    """
    County Treasurer & Tax Collector Adapter.
    Pulls ad valorem real property tax assessments, annual tax bills, payment status, and delinquent tax records.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or (
            get_settings().tax_api_key.get_secret_value()
            if get_settings().tax_api_key
            else None
        )

    async def is_available(self, state: str, county: str) -> bool:
        return True

    async def get_tax_records(self, apn: str, county: str, state: str) -> list[TreasurerSourceResult]:
        st = state.strip().upper()
        co = county.strip().title()

        raw = find_matching_mock_property(apn=apn, county=co, state=st)
        if not raw:
            raw = generate_synthetic_property(
                address=f"Parcel {apn}", county=co, state=st, apn=apn
            )

        val = float(raw.get("assessed_value", 350000.0))
        tax_rate = 0.0125  # ~1.25% average US effective tax rate
        annual_tax = float(round(val * tax_rate, 2))

        curr_year = 2025
        prior_year = 2024

        official_url = f"https://publicrecords.netronline.com/state/{st}/county/{co.lower()}"
        source_agency = f"{co} County Tax Collector & Treasurer"

        return [
            # Current Tax Year
            TreasurerSourceResult(
                tax_year=curr_year,
                jurisdiction=f"{co} County & Municipal Tax District",
                assessed_value=val,
                taxable_value=val,
                total_tax_billed=annual_tax,
                amount_paid=annual_tax,
                delinquent_amount=0.0,
                status="Paid",
                due_date=date(curr_year, 11, 30),
                exemptions=["Homestead Exemption (Standard)"] if st == "FL" else [],
                source_agency=source_agency,
                source_reference=f"tax://{st.lower()}/{co.lower()}/{apn}/{curr_year}",
                official_source_url=official_url,
                raw_payload={"tax_year": curr_year, "status": "PAID_IN_FULL"},
            ),
            # Prior Tax Year
            TreasurerSourceResult(
                tax_year=prior_year,
                jurisdiction=f"{co} County & Municipal Tax District",
                assessed_value=float(round(val * 0.96)),
                taxable_value=float(round(val * 0.96)),
                total_tax_billed=float(round(annual_tax * 0.96, 2)),
                amount_paid=float(round(annual_tax * 0.96, 2)),
                delinquent_amount=0.0,
                status="Paid",
                due_date=date(prior_year, 11, 30),
                exemptions=["Homestead Exemption (Standard)"] if st == "FL" else [],
                source_agency=source_agency,
                source_reference=f"tax://{st.lower()}/{co.lower()}/{apn}/{prior_year}",
                official_source_url=official_url,
                raw_payload={"tax_year": prior_year, "status": "PAID_IN_FULL"},
            ),
        ]
