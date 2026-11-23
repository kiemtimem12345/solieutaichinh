#!/usr/bin/env python3
"""VPB 2026Q3 signed 9M issuer B02 B03 B04 and independently reviewed H1 quarterly bank cash."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1]
A=R/"reports/source-audits/VPB-2026Q3-original-9M-reviewedH1-bank-million-vnd.json"
H1=R/"reports/source-audits/VPB-2026Q2-original-and-H1-bank-million-vnd.json"
F=R/"data/financials-VPB.json"
STATUS="issuer_signed_VPB_2026Q3_original_B02a_B03a_9M_minus_reviewed_H1_B04a_verified"
def check(a,h1,f):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("VPB","2026-Q3","consolidated","triệu VND")
 s=a["sources"]
 assert (s["archive_sha256"],s["original_signed_pdf_sha256"],s["lookup_pdf_sha256"],s["source_run"])==(
 "99a59d7b4f87ab28292eedd9797a31a83f9caab324c5a3bd0cb0544f72e5cdd5",
 "026ad3ab3f672bd44ec3af074ce080795199f1e506720feabefb8cb1af290fda",
 "6e3d63a04332123a26310e24884a24244accc45c6b2f146917e67b2673e9eeff",45255183223)
 b,p,c,q=a["B02a"],a["B03a_Q3_direct"],a["B04a_9M_original"],a["B04a_Q3_9M_less_reviewed_H1"]
 h=a["B04a_reviewed_H1"]
 assert h==h1["B04a_6M_reviewed"]
 def ss(o,keys):return sum(o[k] for k in keys)
 e={}
 e["asset"]=ss(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 e["liab"]=ss(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 e["equity"]=ss(b,("capital","funds","retained","minority"))-b["total_equity"]
 e["balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 e["interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 e["service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 e["other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 e["operating"]=ss(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 e["preprovision"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 e["PBT"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 e["tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 e["PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 e["parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 e["B04_preWC"]=ss(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 e["B04_CFO"]=c["pre_wc_cash"]+ss(c,("assets_interbank","assets_securities","assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other"))-c["CFO"]
 e["B04_CFI"]=ss(c,("capex","asset_disposals","investments_in_subsidiaries","investment_distributions"))-c["CFI"]
 e["B04_CFF"]=c["share_proceeds"]+c["dividends"]-c["CFF"]
 e["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 e["B04_cash"]=c["opening_cash"]+c["net_cash_change"]-c["closing_cash"]
 for k in ("CFO","CFI","CFF","FX_effect","net_cash_change"):
  e["Q3_"+k]=c[k]-h[k]-q[k]
 e["Q3_start"]=h["closing_cash"]-q["opening_cash"]
 e["Q3_end"]=c["closing_cash"]-q["closing_cash"]
 e["Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]+q["FX_effect"]-q["net_cash_change"]
 e["Q3_cash"]=q["opening_cash"]+q["net_cash_change"]-q["closing_cash"]
 assert not any(e.values()),e
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(1610786686,1410708432,200078254)
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"],p["parent_profit"])==(22083615,11030887,8862910,8643626)
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["closing_cash"])==(46180388,-11841627,-3965367,30373394,226470613)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["opening_cash"],q["closing_cash"])==(34031625,-10607996,0,23423629,203046984,226470613)
 assert len(f["items"])==7 and [r["period"] for r in f["items"]]==[
 "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(r["verification_status"].startswith("issuer_signed_VPB_") for r in f["items"])
 row=f["items"][6];sv=row["source_validation"]
 assert row["verification_status"]==STATUS
 assert sv["original_zip_sha256"]==s["archive_sha256"]
 assert sv["original_pdf_sha256"]==s["original_signed_pdf_sha256"]
 assert sv["source_audit_ledger"]==str(A.relative_to(R))
 assert sv["signed_9M_minus_reviewed_H1_cash_exact"] and sv["reviewed_H1_CFO_CFI_reclass_84346_retained"]
 for k,v in {"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
 "net_profit_attributable":p["parent_profit"],"operating_cash_flow":q["CFO"],
 "investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net_cash_change"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"eps_ytd":2323}.items():assert row[k]==v,(k,row.get(k),v)
 for prefix,values in (("b02a",b),("b03a",p),("b04a_9m",c)):
  for k,v in values.items():assert row["signed_source_"+prefix+"_"+k]==v
 assert row["eps"] is None and row["roa"]==2.28 and row["roe"]==18.12
 assert not any(r["period"].startswith("2024") for r in f["items"])
 return len(e)
def main():
 a=json.loads(A.read_text("utf8"));h=json.loads(H1.read_text("utf8"));f=json.loads(F.read_text("utf8"))
 n=check(a,h,f)
 cases=("asset","PBT","PAT","source_CFO","reviewed_H1","Q3_CFO","Q3_CFI","Q3_net","fake_FX","cash_end","Q3_status","source_SHA","prior_Q2","2024")
 for kind in cases:
  aa,hh,ff=copy.deepcopy(a),copy.deepcopy(h),copy.deepcopy(f)
  if kind=="asset":aa["B02a"]["total_assets"]+=1
  elif kind=="PBT":aa["B03a_Q3_direct"]["pretax_profit"]+=1
  elif kind=="PAT":ff["items"][6]["net_profit"]+=1
  elif kind=="source_CFO":aa["B04a_9M_original"]["CFO"]+=1
  elif kind=="reviewed_H1":hh["B04a_6M_reviewed"]["CFO"]+=1
  elif kind=="Q3_CFO":ff["items"][6]["operating_cash_flow"]=42624493
  elif kind=="Q3_CFI":ff["items"][6]["investing_cash_flow"]+=1
  elif kind=="Q3_net":aa["B04a_Q3_9M_less_reviewed_H1"]["net_cash_change"]+=1
  elif kind=="fake_FX":aa["B04a_Q3_9M_less_reviewed_H1"]["FX_effect"]+=1
  elif kind=="cash_end":ff["items"][6]["cash_ending"]+=1
  elif kind=="Q3_status":ff["items"][6]["verification_status"]="tampered"
  elif kind=="source_SHA":aa["sources"]["archive_sha256"]="0"*64
  elif kind=="prior_Q2":ff["items"][5]["verification_status"]="tampered"
  elif kind=="2024":ff["items"].append({"period":"2024-Q4"})
  try:check(aa,hh,ff)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("VPB Q3 corruption not rejected "+kind)
 print(f"PASS VPB signed 2026 Q3 B02/B03 9M B04 vs reviewed H1: {n} exact source cash identities, {len(cases)} negative tamper controls; all 7 quarterly VPB periods verified.")
if __name__=="__main__":main()
