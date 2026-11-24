#!/usr/bin/env python3
"""CTG 2025Q3 61p issuer signed 9M vs independently PwC-reviewed 6M (cash FX aware).
Source originals / PwC reclassification 79,310m retained, prior Q1/Q2 and 2026Q3 frozen.
"""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1]
LEDGER=R/"reports/source-audits/CTG-2025Q3-original-9M-PwC-H1-million-vnd.json"
H1=R/"reports/source-audits/CTG-2025Q2-original-PwC-H1-bank-million-vnd.json"
FIN=R/"data/financials-CTG.json"
SHA="255b340f3eb40e53e641e661d688671bd9cb3b0cfb86df155b77960424bd7543"
PWC_SHA="6dd260b0197fc4994ded9f42e60d24acc49b6c86755b09012e5b67ccfa41bcaa"
STATUS="issuer_signed_CTG_2025Q3_original_B02a_B03a_9M_minus_PwC_H1_B04a_FX_exact_verified"
LOCK1="issuer_signed_CTG_2025Q1_consolidated_B02a_B03a_B04a_true_CFO_FX_exact_verified"
LOCK2="issuer_signed_CTG_2025Q2_original_B02a_B03a_PwC_H1_minus_Q1_B04a_79310_reclass_verified"
LOCK7="issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"
def verify(a,prior,d):
 assert (a["ticker"],a["period"],a["unit"])==("CTG","2025-Q3","triệu VND")
 assert "consolidated" in a["scope"]
 s=a["original_source"]
 assert s["url"]=="https://investor.vietinbank.vn/documents/20126/168545/BCTC%20hop%20nhat%203Q2025..pdf.pdf/7cebff86-0a61-f4d6-ca68-b41a07a7b556?download=true"
 assert (s["pdf_sha256"],s["pages"],s["bytes"],s["workflow_run"])==(SHA,61,3387049,45344358932)
 h1s=prior["sources"]
 assert h1s["PwC_H1_reviewed"]["pdf_sha256"]==PWC_SHA
 assert a["previous_reviewed_H1"]["PwC_H1_pdf_sha256"]==PWC_SHA
 b,p,c,q,h=(a[x] for x in ("B02a_original_signed","B03a_Q3_direct_signed","B04a_9M_original_signed","B04a_standalone_Q3_9M_minus_PwC_H1","B04a_PwC_H1_reviewed"))
 real_h1=h1s and prior["B04a_PwC_reviewed_H1"]
 for k,v in h.items():assert real_h1[k]==v,(k,real_h1.get(k),v)
 realP=prior["B03a_H1_comparator"]
 for k,v in a["B03a_PwC_reviewed_H1_ytd"].items():assert realP[k]==v
 def S(o,keys):return sum(o[k] for k in keys)
 E={}
 E["B02_assets"]=S(b,("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","investment_securities","long_investments","fixed_assets","other_assets"))-b["assets"]
 E["B02_liabilities"]=S(b,("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["liabs"]
 E["B02_equity"]=S(b,("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity"))-b["equity"]
 E["B02_balance"]=b["assets"]-b["liabs"]-b["equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_op"]
 E["B03_revenue"]=S(p,("net_interest","services","FX","trading","investment","other_op","contribution"))-p["revenue"]
 E["B03_preprovision"]=p["revenue"]-p["opex"]-p["before_prov"]
 E["B03_pbt"]=p["before_prov"]-p["provision"]-p["pbt"]
 E["B03_tax"]=p["tax_current"]+p["tax_deferred"]-p["tax"]
 E["B03_PAT"]=p["pbt"]-p["tax"]-p["pat"]
 E["B03_parent"]=p["pat"]-p["nci"]-p["parent_pat"]
 y=a["B03a_original_9M_ytd"]
 E["B03_9m_vs_PwC_H1_PBT"]=p["pbt"]+realP["pretax_profit"]-y["pretax_profit"]
 E["B03_9m_vs_PwC_H1_PAT"]=p["pat"]+realP["net_profit"]-y["net_profit"]
 E["B03_9m_vs_PwC_H1_parent"]=p["parent_pat"]+realP["parent_profit"]-y["parent_profit"]
 E["B04_preWC"]=S(c,("interest_received","interest_paid","service_cash","FX_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["before_wc"]
 E["B04_assets"]=S(c,("wc_asset_interbank","wc_asset_trading","wc_asset_derivatives","wc_asset_loans","wc_asset_credit_provision","wc_asset_other"))-c["wc_assets"]
 E["B04_liabs"]=S(c,("wc_liabs_government","wc_liabs_interbank","wc_liabs_customer_deposits","wc_liabs_valuable_papers","wc_liabs_trust","wc_liabs_derivative","wc_liabs_other","wc_liabs_reserves"))-c["wc_liabs"]
 E["B04_CFO"]=c["before_wc"]+c["wc_assets"]+c["wc_liabs"]-c["CFO"]
 E["B04_CFI"]=S(c,("capex","asset_sales","asset_disposal_expense","dividends_invest"))-c["CFI"]
 E["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net"]
 E["B04_FXcash"]=c["opening"]+c["net"]+c["FX_cash"]-c["closing"]
 E["Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net"]
 E["Q3_FXcash"]=q["opening"]+q["net"]+q["FX_cash"]-q["closing"]
 for k in ("CFO","CFI","CFF","net","FX_cash","capex"):
  E["Q3_delta_"+k]=c[k]-real_h1[k]-q[k]
 E["Q3_begin"]=q["opening"]-real_h1["closing"]
 E["Q3_end"]=q["closing"]-c["closing"]
 assert len(E)==33 and E==a["source_accounting_zero_residual_million_vnd"] and all(v==0 for v in E.values()),E
 assert (b["assets"],b["liabs"],b["equity"])==(2761550938,2591669938,169881000)
 assert (p["pbt"],p["pat"],p["parent_pat"],p["before_prov"],p["provision"])==(10614390,8512463,8448784,16477799,5863409)
 assert (c["before_wc"],c["CFO"],c["CFI"],c["CFF"],c["net"],c["FX_cash"],c["opening"],c["closing"])==(40765800,85022836,-1154686,0,83868150,174268,373319556,457361974)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net"],q["FX_cash"],q["opening"],q["closing"])==(66767196,-572769,0,66194427,-6801,391174348,457361974)
 assert prior["source_vintage_PwC_less_issuer"]["CFO"]==-79310
 assert prior["source_vintage_PwC_less_issuer"]["CFI"]==79310
 assert [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert (d["items"][0]["verification_status"],d["items"][1]["verification_status"],d["items"][6]["verification_status"])==(LOCK1,LOCK2,LOCK7)
 assert d["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 row=d["items"][2];v=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert v["original_pdf_hash_verified"] and v["original_pdf_sha256"]==SHA and v["original_pdf_pages"]==61
 assert v["bank_signed_9M_minus_PwC_H1_FX_cash_exact"]
 assert v["PwC_H1_79310_CFO_CFI_reclass_preserved"]
 assert v["source_33_accounting_identities_zero"]
 assert v["source_audit_ledger"]==str(LEDGER.relative_to(R))
 mapped={"total_assets":b["assets"],"total_liabilities":b["liabs"],"equity":b["equity"],
 "revenue":p["revenue"],"pretax_profit":p["pbt"],"net_profit":p["pat"],"net_profit_attributable":p["parent_pat"],
 "bank_customer_loans":b["customer_loans"],"bank_customer_loans_gross":1990563217,"bank_customer_loan_loss_allowance":-38336311,
 "bank_provision_expense":p["provision"],"bank_pre_provision_operating_profit":p["before_prov"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],"net_cash_change":q["net"],
 "cashflow_fx":q["FX_cash"],"cash_beginning":q["opening"],"cash_ending":q["closing"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],
 "net_cash_change_ytd":c["net"],"cashflow_fx_ytd":c["FX_cash"]}
 for k,value in mapped.items():assert row[k]==value,(k,row.get(k),value)
 for prefix,vals in (("b02a",b),("b03a",p),("b04a_9M",c)):
  for k,value in vals.items():assert row["signed_source_"+prefix+"_"+k]==value,(prefix,k)
 assert row["roa"]==1.27 and row["roe"]==20.25 and row["eps"] is None
 assert all(x["period"]>="2025-Q1" for x in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(LEDGER.read_text("utf8"));h=json.loads(H1.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 n,m=verify(a,h,d)
 cases=("source_sha","source_page","reviewed_H1_SHA","B02_asset","B02_liabs","B02_equity","row_asset",
 "B03_interest","B03_service","B03_revenue","B03_provision","B03_pat","B03_9m_pat",
 "B04_pre_wc","B04_assets","B04_liabs","B04_CFO","B04_CFI","B04_net","B04_fx",
 "Q3_9M_as_CFO","Q3_CFI","Q3_CFF_from_2024","Q3_net","Q3_FX_discarded","Q3_cash_open","Q3_cash_end",
 "PwC_H1_CFO","PwC_H1_CFI","PwC_reclass_missing","original_Q2_locked","original_Q1_locked",
 "Q3_2026_locked","EPS_imputed","2024_dashboard","loan_300k_mistake","source_residual_forged","original_source_link")
 for case in cases:
  aa,hh,dd=copy.deepcopy(a),copy.deepcopy(h),copy.deepcopy(d)
  b,p,c,q=(aa[k] for k in ("B02a_original_signed","B03a_Q3_direct_signed","B04a_9M_original_signed","B04a_standalone_Q3_9M_minus_PwC_H1"))
  row=dd["items"][2]
  if case=="source_sha":aa["original_source"]["pdf_sha256"]="0"*64
  elif case=="source_page":aa["original_source"]["pages"]-=1
  elif case=="reviewed_H1_SHA":aa["previous_reviewed_H1"]["PwC_H1_pdf_sha256"]="0"*64
  elif case=="B02_asset":b["assets"]+=1
  elif case=="B02_liabs":b["liabs"]+=1
  elif case=="B02_equity":b["equity"]+=1
  elif case=="row_asset":row["total_assets"]+=1
  elif case=="B03_interest":p["net_interest"]+=1
  elif case=="B03_service":p["services"]+=1
  elif case=="B03_revenue":row["revenue"]+=1
  elif case=="B03_provision":p["provision"]+=1
  elif case=="B03_pat":p["pat"]+=1
  elif case=="B03_9m_pat":aa["B03a_original_9M_ytd"]["net_profit"]+=1
  elif case=="B04_pre_wc":c["before_wc"]+=1
  elif case=="B04_assets":c["wc_assets"]+=1
  elif case=="B04_liabs":c["wc_liabs"]+=1
  elif case=="B04_CFO":c["CFO"]+=1
  elif case=="B04_CFI":c["CFI"]+=1
  elif case=="B04_net":c["net"]+=1
  elif case=="B04_fx":c["FX_cash"]+=1
  elif case=="Q3_9M_as_CFO":row["operating_cash_flow"]=85022836
  elif case=="Q3_CFI":row["investing_cash_flow"]+=1
  elif case=="Q3_CFF_from_2024":row["financing_cash_flow"]=1537
  elif case=="Q3_net":q["net"]+=1
  elif case=="Q3_FX_discarded":q["FX_cash"]=0
  elif case=="Q3_cash_open":row["cash_beginning"]+=1
  elif case=="Q3_cash_end":row["cash_ending"]+=1
  elif case=="PwC_H1_CFO":hh["B04a_PwC_reviewed_H1"]["CFO"]+=1
  elif case=="PwC_H1_CFI":hh["B04a_PwC_reviewed_H1"]["CFI"]+=1
  elif case=="PwC_reclass_missing":hh["source_vintage_PwC_less_issuer"]["CFO"]=0
  elif case=="original_Q2_locked":dd["items"][1]["verification_status"]="pending"
  elif case=="original_Q1_locked":dd["items"][0]["verification_status"]="pending"
  elif case=="Q3_2026_locked":dd["items"][6]["verification_status"]="pending"
  elif case=="EPS_imputed":row["eps"]=3000
  elif case=="2024_dashboard":dd["items"].append({"period":"2024-Q4"})
  elif case=="loan_300k_mistake":row["bank_customer_loans"]=1952226909
  elif case=="source_residual_forged":aa["source_accounting_zero_residual_million_vnd"]["B04_CFO"]=1
  elif case=="original_source_link":aa["original_source"]["url"]="https://example.com/fake.pdf"
  try:verify(aa,hh,dd)
  except (AssertionError,KeyError,IndexError,ValueError,TypeError):pass
  else:raise AssertionError("CTG Q3 2025 source tamper escaped "+case)
 print(f"PASS CTG 2025Q3 original issuer signed 61p: {n} exact zero identities, {m} mapped key fields, {len(cases)} negative tamper tests")
 print("PASS 9M-minus-PwC H1 CFO +66,767,196 CFI -572,769 CFF 0 net +66,194,427 FX -6,801 and cash 457,361,974; 79,310 reclass and prior CTG 2026Q3 preserved")
if __name__=="__main__":main()
