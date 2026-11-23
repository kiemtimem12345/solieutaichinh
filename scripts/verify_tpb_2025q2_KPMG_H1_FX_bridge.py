#!/usr/bin/env python3
"""TPB Q2/2025 signed source + independently KPMG-reviewed H1 bank exact QA.

Q1 B04a contains explicit +210436 FX effect, while 6M B04a has no FX line;
the mathematically implied Q2 FX difference -210436 is NOT an independently
published Q2 FX expense. Preserve issuer source values and source-period
presentation provenance rather than silently plug operating cash flow.
"""
from copy import deepcopy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2025Q2-signed-original-KPMG-H1-reviewed-FX-quarter-million-vnd.json"
Q1LEDGER=ROOT/"reports/source-audits/TPB-2025Q1-signed-original-B02a-B03a-B04a-FX-million-vnd.json"
FIN=ROOT/"data/financials-TPB.json"

def verify(a,q1,fin):
 assert a["symbol"]=="TPB" and a["period"]=="2025-Q2" and a["scope"]=="consolidated" and a["unit"]=="triệu VND"
 src,rev,p=a["original_Q2"],a["reviewed_H1"],a["signed_Q1"]
 assert src["sha256"]=="b30bb9d09e613f2791062ce80910037bd9c249d1b3072ec45461f657fa4fd938"
 assert rev["sha256"]=="742dbc45b1f5f7612100fd6e078977e206f700693a1f132e3373b81386934b8c"
 assert src["pages"]==52 and src["bytes"]==10416581
 assert rev["pages"]==97 and rev["bytes"]==8825841
 assert src["pdf_B02a_pages"]==[5,6] and src["pdf_B03a_page"]==8 and src["pdf_B04a_pages"]==[9,10]
 assert rev["pdf_B02a_pages"]==[10,11] and rev["pdf_B03a_pages"]==[13,14] and rev["pdf_B04a_pages"]==[15,16]
 assert rev["reviewer"]=="KPMG"
 assert p["pdf_sha256"]==q1["original"]["sha256"]
 assert p["B03a_Q1"]==q1["B03a_Q1"] and p["B04a_Q1"]==q1["B04a_Q1"]
 b,x,y,cf=a["B02a_Q2_first"],a["B03a_Q2_first"],a["B03a_6m_H1_reviewed"],a["B04a_6m_H1_reviewed"]
 cf_first=a["B04a_6m_first"]
 delta=a["Q2_cash_6m_reviewed_minus_Q1_signed"]
 q1cf=p["B04a_Q1"]
 tests={}
 tests["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 tests["B02_assets"]=sum(b[k] for k in ("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","fixed_assets","other_assets"))-b["total_assets"]
 tests["B02_liabs"]=sum(b[k] for k in ("government_liabilities","interbank_liabilities","customer_deposits","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 tests["B02_equity"]=sum(b[k] for k in ("bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 tests["B02_reviewed_assets"]=a["B02a_H1_reviewed"]["total_assets"]-b["total_assets"]
 tests["B02_reviewed_liabs"]=a["B02a_H1_reviewed"]["total_liabilities"]-b["total_liabilities"]
 tests["B02_reviewed_equity"]=a["B02a_H1_reviewed"]["total_equity"]-b["total_equity"]
 tests["B03_Q2_interest"]=x["interest_income"]+x["interest_expense"]-x["net_interest"]
 tests["B03_Q2_service"]=x["service_income"]+x["service_expense"]-x["services_net"]
 tests["B03_Q2_other"]=x["other_income"]+x["other_expense"]-x["other_net"]
 earning=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 tests["B03_Q2_income"]=sum(x[k] for k in earning)-x["operating_income"]
 tests["B03_H1_income"]=sum(y[k] for k in earning)-y["operating_income"]
 tests["B03_Q2_preprov"]=x["operating_income"]-x["operating_expenses"]-x["before_provision"]
 tests["B03_H1_preprov"]=y["operating_income"]-y["operating_expenses"]-y["before_provision"]
 tests["B03_Q2_provision"]=x["before_provision"]-x["credit_provision"]-x["pretax_profit"]
 tests["B03_H1_provision"]=y["before_provision"]-y["credit_provision"]-y["pretax_profit"]
 tests["B03_Q2_aftertax"]=x["pretax_profit"]-x["income_tax"]-x["net_profit"]
 tests["B03_H1_aftertax"]=y["pretax_profit"]-y["income_tax"]-y["net_profit"]
 tests["B03_Q2_parent"]=x["net_profit"]-x["noncontrolling_profit"]-x["parent_profit"]
 tests["B03_H1_parent"]=y["net_profit"]-y["noncontrolling_profit"]-y["parent_profit"]
 b03_keys=(*earning,"operating_income","operating_expenses","before_provision",
           "credit_provision","pretax_profit","income_tax","net_profit","noncontrolling_profit","parent_profit")
 for key in b03_keys:
  tests["B03_H1_minus_Q1_"+key]=y[key]-p["B03a_Q1"][key]-x[key]
 assert a["B03a_6m_first"]==a["B03a_6m_H1_reviewed"]
 assert cf_first==cf
 pre_cash=("interest_cash_received","interest_cash_paid","services_cash",
 "fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid")
 assets=("asset_interbank","asset_securities","asset_derivatives","asset_customer_loans",
         "asset_credit_provisions","asset_other")
 liabilities=("liability_government","liability_interbank","liability_customer_deposits",
              "liability_papers","liability_trust","liability_derivatives","liability_other")
 tests["B04_H1_preWC"]=sum(cf[k] for k in pre_cash)-cf["pre_working_capital_cash"]
 tests["B04_H1_actual_CFO"]=cf["pre_working_capital_cash"]+sum(cf[k] for k in assets)+sum(cf[k] for k in liabilities)-cf["CFO"]
 tests["B04_H1_CFI"]=sum(cf[k] for k in ("capex","disposal_proceeds","dividends_investing"))-cf["CFI"]
 tests["B04_H1_CFF"]=sum(cf[k] for k in ("financing_new_debt","financing_debt_repayment","financing_dividends_paid"))-cf["CFF"]
 tests["B04_H1_net"]=cf["CFO"]+cf["CFI"]+cf["CFF"]-cf["net_cash_change"]
 tests["B04_H1_cash"]=cf["opening_cash"]+cf["net_cash_change"]+cf["FX_effect_reported_6m"]-cf["closing_cash"]
 for name,key in (("CFO","operating_cash_flow"),("CFI","investing_cash_flow"),
                  ("CFF","financing_cash_flow"),("net_cash_change","net_cash_change")):
  tests["Q2_6M_minus_Q1_"+name]=cf[name]-q1cf[key]-delta[name]
 tests["Q2_open"]=delta["opening_cash"]-q1cf["ending_cash"]
 tests["Q2_end"]=delta["closing_cash"]-cf["closing_cash"]
 tests["Q2_FX_YTD"]=delta["FX_YTD_6m_reported"]-cf["FX_effect_reported_6m"]
 tests["Q2_FX_Q1"]=delta["FX_Q1_signed"]-q1cf["fx_cash_effect"]
 tests["Q2_FX_derived"]=delta["FX_reconciliation_implied"]-(cf["FX_effect_reported_6m"]-q1cf["fx_cash_effect"])
 tests["Q2_net"]=delta["CFO"]+delta["CFI"]+delta["CFF"]-delta["net_cash_change"]
 tests["Q2_openclose_fx_bridge"]=delta["opening_cash"]+delta["net_cash_change"]+delta["FX_reconciliation_implied"]-delta["closing_cash"]
 tests["Q2_CFI_capex"]=delta["capex"]-(cf["capex"]-q1cf["investing_capex"])
 tests["Q2_CFI_disposal"]=delta["disposal_proceeds"]-(cf["disposal_proceeds"]-q1cf["investing_disposal_receipts"])
 tests["Q2_financing_repay"]=delta["financing_debt_repayment"]-(cf["financing_debt_repayment"]-q1cf["financing_longterm_repayment"])
 assert len(tests)>=50 and all(v==0 for v in tests.values()),(len(tests),{k:v for k,v in tests.items() if v!=0})
 assert cf["CFO"]==-19720550 and cf["pre_working_capital_cash"]==3923579
 assert cf["interest_cash_received"]==12784580 and cf["interest_cash_received"]!=cf["CFO"]
 assert delta["CFO"]==21755856 and delta["CFI"]==-62379 and delta["CFF"]==1014444
 assert delta["net_cash_change"]==22707921 and delta["FX_reconciliation_implied"]==-210436
 assert delta["opening_cash"]==44780913 and delta["closing_cash"]==67278398
 assert fin["symbol"]=="TPB" and [z["period"] for z in fin["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=fin["items"][1];s=row["source_validation"]
 assert row["verification_status"]=="issuer_signed_TPB_2025Q2_original_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_vintage_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 assert s["manually_visual_reviewed"] and s["original_pdf_hash_verified"]
 assert s["original_pdf_sha256"]==src["sha256"] and s["reviewed_H1_pdf_sha256"]==rev["sha256"]
 assert s["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert s["FX_Q2_negative_210436_implied_not_reported"] and s["Q1_FX_explicit_210436_true"]
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"] and row["equity"]==b["total_equity"]
 assert row["pretax_profit"]==x["pretax_profit"] and row["net_profit"]==x["net_profit"] and row["revenue"]==x["operating_income"]
 assert row["net_profit_attributable"]==x["parent_profit"]
 assert row["operating_cash_flow"]==delta["CFO"] and row["investing_cash_flow"]==delta["CFI"]
 assert row["financing_cash_flow"]==delta["CFF"] and row["net_cash_change"]==delta["net_cash_change"]
 assert row["cashflow_fx"]==delta["FX_reconciliation_implied"] and row["cashflow_fx_ytd"]==0
 assert row["cash_beginning"]==delta["opening_cash"] and row["cash_ending"]==delta["closing_cash"]
 assert row["operating_cash_flow_ytd"]==cf["CFO"] and row["investing_cash_flow_ytd"]==cf["CFI"]
 assert row["financing_cash_flow_ytd"]==cf["CFF"] and row["net_cash_change_ytd"]==cf["net_cash_change"]
 assert row["roa"]==round(400*x["net_profit"]/((b["total_assets"]+fin["items"][0]["total_assets"])/2),2)==1.59
 assert row["roe"]==round(400*x["net_profit"]/((b["total_equity"]+fin["items"][0]["equity"])/2),2)==16.77
 assert row["financial_line_items_rejected_values"]=={} and row["financial_line_items_rejected_fields"]==[]
 for prefix,obj in (("b02a_Q2",b),("b03a_Q2",x),("b03a_6m_reviewed",y),("b04a_6m_reviewed",cf),("b04a_q2",delta)):
  for key,val in obj.items():
   if isinstance(val,int): assert row["signed_source_"+prefix+"_"+key]==val,(prefix,key)
 assert fin["items"][0]["verification_status"]=="issuer_signed_TPB_2025Q1_consolidated_B02a_B03a_B04a_FX_aware_verified"
 assert [z["verification_status"] for z in fin["items"][2:]]==[
 "issuer_signed_TPB_2025Q3_consolidated_B02a_B03a_B04a_9M_minus_KPMG_H1_FX_exact_verified","issuer_signed_TPB_2025Q4_original_B02a_B03a_KPMG_FY_audited_minus_9M_B04a_FX_vintage_verified",
 "issuer_signed_TPB_2026Q1_B02a_B03a_B04a_exact_FX_2025_represented_comparative_verified","issuer_signed_TPB_2026Q2_first_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_verified"]
 assert all(not z["period"].startswith("2024") for z in fin["items"])
 return len(tests)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 q=json.loads(Q1LEDGER.read_text("utf-8"))
 fin=json.loads(FIN.read_text("utf-8"))
 n=verify(a,q,fin)
 for kind in ("B02","B03","B04_CFO","B04_interest_as_CFO","FX_omitted","FX_as_unaudited",
              "cash_end","bad_pdf","wrong_H1","prior_Q1","other_Q3","ratio"):
  aa,qq,ff=deepcopy(a),deepcopy(q),deepcopy(fin)
  if kind=="B02":aa["B02a_Q2_first"]["total_assets"]+=1
  elif kind=="B03":aa["B03a_Q2_first"]["net_profit"]+=1
  elif kind=="B04_CFO":aa["B04a_6m_H1_reviewed"]["CFO"]+=1
  elif kind=="B04_interest_as_CFO":ff["items"][1]["operating_cash_flow"]=aa["B04a_6m_H1_reviewed"]["interest_cash_received"]
  elif kind=="FX_omitted":ff["items"][1]["cashflow_fx"]=0
  elif kind=="FX_as_unaudited":aa["Q2_cash_6m_reviewed_minus_Q1_signed"]["FX_reconciliation_implied"]=0
  elif kind=="cash_end":ff["items"][1]["cash_ending"]+=1
  elif kind=="bad_pdf":aa["original_Q2"]["sha256"]="0"*64
  elif kind=="wrong_H1":aa["reviewed_H1"]["sha256"]="f"*64
  elif kind=="prior_Q1":ff["items"][0]["verification_status"]="fake"
  elif kind=="other_Q3":ff["items"][2]["verification_status"]="fake"
  elif kind=="ratio":ff["items"][1]["roe"]=88
  try:verify(aa,qq,ff)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Unexpected tamper pass: "+kind)
 print(f"PASS TPB Q2 2025 signed original 52p and KPMG reviewed H1 97p: {n} exact identities, 16 6M-Q1 B03 bridges, 12 mutation gates.")
 print("PASS TPB Q2 bank CFO +21,755,856 CFI -62,379 CFF +1,014,444 net +22,707,921, Q1 FX +210,436 vs H1 FX 0 gives explicitly sourced implied Q2 delta -210,436.")
 print("PASS original Q1 preserved, TPB 2025Q3–2026Q2 provisional unchanged; no 2024 dashboard quarters.")
if __name__=="__main__":main()
