#!/usr/bin/env python3
"""STB 2025Q4 signed original B02/B03, KPMG-audited FY B04 vs original 9M B04.
Cash is FX aware; source-vintage differences +3 CFO / -3 CFI must cancel; Q4 loss is real.
"""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/STB-2025Q4-original-KPMG-FY-bank-million-vnd.json"
PREV=ROOT/"reports/source-audits/STB-2025Q3-original-9M-KPMG-reviewed-H1-million-vnd.json"
DATA=ROOT/"data/financials-STB.json"
STATUS="issuer_signed_STB_2025Q4_original_B02a_B03a_KPMG_FY_minus_9M_B04a_FX_verified"
def verify(a,old,d):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("STB","2025-Q4","consolidated","triệu VND")
 src=a["source"];sha=src["original_sha256"];auditsha=src["audited_FY_sha256"]
 assert sha=="b0b7438ed502a175a79940e08b254789d8b766af0524d9bbb0d36171adbe0dbf"
 assert auditsha=="57f65260cfc9b3d6b089bc831fec8e3f4e483be3e9c1ff2e2e31ccec8343e15f"
 assert src["source_inspection_workflow_run"]==45271206207
 b,p,c,v,prev,q=(a[k] for k in ("B02a_Audited_FY","B03a_Q4_original_direct","B04a_FY_KPMG_audited","B04a_FY_original","B04a_9M_prior","B04a_Q4_audited_FY_minus_original_9M"))
 assert prev["CFO"]==old["B04a_original_9M"]["CFO"] and prev["FX_effect"]==old["B04a_original_9M"]["FX_effect"]
 def sm(o,keys):return sum(o[k] for k in keys)
 E={}
 E["assets"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","investment_property","other_assets"))-b["total_assets"]
 E["liabilities"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["equity"]=sm(b,("capital","reserves","fx_reserve","retained","minority"))-b["total_equity"]
 E["balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["operating"]=sm(p,("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income"))-p["operating_income"]
 E["preprov"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["pretax"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["FY_preWC"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["FY_CFO"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities","assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other","payments_from_bank_reserves"))-c["CFO"]
 E["FY_CFI"]=sm(c,("capex","asset_disposals","investment_distributions"))-c["CFI"]
 E["FY_CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
 E["FY_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["FY_FXclose"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 E["vintage_CFO"]=c["CFO"]-v["CFO"]-3
 E["vintage_CFI"]=c["CFI"]-v["CFI"]+3
 E["vintage_net"]=v["CFO"]+v["CFI"]+v["CFF"]-v["net_cash_change"]
 E["vintage_FXclose"]=v["opening_cash"]+v["net_cash_change"]+v["FX_effect"]-v["closing_cash"]
 for k in ("CFO","CFI","CFF","net_cash_change","FX_effect","capex"):
  E["quarter_"+k]=c[k]-prev[k]-q[k]
 E["quarter_begin"]=prev["closing_cash"]-q["opening_cash"]
 E["quarter_end"]=c["closing_cash"]-q["closing_cash"]
 E["quarter_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["quarter_FXclose"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 assert len(E)>=30 and all(val==0 for val in E.values()),E
 assert a["source_identity_residuals"]=={k:0 for k in a["source_identity_residuals"]}
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(917119803,857253059,59866744)
 assert (p["before_provision"],p["credit_provision"],p["pretax_profit"],p["income_tax"],p["net_profit"])==(5872007,9232152,-3360145,-607683,-2752462)
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"],c["closing_cash"])==(92478004,-764340,-3818948,87894716,84812,194472583)
 assert (v["CFO"],v["CFI"],v["net_cash_change"],v["closing_cash"])==(92478001,-764337,87894716,194472583)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["FX_effect"],q["opening_cash"],q["closing_cash"])==(57606771,-354438,-432812,56819521,-81479,137734541,194472583)
 assert a["B03a_Audited_FY"]["pretax_profit"]-old["B03a_original_9M_YTD"]["pretax_profit"]==p["pretax_profit"]
 assert a["B03a_Audited_FY"]["net_profit"]-old["B03a_original_9M_YTD"]["net_profit"]==p["net_profit"]
 assert [v["period"] for v in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(v["verification_status"].startswith("issuer_signed_STB") for v in d["items"][:4])
 assert d["items"][3]["verification_status"]==STATUS
 assert [v["verification_status"] for v in d["items"]][4:]==[
 "issuer_signed_STB_2026Q1_original_B02a_B03a_B04a_FX_exact_verified","issuer_signed_STB_2026Q2_original_B02a_B03a_EY_H1_minus_Q1_B04a_FX_vintage_verified","issuer_signed_STB_2026Q3_original_VI_EN_B02a_B03a_9M_minus_EY_H1_B04a_FX_verified"]
 row=d["items"][3];sv=row["source_validation"]
 assert sv["original_pdf_sha256"]==sha and sv["audited_FY_pdf_sha256"]==auditsha
 assert sv["original_pdf_hash_verified"] and sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["bank_FY_minus_9M_FX_cash_exact"] and sv["original_vs_audited_FY_CFO_plus3m_CFI_minus3m"]
 mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],
 "equity":b["total_equity"],"revenue":p["operating_income"],
 "pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
 "bank_provision_expense":p["credit_provision"],"bank_pre_provision_operating_profit":p["before_provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net_cash_change"],"cashflow_fx":q["FX_effect"],"cash_beginning":q["opening_cash"],
 "cash_ending":q["closing_cash"],"operating_cash_flow_ytd":c["CFO"],
 "investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],
 "net_cash_change_ytd":c["net_cash_change"],"cashflow_fx_ytd":c["FX_effect"]}
 for k,value in mapped.items():assert row[k]==value,(k,row.get(k),value)
 for prefix,values in (("b02a",b),("b03a",p),("b04a_FY_audited",c)):
  for k,v in values.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["eps"] is None and row["eps_ytd"]==3150
 assert row["roa"]==-1.25 and row["roe"]==-17.96
 assert not any(x["period"].startswith("2024") for x in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(LEDGER.read_text("utf8"));old=json.loads(PREV.read_text("utf8"));d=json.loads(DATA.read_text("utf8"))
 n,m=verify(a,old,d)
 cases=("asset","liab","equity","net_interest","service","gross_income","provision",
 "PBT","negative_PAT","tax_refund_sign","FY_CFO","FY_CFI","FY_CFF","FY_net",
 "FY_FX","original_CFO","original_CFI","original_vintage_FX","Q4_CFO_preWC",
 "Q4_CFO","Q4_CFI","Q4_CFF","Q4_net","Q4_FX","opening_cash","ending_cash",
 "source_original_SHA","auditor_SHA","Q3_9M_CFO","Q1_locked","Q3_locked","YTD_EPS_misused","2024_period")
 for case in cases:
  aa,old2,dd=copy.deepcopy(a),copy.deepcopy(old),copy.deepcopy(d)
  b,p,c,v,q=(aa[k] for k in ("B02a_Audited_FY","B03a_Q4_original_direct","B04a_FY_KPMG_audited","B04a_FY_original","B04a_Q4_audited_FY_minus_original_9M"))
  row=dd["items"][3]
  if case=="asset":b["total_assets"]+=1
  elif case=="liab":row["total_liabilities"]+=1
  elif case=="equity":row["equity"]+=1
  elif case=="net_interest":p["net_interest"]+=1
  elif case=="service":p["services_net"]+=1
  elif case=="gross_income":row["revenue"]+=1
  elif case=="provision":p["credit_provision"]+=1
  elif case=="PBT":row["pretax_profit"]+=1
  elif case=="negative_PAT":p["net_profit"]=-p["net_profit"]
  elif case=="tax_refund_sign":p["income_tax"]=-p["income_tax"]
  elif case=="FY_CFO":c["CFO"]+=1
  elif case=="FY_CFI":c["CFI"]+=1
  elif case=="FY_CFF":c["CFF"]+=1
  elif case=="FY_net":c["net_cash_change"]+=1
  elif case=="FY_FX":c["FX_effect"]+=1
  elif case=="original_CFO":v["CFO"]+=1
  elif case=="original_CFI":v["CFI"]+=1
  elif case=="original_vintage_FX":v["FX_effect"]+=1
  elif case=="Q4_CFO_preWC":row["operating_cash_flow"]=c["pre_wc_cash"]
  elif case=="Q4_CFO":q["CFO"]+=1
  elif case=="Q4_CFI":row["investing_cash_flow"]+=1
  elif case=="Q4_CFF":row["financing_cash_flow"]+=1
  elif case=="Q4_net":q["net_cash_change"]+=1
  elif case=="Q4_FX":q["FX_effect"]+=1
  elif case=="opening_cash":row["cash_beginning"]+=1
  elif case=="ending_cash":row["cash_ending"]+=1
  elif case=="source_original_SHA":aa["source"]["original_sha256"]="0"*64
  elif case=="auditor_SHA":aa["source"]["audited_FY_sha256"]="0"*64
  elif case=="Q3_9M_CFO":old2["B04a_original_9M"]["CFO"]+=1
  elif case=="Q1_locked":dd["items"][0]["verification_status"]="tampered"
  elif case=="Q3_locked":dd["items"][2]["verification_status"]="tampered"
  elif case=="YTD_EPS_misused":row["eps"]=3150
  elif case=="2024_period":dd["items"].append({"period":"2024-Q4"})
  try:verify(aa,old2,dd)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("STB Q4 source tamper escaped: "+case)
 print(f"PASS STB 2025Q4 signed original vs KPMG audited FY: {n} exact source identities, {m} normalized mappings, {len(cases)} tamper tests")
 print("PASS Q4 actual PBT -3,360,145 PAT -2,752,462 credit provision 9,232,152; CFO +57,606,771 CFI -354,438 CFF -432,812 FX -81,479; source vintage FY CFO +3, CFI -3")
if __name__=="__main__":main()
