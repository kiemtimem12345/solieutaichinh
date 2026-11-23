#!/usr/bin/env python3
"""Exact source and source-vintage validation for STB Q2 2025, signed original vs KPMG-reviewed H1.
True quarterly bank B04 = KPMG reviewed 6M - verified Q1 (FX-aware). Prevent false pre-WC CFO.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"reports/source-audits/STB-2025Q2-original-KPMG-reviewed-H1-million-vnd.json"
Q1FILE=ROOT/"reports/source-audits/STB-2025Q1-original-signed-bank-million-vnd.json"
PROD=ROOT/"data/financials-STB.json"
STATUS="issuer_signed_STB_2025Q2_original_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_verified"
ZIP="7260dccced5ae737046bf19a297a2416194ad7335b518226e631d26aa9646656"
KPMG="244de4c8a97ada2e086b27ac78484265b825d4cde9cbfcaebbda62ec3e4b3833"
def verify(a,prev,d):
 assert (a["symbol"],a["period"],a["unit"],a["scope"])==("STB","2025-Q2","triệu VND","consolidated")
 src=a["source"]
 assert (src["original_Q2"]["sha256"],src["original_Q2"]["bytes"],src["original_Q2"]["pages"])==(ZIP,27665099,48)
 assert (src["KPMG_H1_reviewed"]["sha256"],src["KPMG_H1_reviewed"]["bytes"],src["KPMG_H1_reviewed"]["pages"])==(KPMG,27878327,104)
 assert src["source_recovery_run"]==45264566289 and src["source_reviewed_focused_run"]==45265036958
 b,p,c,orig,q=(a[k] for k in ("B02a_reviewed_H1","B03a_Q2_direct","B04a_6M_KPMG_reviewed","B04a_6M_original","B04a_Q2_KPMG_H1_minus_Q1"))
 q1=prev["B04a"]
 def ss(o,keys):return sum(o[k] for k in keys)
 E={}
 E["assets"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
 "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets",
 "investment_property","other_assets"))-b["total_assets"]
 E["liabs"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs",
 "valuable_papers","other_liabs"))-b["total_liabilities"]
 E["equity"]=ss(b,("capital","reserves","fx_reserve","retained","minority"))-b["total_equity"]
 E["balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["operating"]=ss(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["preprov"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["pretax"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 for name,h in (("ORIG",orig),("KPMG",c)):
  E[name+"_preWC"]=ss(h,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
  "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-h["pre_wc_cash"]
  E[name+"_CFO"]=h["pre_wc_cash"]+ss(h,("assets_interbank","assets_securities","assets_derivatives",
  "assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank",
  "liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other",
  "payments_from_bank_reserves"))-h["CFO"]
  E[name+"_CFI"]=ss(h,("capex","asset_disposals","investment_distributions"))-h["CFI"]
  E[name+"_CFF"]=ss(h,("financing_bonds_issued","financing_bonds_repaid"))-h["CFF"]
  E[name+"_net"]=h["CFO"]+h["CFI"]+h["CFF"]-h["net_cash_change"]
  E[name+"_FX_close"]=h["opening_cash"]+h["net_cash_change"]+h["FX_effect"]-h["closing_cash"]
 E["vintage_CFO"]=c["CFO"]-orig["CFO"]+1
 E["vintage_net"]=c["net_cash_change"]-orig["net_cash_change"]+1
 E["vintage_FX"]=c["FX_effect"]-orig["FX_effect"]-1
 E["vintage_CFI"]=c["CFI"]-orig["CFI"]
 E["vintage_CFF"]=c["CFF"]-orig["CFF"]
 E["vintage_cash_end"]=c["closing_cash"]-orig["closing_cash"]
 for k in ("CFO","CFI","CFF","net_cash_change","FX_effect","capex"):
  E["Q2_"+k]=c[k]-q1[k]-q[k]
 E["Q2_open"]=q1["closing_cash"]-q["opening_cash"]
 E["Q2_end"]=c["closing_cash"]-q["closing_cash"]
 E["Q2_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["Q2_FX_cash"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 assert len(E)>=40 and all(x==0 for x in E.values()),E
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(807339224,747518017,59821207)
 assert (p["operating_income"],p["operating_expenses"],p["before_provision"],p["credit_provision"],
 p["pretax_profit"],p["net_profit"])==(7769380,3199817,4569563,912321,3657242,2893598)
 assert (orig["CFO"],orig["CFI"],orig["CFF"],orig["net_cash_change"],orig["FX_effect"])==(22993305,-295309,-3885533,18812463,184938)
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"],c["closing_cash"])==(22993304,-295309,-3885533,18812462,184939,125490456)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["FX_effect"],q["opening_cash"],q["closing_cash"])==(27495786,-188633,-2247249,25059904,195326,100235226,125490456)
 assert prev["source"]["sha256"]=="d69ecb46b8b488f4a596db04640b2a0553700ae29e50675d3554a599d47f2cd0"
 assert len(d["items"])==6 and [x["period"] for x in d["items"]]==[
 "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 assert d["items"][0]["verification_status"]=="issuer_signed_STB_2025Q1_original_B02a_B03a_B04a_FX_cash_verified"
 assert [x["verification_status"] for x in d["items"]][1:]==[
 STATUS,"issuer_signed_STB_2025Q3_original_B02a_B03a_9M_minus_KPMG_H1_B04a_FX_tolerance_verified","issuer_signed_STB_2025Q4_original_B02a_B03a_KPMG_FY_minus_9M_B04a_FX_verified",
 "auto_extracted_pending_visual_review","manual_review_required_pending_extraction"]
 row=d["items"][1];sv=row["source_validation"]
 assert sv["original_pdf_sha256"]==ZIP and sv["KPMG_reviewed_H1_pdf_sha256"]==KPMG
 assert sv["original_pdf_hash_verified"] and sv["reviewed_6M_minus_signed_Q1_cash_FX_exact"]
 assert sv["reviewed_H1_CFO_original_vintage_difference_minus_one"] and sv["reviewed_H1_FX_original_vintage_difference_plus_one"]
 assert sv["source_audit_ledger"]==str(FILE.relative_to(ROOT))
 mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
 "net_profit_attributable":p["parent_profit"],"bank_operating_expenses":p["operating_expenses"],
 "bank_pre_provision_operating_profit":p["before_provision"],"bank_provision_expense":p["credit_provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net_cash_change"],"cashflow_fx":q["FX_effect"],"cash_beginning":q["opening_cash"],
 "cash_ending":q["closing_cash"],"operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],"cashflow_fx_ytd":c["FX_effect"]}
 for k,v in mapped.items():assert row[k]==v,(k,row.get(k),v)
 for prefix,vals in (("b02a",b),("b03a",p),("b04a_KPMG_H1",c)):
  for k,v in vals.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["eps"] is None and row["eps_ytd"] is None
 assert row["roa"]==1.48 and row["roe"]==19.67
 assert not any(row["period"].startswith("2024") for row in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(FILE.read_text("utf8"));prior=json.loads(Q1FILE.read_text("utf8"));d=json.loads(PROD.read_text("utf8"))
 n,m=verify(a,prior,d)
 cases=("asset","liabs","equity","profit","original_PBT","CFO_preWC","source_original_CFO","KPMG_CFO",
 "KPMG_CFI","original_FX","KPMG_FX","quarter_CFO","quarter_CFI","quarter_CFF","quarter_FX",
 "quarter_net","cash_start","cash_end","source_sha","KPMG_sha","Q1_cash","Q1_status",
 "future_Q3_unverified","EPS_original_not_quarter","2024_added")
 for kind in cases:
  aa,pp,dd=copy.deepcopy(a),copy.deepcopy(prior),copy.deepcopy(d)
  if kind=="asset":aa["B02a_reviewed_H1"]["total_assets"]+=1
  elif kind=="liabs":dd["items"][1]["total_liabilities"]+=1
  elif kind=="equity":dd["items"][1]["equity"]+=1
  elif kind=="profit":aa["B03a_Q2_direct"]["pretax_profit"]+=1
  elif kind=="original_PBT":dd["items"][1]["pretax_profit"]+=1
  elif kind=="CFO_preWC":dd["items"][1]["operating_cash_flow"]=7716558
  elif kind=="source_original_CFO":aa["B04a_6M_original"]["CFO"]+=1
  elif kind=="KPMG_CFO":aa["B04a_6M_KPMG_reviewed"]["CFO"]+=1
  elif kind=="KPMG_CFI":aa["B04a_6M_KPMG_reviewed"]["CFI"]+=1
  elif kind=="original_FX":aa["B04a_6M_original"]["FX_effect"]+=1
  elif kind=="KPMG_FX":aa["B04a_6M_KPMG_reviewed"]["FX_effect"]+=1
  elif kind=="quarter_CFO":dd["items"][1]["operating_cash_flow"]=22993304
  elif kind=="quarter_CFI":dd["items"][1]["investing_cash_flow"]+=1
  elif kind=="quarter_CFF":dd["items"][1]["financing_cash_flow"]+=1
  elif kind=="quarter_FX":aa["B04a_Q2_KPMG_H1_minus_Q1"]["FX_effect"]+=1
  elif kind=="quarter_net":aa["B04a_Q2_KPMG_H1_minus_Q1"]["net_cash_change"]+=1
  elif kind=="cash_start":dd["items"][1]["cash_beginning"]+=1
  elif kind=="cash_end":dd["items"][1]["cash_ending"]+=1
  elif kind=="source_sha":aa["source"]["original_Q2"]["sha256"]="0"*64
  elif kind=="KPMG_sha":aa["source"]["KPMG_H1_reviewed"]["sha256"]="0"*64
  elif kind=="Q1_cash":pp["B04a"]["CFO"]+=1
  elif kind=="Q1_status":dd["items"][0]["verification_status"]="tampered"
  elif kind=="future_Q3_unverified":dd["items"][2]["verification_status"]="tampered"
  elif kind=="EPS_original_not_quarter":dd["items"][1]["eps"]=6148
  elif kind=="2024_added":dd["items"].append({"period":"2024-Q4"})
  try:verify(aa,pp,dd)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("STB signed Q2 source corruption escaped: "+kind)
 print(f"PASS STB 2025Q2 first-issued signed original and KPMG reviewed H1: {n} zero identities, {m} normalized mappings, {len(cases)} negative tamper cases")
 print("PASS reviewed H1 CFO 22,993,304 CFI -295,309 CFF -3,885,533 and FX +184,939; Q2 CFO +27,495,786 CFI -188,633 CFF -2,247,249 FX +195,326 cash 100,235,226 -> 125,490,456")
if __name__=="__main__":main()
