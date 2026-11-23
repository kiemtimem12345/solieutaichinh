#!/usr/bin/env python3
"""TPB Q1/2025 original issuer source B02a B03a B04a bank cash FX QA.

Proves true signed CFO, rejects interest receipts mistakenly parsed as CFO,
rejects pre-working-capital as CFO and missing 210,436-million FX.
"""
from copy import deepcopy
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2025Q1-signed-original-B02a-B03a-B04a-FX-million-vnd.json"
DATA=ROOT/"data/financials-TPB.json"

def verify(a:dict,fin:dict)->int:
 assert a["symbol"]=="TPB" and a["period"]=="2025-Q1" and a["scope"]=="consolidated"
 assert a["unit"]=="triệu VND"
 source=a["original"]
 assert source["sha256"]=="f95e7cacd969ceb004fb516d39e81871372a93d02ec9b5edc611e1e578788533"
 assert source["pages"]==54 and source["bytes"]==7895615
 assert source["B02a_pdf_pages"]==[7,8] and source["B03a_pdf_page"]==10 and source["B04a_pdf_pages"]==[11,12]
 assert source["visual_signed_original"] is True
 b,p,c=a["B02a_current"],a["B03a_Q1"],a["B04a_Q1"]
 checks={}
 checks["B02a_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 checks["B02a_asset_classes"]=sum(b[k] for k in (
  "cash_vault","deposits_SBV","interbank_assets","trading_securities",
  "derivative_assets","net_customer_loans","purchased_debt_net",
  "investment_securities","fixed_assets","other_assets"))-b["total_assets"]
 checks["B02a_liability_classes"]=sum(b[k] for k in (
  "government_liabilities","interbank_liabilities","customer_deposits",
  "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 checks["B02a_equity_classes"]=sum(b[k] for k in (
  "bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 checks["B03a_net_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 checks["B03a_services"]=p["service_income"]+p["service_expense"]-p["services_net"]
 checks["B03a_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 checks["B03a_7_income"]=sum(p[k] for k in (
  "net_interest","services_net","FX_net","trading_net",
  "invest_net","other_net","contribution_income"))-p["operating_income"]
 checks["B03a_preprovision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 checks["B03a_credit_provision"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 checks["B03a_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 checks["B03a_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 checks["B03a_parent_negative_NCI"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 checks["B04a_cash_before_WC"]=sum(c[k] for k in (
  "interest_cash_received","interest_cash_paid","services_cash",
  "fx_trading_cash","other_cash","recovered_bad_debts_cash",
  "staff_admin_cash","tax_paid"))-c["cash_before_working_capital"]
 checks["B04a_actual_CFO"]=c["cash_before_working_capital"]+sum(c[k] for k in (
  "assets_interbank","assets_securities","assets_derivatives",
  "assets_customer_loans","assets_credit_provisions","assets_other",
  "liability_government","liability_interbank","liability_customer_deposits",
  "liability_papers","liability_trust","liability_derivatives","liability_other"
 ))-c["operating_cash_flow"]
 checks["B04a_CFI"]=c["investing_capex"]+c["investing_disposal_receipts"]-c["investing_cash_flow"]
 checks["B04a_CFF"]=c["financing_longterm_repayment"]-c["financing_cash_flow"]
 checks["B04a_net_cash"]=c["operating_cash_flow"]+c["investing_cash_flow"]+c["financing_cash_flow"]-c["net_cash_change"]
 checks["B04a_FX_adjusted_cash"]=c["year_open_cash"]+c["net_cash_change"]+c["fx_cash_effect"]-c["ending_cash"]
 checks["B04a_FX_derived"]=c["ending_cash"]-c["year_open_cash"]-c["net_cash_change"]-c["fx_cash_effect"]
 assert len(checks)==20 and all(v==0 for v in checks.values()),checks
 assert c["interest_cash_received"]==6286794 and c["cash_before_working_capital"]==1870090
 assert c["operating_cash_flow"]==-41476406
 assert c["operating_cash_flow"]!=c["interest_cash_received"]!=c["cash_before_working_capital"]
 assert c["net_cash_change"]==-41578162 and c["fx_cash_effect"]==210436
 assert c["ending_cash"]==44780913 and p["noncontrolling_profit"]==-1
 assert fin["symbol"]=="TPB" and [x["period"] for x in fin["items"]]==[
   "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=fin["items"][0]
 assert row["verification_status"]=="issuer_signed_TPB_2025Q1_consolidated_B02a_B03a_B04a_FX_aware_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 sv=row["source_validation"]
 assert sv["original_pdf_sha256"]==source["sha256"]
 assert sv["original_pdf_hash_verified"] and sv["manually_visual_reviewed"]
 assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["cashflow_FX_aware_B04a_exact"] and sv["bank_interest_cash_received_6286794_NOT_CFO"]
 assert sv["historical_auto_rejected_values"]["operating_cash_flow"]["value"]==6286794
 assert sv["original_2024_FY_comparative_in_2025Q1_only"]
 assert row["financial_line_items_rejected_values"]=={} and row["financial_line_items_rejected_fields"]==[]
 mapping={
  "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
  "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
  "net_profit_attributable":p["parent_profit"],"income_tax":p["income_tax"],
  "bank_cash_on_hand":b["cash_vault"],"bank_deposits_at_state_bank":b["deposits_SBV"],
  "bank_deposits_and_loans_to_credit_institutions":b["interbank_assets"],
  "bank_customer_loans":b["net_customer_loans"],"bank_purchased_debt_net":b["purchased_debt_net"],
  "bank_trading_securities":b["trading_securities"],
  "bank_investment_securities":b["investment_securities"],"fixed_assets":b["fixed_assets"],
  "bank_other_assets":b["other_assets"],
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
  "operating_profit":p["before_provision"],"bank_service_income":p["service_income"],
  "bank_service_expense":p["service_expense"],
  "operating_cash_flow":c["operating_cash_flow"],"investing_cash_flow":c["investing_cash_flow"],
  "financing_cash_flow":c["financing_cash_flow"],"net_cash_change":c["net_cash_change"],
  "operating_cash_flow_ytd":c["operating_cash_flow"],"investing_cash_flow_ytd":c["investing_cash_flow"],
  "financing_cash_flow_ytd":c["financing_cash_flow"],"net_cash_change_ytd":c["net_cash_change"],
  "cashflow_fx":c["fx_cash_effect"],"cashflow_fx_ytd":c["fx_cash_effect"],
  "cash_beginning":c["year_open_cash"],"cash_ending":c["ending_cash"],
  "cash_beginning_reported_ytd":c["year_open_cash"],"cash_ending_ytd":c["ending_cash"],
  "capital_expenditure":c["investing_capex"],"capital_expenditure_ytd":c["investing_capex"]
 }
 assert len(mapping)==50 and set(row["financial_line_items_manually_verified_fields"])==set(mapping)
 for k,v in mapping.items():
  assert type(row[k]) is int and row[k]==v,(k,row.get(k),v)
 for prefix,rec in (("b02a",b),("b03a",p),("b04a",c)):
  for key,value in rec.items():
   assert row["signed_source_"+prefix+"_"+key]==value,(prefix,key)
 audited=a["B02a_prior_audited_comparative_only"]
 assert row["roa"]==round(400*p["net_profit"]/((b["total_assets"]+audited["total_assets"])/2),2)==1.67
 assert row["roe"]==round(400*p["net_profit"]/((b["total_equity"]+audited["total_equity"])/2),2)==17.5
 assert audited["total_equity"]==37594469 and audited["total_assets"]==418028391
 assert [x["verification_status"] for x in fin["items"][1:]] == [
  "issuer_signed_TPB_2025Q2_original_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_vintage_verified",
  "issuer_signed_TPB_2025Q3_consolidated_B02a_B03a_B04a_9M_minus_KPMG_H1_FX_exact_verified",
  "issuer_signed_TPB_2025Q4_original_B02a_B03a_KPMG_FY_audited_minus_9M_B04a_FX_vintage_verified",
  "issuer_signed_TPB_2026Q1_B02a_B03a_B04a_exact_FX_2025_represented_comparative_verified",
  "issuer_signed_TPB_2026Q2_first_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_verified"
 ]
 assert not any(x["period"].startswith("2024") for x in fin["items"])
 return len(checks)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 d=json.loads(DATA.read_text("utf-8"))
 n=verify(a,d)
 cases=("cash_interest_not_CFO","cash_before_wc_not_CFO","FX_dropped","source_bal","source_profit","source_hash","prior_audited_equity","minority_sign","other_assets","unverified_period")
 for name in cases:
  s,f=deepcopy(a),deepcopy(d)
  if name=="cash_interest_not_CFO":f["items"][0]["operating_cash_flow"]=6286794
  elif name=="cash_before_wc_not_CFO":f["items"][0]["operating_cash_flow"]=1870090
  elif name=="FX_dropped":f["items"][0]["cashflow_fx"]=0
  elif name=="source_bal":s["B02a_current"]["total_assets"]+=1
  elif name=="source_profit":s["B03a_Q1"]["net_profit"]+=1
  elif name=="source_hash":s["original"]["sha256"]="0"*64
  elif name=="prior_audited_equity":s["B02a_prior_audited_comparative_only"]["total_equity"]+=1942
  elif name=="minority_sign":s["B03a_Q1"]["noncontrolling_profit"]=1
  elif name=="other_assets":f["items"][0]["bank_other_assets"]=5590919
  elif name=="unverified_period":f["items"][1]["verification_status"]="forged_completed"
  try:verify(s,f)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Corruption not caught "+name)
 print(f"PASS TPB Q1/2025 original signed 54 pages B02a B03a B04a, {n} exact accounting/FX identities, 50 source fields and {len(cases)} negative corruption cases.")
 print("PASS TPB actual CFO -41,476,406; interest received +6,286,794 NOT CFO, preWC +1,870,090 NOT CFO.")
 print("PASS cash bridge opening 86,148,639 + net -41,578,162 + exchange +210,436 = closing 44,780,913 million VND; no 2024 reporting periods.")
if __name__=="__main__":main()
