#!/usr/bin/env python3
"""STB 2026Q2 issuer signed B02/B03 and EY-reviewed H1 bank B04 2026 original source.
Exact direct Q2 profits, source vintage CFO -2/CFI +1, cash FX +1; 6M-minus-Q1 cash exact.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/STB-2026Q2-original-EY-reviewed-H1-million-vnd.json"
Q1=ROOT/"reports/source-audits/STB-2026Q1-original-signed-bank-million-vnd.json"
FIN=ROOT/"data/financials-STB.json"
ORIGINAL="b50173a5c871d979f1cdcb42bcb8f3bb1860a27afe9b72bfa90f3edca1f07ff0"
EY="f2a79faff2d0d497ce0be06efc37f6673116f809b2963fa1833dc73d7fc853d5"
STATUS="issuer_signed_STB_2026Q2_original_B02a_B03a_EY_H1_minus_Q1_B04a_FX_vintage_verified"
def verify(a,q1,d):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("STB","2026-Q2","consolidated","triệu VND")
 s=a["source"]
 assert s["original_sha256"]==ORIGINAL and s["reviewed_H1_sha256"]==EY
 assert s["original_pdf_pages"]==46 and s["reviewed_H1_pdf_pages"]==96
 assert s["original_pdf_bytes"]==14625280 and s["reviewed_H1_pdf_bytes"]==20078883
 assert s["source_workflow_run"]==45273494680 and s["reviewer"]=="Ernst & Young Vietnam Limited"
 b,p,o,e,q,first=(a[k] for k in ("B02a_reviewed_H1","B03a_Q2_direct","B04a_6M_original","B04a_6M_EY_reviewed","B04a_Q2_EY_reviewed_H1_minus_original_Q1","B04a_Q1_prior"))
 def sm(x,keys):return sum(x[k] for k in keys)
 E={}
 E["asset"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","investment_property","other_assets"))-b["total_assets"]
 E["liab"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["equity"]=sm(b,("capital","reserves","fx_reserve","retained","minority"))-b["total_equity"]
 E["balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["operating"]=sm(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["preprov"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["pretax"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 for name,c in (("original",o),("EY",e)):
  E[name+"_preWC"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
  E[name+"_trueCFO"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities","assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other","payments_from_bank_reserves"))-c["CFO"]
  E[name+"_CFI"]=c["capex"]+c["asset_disposals"]+c["investment_distributions"]-c["CFI"]
  E[name+"_CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
  E[name+"_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
  E[name+"_FXclose"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 E["vintage_CFO"]=e["CFO"]-o["CFO"]+2
 E["vintage_CFI"]=e["CFI"]-o["CFI"]-1
 E["vintage_net"]=e["net_cash_change"]-o["net_cash_change"]+1
 E["vintage_FX"]=e["FX_effect"]-o["FX_effect"]-1
 for k in ("CFO","CFI","CFF","net_cash_change","FX_effect","capex"):
  E["Q2_"+k]=e[k]-first[k]-q[k]
 E["Q2_cash_open"]=first["closing_cash"]-q["opening_cash"]
 E["Q2_cash_end"]=e["closing_cash"]-q["closing_cash"]
 E["Q2_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["Q2_FXcash"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 assert len(E)>=35 and all(v==0 for v in E.values()),E
 assert a["source_vintage_delta_EY_less_original"]=={"CFO":-2,"CFI":1,"CFF":0,"net_cash_change":-1,"FX_effect":1,"closing_cash":0}
 assert len(a["source_identity_residuals"])==21 and all(v==0 for v in a["source_identity_residuals"].values())
 assert first["CFO"]==q1["B04a"]["CFO"] and first["closing_cash"]==q1["B04a"]["closing_cash"]
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(892048566,829241317,62807249)
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"])==(9950076,2029891,1346691)
 assert (o["CFO"],o["CFI"],o["CFF"],o["net_cash_change"],o["FX_effect"],o["closing_cash"])==(-41480644,-147599,-1468762,-43097005,-5701,151369877)
 assert (e["CFO"],e["CFI"],e["CFF"],e["net_cash_change"],e["FX_effect"],e["closing_cash"])==(-41480646,-147598,-1468762,-43097006,-5700,151369877)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["FX_effect"],q["opening_cash"],q["closing_cash"])==(17064706,-19476,-1444350,15600880,-16052,135785049,151369877)
 assert [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 assert all(x["verification_status"].startswith("issuer_signed_STB") for x in d["items"])
 row=d["items"][5];v=row["source_validation"]
 assert row["verification_status"]==STATUS
 assert v["original_pdf_hash_verified"] and v["original_pdf_sha256"]==ORIGINAL and v["reviewed_H1_pdf_sha256"]==EY
 assert v["bank_EY_H1_minus_signed_Q1_FX_cash_exact"] and v["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
 "bank_pre_provision_operating_profit":p["before_provision"],"bank_provision_expense":p["credit_provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net_cash_change"],"cashflow_fx":q["FX_effect"],
 "cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
 "operating_cash_flow_ytd":e["CFO"],"investing_cash_flow_ytd":e["CFI"],"financing_cash_flow_ytd":e["CFF"],
 "net_cash_change_ytd":e["net_cash_change"],"cashflow_fx_ytd":e["FX_effect"]}
 for k,value in mapped.items():assert row[k]==value,(k,value,row.get(k))
 for prefix,values in (("b02a",b),("b03a",p),("b04a_EY_H1_reviewed",e)):
  for k,value in values.items():assert row["signed_source_"+prefix+"_"+k]==value,(prefix,k)
 assert row["eps"] is None and row["eps_ytd"]==1555 and row["roa"]==0.62 and row["roe"]==8.67
 assert not any(x["period"].startswith("2024") for x in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(LEDGER.read_text("utf8"));q1=json.loads(Q1.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 n,m=verify(a,q1,d)
 cases=("source_SHA","reviewer_SHA","balance","asset","liabs","equity","net_interest","service",
 "operating","pretax","provision","PAT","source_original_CFO","source_original_CFI","EY_CFO","EY_CFI",
 "EY_FX","EY_cash","Q2_true_CFO","Q2_CFI","Q2_CFF","Q2_net","Q2_FX","Q2_cash_begin",
 "Q2_cash_end","Q1_CFO","Q1_locked","earlier_Q4_locked","original_EPS_as_quarter",
 "2024_period","prior_H1_vintage_forced","original_6M_preWC_as_trueCFO")
 for case in cases:
  aa,qq,dd=copy.deepcopy(a),copy.deepcopy(q1),copy.deepcopy(d)
  bb,pp,oo,ee,cc=(aa[k] for k in ("B02a_reviewed_H1","B03a_Q2_direct","B04a_6M_original","B04a_6M_EY_reviewed","B04a_Q2_EY_reviewed_H1_minus_original_Q1"))
  row=dd["items"][5]
  if case=="source_SHA":aa["source"]["original_sha256"]="0"*64
  elif case=="reviewer_SHA":aa["source"]["reviewed_H1_sha256"]="0"*64
  elif case=="balance":bb["total_assets"]+=1
  elif case=="asset":row["total_assets"]+=1
  elif case=="liabs":row["total_liabilities"]+=1
  elif case=="equity":bb["total_equity"]+=1
  elif case=="net_interest":pp["net_interest"]+=1
  elif case=="service":pp["services_net"]+=1
  elif case=="operating":row["revenue"]+=1
  elif case=="pretax":pp["pretax_profit"]+=1
  elif case=="provision":pp["credit_provision"]+=1
  elif case=="PAT":row["net_profit"]+=1
  elif case=="source_original_CFO":oo["CFO"]+=1
  elif case=="source_original_CFI":oo["CFI"]+=1
  elif case=="EY_CFO":ee["CFO"]+=1
  elif case=="EY_CFI":ee["CFI"]+=1
  elif case=="EY_FX":ee["FX_effect"]+=1
  elif case=="EY_cash":ee["closing_cash"]+=1
  elif case=="Q2_true_CFO":row["operating_cash_flow"]=ee["pre_wc_cash"]
  elif case=="Q2_CFI":row["investing_cash_flow"]+=1
  elif case=="Q2_CFF":row["financing_cash_flow"]+=1
  elif case=="Q2_net":cc["net_cash_change"]+=1
  elif case=="Q2_FX":cc["FX_effect"]+=1
  elif case=="Q2_cash_begin":row["cash_beginning"]+=1
  elif case=="Q2_cash_end":row["cash_ending"]+=1
  elif case=="Q1_CFO":qq["B04a"]["CFO"]+=1
  elif case=="Q1_locked":dd["items"][4]["verification_status"]="pending"
  elif case=="earlier_Q4_locked":dd["items"][3]["verification_status"]="pending"
  elif case=="original_EPS_as_quarter":row["eps"]=1634
  elif case=="2024_period":dd["items"].append({"period":"2024-Q4"})
  elif case=="prior_H1_vintage_forced":aa["source_vintage_delta_EY_less_original"]["CFO"]=0
  elif case=="original_6M_preWC_as_trueCFO":row["operating_cash_flow"]=ee["pre_wc_cash"]
  try:verify(aa,qq,dd)
  except (AssertionError,KeyError,IndexError,TypeError):pass
  else:raise AssertionError("STB 2026Q2 tamper escaped: "+case)
 print(f"PASS STB 2026Q2 issuer 46p + EY H1 96p: {n} zero identities, {m} production mappings, {len(cases)} tamper tests")
 print("PASS reviewed H1 CFO -41,480,646 CFI -147,598, Q2 CFO +17,064,706 CFI -19,476 CFF -1,444,350 net +15,600,880 FX -16,052 cash 135,785,049 -> 151,369,877")
if __name__=="__main__":main()
