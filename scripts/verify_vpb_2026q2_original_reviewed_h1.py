#!/usr/bin/env python3
"""VPB 2026Q2 original B02/B03, reviewed H1 B04 and Q1-signed quarter cash."""
import json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"reports/source-audits/VPB-2026Q2-original-and-H1-bank-million-vnd.json"
F=ROOT/"data/financials-VPB.json"
Q1=ROOT/"reports/source-audits/VPB-2026Q1-issuer-original-B02a-B03a-B04a-million-vnd.json"
STATUS="issuer_signed_VPB_2026Q2_original_B02a_B03a_reviewed_H1_minus_Q1_B04a_verified"
def check(a,f,q1):
 b,p,c,old,q=(a[k] for k in ("B02a","B03a_Q2_direct","B04a_6M_reviewed","B04a_6M_original","B04a_Q2_reviewed_H1_less_signed_Q1"))
 def ss(x,ks):return sum(x[k] for k in ks)
 E={}
 E["B02_assets"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liab"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["B02_equity"]=ss(b,("capital","funds","retained","minority"))-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["B03_operating"]=ss(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["B03_profit"]=p["operating_income"]-p["operating_expenses"]-p["credit_provision"]-p["pretax_profit"]
 E["B03_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["B03_parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 for label,v in (("orig",old),("reviewed",c)):
  E[label+"_preWC"]=ss(v,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-v["pre_wc_cash"]
  E[label+"_CFO"]=v["pre_wc_cash"]+ss(v,("assets_interbank","assets_securities","assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other"))-v["CFO"]
  E[label+"_CFI"]=ss(v,("capex","asset_disposals","investments_in_subsidiaries","investment_distributions"))-v["CFI"]
  E[label+"_CFF"]=v["share_proceeds"]+v["dividends"]-v["CFF"]
  E[label+"_net"]=v["CFO"]+v["CFI"]+v["CFF"]-v["net_cash_change"]
  E[label+"_cash"]=v["opening_cash"]+v["net_cash_change"]-v["closing_cash"]
 E["vintage_CFO"]=c["CFO"]-old["CFO"]-84346
 E["vintage_CFI"]=c["CFI"]-old["CFI"]+84346
 E["vintage_net"]=c["net_cash_change"]-old["net_cash_change"]
 prev=q1["B04a"]
 for k in ("CFO","CFI","CFF","net_cash_change"):
  E["Q2_"+k]=c[k]-prev[k]-q[k]
 E["Q2_open"]=prev["closing_cash"]-q["opening_cash"]
 E["Q2_close"]=c["closing_cash"]-q["closing_cash"]
 E["Q2_FX"]=q["FX_effect"]-c["FX_effect"]
 E["Q2_net"]=q["CFO"]+q["CFI"]+q["CFF"]+q["FX_effect"]-q["net_cash_change"]
 E["Q2_cash"]=q["opening_cash"]+q["net_cash_change"]-q["closing_cash"]
 assert not any(E.values()),E
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(1502526376,1311311032,191215344)
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"],p["parent_profit"])==(23483634,10959179,8775909,8384630)
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"])==(12148763,-1233631,-3965367,6949765)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["opening_cash"],q["closing_cash"])==(3065,-1215629,-3965367,-5177931,208224915,203046984)
 assert f["items"][4]["verification_status"]=="issuer_signed_VPB_2026Q1_original_B02a_B03a_B04a_true_CFO_verified"
 assert f["items"][5]["verification_status"]==STATUS and f["items"][6]["verification_status"]=="issuer_signed_VPB_2026Q3_original_B02a_B03a_9M_minus_reviewed_H1_B04a_verified"
 row=f["items"][5];sv=row["source_validation"]
 assert sv["original_zip_sha256"]==a["sources"]["archive_sha256"]
 assert sv["reviewed_H1_pdf_sha256"]==a["sources"]["reviewed_H1_sha256"]
 assert sv["reviewed_H1_CFO_CFI_84346_reclassification_verified"]
 assert sv["source_audit_ledger"]==str(A.relative_to(ROOT))
 for k,v in {"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],"revenue":p["operating_income"],"net_profit":p["net_profit"],"pretax_profit":p["pretax_profit"],"operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],"net_cash_change":q["net_cash_change"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],"operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],"eps_ytd":1838}.items(): assert row[k]==v,(k,row.get(k),v)
 assert row["eps"] is None
 assert row["roa"]==2.44 and row["roe"]==18.58
 assert not any(x["period"].startswith("2024") for x in f["items"])
 return len(E)
def main():
 a=json.loads(A.read_text("utf8"));f=json.loads(F.read_text("utf8"));q1=json.loads(Q1.read_text("utf8"))
 n=check(a,f,q1)
 for name in ("balance","income","source_CFO","reviewed_CFO","reviewed_CFI","Q2_CFO","Q2_CFI","Q2_close","fake_fx","Q1_corrupt","Q3_premature","extra_2024"):
  aa,ff,pp=copy.deepcopy(a),copy.deepcopy(f),copy.deepcopy(q1)
  if name=="balance":aa["B02a"]["total_assets"]+=1
  elif name=="income":aa["B03a_Q2_direct"]["net_profit"]+=1
  elif name=="source_CFO":aa["B04a_6M_original"]["CFO"]+=1
  elif name=="reviewed_CFO":aa["B04a_6M_reviewed"]["CFO"]+=1
  elif name=="reviewed_CFI":aa["B04a_6M_reviewed"]["CFI"]+=1
  elif name=="Q2_CFO":ff["items"][5]["operating_cash_flow"]=28080406
  elif name=="Q2_CFI":ff["items"][5]["investing_cash_flow"]+=1
  elif name=="Q2_close":ff["items"][5]["cash_ending"]+=1
  elif name=="fake_fx":aa["B04a_Q2_reviewed_H1_less_signed_Q1"]["FX_effect"]=100
  elif name=="Q1_corrupt":pp["B04a"]["CFO"]+=1
  elif name=="Q3_premature":ff["items"][6]["verification_status"]="tampered"
  elif name=="extra_2024":ff["items"].append({"period":"2024-Q4"})
  try:check(aa,ff,pp)
  except (AssertionError,KeyError,IndexError,TypeError):pass
  else:raise AssertionError("Q2 tamper missed "+name)
 print(f"PASS VPB 2026Q2 signed original B02/B03 and reviewed H1 bank B04: {n} exact identities, 12 negative tamper tests. Reviewed H1 CFO +84,346 CFI -84,346 versus first-issued; Q2 CFO +3,065 CFI -1,215,629 CFF -3,965,367.")
if __name__=="__main__":main()
