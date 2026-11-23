#!/usr/bin/env python3
"""Verify STB 2025Q1 original 47-page consolidated scanned issuer bank source.
Reject false positive OCR, CFO/pre-working-capital confusion, 2024 dashboard and
incorrect FX treatment; retain signed 2025Q1 immutable after merge.
"""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/STB-2025Q1-original-signed-bank-million-vnd.json"
DATA=ROOT/"data/financials-STB.json"
STATUS="issuer_signed_STB_2025Q1_original_B02a_B03a_B04a_FX_cash_verified"
DIGEST="d69ecb46b8b488f4a596db04640b2a0553700ae29e50675d3554a599d47f2cd0"
def verify(a,d):
 assert (a["symbol"],a["period"],a["unit"],a["scope"])==("STB","2025-Q1","triệu VND","consolidated")
 assert a["source"]["sha256"]==DIGEST and a["source"]["bytes"]==10950303
 assert a["source"]["pages"]==47 and a["source"]["source_workflow_run"]==45263488979
 assert a["source"]["source_pdf_pages"]=={"B02a":[2,3],"B03a":[4],"B04a":[5,6]}
 assert a["source"]["scan_ocr"] and a["source"]["original_issuer_document"]
 b,p,c=a["B02a"],a["B03a"],a["B04a"]
 def sm(obj,keys):return sum(obj[k] for k in keys)
 E={}
 E["balance_assets"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities",
 "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
 "longterm_investments","fixed_assets","investment_property","other_assets"))-b["total_assets"]
 E["balance_liabilities"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
 "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["balance_equity"]=sm(b,("capital","reserves","fx_reserve","retained"))-b["total_equity"]
 E["balance_equation"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["profit_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["profit_services"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["profit_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["profit_operating"]=sm(p,("net_interest","services_net","FX_net","trading_net","invest_net",
 "other_net","contribution_income"))-p["operating_income"]
 E["profit_pre_provision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["profit_pre_tax"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["profit_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["profit_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["profit_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["cash_pre_working_capital"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash",
 "fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["cash_true_CFO"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities","assets_derivatives",
 "assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank",
 "liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives",
 "liabs_other","payments_from_bank_reserves"))-c["CFO"]
 E["cash_CFI"]=c["capex"]+c["asset_disposals"]-c["CFI"]
 E["cash_CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
 E["cash_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["cash_FX_bridge"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 assert len(E)==19 and all(v==0 for v in E.values()),E
 assert len(a["source_identity_residuals"])==19 and all(v==0 for v in a["source_identity_residuals"].values())
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(757093326,699230949,57862377)
 assert (p["operating_income"],p["operating_expenses"],p["before_provision"],p["credit_provision"],
  p["pretax_profit"],p["net_profit"],p["parent_profit"])==(7796440,3927147,3869293,195263,3674030,2896692,2896692)
 assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"],
  c["opening_cash"],c["closing_cash"])==(2196830,-4502482,-106676,-1638284,-6247442,-10387,106493055,100235226)
 assert len(d["items"])==6 and [v["period"] for v in d["items"]]==[
  "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=d["items"][0];sv=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert sv["original_pdf_sha256"]==DIGEST and sv["original_pdf_hash_verified"]
 assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["original_source_run"]==45263488979
 assert sv["cash_FX_effect_included"] and sv["no_2024_dashboard_periods"]
 assert sv["source_cfo_after_working_capital_verified"]
 mappings={
 "total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],
 "equity":b["total_equity"],"revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],
 "net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
 "bank_interest_income":p["interest_income"],"bank_interest_expense":p["interest_expense"],
 "bank_net_interest_income":p["net_interest"],"bank_net_service_income":p["services_net"],
 "bank_operating_expenses":p["operating_expenses"],"bank_pre_provision_operating_profit":p["before_provision"],
 "bank_provision_expense":p["credit_provision"],"income_tax":p["income_tax"],
 "bank_dividend_and_capital_income":0,
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],
 "financing_cash_flow":c["CFF"],"net_cash_change":c["net_cash_change"],
 "cashflow_fx":c["FX_effect"],"cash_beginning":c["opening_cash"],"cash_ending":c["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
 "capital_expenditure":c["capex"],"capital_expenditure_ytd":c["capex"]}
 for k,v in mappings.items():assert row[k]==v,(k,row.get(k),v)
 for prefix,values in (("b02a",b),("b03a",p),("b04a",c)):
  for k,v in values.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 opening=a["prior_2024_opening_B02a"]
 assert row["roa"]==round(400*p["net_profit"]/((opening["assets"]+b["total_assets"])/2),2)==1.54
 assert row["roe"]==round(400*p["net_profit"]/((opening["equity"]+b["total_equity"])/2),2)==20.54
 assert row["eps"] is None and row["eps_ytd"] is None
 assert "5767" in row["eps_basis"].replace(",","") or "5,767" in row["eps_basis"]
 assert all(v["verification_status"]!=STATUS for v in d["items"][1:])
 assert all(not v["period"].startswith("2024") for v in d["items"])
 return len(E),len(mappings)
def main():
 a=json.loads(LEDGER.read_text("utf8"));d=json.loads(DATA.read_text("utf8"))
 n,m=verify(a,d)
 cases=("asset","liability","equity","profit","income","service","provision","PAT","source_forgery",
 "incorrect_CFO_preWC","CFO","CFI","CFF","cash_net","cash_open","cash_close","FX_missing",
 "FX_forgery","bank_cash_negative_sign","bank_dividend_old_OCR","quarter_not_verified",
 "eps_unverified","2024_dashboard","tampered_original_B04")
 for kind in cases:
  aa,dd=copy.deepcopy(a),copy.deepcopy(d)
  if kind=="asset":aa["B02a"]["total_assets"]+=1
  elif kind=="liability":dd["items"][0]["total_liabilities"]+=1
  elif kind=="equity":dd["items"][0]["equity"]+=1
  elif kind=="profit":aa["B03a"]["operating_income"]+=1
  elif kind=="income":dd["items"][0]["revenue"]+=1
  elif kind=="service":aa["B03a"]["services_net"]+=1
  elif kind=="provision":aa["B03a"]["credit_provision"]+=1
  elif kind=="PAT":dd["items"][0]["net_profit"]+=1
  elif kind=="source_forgery":aa["source"]["sha256"]="0"*64
  elif kind=="incorrect_CFO_preWC":dd["items"][0]["operating_cash_flow"]=2196830
  elif kind=="CFO":aa["B04a"]["CFO"]+=1
  elif kind=="CFI":aa["B04a"]["CFI"]+=1
  elif kind=="CFF":dd["items"][0]["financing_cash_flow"]+=1
  elif kind=="cash_net":aa["B04a"]["net_cash_change"]+=1
  elif kind=="cash_open":dd["items"][0]["cash_beginning"]+=1
  elif kind=="cash_close":dd["items"][0]["cash_ending"]+=1
  elif kind=="FX_missing":dd["items"][0]["cashflow_fx"]=0
  elif kind=="FX_forgery":aa["B04a"]["FX_effect"]+=1
  elif kind=="bank_cash_negative_sign":dd["items"][0]["operating_cash_flow"]=-dd["items"][0]["operating_cash_flow"]
  elif kind=="bank_dividend_old_OCR":dd["items"][0]["bank_dividend_and_capital_income"]=18
  elif kind=="quarter_not_verified":dd["items"][0]["verification_status"]="auto_extracted_pending_visual_review"
  elif kind=="eps_unverified":dd["items"][0]["eps"]=5767
  elif kind=="2024_dashboard":dd["items"].append({"period":"2024-Q4"})
  elif kind=="tampered_original_B04":dd["items"][0]["signed_source_b04a_pre_wc_cash"]+=1
  try:verify(aa,dd)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("STB signed original Q1 tamper escaped: "+kind)
 print(f"PASS STB 2025Q1 47p original signed consolidated bank: {n} exact identities, {m} primary normalized mappings, {len(cases)} negative tamper cases")
 print("PASS bank cash CFO -4502482 CFI -106676 CFF -1638284 net -6247442 FX -10387 opening 106493055 closing 100235226; Q1 ROA 1.54% ROE 20.54%")
 print("PASS 2025Q1 source EPS source 5767 flagged for review instead of silently overriding dashboard")
if __name__=="__main__":main()
