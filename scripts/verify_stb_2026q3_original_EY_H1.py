#!/usr/bin/env python3
"""Close STB 7/7, signed 2026Q3 original Vietnamese & issuer English vs EY-reviewed H1 cash.
Reject sign mistakes, 9M instead of Q3 CFO, altered quarter EPS and source vintage drift.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
Q3FILE=ROOT/"reports/source-audits/STB-2026Q3-original-9M-EY-reviewed-H1-million-vnd.json"
H1FILE=ROOT/"reports/source-audits/STB-2026Q2-original-EY-reviewed-H1-million-vnd.json"
DATAFILE=ROOT/"data/financials-STB.json"
VI_SHA="961131a32f0c5b7605666b4bc89e4c15e7c464474c1d496cc5ce13b62390ccc9"
EN_SHA="bb52dfb3fb6c1b21bc62596436c0badf5a7934f0f7dac2fa6b1e518169fa5a3f"
EY_SHA="f2a79faff2d0d497ce0be06efc37f6673116f809b2963fa1833dc73d7fc853d5"
STATUS="issuer_signed_STB_2026Q3_original_VI_EN_B02a_B03a_9M_minus_EY_H1_B04a_FX_verified"
PERIODS=["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
def verify(a,prior,d):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("STB","2026-Q3","consolidated","triệu VND")
 s=a["source"]
 assert s["original_VI_sha256"]==VI_SHA and s["official_EN_sha256"]==EN_SHA
 assert (s["original_VI_pages"],s["original_VI_bytes"],s["official_EN_pages"],s["official_EN_bytes"])==(47,2866322,46,10117932)
 assert s["source_workflow_run"]==45274659850 and s["EY_H1_source_sha256"]==EY_SHA
 assert s["EY_H1_source_sha256"]==prior["source"]["reviewed_H1_sha256"]
 b,p,c,q,h=(a[k] for k in ("B02a_original","B03a_Q3_direct","B04a_original_9M","B04a_Q3_9M_minus_EY_H1","B04a_EY_reviewed_H1"))
 realH1=prior["B04a_6M_EY_reviewed"]
 for k,v in h.items():assert realH1[k]==v,(k,realH1.get(k),v)
 def sm(obj,keys):return sum(obj[k] for k in keys)
 E={}
 E["assets"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
 "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets",
 "investment_property","other_assets"))-b["total_assets"]
 E["liabs"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs",
 "valuable_papers","other_liabs"))-b["total_liabilities"]
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
 E["preWC"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
 "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["CFO"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities","assets_derivatives",
 "assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank",
 "liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other",
 "payments_from_bank_reserves"))-c["CFO"]
 E["CFI"]=c["capex"]+c["asset_disposals"]+c["investment_distributions"]-c["CFI"]
 E["CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
 E["net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["FXcash"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 E["Q3net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["Q3FXcash"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 for k in ("CFO","CFI","CFF","net_cash_change","FX_effect","capex"):
  E["Q3_"+k]=c[k]-h[k]-q[k]
 assert len(E)==27 and all(v==0 for v in E.values()), E
 assert a["source_identity_residuals"]==E
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(1057397840,993261201,64136639)
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"])==(10305789,1757323,1346682)
 assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"],c["closing_cash"])==(22579777,17383584,-197531,12850000,30036053,-24032,224484604)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["FX_effect"],q["opening_cash"],q["closing_cash"])==(58864230,-49933,14318762,73133059,-18332,151369877,224484604)
 src_profit=a["B03a_9M_YTD"]
 variance={"PBT_YTD_minus_EY_H1_minus_direct_Q3":src_profit["pretax_profit"]-prior["B03a_H1_EY_reviewed"]["pretax_profit"]-p["pretax_profit"],
 "PAT_YTD_minus_EY_H1_minus_direct_Q3":src_profit["net_profit"]-prior["B03a_H1_EY_reviewed"]["net_profit"]-p["net_profit"]}
 assert variance=={"PBT_YTD_minus_EY_H1_minus_direct_Q3":2,"PAT_YTD_minus_EY_H1_minus_direct_Q3":1}
 assert a["source_profits_cross_vintage_residual_million_vnd"]==variance
 assert all(100*abs(v)/abs(p["pretax_profit"] if k.startswith("PBT") else p["net_profit"])<=a["validation_rules"]["source_ytd_profit_vintage_differences_accepted_below_percent"] for k,v in variance.items())
 assert [v["period"] for v in d["items"]]==PERIODS
 assert all(v["verification_status"].startswith("issuer_signed_STB") for v in d["items"])
 row=d["items"][-1];sv=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert sv["original_pdf_hash_verified"] and sv["original_pdf_sha256"]==VI_SHA and sv["issuer_EN_pdf_sha256"]==EN_SHA
 assert sv["EY_H1_reviewed_pdf_sha256"]==EY_SHA
 assert sv["source_audit_ledger"]==str(Q3FILE.relative_to(ROOT))
 assert sv["B03_YTD_minus_EY_H1_PBT_differ_from_direct_Q3_million_vnd"]==2
 assert sv["B03_YTD_minus_EY_H1_PAT_differ_from_direct_Q3_million_vnd"]==1
 assert sv["B03_comparative_vintage_accepted_within_0_01pct"] and sv["no_balancing_plug"]
 assert sv["bank_9M_minus_EY_H1_FX_cash_exact"]
 mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],
 "net_profit_attributable":p["parent_profit"],"bank_pre_provision_operating_profit":p["before_provision"],
 "bank_provision_expense":p["credit_provision"],"operating_cash_flow":q["CFO"],
 "investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],"net_cash_change":q["net_cash_change"],
 "cashflow_fx":q["FX_effect"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
 "cashflow_fx_ytd":c["FX_effect"],"capital_expenditure":q["capex"],
 "bank_customer_loans_gross":700346512,"bank_customer_loan_loss_allowance":-17890003}
 for k,v in mapped.items():assert row[k]==v,(k,row.get(k),v)
 assert row["bank_customer_loans"]==b["customer_loans_net"]==700346512-17890003
 for prefix,obj in (("b02a",b),("b03a",p),("b04a_original_9M",c)):
  for k,v in obj.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["roa"]==0.55 and row["roe"]==8.49
 assert row["eps"] is None and row["eps_ytd"]==src_profit["EPS_9M_YTD_reported"]==809
 assert row["source_url"]==s["original_VI_url"]
 assert all(v["period"]>="2025-Q1" for v in d["items"])
 assert a["validation_rules"]["preserve_prior_6_quarters"] and not a["validation_rules"]["quarterly_EPS_not_estimated"] is False
 return len(E),len(mapped)
def main():
 a=json.loads(Q3FILE.read_text("utf8"));h=json.loads(H1FILE.read_text("utf8"));d=json.loads(DATAFILE.read_text("utf8"))
 n,m=verify(a,h,d)
 cases=("VI_sha","EN_sha","reviewer_sha","source_pdf_page","balance","assets","liabs","equity",
 "net_interest","service","other","operating","provision","PAT","Q3profit_vintage","YTD_PAT_vintage",
 "tolerance_abused","CFO_9M","CFO_preWC","CFI_9M","CFF_9M","FX_9M","net_9M",
 "Q3_CFO_wrong_YTD","Q3_CFI","Q3_CFF","Q3_net","Q3_fx","Q3_open","Q3_close",
 "EY_H1_CFO","EY_H1_FX","EY_H1_source_SHA","Q1_locked","Q2_locked","2025Q4_locked",
 "EPS_as_quarter","2024_period","duplicate_Q3","loan_OCR_300m_error","source_identity_forgery",
 "vintage_residual_forgery")
 for case in cases:
  aa,hh,dd=copy.deepcopy(a),copy.deepcopy(h),copy.deepcopy(d)
  b,p,c,q=(aa[k] for k in ("B02a_original","B03a_Q3_direct","B04a_original_9M","B04a_Q3_9M_minus_EY_H1"))
  row=dd["items"][-1]
  if case=="VI_sha":aa["source"]["original_VI_sha256"]="0"*64
  elif case=="EN_sha":aa["source"]["official_EN_sha256"]="0"*64
  elif case=="reviewer_sha":aa["source"]["EY_H1_source_sha256"]="0"*64
  elif case=="source_pdf_page":aa["source"]["original_VI_pages"]=46
  elif case=="balance":b["total_assets"]+=1
  elif case=="assets":row["total_assets"]+=1
  elif case=="liabs":b["total_liabilities"]+=1
  elif case=="equity":row["equity"]+=1
  elif case=="net_interest":p["net_interest"]+=1
  elif case=="service":p["services_net"]+=1
  elif case=="other":p["other_net"]+=1
  elif case=="operating":p["operating_income"]+=1
  elif case=="provision":p["credit_provision"]+=1
  elif case=="PAT":p["net_profit"]+=1
  elif case=="Q3profit_vintage":aa["B03a_9M_YTD"]["pretax_profit"]+=1
  elif case=="YTD_PAT_vintage":aa["B03a_9M_YTD"]["net_profit"]+=1
  elif case=="tolerance_abused":aa["validation_rules"]["source_ytd_profit_vintage_differences_accepted_below_percent"]=0.000001
  elif case=="CFO_9M":c["CFO"]+=1
  elif case=="CFO_preWC":row["operating_cash_flow"]=22579777
  elif case=="CFI_9M":c["CFI"]+=1
  elif case=="CFF_9M":c["CFF"]+=1
  elif case=="FX_9M":c["FX_effect"]+=1
  elif case=="net_9M":c["net_cash_change"]+=1
  elif case=="Q3_CFO_wrong_YTD":row["operating_cash_flow"]=17383584
  elif case=="Q3_CFI":row["investing_cash_flow"]+=1
  elif case=="Q3_CFF":row["financing_cash_flow"]+=1
  elif case=="Q3_net":q["net_cash_change"]+=1
  elif case=="Q3_fx":q["FX_effect"]+=1
  elif case=="Q3_open":row["cash_beginning"]+=1
  elif case=="Q3_close":row["cash_ending"]+=1
  elif case=="EY_H1_CFO":hh["B04a_6M_EY_reviewed"]["CFO"]+=1
  elif case=="EY_H1_FX":hh["B04a_6M_EY_reviewed"]["FX_effect"]+=1
  elif case=="EY_H1_source_SHA":hh["source"]["reviewed_H1_sha256"]="0"*64
  elif case=="Q1_locked":dd["items"][0]["verification_status"]="pending"
  elif case=="Q2_locked":dd["items"][5]["verification_status"]="pending"
  elif case=="2025Q4_locked":dd["items"][3]["verification_status"]="pending"
  elif case=="EPS_as_quarter":row["eps"]=809
  elif case=="2024_period":dd["items"].append({"period":"2024-Q4"})
  elif case=="duplicate_Q3":dd["items"].append(copy.deepcopy(row))
  elif case=="loan_OCR_300m_error":row["bank_customer_loans"]=682456809
  elif case=="source_identity_forgery":aa["source_identity_residuals"]["CFO"]=1
  elif case=="vintage_residual_forgery":aa["source_profits_cross_vintage_residual_million_vnd"]["PBT_YTD_minus_EY_H1_minus_direct_Q3"]=0
  try:verify(aa,hh,dd)
  except (AssertionError,KeyError,IndexError,TypeError):pass
  else:raise AssertionError("STB 2026Q3 negative tamper test escaped: "+case)
 print(f"PASS STB 2026Q3 original VI 47p EN 46p versus EY reviewed H1: {n} zero accounting cash identities, {m} source mappings, {len(cases)} negative tamper cases; all 7/7 STB periods source-verified")
 print("PASS source 9M PBT-to-direct-Q3 +2m and PAT +1m version differences within 0.01% retained, no plug")
 print("PASS Q3 CFO +58,864,230 CFI -49,933 CFF +14,318,762 net +73,133,059 FX -18,332; cash 151,369,877 -> 224,484,604")
if __name__=="__main__":main()
