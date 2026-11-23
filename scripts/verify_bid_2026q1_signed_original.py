#!/usr/bin/env python3
"""BID signed Q1 2026 full bank-source accounting validation, million VND.

Compares original Q1 B01/B03/direct-method B04 with verified audited 2025
FY comparatives, restores true bank operating CFO (not pre-WC cash).
"""
from copy import deepcopy
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/BID-2026Q1-signed-consolidated-exact-million-vnd.json"
FY=ROOT/"reports/source-audits/BID-2025Q4-signed-original-vs-audited-FY-million-vnd.json"
DATA=ROOT/"data/financials-BID.json"

def validate(a:dict,fy:dict,data:dict)->int:
 assert a["symbol"]=="BID" and a["scope"]=="consolidated" and a["period"]=="2026-Q1"
 assert a["unit"]=="triệu VND"
 original=a["signed_q1_source"];old=a["audited_2025_FY_comparative"]
 assert original["sha256"]=="187ace9c81d224372382b96af20ee98a2469fd2f1ebe5b2d6e49b6d44aa7669e"
 assert original["pages"]==36 and original["bytes"]==15647587
 assert original["visual_B01_pages"]==[4,5] and original["visual_B03_pages"]==[7] and original["visual_B04_pages"]==[8,9]
 assert old["signed_audited_SHA256"]==fy["signed_FY_audited"]["sha256"]
 assert old["b01_dec31"]==fy["B01_FY_audited"]
 assert old["bank_cash_start"]==fy["B04_FY_audited"]["closing_cash"]
 b,p,c=a["B01_q1"],a["B03_q1"],a["B04_q1"]
 tests={}
 tests["B01_balanced"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 tests["B01_assets"]=sum(b[k] for k in (
  "cash_vault","deposits_SBV","interbank_assets","trading_securities",
  "derivative_assets","customer_loans_net","investment_securities",
  "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 tests["B01_liabilities"]=sum(b[k] for k in (
  "government_liabilities","interbank_liabilities","customer_deposits",
  "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 tests["B01_equity"]=sum(b[k] for k in (
  "bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 tests["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 tests["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 tests["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 tests["B03_income"]=sum(p[k] for k in (
  "net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 tests["B03_opex"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 tests["B03_provision"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 tests["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 tests["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 tests["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 tests["B04_before_WC"]=sum(c[k] for k in (
  "interest_received","interest_paid","services_cash","fx_trading_cash",
  "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["before_working_capital"]
 tests["B04_CFO_after_WC"]=c["before_working_capital"]+sum(c[k] for k in (
  "assets_interbank","assets_trading","assets_derivatives","assets_customer_loans",
  "assets_credit_provisions","assets_other","liability_government","liability_interbank",
  "liability_customer_deposits","liability_papers","liability_trust",
  "liability_derivatives","liability_other"))-c["CFO"]
 tests["B04_CFI"]=sum(c[k] for k in (
  "capital_expenditure","disposal_receipts","disposal_expenses","dividend_investing"))-c["CFI"]
 tests["B04_CFF"]=c["equity_issuance"]+c["financing_debt_received"]+c["financing_debt_repaid"]-c["CFF"]
 tests["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 tests["B04_open_end"]=c["opening_cash"]+c["net_cash_change"]-c["closing_cash"]
 tests["B04_prior_FY_audited"]=c["opening_cash"]-old["bank_cash_start"]
 tests["B01_prior_comparative_assets"]=old["b01_dec31"]["total_assets"]-3330825720
 tests["B01_prior_comparative_equity"]=old["b01_dec31"]["total_equity"]-173552902
 assert len(tests)==22 and all(v==0 for v in tests.values()),tests
 assert c["CFO"]==1179080 and c["before_working_capital"]==8548364
 assert c["CFO"]!=c["before_working_capital"]
 assert (c["CFI"],c["CFF"],c["net_cash_change"],c["closing_cash"])==(-249766,13321988,14251302,544528992)
 assert len(data["items"])==7 and data["symbol"]=="BID"
 assert [x["period"] for x in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 row=data["items"][4]
 assert row["verification_status"]=="issuer_signed_BID_2026Q1_consolidated_B01_B03_B04_direct_exact_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 source=row["source_validation"]
 assert source["original_pdf_sha256"]==original["sha256"] and source["original_pdf_hash_verified"]
 assert source["manually_visual_reviewed"] and source["source_is_consolidated_financial_statements"]
 assert source["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert source["FY2025_audited_b01_sha256"]==fy["signed_FY_audited"]["sha256"]
 assert source["FY2025_audited_yearend_bank_cash_eq_Q1_begin"]
 assert source["bank_B04_pre_wc_8548364_NOT_actual_CFO"]
 assert source["prior_automated_rejected_values"]["operating_cash_flow"]["value"]==8548364
 assert row["financial_line_items_rejected_fields"]==[] and row["financial_line_items_rejected_values"]=={}
 mapping={
  "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
  "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
  "net_profit_attributable":p["parent_profit"],"income_tax":p["income_tax"],
  "bank_cash_on_hand":b["cash_vault"],"bank_deposits_at_state_bank":b["deposits_SBV"],
  "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
  "bank_customer_loans":b["customer_loans_net"],"bank_trading_securities":b["trading_securities"],
  "bank_investment_securities":b["investment_securities"],
  "bank_contributions_and_long_term_investments":b["longterm_investments"],
  "fixed_assets":b["fixed_assets"],"bank_other_assets":b["other_assets"],
  "bank_deposits_and_borrowings_from_credit_institutions":b["interbank_liabilities"],
  "bank_customer_deposits":b["customer_deposits"],"bank_valuable_papers":b["valuable_papers"],
  "bank_funding_and_trust_liabilities":b["trust_liabilities"],
  "bank_other_liabilities":b["other_liabilities"],
  "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
  "bank_fx_net_income":p["FX_net"],"bank_other_operating_net":p["other_net"],
  "bank_dividend_and_capital_income":p["contribution_income"],
  "bank_operating_expenses":p["operating_expenses"],
  "bank_pre_provision_operating_profit":p["before_provision"],
  "bank_provision_expense":p["credit_provision"],"bank_non_controlling_profit":p["noncontrolling_profit"],
  "operating_profit":p["before_provision"],
  "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],
  "financing_cash_flow":c["CFF"],"net_cash_change":c["net_cash_change"],
  "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
  "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
  "cash_beginning":c["opening_cash"],"cash_ending":c["closing_cash"],
  "cash_beginning_reported_ytd":c["opening_cash"],"cash_ending_ytd":c["closing_cash"],
  "capital_expenditure":c["capital_expenditure"],"capital_expenditure_ytd":c["capital_expenditure"],
 }
 assert len(mapping)==46 and set(row["financial_line_items_manually_verified_fields"])==set(mapping)
 for k,v in mapping.items():
  assert type(row[k]) is int and row[k]==v,(k,row.get(k),v)
 for pref,ledger in (("b01",b),("b03",p),("b04",c)):
  for k,v in ledger.items():
   assert row["signed_source_"+pref+"_"+k]==v,(pref,k)
 assert row["roa"]==round(4*100*p["net_profit"]/((b["total_assets"]+old["b01_dec31"]["total_assets"])/2),2)==0.82
 assert row["roe"]==round(4*100*p["net_profit"]/((b["total_equity"]+old["b01_dec31"]["total_equity"])/2),2)==15.11
 assert all(x["verification_status"].startswith("issuer_signed") for i,x in enumerate(data["items"]) if i not in (5,))
 assert data["items"][5]["verification_status"]=="auto_extracted_pending_visual_review"
 assert not any(x["period"].startswith("2024") for x in data["items"])
 return len(tests)

def main():
 audit=json.loads(LEDGER.read_text("utf-8"))
 prev=json.loads(FY.read_text("utf-8"))
 data=json.loads(DATA.read_text("utf-8"))
 n=validate(audit,prev,data)
 cases=("cash_before_wc","operating_cash","source_assets","source_profit","source_sha","audited_comparative","prior_completed","Q2_unverified","ROE")
 for case in cases:
  a,b,d=deepcopy(audit),deepcopy(prev),deepcopy(data)
  if case=="cash_before_wc":d["items"][4]["operating_cash_flow"]=8548364
  elif case=="operating_cash":a["B04_q1"]["CFO"]+=1
  elif case=="source_assets":a["B01_q1"]["total_assets"]+=1
  elif case=="source_profit":a["B03_q1"]["net_profit"]+=1
  elif case=="source_sha":a["signed_q1_source"]["sha256"]="0"*64
  elif case=="audited_comparative":b["B01_FY_audited"]["total_assets"]+=1
  elif case=="prior_completed":d["items"][3]["verification_status"]="unverified"
  elif case=="Q2_unverified":d["items"][5]["verification_status"]="forged_completed"
  elif case=="ROE":d["items"][4]["roe"]+=1
  try:validate(a,b,d)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Uncaught tamper case: "+case)
 print(f"PASS BID 2026-Q1 36p signed original B01/B03/B04: {n} exact bank source checks, 46 production fields, {len(cases)} negative corruption tests.")
 print("PASS Q1 actual bank CFO 1,179,080 (before WC 8,548,364 NOT CFO), CFI -249,766 CFF 13,321,988 net 14,251,302, cash 530,277,690 to 544,528,992.")
 print("PASS 2025 FY AUDITED beginning assets/equity for Q1 ratios; prior 2025 Q1-Q4 and 2026 Q3 complete; 2026 Q2 pending original source.")
if __name__=="__main__":main()
