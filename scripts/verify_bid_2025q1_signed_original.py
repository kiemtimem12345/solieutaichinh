#!/usr/bin/env python3
"""BID 2025Q1 signed consolidated original B01/B03/B04 exact million-VND QA.

Regression against provenance SHA and original issuer quarter. In particular,
B04 cash before changes in banking balance sheet is NOT actual corporate CFO.
"""
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/source-audits/BID-2025Q1-signed-original-consolidated-million-vnd.json"
DATA = ROOT / "data/financials-BID.json"

def validate(a: dict, data: dict) -> int:
    assert a["ticker"] == "BID" and a["period"] == "2025-Q1" and a["scope"] == "consolidated"
    assert a["unit"] == "triệu VND"
    src = a["original"]
    assert src["sha256"] == "52b8a37dc84ef8d83fb515a38a931692a71cf1450b99ae5aeb9134f1c4b734d3"
    assert src["pages"] == 34 and src["bytes"] == 15035938
    assert src["visual_B01_pages"] == [4, 5] and src["visual_B03_pages"] == [7]
    assert src["visual_B04_pages"] == [8, 9] and src["source_is_signed_original"] is True
    b, p, c = a["B01_2025_03_31_million_vnd"], a["B03_2025Q1_direct_million_vnd"], a["B04_2025Q1_direct_million_vnd"]
    assert all(type(x) is int for obj in (b, p, c) for x in obj.values())
    E = {}
    E["b01_balance"] = b["total_assets"] - b["total_liabilities"] - b["equity"]
    E["b01_assets"] = sum(b[k] for k in (
        "cash_vault", "deposits_SBV", "interbank_assets", "trading_securities",
        "derivative_assets", "customer_loans_net", "investment_securities",
        "long_term_investments", "fixed_assets", "other_assets")) - b["total_assets"]
    E["b01_liabilities"] = sum(b[k] for k in (
        "government_liabilities", "interbank_liabilities", "customer_deposits",
        "derivative_liabilities", "trust_liabilities", "valuable_papers",
        "other_liabilities")) - b["total_liabilities"]
    E["b01_equity"] = sum(b[k] for k in (
        "capital", "funds", "fx_equity", "retained", "noncontrolling_equity")) - b["equity"]
    E["b03_net_interest"] = p["gross_interest_income"] + p["interest_expense"] - p["net_interest"]
    E["b03_services"] = p["service_income"] + p["service_expense"] - p["service_net"]
    E["b03_other"] = p["other_income"] + p["other_expense"] - p["other_net"]
    E["b03_operating_income"] = sum(p[k] for k in (
        "net_interest", "service_net", "fx_net", "trading_net",
        "investment_net", "other_net", "capital_contribution_income")) - p["bank_total_operating_income"]
    E["b03_pre_provision"] = p["bank_total_operating_income"] - p["operating_expense"] - p["pre_provision_profit"]
    E["b03_pretax"] = p["pre_provision_profit"] - p["provision_expense"] - p["pretax_profit"]
    E["b03_pat"] = p["pretax_profit"] - p["income_tax"] - p["net_profit"]
    E["b03_parent_nci"] = p["net_profit"] - p["noncontrolling_profit"] - p["parent_attributable_profit"]
    E["b04_before_wc"] = sum(c[k] for k in (
        "interest_cash_received", "interest_cash_paid", "services_cash",
        "fx_trade_cash", "other_cash", "recovered_bad_debts_cash",
        "staff_admin_cash", "tax_paid_cash")) - c["cash_before_working_capital"]
    asset_keys = ("operating_asset_interbank", "operating_asset_securities",
                  "operating_asset_derivatives", "operating_asset_customer_loans",
                  "operating_asset_provisions", "operating_asset_other")
    liability_keys = ("operating_liability_government", "operating_liability_interbank",
                      "operating_liability_customer_deposits", "operating_liability_valuables",
                      "operating_liability_trust", "operating_liability_derivatives",
                      "operating_liability_other")
    assets = sum(c[k] for k in asset_keys)
    liabilities = sum(c[k] for k in liability_keys)
    E["b04_CFO_including_wc"] = c["cash_before_working_capital"] + assets + liabilities - c["operating_cash_flow"]
    E["b04_CFI"] = sum(c[k] for k in (
        "investing_capex", "investing_disposal_receipts",
        "investing_disposal_costs", "investing_dividends")) - c["investing_cash_flow"]
    E["b04_CFF"] = c["financing_new_equity"] + c["financing_long_term_repayments"] - c["financing_cash_flow"]
    E["b04_net_change"] = c["operating_cash_flow"] + c["investing_cash_flow"] + c["financing_cash_flow"] - c["net_cash_change"]
    E["b04_opening_closing"] = c["opening_cash"] + c["net_cash_change"] - c["ending_cash"]
    assert len(E) == 18 and all(v == 0 for v in E.values()), E
    assert assets == -59002975 and liabilities == 89000462
    assert c["cash_before_working_capital"] == 5947885 and c["operating_cash_flow"] == 35945372
    assert c["operating_cash_flow"] != c["cash_before_working_capital"]
    assert (c["investing_cash_flow"], c["financing_cash_flow"], c["net_cash_change"]) == (-506151, 3673654, 39112875)
    assert data["symbol"] == "BID" and len(data["items"]) == 7
    assert [r["period"] for r in data["items"]] == [
        "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"
    ]
    row = data["items"][0]
    assert row["verification_status"] == "issuer_signed_BID_2025Q1_consolidated_B01_B03_B04_exact_VND_verified"
    assert row["unit"] == "triệu VND" and "hợp nhất" in row["report_type"].lower()
    assert row["cashflow_period_basis"] == "year_to_date"
    sv = row["source_validation"]
    assert sv["original_pdf_sha256"] == src["sha256"] and sv["original_pdf_hash_verified"]
    assert sv["original_signed_B01_B03_B04_verified"] and sv["manually_visual_reviewed"]
    assert sv["source_audit_ledger"] == str(AUDIT.relative_to(ROOT))
    assert sv["bank_direct_B04_cash_before_wc_not_CFO"]
    assert sv["legacy_auto_rejected_cashflow_before_signed_recovery"]["operating_cash_flow"]["value"] == 5947885
    assert row["financial_line_items_rejected_fields"] == []
    assert row["financial_line_items_rejected_values"] == {}
    mapping = {
        "total_assets": b["total_assets"], "total_liabilities": b["total_liabilities"], "equity": b["equity"],
        "pretax_profit": p["pretax_profit"], "net_profit": p["net_profit"],
        "net_profit_attributable": p["parent_attributable_profit"],
        "revenue": p["bank_total_operating_income"], "income_tax": p["income_tax"],
        "bank_cash_on_hand": b["cash_vault"], "bank_deposits_at_state_bank": b["deposits_SBV"],
        "bank_deposits_and_loans_to_credit_institutions": b["interbank_assets"],
        "bank_customer_loans": b["customer_loans_net"], "bank_trading_securities": b["trading_securities"],
        "bank_investment_securities": b["investment_securities"],
        "bank_contributions_and_long_term_investments": b["long_term_investments"],
        "fixed_assets": b["fixed_assets"], "bank_other_assets": b["other_assets"],
        "bank_deposits_and_borrowings_from_credit_institutions": b["interbank_liabilities"],
        "bank_customer_deposits": b["customer_deposits"],
        "bank_valuable_papers": b["valuable_papers"],
        "bank_funding_and_trust_liabilities": b["trust_liabilities"],
        "bank_other_liabilities": b["other_liabilities"],
        "bank_net_interest_income": p["net_interest"], "bank_net_service_income": p["service_net"],
        "bank_fx_net_income": p["fx_net"], "bank_other_operating_net": p["other_net"],
        "bank_dividend_and_capital_income": p["capital_contribution_income"],
        "bank_operating_expenses": p["operating_expense"],
        "bank_pre_provision_operating_profit": p["pre_provision_profit"],
        "bank_provision_expense": p["provision_expense"],
        "bank_non_controlling_profit": p["noncontrolling_profit"],
        "operating_profit": p["pre_provision_profit"],
        "operating_cash_flow": c["operating_cash_flow"],
        "investing_cash_flow": c["investing_cash_flow"],
        "financing_cash_flow": c["financing_cash_flow"],
        "net_cash_change": c["net_cash_change"],
        "operating_cash_flow_ytd": c["operating_cash_flow"],
        "investing_cash_flow_ytd": c["investing_cash_flow"],
        "financing_cash_flow_ytd": c["financing_cash_flow"],
        "net_cash_change_ytd": c["net_cash_change"],
        "cash_beginning": c["opening_cash"], "cash_ending": c["ending_cash"],
        "cash_beginning_reported_ytd": c["opening_cash"], "cash_ending_ytd": c["ending_cash"],
        "capital_expenditure": c["investing_capex"], "capital_expenditure_ytd": c["investing_capex"],
    }
    assert len(mapping) == 46
    assert set(row["financial_line_items_manually_verified_fields"]) == set(mapping)
    for field, value in mapping.items():
        assert type(row[field]) is int and row[field] == value, (field, row.get(field), value)
    for prefix, data_source in (("b01", b), ("b03", p), ("b04", c)):
        for key, amount in data_source.items():
            assert row["signed_source_" + prefix + "_" + key] == amount, (prefix, key)
    avga = (b["total_assets"] + b["comparative_opening_31dec2024_assets_only_for_2025Q1_ratios"]) / 2
    avge = (b["equity"] + b["comparative_opening_31dec2024_equity_only_for_2025Q1_ratios"]) / 2
    assert row["roa"] == round(4 * 100 * p["net_profit"] / avga, 2)
    assert row["roe"] == round(4 * 100 * p["net_profit"] / avge, 2)
    assert row["roa"] == 0.85 and row["roe"] == 15.84
    assert data["items"][1]["verification_status"] == "issuer_signed_BID_2025Q2_first_issued_B01_B03_reviewedH1_minus_Q1_B04_verified"
    assert data["items"][2]["verification_status"] == "issuer_signed_BID_2025Q3_consolidated_B01_B03_B04_reviewedH1_quarter_exact_verified"
    assert data["items"][3]["verification_status"] == "issuer_signed_BID_2025Q4_first_issued_B01_B03_FY_audited_minus_signed9M_B04_verified"
    assert data["items"][4]["verification_status"] == "issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
    assert all(x["verification_status"] == "auto_extracted_pending_visual_review" for x in data["items"][5:-1])
    assert data["items"][-1]["verification_status"] == "issuer_signed_BID_2026Q3_consolidated_B01_B03_B04_reviewedH1_quarter_verified"
    assert all(not x["period"].startswith("2024") for x in data["items"])
    return len(E)

def main() -> None:
    a = json.loads(AUDIT.read_text("utf-8"))
    d = json.loads(DATA.read_text("utf-8"))
    count = validate(a, d)
    for name in ("CFO_before_wc", "B01_assets", "B03_profit", "net_cash", "PDF_hash", "old_period", "ratio"):
        aa, dd = deepcopy(a), deepcopy(d)
        if name == "CFO_before_wc":
            dd["items"][0]["operating_cash_flow"] = 5947885
        elif name == "B01_assets":
            aa["B01_2025_03_31_million_vnd"]["total_assets"] += 1
        elif name == "B03_profit":
            aa["B03_2025Q1_direct_million_vnd"]["net_profit"] += 1
        elif name == "net_cash":
            dd["items"][0]["net_cash_change"] += 1
        elif name == "PDF_hash":
            aa["original"]["sha256"] = "0" * 64
        elif name == "old_period":
            dd["items"][1]["verification_status"] = "completed_without_source"
        else:
            dd["items"][0]["roe"] = 15.53
        try:
            validate(aa, dd)
        except (AssertionError, KeyError, TypeError):
            pass
        else:
            raise AssertionError("Negative tampering was not caught: " + name)
    print(f"PASS BID Q1 2025 signed original 34p B01 B03 B04; {count} exact accounting identities, 46 normalized fields and 7 negative tamper tests.")
    print("PASS actual Q1 B04 CFO 35,945,372; pre-WC 5,947,885 not CFO. Q1 row restored, BID other periods preserved.")

if __name__ == "__main__":
    main()
