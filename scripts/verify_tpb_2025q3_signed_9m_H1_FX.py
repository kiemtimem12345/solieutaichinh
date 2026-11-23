#!/usr/bin/env python3
"""Verify TPB signed 2025Q3 original B02a/B03a/B04a vs reviewed 2025H1.

The 9M bank CFO is after changes in operating assets and liabilities, and
cash opening + net cash flow + signed FX effect must equal final cash.
Standalone Q3 = signed 9M − accepted KPMG reviewed 6M; never invent cash.
"""
import json
from pathlib import Path
from copy import deepcopy

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2025Q3-signed-9M-KPMG-H1-bank-FX-million-vnd.json"
H1=ROOT/"reports/source-audits/TPB-2025Q2-signed-original-KPMG-H1-reviewed-FX-quarter-million-vnd.json"
FIN=ROOT/"data/financials-TPB.json"

def verify(a,h1,fin):
 assert a["symbol"]=="TPB" and a["period"]=="2025-Q3" and a["scope"]=="consolidated" and a["unit"]=="triệu VND"
 doc=a["original_Q3"]
 assert doc["sha256"]=="3849167a56b8ea2a6285087aba363a8c0aeaf93f74fcea69da9743700a22dfc4"
 assert doc["bytes"]==9861954 and doc["pages"]==54
 assert doc["pdf_B02a_pages"]==[5,6] and doc["pdf_B03a_page"]==8 and doc["pdf_B04a_pages"]==[9,10]
 assert a["H1_reviewed"]["pdf_sha256"]==h1["reviewed_H1"]["sha256"]
 assert a["H1_reviewed"]["B03a_6m"]==h1["B03a_6m_H1_reviewed"]
 assert a["H1_reviewed"]["B04a_6m"]==h1["B04a_6m_H1_reviewed"]
 b,p,y,c,q=a["B02a_Q3"],a["B03a_Q3_direct"],a["B03a_9m"],a["B04a_9m"],a["Q3_cash_9m_minus_H1"]
 h3=a["H1_reviewed"]["B03a_6m"];h4=a["H1_reviewed"]["B04a_6m"]
 e={}
 e["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 e["B02_assets"]=sum(b[k] for k in ("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
 "customer_loans_net","purchased_debt_net","investment_securities","fixed_assets","other_assets"))-b["total_assets"]
 e["B02_liabs"]=sum(b[k] for k in ("government_liabilities","interbank_liabilities","customer_deposits","derivative_liabilities",
 "trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 e["B02_equity"]=sum(b[k] for k in ("bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 e["B03_Q3_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 e["B03_Q3_services"]=p["service_income"]+p["service_expense"]-p["services_net"]
 e["B03_Q3_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 income=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 e["B03_Q3_income"]=sum(p[k] for k in income)-p["operating_income"]
 e["B03_9M_income"]=sum(y[k] for k in income)-y["operating_income"]
 for name,obj in (("Q3",p),("9M",y)):
  e["B03_"+name+"_preprov"]=obj["operating_income"]-obj["operating_expenses"]-obj["before_provision"]
  e["B03_"+name+"_pretax"]=obj["before_provision"]-obj["credit_provision"]-obj["pretax_profit"]
  e["B03_"+name+"_PAT"]=obj["pretax_profit"]-obj["income_tax"]-obj["net_profit"]
  e["B03_"+name+"_parent"]=obj["net_profit"]-obj["noncontrolling_profit"]-obj["parent_profit"]
 b03_keys=(*income,"operating_income","operating_expenses","before_provision",
 "credit_provision","pretax_profit","income_tax","net_profit","noncontrolling_profit","parent_profit")
 for key in b03_keys:
  e["B03_signedQ3_vs_9M_lessH1_"+key]=y[key]-h3[key]-p[key]
 before=("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
 "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid")
 current_assets=("asset_interbank","asset_securities","asset_derivatives","asset_customer_loans",
 "asset_credit_provisions","asset_other")
 current_liabs=("liability_government","liability_interbank","liability_customer_deposits",
 "liability_papers","liability_trust","liability_derivatives","liability_other")
 e["B04_9M_pre_wc"]=sum(c[k] for k in before)-c["pre_working_capital_cash"]
 e["B04_9M_true_CFO"]=c["pre_working_capital_cash"]+sum(c[k] for k in current_assets)+sum(c[k] for k in current_liabs)-c["CFO"]
 e["B04_9M_CFI"]=sum(c[k] for k in ("capex","disposal_proceeds","dividends_investing"))-c["CFI"]
 e["B04_9M_CFF"]=sum(c[k] for k in ("financing_new_debt","financing_debt_repayment","financing_dividends_paid"))-c["CFF"]
 e["B04_9M_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 e["B04_9M_FX_cash"]=c["opening_cash"]+c["net_cash_change"]+c["fx_cash_effect"]-c["closing_cash"]
 for name in ("CFO","CFI","CFF","net_cash_change"):
  e["B04_Q3_9M_minus_H1_"+name]=c[name]-h4[name]-q[name]
 e["B04_Q3_open"]=q["opening_cash"]-h4["closing_cash"]
 e["B04_Q3_close"]=q["closing_cash"]-c["closing_cash"]
 e["B04_Q3_FX"]=q["fx_effect"]-(c["fx_cash_effect"]-h4["FX_effect_reported_6m"])
 e["B04_Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 e["B04_Q3_openclose"]=q["opening_cash"]+q["net_cash_change"]+q["fx_effect"]-q["closing_cash"]
 e["B04_Q3_capex"]=q["capex"]-(c["capex"]-h4["capex"])
 e["B04_Q3_disposal"]=q["disposal_proceeds"]-(c["disposal_proceeds"]-h4["disposal_proceeds"])
 e["B04_Q3_dividends"]=q["dividends_investing"]-(c["dividends_investing"]-h4["dividends_investing"])
 e["B04_Q3_newdebt"]=q["financing_new_debt"]-(c["financing_new_debt"]-h4["financing_new_debt"])
 e["B04_Q3_repayment"]=q["financing_debt_repayment"]-(c["financing_debt_repayment"]-h4["financing_debt_repayment"])
 e["B04_Q3_dividends_paid"]=q["financing_dividends_paid"]-(c["financing_dividends_paid"]-h4["financing_dividends_paid"])
 assert len(e)>=50 and all(v==0 for v in e.values()),(len(e),{k:v for k,v in e.items() if v})
 assert c["CFO"]==-1958525 and c["pre_working_capital_cash"]==7478930
 assert c["interest_cash_received"]==20965847 and c["CFO"]!=c["pre_working_capital_cash"]
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"])==(17762025,-27331,1347200,19081894)
 assert (q["opening_cash"],q["closing_cash"],q["fx_effect"])==(67278398,86612489,252197)
 assert fin["symbol"]=="TPB" and [x["period"] for x in fin["items"]]==[
  "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=fin["items"][2];src=row["source_validation"]
 assert row["verification_status"]=="issuer_signed_TPB_2025Q3_consolidated_B02a_B03a_B04a_9M_minus_KPMG_H1_FX_exact_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 assert src["original_pdf_sha256"]==doc["sha256"] and src["original_pdf_hash_verified"]
 assert src["manually_visual_reviewed"] and src["source_is_consolidated_financial_statements"]
 assert src["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert src["H1_reviewed_pdf_sha256"]==a["H1_reviewed"]["pdf_sha256"]
 assert src["signed_Q3_direct_B03a_equal_signed9M_minus_KPMG_reviewedH1_16_fields"]
 assert src["signed_Q3_B04a_9M_minus_KPMG_H1_cash_exact"]
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"] and row["equity"]==b["total_equity"]
 assert row["pretax_profit"]==p["pretax_profit"] and row["net_profit"]==p["net_profit"]
 assert row["revenue"]==p["operating_income"] and row["net_profit_attributable"]==p["parent_profit"]
 for name,raw in (("operating_cash_flow","CFO"),("investing_cash_flow","CFI"),
 ("financing_cash_flow","CFF"),("net_cash_change","net_cash_change"),("cashflow_fx","fx_effect"),
 ("cash_beginning","opening_cash"),("cash_ending","closing_cash")):
  assert row[name]==q[raw],name
 for name,raw in (("operating_cash_flow_ytd","CFO"),("investing_cash_flow_ytd","CFI"),
 ("financing_cash_flow_ytd","CFF"),("net_cash_change_ytd","net_cash_change"),
 ("cashflow_fx_ytd","fx_cash_effect")):
  assert row[name]==c[raw],name
 assert row["roa"]==round(400*p["net_profit"]/((b["total_assets"]+fin["items"][1]["total_assets"])/2),2)==1.38
 assert row["roe"]==round(400*p["net_profit"]/((b["total_equity"]+fin["items"][1]["equity"])/2),2)==15.55
 assert set(row["financial_line_items_rejected_values"])==set() and row["financial_line_items_rejected_fields"]==[]
 for prefix,obj in (("b02a_Q3",b),("b03a_Q3",p),("b03a_9m",y),("b04a_9m",c),("b04a_Q3",q)):
  for key,value in obj.items():
   if isinstance(value,int):assert row["signed_source_"+prefix+"_"+key]==value,(prefix,key)
 assert fin["items"][0]["verification_status"]=="issuer_signed_TPB_2025Q1_consolidated_B02a_B03a_B04a_FX_aware_verified"
 assert fin["items"][1]["verification_status"]=="issuer_signed_TPB_2025Q2_original_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_vintage_verified"
 assert all(x["verification_status"]=="auto_extracted_pending_visual_review" for x in fin["items"][3:])
 assert not any(x["period"].startswith("2024") for x in fin["items"])
 return len(e)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 h=json.loads(H1.read_text("utf-8"))
 d=json.loads(FIN.read_text("utf-8"))
 count=verify(a,h,d)
 for case in ("B02","profit","source_pdf","H1_source","CFO","pre_wc_as_CFO",
              "no_FX","net","cash_end","prior_Q2","future_fake","ROE"):
  aa,hh,dd=deepcopy(a),deepcopy(h),deepcopy(d)
  if case=="B02":aa["B02a_Q3"]["total_assets"]+=1
  elif case=="profit":aa["B03a_Q3_direct"]["net_profit"]+=1
  elif case=="source_pdf":aa["original_Q3"]["sha256"]="0"*64
  elif case=="H1_source":hh["reviewed_H1"]["sha256"]="f"*64
  elif case=="CFO":aa["B04a_9m"]["CFO"]+=1
  elif case=="pre_wc_as_CFO":dd["items"][2]["operating_cash_flow"]=7478930
  elif case=="no_FX":dd["items"][2]["cashflow_fx"]=0
  elif case=="net":dd["items"][2]["net_cash_change"]+=1
  elif case=="cash_end":aa["B04a_9m"]["closing_cash"]+=1
  elif case=="prior_Q2":dd["items"][1]["verification_status"]="fake"
  elif case=="future_fake":dd["items"][3]["verification_status"]="forged"
  elif case=="ROE":dd["items"][2]["roe"]+=1
  try:verify(aa,hh,dd)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Source tampering not caught: "+case)
 print(f"PASS TPB 2025 Q3 original signed 54-page B02a B03a B04a and reviewed H1: {count} exact accounting/cash/FX identities, 16 Q3 B03 bridges, 12 tamper cases.")
 print("PASS standalone Q3 CFO +17,762,025 CFI -27,331 CFF +1,347,200 net +19,081,894 FX +252,197, cash 67,278,398 → 86,612,489 million VND.")
 print("PASS TPB source-verified Q1 Q2 Q3 2025, 2025Q4–2026Q2 provisional untouched, no 2024 data.")
if __name__=="__main__":main()
