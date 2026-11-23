#!/usr/bin/env python3
"""Full source-ledger exact-VND validation for BID signed Q3 and reviewed H1.

Preserve 2025Q1-2026Q2 provisional records. Independently recompute 16 Q3
signed B03 lines vs 9M-H1, bank direct-method B04 quarter, and first-issued
vs reviewed H1 balance-sheet vintage. Fail closed on any unvalidated change.
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
    assert a["production_eligible"] is True
    assert a["do_not_overwrite_previously_unverified_bid_2025_or_2026q1q2"] is True
    assert len(a["required_completion_gates"]) == 5
    assert data["symbol"] == "BID"
    assert [r["period"] for r in data["items"]] == [
        "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"
    ], "BID periods must be 2025-Q1 to issuer-verified 2026-Q3 exactly"
    assert data["items"][0]["verification_status"] == "issuer_signed_BID_2025Q1_consolidated_B01_B03_B04_exact_VND_verified"
    assert data["items"][1]["verification_status"] == "issuer_signed_BID_2025Q2_first_issued_B01_B03_reviewedH1_minus_Q1_B04_verified"
    assert data["items"][2]["verification_status"] == "issuer_signed_BID_2025Q3_consolidated_B01_B03_B04_reviewedH1_quarter_exact_verified"
    assert data["items"][3]["verification_status"] == "issuer_signed_BID_2025Q4_first_issued_B01_B03_FY_audited_minus_signed9M_B04_verified"
    assert data["items"][4]["verification_status"] == "issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
    assert all(r.get("verification_status") == "auto_extracted_pending_visual_review" for r in data["items"][5:-1])
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

    h, hcash, qc = (
        a["b03_H1_reviewed_6m_million_vnd"],
        a["b04_H1_reviewed_6m_million_vnd"],
        a["b04_Q3_standalone_same_scope_million_vnd"],
    )
    reviewed_b01 = a["b01_H1_reviewed_2026_06_30_million_vnd"]
    eq["h1_balance"] = reviewed_b01["total_assets"] - reviewed_b01["total_liabilities"] - reviewed_b01["equity"]
    eq["h1_income"] = sum(h[k] for k in income_cols) - h["operating_income"]
    eq["h1_preprov"] = h["operating_income"] - h["operating_expenses"] - h["before_provision"]
    eq["h1_pretax"] = h["before_provision"] - h["credit_provision"] - h["pretax_profit"]
    eq["h1_profit"] = h["pretax_profit"] - h["tax_expense"] - h["net_profit"]
    eq["h1_parent"] = h["net_profit"] - h["nci_profit"] - h["parent_profit"]
    # All 16 signed direct Q3 current-period B03 values must equal 9M minus reviewed 6M.
    for k in ("net_interest", "services", "fx", "trading", "investment", "other",
              "contribution", "operating_income", "operating_expenses", "before_provision",
              "credit_provision", "pretax_profit", "tax_expense", "net_profit",
              "nci_profit", "parent_profit"):
        ykey = ("investment_visual_confirmed" if k == "investment" else
                "operating_income_from_printed_preprovision_plus_opex" if k == "operating_income"
                else k)
        eq["b03_Q3_9M_minus_reviewed_H1_" + k] = y[ykey] - h[k] - q[k]
    eq["h1_investing"] = (
        hcash["investing_capex"] + hcash["investing_sale_proceeds"] +
        hcash["investing_disposal_cost"] + hcash["investing_dividends"] -
        hcash["investing"]
    )
    eq["h1_financing"] = (
        hcash["financing_new_equity"] + hcash["financing_new_longterm"] +
        hcash["financing_repaid_longterm"] - hcash["financing"]
    )
    eq["h1_cash_sections"] = hcash["operating"] + hcash["investing"] + hcash["financing"] - hcash["net_cash_change"]
    eq["h1_cash_begin_end"] = hcash["year_open_cash"] + hcash["net_cash_change"] - hcash["ending_cash"]
    eq["year_open_cash_same_vintage"] = c["year_open_cash"] - hcash["year_open_cash"]
    for key in ("operating", "investing", "financing", "net_cash_change"):
        eq["q3_b04_9M_minus_H1_" + key] = c[key] - hcash[key] - qc[key]
    eq["q3_cash_period_open"] = qc["quarter_open_cash"] - hcash["ending_cash"]
    eq["q3_cash_period_end"] = qc["quarter_end_cash"] - c["ending_cash"]
    eq["q3_cash_sections"] = qc["operating"] + qc["investing"] + qc["financing"] - qc["net_cash_change"]
    eq["q3_cash_open_end"] = qc["quarter_open_cash"] + qc["net_cash_change"] - qc["quarter_end_cash"]
    eq["q3_investing_components"] = (
        sum(qc[k] for k in ("quarter_capex", "quarter_investing_sale",
                           "quarter_disposal_cost", "quarter_dividends_from_investments"))
        - qc["investing"]
    )
    eq["q3_financing_components"] = (
        sum(qc[k] for k in ("quarter_new_equity", "quarter_long_term_financing_received",
                           "quarter_long_term_financing_repaid", "quarter_dividends_paid"))
        - qc["financing"]
    )
    assert len(eq) == 17 + 6 + 16 + 5 + 4 + 6, (len(eq), eq)
    assert all(value == 0 for value in eq.values()), eq
    assert (qc["operating"], qc["investing"], qc["financing"], qc["net_cash_change"]) == (
        -19191844, -624542, 220486, -19595900
    )
    assert qc["quarter_open_cash"] == 522150455 and qc["quarter_end_cash"] == 502554555
    assert qc["quarter_new_equity"] == -1, "One-million same-basis Q3 financing offset is source-attributed, not a plug"
    vintage = a["H1_reviewed_vs_Q2_first_issued_scope_vintage"]
    older = data["items"][-2]
    assert older["period"] == "2026-Q2" and older["verification_status"] == "auto_extracted_pending_visual_review"
    assert older["total_assets"] == vintage["q2_original_provisional_assets"]
    assert older["total_liabilities"] == vintage["q2_original_provisional_liabilities"]
    assert older["equity"] == vintage["q2_original_provisional_equity"]
    assert reviewed_b01["total_assets"] - older["total_assets"] == vintage["asset_vintage_delta"]
    assert reviewed_b01["total_liabilities"] - older["total_liabilities"] == vintage["liabilities_vintage_delta"]
    assert reviewed_b01["equity"] - older["equity"] == vintage["equity_vintage_delta"]
    assert vintage["production_Q2_row_unchanged"] is True
    r = data["items"][-1]
    assert r["unit"] == "triệu VND" and "hợp nhất" in r["report_type"].lower()
    assert r["verification_status"] == "issuer_signed_BID_2026Q3_consolidated_B01_B03_B04_reviewedH1_quarter_verified"
    v = r["source_validation"]
    assert v["source_audit_ledger"] == str(LEDGER.relative_to(ROOT))
    assert v["original_pdf_sha256"] == a["q3_signed_source_pdf"]["pdf_sha256"]
    assert v["H1_source_pdf_sha256"] == a["h1_reviewed_consolidated_original"]["pdf_sha256"]
    assert v["manually_visual_reviewed"] and v["source_is_consolidated_financial_statements"]
    assert v["source_B03_Q3_16_exact_direct_income_9M_less_H1"] and v["B04_Q3_9M_minus_reviewed_H1_sections_cash_exact"]
    mapping = {
        "total_assets": b["total_assets"], "total_liabilities": b["total_liabilities"],
        "equity": b["equity"], "revenue": q["operating_income"],
        "pretax_profit": q["pretax_profit"], "net_profit": q["net_profit"],
        "net_profit_attributable": q["parent_profit"], "income_tax": q["tax_expense"],
        "bank_cash_on_hand": b["cash_vault"], "bank_customer_loans": b["customer_loans_net"],
        "bank_customer_deposits": b["customer_deposits"],
        "bank_deposits_and_borrowings_from_credit_institutions": b["interbank_liabilities"],
        "bank_funding_and_trust_liabilities": b["trust_liabilities"],
        "bank_valuable_papers": b["valuable_papers"], "bank_other_liabilities": b["other_liabilities"],
        "bank_net_interest_income": q["net_interest"], "bank_net_service_income": q["services"],
        "bank_fx_net_income": q["fx"], "bank_other_operating_net": q["other"],
        "bank_dividend_and_capital_income": q["contribution"],
        "bank_operating_expenses": q["operating_expenses"],
        "bank_pre_provision_operating_profit": q["before_provision"],
        "bank_provision_expense": q["credit_provision"],
        "bank_non_controlling_profit": q["nci_profit"],
        "operating_cash_flow_ytd": c["operating"], "investing_cash_flow_ytd": c["investing"],
        "financing_cash_flow_ytd": c["financing"], "net_cash_change_ytd": c["net_cash_change"],
        "cash_beginning_reported_ytd": c["year_open_cash"], "cash_ending_ytd": c["ending_cash"],
        "operating_cash_flow": qc["operating"], "investing_cash_flow": qc["investing"],
        "financing_cash_flow": qc["financing"], "net_cash_change": qc["net_cash_change"],
        "cash_beginning": qc["quarter_open_cash"], "cash_ending": qc["quarter_end_cash"],
        "capital_expenditure_ytd": c["investing_capex"],
        "capital_expenditure": qc["quarter_capex"]
    }
    assert len(mapping) == 38 and set(r["financial_line_items_manually_verified_fields"]) == set(mapping)
    assert set(r["financial_line_items_extracted_fields"]) == set(mapping)
    for key, amount in mapping.items():
        assert type(r[key]) is int and r[key] == amount, (key, r.get(key), amount)
    assert r["source_url"] == a["q3_signed_source_pdf"]["url"]
    assert r["cashflow_period_basis"] == "year_to_date"
    assert r["cash_beginning"] + r["net_cash_change"] == r["cash_ending"]
    assert r["cash_beginning_reported_ytd"] + r["net_cash_change_ytd"] == r["cash_ending_ytd"]
    assert r["roa"] == round(4 * 100 * q["net_profit"] / ((b["total_assets"] + reviewed_b01["total_assets"]) / 2), 2)
    assert r["roe"] == round(4 * 100 * q["net_profit"] / ((b["equity"] + reviewed_b01["equity"]) / 2), 2)
    for prefix, source in (
        ("b01", b), ("b03_q3", q), ("b03_9m", y),
        ("b03_H1", h), ("b04_9m", c), ("b04_H1", hcash), ("b04_q3", qc)
    ):
        for key, amount in source.items():
            assert r["signed_source_" + prefix + "_" + key] == amount, (prefix, key)
    assert not any(item["period"].startswith("2024") for item in data["items"])


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
    assert a["production_eligible"] is True
    assert exception["signed_visual_component_million"] == 6245
    assert exception["visual_component_sum_million"] == y["operating_income_from_printed_preprovision_plus_opex"]
    assert exception["accounting_residual_after_visual_million"] == 0
    assert exception["status"] == "resolved_by_signed_original_visual_20261123"
    return len(eq)

def main() -> None:
    src = json.loads(LEDGER.read_text("utf-8"))
    production = json.loads(PRODUCTION.read_text("utf-8"))
    checks = verify(src, production)
    for name in ("tamper_balance", "tamper_cash", "tamper_profit", "publish_unverified", "tamper_visual_sign", "tamper_H1_CFO", "tamper_quarter_CFO", "tamper_prior_vintage"):
        clone, pdata = deepcopy(src), deepcopy(production)
        if name == "tamper_balance":
            clone["b01_2026_09_30_million_vnd"]["total_assets"] += 1
        elif name == "tamper_cash":
            clone["b04_9m_ytd_million_vnd"]["operating"] += 1
        elif name == "tamper_profit":
            clone["b03_q3_direct_million_vnd"]["net_profit"] += 1
        elif name == "tamper_visual_sign":
            clone["b03_9m_ytd_million_vnd"]["investment_visual_confirmed"] = -6245
        elif name == "tamper_H1_CFO":
            clone["b04_H1_reviewed_6m_million_vnd"]["operating"] += 1
        elif name == "tamper_quarter_CFO":
            pdata["items"][-1]["operating_cash_flow"] += 1
        elif name == "tamper_prior_vintage":
            pdata["items"][-2]["total_assets"] += 1
        else:
            clone["production_eligible"] = False
        try:
            verify(clone, pdata)
        except (AssertionError, TypeError, KeyError):
            pass
        else:
            raise AssertionError("Failed to catch " + name)
    print(f"PASS BID 2026Q3 source-signed 37p Q3 and 57p reviewed H1, {checks} exact accounting identities, 16 quarter income bridges, 8 negative controls.")
    print("PASS BID issuer Q3 B04 CFO -19,191,844 CFI -624,542 CFF +220,486 net -19,595,900; issuer-verified Q1/2025 preserved, remaining 2025Q4–2026Q2 provisional records unmodified.")
if __name__ == "__main__":
    main()
