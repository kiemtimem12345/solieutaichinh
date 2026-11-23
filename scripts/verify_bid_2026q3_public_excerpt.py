#!/usr/bin/env python3
"""Read-only exact-VND crosscheck of the provisional BID Q3/2026 issuer excerpt.

This is not a source PDF hash verification and must never promote BID 2026Q3
or previously unverified BID periods to validated production automatically.
"""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/BID-2026Q3-official-web-excerpt-preliminary-million-vnd.json"
PRODUCTION = ROOT / "data/financials-BID.json"

def verify(a: dict, data: dict) -> int:
    assert a["ticker"] == "BID" and a["period"] == "2026-Q3"
    assert a["scope"] == "consolidated" and a["unit"] == "triệu VND"
    assert a["source_pdf_sha256_verified"] is True
    assert a["q3_signed_source_pdf"]["pdf_sha256"] == "98a9b501e706c1a195c3a475f81ab60dcaa7db3c43ae2bfd10a77b3faf0424be"
    assert a["h1_reviewed_consolidated_original"]["pdf_sha256"] == "3c3f6c39c9ca9f737c3d8d52893d7320be29dbb1a4bcecfdf062fad2b45106d2"
    assert a["manually_visual_reviewed"] is True
    assert a["q3_signed_source_pdf"]["visual_source_verified"] is True
    assert a["production_eligible"] is False
    assert a["do_not_overwrite_previously_unverified_bid_2025_or_2026q1q2"] is True
    assert len(a["required_completion_gates"]) == 5
    assert data["symbol"] == "BID"
    assert [r["period"] for r in data["items"]] == [
        "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"
    ], "Cannot silently publish an excerpt-only BID Q3 record"
    assert all(r.get("verification_status") == "auto_extracted_pending_visual_review" for r in data["items"])
    b, q, y, c = (
        a["b01_2026_09_30_million_vnd"],
        a["b03_q3_direct_million_vnd"],
        a["b03_9m_ytd_million_vnd"],
        a["b04_9m_ytd_million_vnd"],
    )
    eq = {}
    eq["b01_balance"] = b["total_assets"] - b["total_liabilities"] - b["equity"]
    eq["b01_liability_classes"] = (
        sum(b[k] for k in (
            "government_borrowings", "interbank_liabilities", "customer_deposits",
            "derivative_liabilities", "trust_liabilities", "valuable_papers",
            "other_liabilities"
        )) - b["total_liabilities"]
    )
    eq["b01_equity_classes"] = (
        sum(b[k] for k in (
            "owner_capital", "owner_funds", "fx_equity", "retained", "minority_equity"
        )) - b["equity"]
    )
    income_cols = ("net_interest", "services", "fx", "trading", "investment", "other", "contribution")
    eq["q3_revenue_7_classes"] = sum(q[k] for k in income_cols) - q["operating_income"]
    eq["q3_preprov"] = q["operating_income"] - q["operating_expenses"] - q["before_provision"]
    eq["q3_pretax"] = q["before_provision"] - q["credit_provision"] - q["pretax_profit"]
    eq["q3_net_profit"] = q["pretax_profit"] - q["tax_expense"] - q["net_profit"]
    eq["q3_parent_nci"] = q["net_profit"] - q["nci_profit"] - q["parent_profit"]
    eq["y9_revenue_visual_7_classes"] = (
        sum(y[k] for k in ("net_interest", "services", "fx", "trading", "other", "contribution"))
        + y["investment_visual_confirmed"]
        - y["operating_income_from_printed_preprovision_plus_opex"]
    )
    eq["y9_preprov"] = y["operating_income_from_printed_preprovision_plus_opex"] - y["operating_expenses"] - y["before_provision"]
    eq["y9_pretax"] = y["before_provision"] - y["credit_provision"] - y["pretax_profit"]
    eq["y9_net_profit"] = y["pretax_profit"] - y["tax_expense"] - y["net_profit"]
    eq["y9_parent_nci"] = y["net_profit"] - y["nci_profit"] - y["parent_profit"]
    eq["b04_investing"] = (
        c["investing_capex"] + c["investing_sale_proceeds"]
        + c["investing_disposal_cost"] + c["investing_dividends"]
        - c["investing"]
    )
    eq["b04_financing"] = (
        c["financing_new_equity"] + c["financing_dividends_paid"]
        + c["financing_new_longterm"] + c["financing_repaid_longterm"]
        - c["financing"]
    )
    eq["b04_cash_sections"] = c["operating"] + c["investing"] + c["financing"] - c["net_cash_change"]
    eq["b04_cash_open_end"] = c["year_open_cash"] + c["net_cash_change"] - c["ending_cash"]
    assert len(eq) == 17 and all(value == 0 for value in eq.values()), eq

    # Important: web text appears to have a sign issue; preserve it as an
    # unresolved source-text exception instead of silently making a 9M subtotal add.
    exception = a["text_extraction_exception"]
    component_sum = sum(y[k] for k in (
        "net_interest", "services", "fx", "trading", "other", "contribution"
    )) + y["investment_text_extraction"]
    residual = component_sum - y["operating_income_from_printed_preprovision_plus_opex"]
    assert residual == -12490 == exception["source_text_difference_million"]
    assert component_sum == exception["component_sum_million"]
    assert y["investment_text_extraction"] == exception["extracted_signed_component_million"]
    deviation = abs(Decimal(residual) / Decimal(y["operating_income_from_printed_preprovision_plus_opex"]) * 100)
    assert deviation < Decimal(str(exception["user_latest_tolerance_pct"]))
    assert a["production_eligible"] is False
    assert exception["signed_visual_component_million"] == 6245
    assert exception["visual_component_sum_million"] == y["operating_income_from_printed_preprovision_plus_opex"]
    assert exception["accounting_residual_after_visual_million"] == 0
    assert exception["status"] == "resolved_by_signed_original_visual_20261123"
    return len(eq)

def main() -> None:
    src = json.loads(LEDGER.read_text("utf-8"))
    production = json.loads(PRODUCTION.read_text("utf-8"))
    checks = verify(src, production)
    for name in ("tamper_balance", "tamper_cash", "tamper_profit", "publish_unverified", "tamper_visual_sign"):
        clone, pdata = deepcopy(src), deepcopy(production)
        if name == "tamper_balance":
            clone["b01_2026_09_30_million_vnd"]["total_assets"] += 1
        elif name == "tamper_cash":
            clone["b04_9m_ytd_million_vnd"]["operating"] += 1
        elif name == "tamper_profit":
            clone["b03_q3_direct_million_vnd"]["net_profit"] += 1
        elif name == "tamper_visual_sign":
            clone["b03_9m_ytd_million_vnd"]["investment_visual_confirmed"] = -6245
        else:
            clone["production_eligible"] = True
        try:
            verify(clone, pdata)
        except (AssertionError, TypeError, KeyError):
            pass
        else:
            raise AssertionError("Failed to catch " + name)
    print(f"PASS provisional BID Q3 issuer PDF text: {checks} exact accounting identities, 5 negative controls.")
    print("BID 2026Q3 source PDF SHA and reviewed H1 quarter cash remain gated; no BID production changes.")
if __name__ == "__main__":
    main()
