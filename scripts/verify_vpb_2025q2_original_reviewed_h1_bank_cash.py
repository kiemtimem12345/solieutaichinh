#!/usr/bin/env python3
"""Fail-closed VPB 2025Q2 original B02a/B03a and independently reviewed H1-minus-Q1 bank B04a."""
import json
from copy import deepcopy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/VPB-2025Q2-original-reviewedH1-B02a-B03a-B04a-million-vnd.json"
DATA = ROOT / "data/financials-VPB.json"
STATUS = "issuer_signed_VPB_2025Q2_original_B02a_B03a_reviewed_H1_minus_Q1_bank_B04a_verified"
Q1_STATUS = "issuer_signed_VPB_2025Q1_consolidated_B02a_B03a_B04a_cash_opening_corrected_verified"

def verify(a, f):
    assert (a["symbol"], a["period"], a["scope"], a["unit"]) == ("VPB", "2025-Q2", "consolidated", "triệu VND")
    so, sh = a["sources"]["original_Q2"], a["sources"]["reviewed_H1"]
    assert (so["sha256"], so["bytes"], so["pages"], so["B02a_pages"], so["B03a_page"], so["B04a_pages"]) == (
        "1db3edcdef5697a720a57ae009ba0134d93abd4d2a053ceacdba8c22e99917da", 7224962, 92, [5,6], 8, [9,10])
    assert (sh["sha256"], sh["bytes"], sh["pages"], sh["B04a_pages"]) == (
        "c9f27ab6b1d69611209dee51e5bd9dc91dd74f491abf4f25a01821964266eecf", 10239403, 104, [13,14])
    assert so["source_run"] == sh["source_run"] == 45244732378
    b,p,h,q1,q = (a[k] for k in ("B02a", "B03a", "B04a_reviewed_H1", "B04a_verified_Q1", "B04a_standalone_Q2"))
    def ss(x, keys): return sum(x[k] for k in keys)
    E = {}
    E["B02a_asset"] = ss(b, ("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
        "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments",
        "fixed_assets","other_assets")) - b["total_assets"]
    E["B02a_liab"] = ss(b, ("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
        "trust_liabs","valuable_papers","other_liabs")) - b["total_liabilities"]
    E["B02a_equity"] = ss(b, ("capital","funds","retained","minority")) - b["total_equity"]
    E["B02a_balanced"] = b["total_assets"]-b["total_liabilities"]-b["total_equity"]
    E["B03a_net_interest"] = p["interest_income"]+p["interest_expense"]-p["net_interest"]
    E["B03a_service"] = p["service_income"]+p["service_expense"]-p["services_net"]
    E["B03a_other"] = p["other_income"]+p["other_expense"]-p["other_net"]
    E["B03a_total_operating"] = ss(p, ("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
    E["B03a_before_provision"] = p["operating_income"]-p["operating_expenses"]-p["before_provision"]
    E["B03a_provision_PBT"] = p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
    E["B03a_income_tax"] = p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
    E["B03a_PAT"] = p["pretax_profit"]-p["income_tax"]-p["net_profit"]
    E["B03a_parent"] = p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
    E["H1_before_wc"] = ss(h, ("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
        "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-h["pre_wc_cash"]
    E["H1_true_CFO"] = h["pre_wc_cash"] + ss(h, ("assets_interbank","assets_securities",
        "assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other",
        "liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers",
        "liabs_trust","liabs_derivatives","liabs_other"))-h["CFO"]
    E["H1_CFI"] = h["capex"]+h["asset_disposals"]+h["investment_distributions"]-h["CFI"]
    E["H1_CFF"] = h["dividends"]-h["CFF"]
    E["H1_net"] = h["CFO"]+h["CFI"]+h["CFF"]+h["FX_effect"]-h["net_cash_change"]
    E["H1_cash"] = h["opening_cash"]+h["net_cash_change"]-h["closing_cash"]
    for k in ("CFO","CFI","CFF","net_cash_change","FX_effect"):
        E["Q2_bridge_"+k] = h[k]-q1[k]-q[k]
    E["Q2_cash_open"] = q1["closing_cash"]-q["opening_cash"]
    E["Q2_cash_close"] = h["closing_cash"]-q["closing_cash"]
    E["Q2_net"] = q["CFO"]+q["CFI"]+q["CFF"]+q["FX_effect"]-q["net_cash_change"]
    E["Q2_cash"] = q["opening_cash"]+q["net_cash_change"]-q["closing_cash"]
    E["Q2_capex"] = h["capex"]-(-64029)-q["capex"]
    E["Q1_previous_cash"] = q1["opening_cash"]+q1["net_cash_change"]-q1["closing_cash"]
    assert all(v == 0 for v in E.values()), E
    assert (b["total_assets"],b["total_liabilities"],b["total_equity"]) == (1104718510,952535825,152182685)
    assert (p["operating_income"],p["credit_provision"],p["pretax_profit"],p["net_profit"],p["parent_profit"]) == (16336568,5915679,6214525,4937496,4862400)
    assert (h["CFO"],h["CFI"],h["CFF"],h["net_cash_change"],h["opening_cash"],h["closing_cash"]) == (23353876,-29653,-3968172,19356051,143002784,162358835)
    assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["opening_cash"],q["closing_cash"],q["FX_effect"]) == (14803070,26194,-3968172,10861092,151497743,162358835,0)
    assert a["rules"]["original_2025Q2_income_is_direct_quarter"] and a["rules"]["year_to_date_bank_B04a_requires_6M_less_Q1"]
    assert f["symbol"] == "VPB" and [x["period"] for x in f["items"]] == [
       "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
    row = f["items"][1]
    assert f["items"][0]["verification_status"] == Q1_STATUS
    assert f["items"][0]["operating_cash_flow"] == q1["CFO"]
    assert f["items"][0]["cash_beginning"] == q1["opening_cash"]
    assert f["items"][0]["cash_ending"] == q1["closing_cash"]
    assert row["verification_status"] == STATUS and row["unit"] == "triệu VND"
    assert row["source_validation"]["original_pdf_sha256"] == so["sha256"]
    assert row["source_validation"]["reviewed_H1_pdf_sha256"] == sh["sha256"]
    assert row["source_validation"]["source_audit_ledger"] == str(LEDGER.relative_to(ROOT))
    assert row["source_validation"]["manually_visual_reviewed"] and row["source_validation"]["bank_6M_minus_Q1_cash_bridge_exact"]
    assert row["source_validation"]["original_B02_B03_and_reviewed_H1_B04_issuer_pages_checked"]
    mapped = {
      "total_assets":b["total_assets"], "total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
      "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],
      "net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
      "bank_deposits_at_state_bank":b["deposits_SBV"],
      "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
      "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabs"],
      "bank_customer_deposits":b["customer_deposits"],"bank_customer_loans":b["customer_loans_net"],
      "bank_cash_on_hand":b["cash_vault"],"bank_purchased_debt_net":b["purchased_debt_net"],
      "fixed_assets":b["fixed_assets"],"bank_other_assets":b["other_assets"],"retained_earnings":b["retained"],
      "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
      "bank_operating_expenses":p["operating_expenses"],"bank_provision_expense":p["credit_provision"],
      "bank_pre_provision_operating_profit":p["before_provision"],"bank_non_controlling_profit":p["noncontrolling_profit"],
      "income_tax":p["income_tax"],"income_tax_current":p["income_tax_current"],"income_tax_deferred":p["income_tax_deferred"],
      "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
      "net_cash_change":q["net_cash_change"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
      "cashflow_fx":q["FX_effect"],"operating_cash_flow_ytd":h["CFO"],"investing_cash_flow_ytd":h["CFI"],
      "financing_cash_flow_ytd":h["CFF"],"net_cash_change_ytd":h["net_cash_change"],
      "cash_beginning_reported_ytd":h["opening_cash"],"cash_ending_ytd":h["closing_cash"],
      "capital_expenditure":q["capex"],"capital_expenditure_ytd":h["capex"]}
    for k,v in mapped.items(): assert row[k] == v, (k,row.get(k),v)
    for prefix, raw in (("b02a",b),("b03a",p),("b04a_h1",h)):
        for k,v in raw.items():assert row["signed_source_"+prefix+"_"+k] == v,(prefix,k)
    avg_assets = (a["prior_Q1_B02a"]["assets"]+b["total_assets"])/2
    avg_equity = (a["prior_Q1_B02a"]["equity"]+b["total_equity"])/2
    assert row["roa"] == round(400*p["net_profit"]/avg_assets,2) == 1.88
    assert row["roe"] == round(400*p["net_profit"]/avg_equity,2) == 13.02
    assert [x["verification_status"] for x in f["items"][2:]] == [
     "issuer_signed_VPB_2025Q3_original_B02a_B03a_9M_minus_reviewedH1_B04a_verified","issuer_signed_VPB_2025Q4_original_B02a_B03a_EY_FY_minus_signed9M_bank_B04a_verified",
     "issuer_signed_VPB_2026Q1_original_B02a_B03a_B04a_true_CFO_verified","issuer_signed_VPB_2026Q2_original_B02a_B03a_reviewed_H1_minus_Q1_B04a_verified",
     "issuer_signed_VPB_2026Q3_original_B02a_B03a_9M_minus_reviewed_H1_B04a_verified"]
    assert all(not x["period"].startswith("2024") for x in f["items"])
    return len(E), len(mapped)

def main():
    a=json.loads(LEDGER.read_text("utf-8"))
    f=json.loads(DATA.read_text("utf-8"))
    n,m=verify(a,f)
    cases=("asset","liab","equity","revenue","provision","CFO","CFI","cash_change",
        "cash_open","fake_fx","reviewed_hash","bad_income_tax","wrong_q2_CFF",
        "ytd_used_as_Q2","Q1_corrupt","premature_Q3","add_2024")
    for key in cases:
        aa, ff=deepcopy(a),deepcopy(f)
        if key=="asset":aa["B02a"]["total_assets"]+=1
        elif key=="liab":ff["items"][1]["total_liabilities"]=652535825
        elif key=="equity":ff["items"][1]["equity"]=452182685
        elif key=="revenue":ff["items"][1]["revenue"]=46336568
        elif key=="provision":ff["items"][1]["bank_provision_expense"]=35915679
        elif key=="CFO":aa["B04a_reviewed_H1"]["CFO"]+=1
        elif key=="CFI":aa["B04a_standalone_Q2"]["CFI"]+=1
        elif key=="cash_change":aa["B04a_standalone_Q2"]["net_cash_change"]+=1
        elif key=="cash_open":ff["items"][1]["cash_beginning"]=143002784
        elif key=="fake_fx":ff["items"][1]["cashflow_fx"]=1
        elif key=="reviewed_hash":aa["sources"]["reviewed_H1"]["sha256"]="0"*64
        elif key=="bad_income_tax":ff["items"][1]["income_tax"]+=1
        elif key=="wrong_q2_CFF":ff["items"][1]["financing_cash_flow"]=0
        elif key=="ytd_used_as_Q2":ff["items"][1]["operating_cash_flow"]=23353876
        elif key=="Q1_corrupt":ff["items"][0]["cash_beginning"]=443002784
        elif key=="premature_Q3":ff["items"][2]["verification_status"]="fake_verified"
        elif key=="add_2024":ff["items"].append({"period":"2024-Q4"})
        try:verify(aa,ff)
        except (AssertionError,KeyError,TypeError,IndexError):pass
        else:raise AssertionError("VPB Q2 source tamper escaped: "+key)
    print(f"PASS VPB 2025Q2 signed original 92p and reviewed H1 104p: {n} exact identities, {m} normalized checks, {len(cases)} negative tamper cases")
    print("PASS bank true Q2 CFO +14,803,070 CFI +26,194 CFF -3,968,172 net +10,861,092 opening 151,497,743 closing 162,358,835 million VND; 2024 excluded")

if __name__=="__main__":main()
