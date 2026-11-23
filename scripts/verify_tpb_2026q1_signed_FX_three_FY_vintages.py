#!/usr/bin/env python3
"""TPB 2026Q1 issuer signed original B02a/B03a/B04a with FX.

The 31/12/2025 B02a comparative is explicitly 'Trình bày lại'; preserve
the distinct 2025 as-filed and KPMG audited prior-year versions.
"""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2026Q1-signed-B02a-B03a-B04a-three-FY-vintages-million-vnd.json"
FY=ROOT/"reports/source-audits/TPB-2025Q4-first-issued-vs-KPMG-FY-audited-bank-million-vnd.json"
DATA=ROOT/"data/financials-TPB.json"

def verify(a,fy,fin):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("TPB","2026-Q1","consolidated","triệu VND")
 src=a["source"]
 assert src["sha256"]=="d8f4e25a6a4b805488312878a3734f6b1b43595f02052eedd831d5958dc1fb08"
 assert src["bytes"]==11546904 and src["pages"]==64
 assert src["B02a_pages"]==[5,6] and src["B03a_page"]==8 and src["B04a_pages"]==[9,10]
 old=a["fy2025_sources"];po=a["B02a_2025_represented_opening"]
 assert old["first_sha256"]==fy["signed_Q4_source"]["sha256"]
 assert old["audit_sha256"]==fy["audited_FY_source"]["sha256"]
 assert old["first_B02"]==[fy["B02_Q4_first"][k] for k in ("total_assets","total_liabilities","total_equity")]
 assert old["audited_B02"]==[fy["B02_FY_audited"][k] for k in ("total_assets","total_liabilities","total_equity")]
 assert old["audited_cash_closing"]==fy["B04_FY_audited"]["closing_cash"]
 assert old["reported_2026Q1_opening_B02"]==[po[k] for k in ("total_assets","total_liabilities","total_equity")]
 for name,k in (("assets","total_assets"),("liabilities","total_liabilities"),("equity","total_equity")):
  index={"assets":0,"liabilities":1,"equity":2}[name]
  assert old["reported_2026Q1_opening_vs_KPMG_audited"][name]==po[k]-old["audited_B02"][index]
 assert old["reported_2026Q1_opening_vs_KPMG_audited"]=={"assets":25093,"liabilities":115738,"equity":-90645}
 assert po["total_assets"]==po["total_liabilities"]+po["total_equity"]
 b,p,c=a["B02a_current"],a["B03a_current"],a["B04a_current"]
 E={}
 E["B02_assets"]=sum(b[k] for k in ("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
 "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liabs"]=sum(b[k] for k in ("government_liabilities","interbank_liabilities","customer_deposits",
 "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 E["B02_equity"]=sum(b[k] for k in ("bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_services"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["B03_revenue"]=sum(p[k] for k in ("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["B03_before_provision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["B03_PBT"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["B04_preWC"]=sum(c[k] for k in ("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash",
 "recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["B04_true_CFO"]=c["pre_wc_cash"]+sum(c[k] for k in ("asset_interbank","asset_securities","asset_derivatives",
 "asset_customer_loans","asset_credit_provisions","asset_other","liability_government","liability_interbank",
 "liability_customer_deposits","liability_papers","liability_trust","liability_derivatives","liability_other"))-c["CFO"]
 E["B04_CFI"]=c["capex"]+c["investment_outflows"]+c["dividends_received"]-c["CFI"]
 E["B04_CFF"]=c["financing_repayment"]-c["CFF"]
 E["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["B04_FX_end"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 E["B04_FY2025_audited_opening_cash"]=c["opening_cash"]-old["audited_cash_closing"]
 assert len(E)==20 and all(v==0 for v in E.values()),E
 assert c["CFO"]==-7280016 and c["pre_wc_cash"]==2394247 and c["interest_cash_received"]==8471388
 assert c["CFO"]!=c["pre_wc_cash"] and c["CFO"]!=c["interest_cash_received"]
 assert (c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"])==(-94901,-192100,-7567017,373117)
 assert (c["opening_cash"],c["closing_cash"])==(115747324,108553424)
 assert fin["symbol"]=="TPB" and [v["period"] for v in fin["items"]]==[
  "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=fin["items"][4];s=row["source_validation"]
 assert row["verification_status"]=="issuer_signed_TPB_2026Q1_B02a_B03a_B04a_exact_FX_2025_represented_comparative_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 assert s["manually_visual_reviewed"] and s["original_pdf_hash_verified"]
 assert s["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert s["original_pdf_sha256"]==src["sha256"] and s["FY2025_KPMG_audited_pdf_sha256"]==old["audit_sha256"]
 assert s["signed_Q1_2026_B02a_2025FY_comparative_represented"]
 assert s["interest_cash_received_8471388_not_CFO"] and s["before_working_capital_cash_2394247_not_CFO"]
 assert s["Q1_cashflow_FX_aware_373117_exact"] and s["prior_TPB_2025Q1_to_2025Q4_completed_unchanged"]
 mapped={
 "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
 "net_profit_attributable":p["parent_profit"],"income_tax":p["income_tax"],
 "income_tax_current":p["income_tax_current"],"income_tax_deferred":p["income_tax_deferred"],
 "bank_cash_on_hand":b["cash_vault"],"bank_deposits_at_state_bank":b["deposits_SBV"],
 "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
 "bank_customer_loans":b["customer_loans_net"],"bank_purchased_debt_net":b["purchased_debt_net"],
 "bank_trading_securities":b["trading_securities"],"bank_investment_securities":b["investment_securities"],
 "bank_contributions_and_long_term_investments":b["longterm_investments"],
 "fixed_assets":b["fixed_assets"],"bank_other_assets":b["other_assets"],
 "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabilities"],
 "bank_customer_deposits":b["customer_deposits"],"bank_valuable_papers":b["valuable_papers"],
 "bank_funding_and_trust_liabilities":b["trust_liabilities"],"bank_other_liabilities":b["other_liabilities"],
 "retained_earnings":b["retained_profit"],"bank_interest_income":p["interest_income"],
 "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
 "bank_service_income":p["service_income"],"bank_service_expense":p["service_expense"],
 "bank_fx_net_income":p["FX_net"],"bank_other_operating_net":p["other_net"],
 "bank_dividend_and_capital_income":p["contribution_income"],
 "bank_operating_expenses":p["operating_expenses"],"bank_pre_provision_operating_profit":p["before_provision"],
 "bank_provision_expense":p["credit_provision"],"bank_non_controlling_profit":p["noncontrolling_profit"],
 "operating_profit":p["before_provision"],"operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],
 "financing_cash_flow":c["CFF"],"net_cash_change":c["net_cash_change"],"cashflow_fx":c["FX_effect"],
 "cash_beginning":c["opening_cash"],"cash_ending":c["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
 "cashflow_fx_ytd":c["FX_effect"],"cash_beginning_reported_ytd":c["opening_cash"],
 "cash_ending_ytd":c["closing_cash"],"capital_expenditure":c["capex"],
 "capital_expenditure_ytd":c["capex"]
 }
 assert len(mapped)==55 and set(row["financial_line_items_manually_verified_fields"])==set(mapped)
 for field,value in mapped.items():
  assert type(row[field]) is int and row[field]==value,field
 for prefix,ledger in (("b02a",b),("b03a",p),("b04a",c)):
  for k,v in ledger.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 for k,v in po.items():
  if isinstance(v,int): assert row["signed_source_b02a_restated_"+k]==v,(k,v)
 assert row["roa"]==round(400*p["net_profit"]/((b["total_assets"]+po["total_assets"])/2),2)==1.30
 assert row["roe"]==round(400*p["net_profit"]/((b["total_equity"]+po["total_equity"])/2),2)==14.32
 assert all(z["verification_status"].startswith("issuer_signed") for z in fin["items"][:5])
 assert fin["items"][5]["verification_status"]=="auto_extracted_pending_visual_review"
 assert not any(z["period"].startswith("2024") for z in fin["items"])
 return len(E)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 f=json.loads(FY.read_text("utf-8"))
 d=json.loads(DATA.read_text("utf-8"))
 n=verify(a,f,d)
 for case in ("assets","equity","profit","sourcecash","publishedcash","FX","sourcePDF",
              "oldFY_source","restatedFY","priorQ4","Q2_notdone","ratio"):
  aa,ff,dd=deepcopy(a),deepcopy(f),deepcopy(d)
  if case=="assets":aa["B02a_current"]["total_assets"]+=1
  elif case=="equity":aa["B02a_current"]["total_equity"]+=1
  elif case=="profit":aa["B03a_current"]["net_profit"]+=1
  elif case=="sourcecash":aa["B04a_current"]["CFO"]+=1
  elif case=="publishedcash":dd["items"][4]["operating_cash_flow"]=8471388
  elif case=="FX":dd["items"][4]["cashflow_fx"]=0
  elif case=="sourcePDF":aa["source"]["sha256"]="0"*64
  elif case=="oldFY_source":ff["audited_FY_source"]["sha256"]="f"*64
  elif case=="restatedFY":aa["B02a_2025_represented_opening"]["total_assets"]+=1
  elif case=="priorQ4":dd["items"][3]["verification_status"]="fake"
  elif case=="Q2_notdone":dd["items"][5]["verification_status"]="forged"
  elif case=="ratio":dd["items"][4]["roe"]+=1
  try:verify(aa,ff,dd)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("TPB 2026Q1 test did not catch source corruption "+case)
 print(f"PASS TPB signed original 2026Q1 64p: {n} exact B02a B03a B04a & cash FX identities, 55 verified fields, 12 corruption tests.")
 print("PASS Q1 2026 bank CFO -7,280,016, not +8,471,388 interest or +2,394,247 before-WC. CFI -94,901, CFF -192,100, net -7,567,017, FX +373,117, cash 115,747,324 to 108,553,424 million VND.")
 print("PASS 2025 KPMG FY, first-issued Q4 and 2026 restated prior year source vintages remain separate; Q1-Q4 2025 immutable, TPB Q2 2026 still pending.")
if __name__=="__main__":main()
