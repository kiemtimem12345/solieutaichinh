#!/usr/bin/env python3
"""VPB 2025Q4 original signed 93p B02a/B03a/B04a vs EY audited FY100p, exact bank cash.
Reject unadjusted OCR/pre-WC CFO, false Q4 YTD, forged FX, bad source vintage and Q1-Q3 regressions.
"""
import json
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/VPB-2025Q4-original-vs-EY-audited-FY-million-vnd.json"
DATA=ROOT/"data/financials-VPB.json"
PRIOR=[
 ROOT/"reports/source-audits/VPB-2025Q1-original-signed-B02a-B03a-B04a-million-vnd.json",
 ROOT/"reports/source-audits/VPB-2025Q2-original-reviewedH1-B02a-B03a-B04a-million-vnd.json",
 ROOT/"reports/source-audits/VPB-2025Q3-original-9M-reviewedH1-bank-B02a-B03a-B04a-million-vnd.json"]
STATUS="issuer_signed_VPB_2025Q4_original_B02a_B03a_EY_FY_minus_signed9M_bank_B04a_verified"
PREFIXES=("issuer_signed_VPB_2025Q1_","issuer_signed_VPB_2025Q2_","issuer_signed_VPB_2025Q3_")
def verify(a,f,priors):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("VPB","2025-Q4","consolidated","triệu VND")
 assert a["stage"]=="issuer_original_Q4_2025_B02a_B03a_B04a_12M_and_independent_EY_FY_audited_100p_exact_verified"
 src=a["sources"];i=src["Q4_first_issued"];ey=src["EY_FY2025_audited"]
 assert (i["archive_sha256"],i["archive_bytes"],i["original_pdf_sha256"],i["original_pdf_bytes"],i["original_pdf_pages"],i["lookup_sha256"])==(
 "e0f7fa6cedc219c5d0e81c2a98c7925b98fb2bffbac44b25d11bae1a4620f03a",22443790,
 "3e9ca79f8e9d7a964de1780498cd760cd863fd557415cd94aa2e28f8ffbbfe9e",23555073,93,
 "ed2ace4b0d029c9de69a61379a4d06850b65a99d4624c9b86dba71534243b254")
 assert (ey["sha256"],ey["bytes"],ey["pages"],ey["B02_pages"],ey["B03_page"],ey["B04_pages"])==(
 "f3298c72cbe58af1eefd8223d235843138761a45648cd7e60c5153ad21776ea0",7578043,100,
 [9,10],12,[13,14])
 assert src["source_comparison_run"]==45249914634
 assert a["FY_original_vs_EY_audited_identical"] and a["issuer_original_B04_12M_versus_EY_B04_12M_equal"]
 assert a["Q4_source_validation_completed_at"]=="2026-11-24"
 b,p,c,q=a["Q4_original_B02a"],a["Q4_original_direct_B03a"],a["EY_FY_B04a"],a["Q4_derived_from_EY_FY_minus_Q3_9M"]
 ann=a["EY_FY_B03a"];prior=a["Q3_original_9M_B04a"]
 assert b==a["EY_FY_B02a"] and ann==a["Q4_original_12M_B03a"]
 assert c==a["Q4_original_12M_B04a"]
 assert priors[2]["B04a_original_9M"]==prior
 def ss(d,ks):return sum(d[k] for k in ks)
 E={}
 E["B02_assets"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
   "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liabilities"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
    "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["B02_equity"]=ss(b,("capital","funds","retained","minority"))-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["B03_operating"]=ss(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["B03_preprovision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["B03_credit_provision"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["FY_B03_operating"]=ss(ann,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-ann["operating_income"]
 E["FY_B03_profit"]=ann["operating_income"]-ann["operating_expenses"]-ann["credit_provision"]-ann["pretax_profit"]
 E["FY_B03_PAT"]=ann["pretax_profit"]-ann["income_tax"]-ann["net_profit"]
 E["FY_B04_pre_wc"]=ss(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash",
    "recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["FY_B04_true_CFO"]=c["pre_wc_cash"]+ss(c,("assets_interbank","assets_securities","assets_derivatives",
    "assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank",
    "liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives",
    "liabs_other"))-c["CFO"]
 E["FY_B04_CFI"]=ss(c,("capex","asset_disposals","disposal_costs","investment_distributions"))-c["CFI"]
 E["FY_B04_CFF"]=c["share_proceeds"]+c["dividends"]-c["CFF"]
 E["FY_B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]+c["FX_effect"]-c["net_cash_change"]
 E["FY_B04_cash"]=c["opening_cash"]+c["net_cash_change"]-c["closing_cash"]
 E["Q3_to_FY_open"]=prior["opening_cash"]-c["opening_cash"]
 for key in ("CFO","CFI","CFF","net_cash_change","FX_effect"):
  E["Q4_FY_minus_9M_"+key]=c[key]-prior[key]-q[key]
 E["Q4_begin"]=prior["closing_cash"]-q["opening_cash"]
 E["Q4_end"]=c["closing_cash"]-q["closing_cash"]
 E["Q4_cash_flow_net"]=q["CFO"]+q["CFI"]+q["CFF"]+q["FX_effect"]-q["net_cash_change"]
 E["Q4_cash_bridge"]=q["opening_cash"]+q["net_cash_change"]-q["closing_cash"]
 E["Q4_capex"]=c["capex"]-prior["capex"]-q["capex"]
 E["Q4_equity_issue"]=c["share_proceeds"]-q["capital_inflow"]
 assert len(E)>=30 and not any(E.values()), E
 assert a["source_identity_residuals"]==dict.fromkeys(a["source_identity_residuals"],0)
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(1260149596,1079873967,180275629)
 assert (p["operating_income"],p["before_provision"],p["credit_provision"],p["pretax_profit"],p["net_profit"],p["parent_profit"])==(22415542,16491301,6262056,10229245,8118409,7957142)
 assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["opening_cash"],c["closing_cash"])==(52478949,44532621,-88786,8650600,53094435,143002784,196097219)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["opening_cash"],q["closing_cash"])==(17134993,-56998,12618772,29696767,166400452,196097219)
 assert q["CFO"]!=c["pre_wc_cash"] and q["CFO"]!=c["CFO"]
 V=a["B03_source_vintage_differences_EY_FY_minus_sum_first_issued_Q1_Q2_Q3_Q4"]
 for key,val in V.items():
  E["vintage_"+key]=ann[key]-sum(pn["B03a"][key] for pn in priors)-p[key]-val
 assert not any(E.values()),E
 assert V["net_interest"]==26774 and V["services_net"]==-26774
 assert V["other_net"]==V["operating_income"]==V["operating_expenses"]==198063
 assert V["before_provision"]==V["pretax_profit"]==V["net_profit"]==V["parent_profit"]==0
 assert len(f["items"])==7 and [x["period"] for x in f["items"]]==[
   "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(f["items"][k]["verification_status"].startswith(PREFIXES[k]) for k in range(3))
 assert [x["verification_status"] for x in f["items"]][3:]==[
  STATUS,"manual_review_required_pending_extraction","manual_review_required_pending_extraction",
  "auto_extracted_pending_visual_review"]
 assert f["items"][2]["cash_ending"]==q["opening_cash"]
 r=f["items"][3];sv=r["source_validation"]
 assert r["unit"]=="triệu VND" and r["verification_status"]==STATUS
 assert sv["original_zip_sha256"]==i["archive_sha256"] and sv["original_zip_hash_verified"]
 assert sv["original_pdf_sha256"]==i["original_pdf_sha256"]
 assert sv["audited_EY_FY_pdf_sha256"]==ey["sha256"]
 assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["source_issuer_Q4_12M_equals_audited_EY_FY"] and sv["bank_audited_12M_minus_Q3_signed_9M_cash_exact"]
 assert sv["FY_sum_quarters_vintage_differences"]==V and sv["no_2024_dashboard_periods"]
 mapped={
   "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
   "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
   "net_profit_attributable":p["parent_profit"],
   "bank_cash_on_hand":b["cash_vault"],"bank_customer_loans":b["customer_loans_net"],
   "bank_customer_deposits":b["customer_deposits"],"bank_deposits_at_state_bank":b["deposits_SBV"],
   "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
   "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabs"],
   "bank_purchased_debt_net":b["purchased_debt_net"],"retained_earnings":b["retained"],
   "bank_interest_income":p["interest_income"],"bank_net_interest_income":p["net_interest"],
   "bank_net_service_income":p["services_net"],"bank_trading_securities_net":p["trading_net"],
   "bank_operating_expenses":p["operating_expenses"],"bank_provision_expense":p["credit_provision"],
   "bank_non_controlling_profit":p["noncontrolling_profit"],"income_tax":p["income_tax"],
   "income_tax_current":p["income_tax_current"],"income_tax_deferred":p["income_tax_deferred"],
   "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
   "net_cash_change":q["net_cash_change"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
   "cashflow_fx":q["FX_effect"],"operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
   "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
   "cash_beginning_reported_ytd":c["opening_cash"],"cash_ending_ytd":c["closing_cash"],
   "capital_expenditure":q["capex"],"capital_expenditure_ytd":c["capex"]
 }
 for k,v in mapped.items():assert r[k]==v,(k,r.get(k),v)
 for prefix,raw in (("b02a",b),("b03a",p),("b04a_fy",c)):
  for k,v in raw.items(): assert r["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert r["roa"]==round(400*p["net_profit"]/((f["items"][2]["total_assets"]+b["total_assets"])/2),2)==2.66
 assert r["roe"]==round(400*p["net_profit"]/((f["items"][2]["equity"]+b["total_equity"])/2),2)==19.11
 assert r["eps"] is None and r["eps_ytd"]==3024
 assert not any(x["period"].startswith("2024") for x in f["items"])
 return len(E),len(mapped)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 f=json.loads(DATA.read_text("utf-8"))
 priors=[json.loads(p.read_text("utf-8")) for p in PRIOR]
 n,m=verify(a,f,priors)
 cases=("asset","liab","equity","FY_income","quarter_income","Q4_PBT","Q4_tax",
  "CFO_as_preWC","FY_CFO","quarter_CFO","CFI","CFF","net_cash",
  "opening_cash","closing_cash","FX_forged","FY_SHA","Q4_original_SHA",
  "vintage_income_198063","vintage_expenses_198063","vintage_interest",
  "preprov_source","Q3_source_altered","Q1_status","Q2_status","Q3_status",
  "2026_premature","2024_period","annual_EPS_wrongly_Q4")
 for kind in cases:
  aa,ff,pr=deepcopy(a),deepcopy(f),deepcopy(priors)
  if kind=="asset":aa["Q4_original_B02a"]["total_assets"]+=1
  elif kind=="liab":ff["items"][3]["total_liabilities"]+=1
  elif kind=="equity":ff["items"][3]["equity"]+=1
  elif kind=="FY_income":aa["EY_FY_B03a"]["operating_income"]+=1
  elif kind=="quarter_income":ff["items"][3]["revenue"]+=1
  elif kind=="Q4_PBT":aa["Q4_original_direct_B03a"]["pretax_profit"]+=1
  elif kind=="Q4_tax":aa["Q4_original_direct_B03a"]["income_tax_current"]+=1
  elif kind=="CFO_as_preWC":ff["items"][3]["operating_cash_flow"]=52478949
  elif kind=="FY_CFO":aa["EY_FY_B04a"]["CFO"]+=1
  elif kind=="quarter_CFO":aa["Q4_derived_from_EY_FY_minus_Q3_9M"]["CFO"]+=1
  elif kind=="CFI":ff["items"][3]["investing_cash_flow"]+=1
  elif kind=="CFF":ff["items"][3]["financing_cash_flow"]=8650600
  elif kind=="net_cash":aa["Q4_derived_from_EY_FY_minus_Q3_9M"]["net_cash_change"]+=1
  elif kind=="opening_cash":ff["items"][3]["cash_beginning"]=143002784
  elif kind=="closing_cash":ff["items"][3]["cash_ending"]+=1
  elif kind=="FX_forged":ff["items"][3]["cashflow_fx"]=42
  elif kind=="FY_SHA":aa["sources"]["EY_FY2025_audited"]["sha256"]="0"*64
  elif kind=="Q4_original_SHA":aa["sources"]["Q4_first_issued"]["original_pdf_sha256"]="0"*64
  elif kind=="vintage_income_198063":aa["B03_source_vintage_differences_EY_FY_minus_sum_first_issued_Q1_Q2_Q3_Q4"]["operating_income"]=0
  elif kind=="vintage_expenses_198063":aa["B03_source_vintage_differences_EY_FY_minus_sum_first_issued_Q1_Q2_Q3_Q4"]["operating_expenses"]=0
  elif kind=="vintage_interest":aa["B03_source_vintage_differences_EY_FY_minus_sum_first_issued_Q1_Q2_Q3_Q4"]["net_interest"]=0
  elif kind=="preprov_source":aa["EY_FY_B03a"]["before_provision"]+=1
  elif kind=="Q3_source_altered":pr[2]["B04a_original_9M"]["CFO"]+=1
  elif kind=="Q1_status":ff["items"][0]["verification_status"]="tampered"
  elif kind=="Q2_status":ff["items"][1]["verification_status"]="tampered"
  elif kind=="Q3_status":ff["items"][2]["cash_ending"]+=1
  elif kind=="2026_premature":ff["items"][4]["verification_status"]="tampered"
  elif kind=="2024_period":ff["items"].append({"period":"2024-Q4"})
  elif kind=="annual_EPS_wrongly_Q4":ff["items"][3]["eps"]=3024
  try:verify(aa,ff,pr)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("Q4 signed source data tamper escaped: "+kind)
 print(f"PASS VPB Q4 original signed 93p vs EY audited FY 100p: {n} zero identities, {m} normalized mappings, {len(cases)} negative source/OCR/tamper gates")
 print("PASS FY verified CFO +44,532,621 and FY CFF +8,650,600; Q4 FY-minus-signed9M CFO +17,134,993 CFI -56,998 CFF +12,618,772 net +29,696,767 cash 166,400,452 -> 196,097,219 million VND")
 print("PASS B03 source vintage offset FY vs sum first-issued quarters +198,063 income and +198,063 expenses, pre-provision/PBT/PAT zero; Q1..Q3 locked and Q1..Q3 2026 provisional")

if __name__=="__main__":main()
