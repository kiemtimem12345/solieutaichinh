#!/usr/bin/env python3
"""VPB Q1 2025 signed bank B02a/B03a/B04a and OCR-correction fail-closed QA.

Original B04a CFO +8,550,806, CFI -55,847, financing CFF ZERO;
net cash +8,494,959 and opening 143,002,784. The old OCR record wrongly
stored opening 443,002,784 and treated net cash as CFF.
"""
from pathlib import Path
from copy import deepcopy
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/VPB-2025Q1-original-signed-B02a-B03a-B04a-million-vnd.json"
DATA=ROOT/"data/financials-VPB.json"
STATUS="issuer_signed_VPB_2025Q1_consolidated_B02a_B03a_B04a_cash_opening_corrected_verified"

def verify(a,fin):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("VPB","2025-Q1","consolidated","triệu VND")
 src=a["source"]
 assert src["sha256"]=="630674877ce105137563dc6cf8f6a968bdc7c2739cd2a24fc3661c9ee4a3466f"
 assert src["bytes"]==4361092 and src["pages"]==94
 assert src["B02a_pages"]==[5,6] and src["B03a_page"]==8 and src["B04a_pages"]==[9,10]
 assert src["source_run"]==45243274388
 b,p,c=a["B02a"],a["B03a"],a["B04a"]
 prior=a["B02a_prior_2024FY_comparison_only"]
 assert prior=={"assets":923847637,"equity":147275262,"liabilities":776572375}
 E={}
 def total(obj, keys):return sum(obj[k] for k in keys)
 E["B02_asset"]=total(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities",
 "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
 "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liab"]=total(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
 "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["B02_equity"]=total(b,("capital","funds","retained","minority"))-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B02_prior_balance"]=prior["assets"]-prior["liabilities"]-prior["equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["B03_operating"]=total(p,("net_interest","services_net","FX_net","trading_net",
 "invest_net","other_net","contribution_income"))-p["operating_income"]
 E["B03_before_provision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["B03_PBT"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["B03_income_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["B04_pre_wc"]=total(c,("interest_cash_received","interest_cash_paid",
 "services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash",
 "staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["B04_real_CFO"]=c["pre_wc_cash"]+total(c,("assets_interbank","assets_securities",
 "assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other",
 "liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers",
 "liabs_trust","liabs_derivatives","liabs_other"))-c["CFO"]
 E["B04_CFI"]=c["capex"]+c["asset_disposals"]-c["CFI"]
 E["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["B04_cash"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 assert len(E)==19 and all(x==0 for x in E.values()),E
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"])==(8550806,-55847,0,8494959)
 assert (c["opening_cash"],c["FX_effect"],c["closing_cash"])==(143002784,0,151497743)
 assert c["pre_wc_cash"]==10147577 and c["interest_cash_received"]==21247343
 assert c["CFO"]!=c["pre_wc_cash"] and c["CFO"]!=c["interest_cash_received"]
 assert c["opening_cash"]!=443002784 and c["CFF"]!=8494959
 assert fin["symbol"]=="VPB" and [r["period"] for r in fin["items"]]==[
 "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 row=fin["items"][0];sv=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert sv["original_pdf_sha256"]==src["sha256"] and sv["original_pdf_hash_verified"]
 assert sv["original_pdf_pages"]==94 and sv["manually_visual_reviewed"]
 assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["original_B02a_B03a_B04a_pages"]==[5,6,8,9,10]
 assert sv["cash_opening_original_143002784_true"] and sv["prior_OCR_cash_opening_443002784_false"]
 assert sv["CFF_no_line_and_zero"] and sv["no_FX_line_and_cash_exact"]
 assert sv["prior_OCR_financing_cashflow_8494959_is_actual_net_cash_change"]
 assert sv["prior_2024FY_only_in_source_comparative"] and sv["no_2024_dashboard_periods"]
 assert sv["legacy_ocr_values_rejected"]["cash_beginning"]==443002784
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"]
 assert row["equity"]==b["total_equity"] and row["revenue"]==p["operating_income"]
 assert row["pretax_profit"]==p["pretax_profit"] and row["net_profit"]==p["net_profit"]
 assert row["net_profit_attributable"]==p["parent_profit"]
 mapped={
 "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],
 "equity":b["total_equity"],"revenue":p["operating_income"],
 "net_profit":p["net_profit"],"pretax_profit":p["pretax_profit"],
 "net_profit_attributable":p["parent_profit"],
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],
 "financing_cash_flow":c["CFF"],"net_cash_change":c["net_cash_change"],
 "cash_beginning":c["opening_cash"],"cash_ending":c["closing_cash"],"cashflow_fx":c["FX_effect"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
 "cashflow_fx_ytd":c["FX_effect"],
 "cash_beginning_reported_ytd":c["opening_cash"],"cash_ending_ytd":c["closing_cash"],
 "bank_cash_on_hand":b["cash_vault"],"bank_customer_loans":b["customer_loans_net"],
 "bank_customer_deposits":b["customer_deposits"],
 "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
 "bank_non_controlling_profit":p["noncontrolling_profit"],
 "income_tax":p["income_tax"],"capital_expenditure":c["capex"],
 "capital_expenditure_ytd":c["capex"]
 }
 for k,v in mapped.items():assert row[k]==v,(k,row[k],v)
 assert len(row["financial_line_items_manually_verified_fields"])==55
 for prefix,raw in (("b02a",b),("b03a",p),("b04a",c)):
  for k,v in raw.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["roa"]==round(400*p["net_profit"]/((prior["assets"]+b["total_assets"])/2),2)==1.64
 assert row["roe"]==round(400*p["net_profit"]/((prior["equity"]+b["total_equity"])/2),2)==10.55
 assert [x["verification_status"] for x in fin["items"][1:]]==[
  "issuer_signed_VPB_2025Q2_original_B02a_B03a_reviewed_H1_minus_Q1_bank_B04a_verified","auto_extracted_pending_visual_review",
  "auto_extracted_pending_visual_review","manual_review_required_pending_extraction",
  "manual_review_required_pending_extraction","auto_extracted_pending_visual_review"]
 assert all(not x["period"].startswith("2024") for x in fin["items"])
 return len(E)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 f=json.loads(DATA.read_text("utf-8"))
 n=verify(a,f)
 cases=("assets","PBT","PAT","CFO","CFF_is_net","wrong_opening",
        "cash_end","FX_forged","source_hash","ratio","later_Q2_status",
        "2024_added","pre_WC_as_CFO","wrong_source_fx")
 for kind in cases:
  aa,ff=deepcopy(a),deepcopy(f)
  if kind=="assets":aa["B02a"]["total_assets"]+=1
  elif kind=="PBT":aa["B03a"]["pretax_profit"]+=1
  elif kind=="PAT":ff["items"][0]["net_profit"]+=1
  elif kind=="CFO":aa["B04a"]["CFO"]+=1
  elif kind=="CFF_is_net":ff["items"][0]["financing_cash_flow"]=8494959
  elif kind=="wrong_opening":ff["items"][0]["cash_beginning"]=443002784
  elif kind=="cash_end":ff["items"][0]["cash_ending"]+=1
  elif kind=="FX_forged":ff["items"][0]["cashflow_fx"]=500
  elif kind=="source_hash":aa["source"]["sha256"]="0"*64
  elif kind=="ratio":ff["items"][0]["roe"]=0
  elif kind=="later_Q2_status":ff["items"][1]["verification_status"]="false_completed"
  elif kind=="2024_added":ff["items"].append({"period":"2024-Q4"})
  elif kind=="pre_WC_as_CFO":ff["items"][0]["operating_cash_flow"]=10147577
  elif kind=="wrong_source_fx":aa["B04a"]["FX_effect"]=500
  try:verify(aa,ff)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("VPB source tamper not blocked: "+kind)
 print(f"PASS VPB 2025Q1 issuer original 94p signed B02a B03a B04a, {n} exact accounting/cash identities, 55 verified normalized fields, {len(cases)} tamper controls.")
 print("PASS CFO +8,550,806 CFI -55,847 CFF 0 net +8,494,959, actual opening cash 143,002,784, closing 151,497,743 million VND; original OCR opening 443,002,784 rejected.")
 print("PASS VPB Q1/2025 ROA 1.64% ROE 10.55%; Q2 separately source-verified while Q1 unchanged, later VPB five periods stay provisional and no 2024 period added.")
if __name__=="__main__":main()
