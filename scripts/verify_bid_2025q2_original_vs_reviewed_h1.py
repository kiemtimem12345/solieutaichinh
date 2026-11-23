#!/usr/bin/env python3
"""Verify BID Q2/2025 original standalone B03 and Deloitte-reviewed H1 B04.

Never mix original Q2 standalone income with reviewed half-year income to force
a false zero. Differences are registered as separate source versions.
"""
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/BID-2025Q2-first-issued-vs-reviewed-H1-million-vnd.json"
FIN = ROOT / "data/financials-BID.json"

def verify(a: dict, data: dict) -> int:
    assert a["ticker"] == "BID" and a["period"] == "2025-Q2"
    assert a["unit"] == "triệu VND" and a["scope"] == "consolidated"
    assert a["original_q2"]["sha256"] == "fd0e5d101d533272c7b2b7de432fa73586f9d78886ec7d122821d4420b7fa35f"
    assert a["reviewed_h1"]["sha256"] == "d55bbf4993c254d4a5275af7f75b8e717f7f397b04141a499a671833236d0f41"
    assert a["original_q2"]["pages"] == 33 and a["reviewed_h1"]["pages"] == 56
    assert a["original_q2"]["B01_pages"] == [3, 4] and a["reviewed_h1"]["B04_pages"] == [13, 14]
    b = a["B01_Q2_first_issued"]
    q = a["B03_Q2_first_issued_direct"]
    o = a["B04_Q2_original_6m"]
    rb = a["B01_H1_reviewed_30jun2025"]
    rq = a["B03_H1_reviewed_6m"]
    rc = a["B04_H1_reviewed_6m"]
    signed_q1 = a["B04_Q1_signed_original"]
    qc = a["B04_Q2_standalone_reviewedH1_minus_Q1"]
    vintage = a["original_vs_reviewed_vintage_delta"]
    checks = {}
    checks["B01_balance"] = b["total_assets"] - b["total_liabilities"] - b["equity"]
    checks["B01_assets"] = sum(b[k] for k in (
        "cash_vault", "deposits_SBV", "interbank_assets", "trading_securities", "derivative_assets",
        "customer_loans_net", "investment_securities", "long_investments", "fixed_assets", "other_assets")) - b["total_assets"]
    checks["B01_liabilities"] = sum(b[k] for k in (
        "government_liabilities", "interbank_liabilities", "customer_deposits", "derivative_liabilities",
        "trust_liabilities", "valuable_papers", "other_liabilities")) - b["total_liabilities"]
    checks["B01_equity"] = sum(b[k] for k in (
        "owner_capital", "owner_funds", "FX_equity", "retained", "noncontrolling_equity")) - b["equity"]
    checks["Q2_net_interest"] = q["interest_income"] + q["interest_expense"] - q["net_interest"]
    checks["Q2_net_service"] = q["services_income"] + q["services_expense"] - q["services_net"]
    checks["Q2_other_net"] = q["other_income"] + q["other_expense"] - q["other_net"]
    checks["Q2_operating_income"] = sum(q[k] for k in (
        "net_interest", "services_net", "FX_net", "trading_net",
        "invest_net", "other_net", "contribution_income")) - q["operating_income"]
    checks["Q2_before_provision"] = q["operating_income"] - q["operating_expenses"] - q["before_provision"]
    checks["Q2_pretax"] = q["before_provision"] - q["credit_provision"] - q["pretax_profit"]
    checks["Q2_tax_net"] = q["income_tax_current"] + q["income_tax_deferred"] - q["income_tax"]
    checks["Q2_after_tax"] = q["pretax_profit"] - q["income_tax"] - q["net_profit"]
    checks["Q2_parent"] = q["net_profit"] - q["noncontrolling_profit"] - q["parent_profit"]
    checks["reviewed_B01_balance"] = rb["total_assets"] - rb["total_liabilities"] - rb["equity"]
    checks["reviewed_B03_income"] = sum(rq[k] for k in (
        "net_interest", "services_net", "FX_net", "trading_net",
        "invest_net", "other_net", "contribution_income")) - rq["operating_income"]
    checks["reviewed_B03_before"] = rq["operating_income"] - rq["operating_expenses"] - rq["before_provision"]
    checks["reviewed_B03_pretax"] = rq["before_provision"] - rq["credit_provision"] - rq["pretax_profit"]
    checks["reviewed_B03_pat"] = rq["pretax_profit"] - rq["income_tax"] - rq["net_profit"]
    checks["reviewed_B03_parent"] = rq["net_profit"] - rq["noncontrolling_profit"] - rq["parent_profit"]
    checks["orig_B04_net"] = o["cfo"] + o["cfi"] + o["cff"] - o["net_cash_change"]
    checks["orig_B04_cash"] = o["year_open_cash"] + o["net_cash_change"] - o["closing_cash"]
    checks["orig_B04_financing"] = o["new_equity_cash"] + o["long_term_finance_issuance"] + o["long_term_finance_repayments"] - o["cff"]
    checks["reviewed_B04_net"] = rc["cfo"] + rc["cfi"] + rc["cff"] - rc["net_cash_change"]
    checks["reviewed_B04_cash"] = rc["year_open_cash"] + rc["net_cash_change"] - rc["closing_cash"]
    checks["reviewed_B04_investing"] = rc["capex"] + rc["disposal_proceeds"] + rc["disposal_costs"] + rc["investment_dividends"] - rc["cfi"]
    checks["reviewed_B04_financing"] = rc["new_equity_cash"] + rc["long_term_finance_issuance"] + rc["long_term_finance_repayments"] - rc["cff"]
    for name in ("cfo", "cfi", "cff", "net_cash_change"):
        checks["Q2_cash_6M_less_Q1_" + name] = rc[name] - signed_q1[name] - qc[name]
    checks["Q2_open"] = qc["opening_cash"] - signed_q1["closing_cash"]
    checks["Q2_close"] = qc["closing_cash"] - rc["closing_cash"]
    checks["Q2_cash_sections"] = qc["cfo"] + qc["cfi"] + qc["cff"] - qc["net_cash_change"]
    checks["Q2_cash_openclose"] = qc["opening_cash"] + qc["net_cash_change"] - qc["closing_cash"]
    checks["vintage_asset"] = rb["total_assets"] - b["total_assets"] - vintage["assets"]
    checks["vintage_liability"] = rb["total_liabilities"] - b["total_liabilities"] - vintage["liabilities"]
    checks["vintage_equity"] = rb["equity"] - b["equity"] - vintage["equity"]
    checks["vintage_cfo"] = rc["cfo"] - o["cfo"] - vintage["H1_cfo"]
    checks["vintage_cfi"] = rc["cfi"] - o["cfi"] - vintage["H1_cfi"]
    checks["vintage_cff"] = rc["cff"] - o["cff"] - vintage["H1_cff"]
    checks["vintage_net"] = rc["net_cash_change"] - o["net_cash_change"] - vintage["H1_net_cash"]
    checks["vintage_pretax"] = rq["pretax_profit"] - (q["pretax_profit"] + data["items"][0]["pretax_profit"]) - vintage["H1_pretax"]
    checks["vintage_PAT"] = rq["net_profit"] - (q["net_profit"] + data["items"][0]["net_profit"]) - vintage["H1_net_profit"]
    assert len(checks) == 43, len(checks)
    assert all(v == 0 for v in checks.values()), checks
    # Preserve printed one-million-VND first-issue investing source subtotal discrepancy,
    # rather than fabricate a component to force the same-vintage reported subtotal.
    first_issue_investing_residual = (
        o["capex"] + o["disposal_proceeds"] + o["disposal_costs"] + o["investment_dividends"] - o["cfi"]
    )
    assert first_issue_investing_residual == a["source_original_q2_cf_investing_component_residual_million_vnd"] == 1
    assert o["cfo"] == 90471834 and rc["cfo"] == 90469802 and rc["cash_before_working_capital"] == 21710391
    assert qc == {"cfo":54524430, "cfi":-361366, "cff":9523000, "net_cash_change":63686064, "opening_cash":363837339, "closing_cash":427523403}
    assert len(data["items"]) == 7 and data["symbol"] == "BID"
    periods = ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
    assert [row["period"] for row in data["items"]] == periods
    row = data["items"][1]
    assert row["verification_status"] == "issuer_signed_BID_2025Q2_first_issued_B01_B03_reviewedH1_minus_Q1_B04_verified"
    assert row["unit"] == "triệu VND" and "hợp nhất" in row["report_type"].lower()
    sv = row["source_validation"]
    assert sv["manually_visual_reviewed"] and sv["original_pdf_hash_verified"] and sv["source_is_consolidated_financial_statements"]
    assert sv["source_audit_ledger"] == str(LEDGER.relative_to(ROOT))
    assert sv["original_pdf_sha256"] == a["original_q2"]["sha256"]
    assert sv["H1_source_pdf_sha256"] == a["reviewed_h1"]["sha256"]
    assert sv["original_vs_reviewed_vintage_delta"] == vintage
    assert sv["bank_direct_B04_cash_before_wc_not_CFO"]
    assert row["financial_line_items_rejected_fields"] == [] and row["financial_line_items_rejected_values"] == {}
    assert row["total_assets"] == b["total_assets"] and row["total_liabilities"] == b["total_liabilities"]
    assert row["equity"] == b["equity"] and row["pretax_profit"] == q["pretax_profit"]
    assert row["net_profit"] == q["net_profit"] and row["net_profit_attributable"] == q["parent_profit"]
    assert row["revenue"] == q["operating_income"]
    assert row["operating_cash_flow"] == qc["cfo"] and row["investing_cash_flow"] == qc["cfi"]
    assert row["financing_cash_flow"] == qc["cff"] and row["net_cash_change"] == qc["net_cash_change"]
    assert row["operating_cash_flow_ytd"] == rc["cfo"] and row["investing_cash_flow_ytd"] == rc["cfi"]
    assert row["financing_cash_flow_ytd"] == rc["cff"] and row["net_cash_change_ytd"] == rc["net_cash_change"]
    assert row["cash_beginning"] == qc["opening_cash"] and row["cash_ending"] == qc["closing_cash"]
    assert row["roa"] == round(4*100*q["net_profit"]/((b["total_assets"]+data["items"][0]["total_assets"])/2),2)
    assert row["roe"] == round(4*100*q["net_profit"]/((b["equity"]+data["items"][0]["equity"])/2),2)
    assert row["roa"] == 0.94 and row["roe"] == 17.33
    for prefix, rec in (
        ("b01_Q2",b),("b03_Q2",q),("b04_Q2",qc),
        ("b01_H1_reviewed",rb),("b03_H1_reviewed",rq),
        ("b04_H1_reviewed",rc),("b04_Q2_original_6m",o)):
        for k,v in rec.items():
            assert row["signed_source_"+prefix+"_"+k] == v, (prefix,k)
    assert data["items"][0]["verification_status"] == "issuer_signed_BID_2025Q1_consolidated_B01_B03_B04_exact_VND_verified"
    assert data["items"][2]["verification_status"] == "issuer_signed_BID_2025Q3_consolidated_B01_B03_B04_reviewedH1_quarter_exact_verified"
    assert data["items"][3]["verification_status"] == "issuer_signed_BID_2025Q4_first_issued_B01_B03_FY_audited_minus_signed9M_B04_verified"
    assert data["items"][4]["verification_status"] == "issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
    assert all(z["verification_status"]=="auto_extracted_pending_visual_review" for z in data["items"][5:-1])
    assert data["items"][-1]["verification_status"]=="issuer_signed_BID_2026Q3_consolidated_B01_B03_B04_reviewedH1_quarter_verified"
    assert all(not z["period"].startswith("2024") for z in data["items"])
    return len(checks)

def main():
    a=json.loads(LEDGER.read_text("utf-8"))
    d=json.loads(FIN.read_text("utf-8"))
    count=verify(a,d)
    for label in ("source_asset","source_profit","reviewed_cash","q2_cash","vintage","hash","previous"):
        aa,dd=deepcopy(a),deepcopy(d)
        if label=="source_asset":aa["B01_Q2_first_issued"]["total_assets"]+=1
        elif label=="source_profit":aa["B03_Q2_first_issued_direct"]["net_profit"]+=1
        elif label=="reviewed_cash":aa["B04_H1_reviewed_6m"]["cfo"]+=1
        elif label=="q2_cash":dd["items"][1]["operating_cash_flow"]+=1
        elif label=="vintage":aa["original_vs_reviewed_vintage_delta"]["H1_cfo"]+=1
        elif label=="hash":aa["original_q2"]["sha256"]="0"*64
        elif label=="previous":dd["items"][0]["verification_status"]="unverified"
        try:verify(aa,dd)
        except (AssertionError,KeyError,TypeError): pass
        else:raise AssertionError("Corruption not detected: "+label)
    print(f"PASS BID Q2/2025 original 33p + reviewed 56p: {count} accounting/quarter/vintage checks, 7 corruption controls.")
    print("PASS Q2 standalone reviewed-H1 less signed-Q1 CFO 54,524,430 CFI -361,366 CFF +9,523,000, cash 363,837,339 -> 427,523,403 million VND.")

if __name__=="__main__":main()
