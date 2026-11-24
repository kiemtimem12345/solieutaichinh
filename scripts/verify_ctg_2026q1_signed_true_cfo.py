#!/usr/bin/env python3
"""CTG 2026Q1 signed original bank B02/B03 and true CFO 127,479,653 with FX cash.
Guard against pre-working-capital 9,152,054 miscast as CFO and 127,164,150 net as CFF.
"""
import json,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
AUD=R/"reports/source-audits/CTG-2026Q1-original-signed-bank-million-vnd.json"
FY=R/"reports/source-audits/CTG-2025Q4-original-PwC-audited-FY-million-vnd.json"
FIN=R/"data/financials-CTG.json"
SHA="294f853b3317bb01648f39d1a81bdab3cbdaf625da27f0dcfe520dd5f15e2c2e"
STATUS="issuer_signed_CTG_2026Q1_original_B02a_B03a_B04a_true_CFO_after_WC_FX_verified"
LOCKS={0:"issuer_signed_CTG_2025Q1_consolidated_B02a_B03a_B04a_true_CFO_FX_exact_verified",
1:"issuer_signed_CTG_2025Q2_original_B02a_B03a_PwC_H1_minus_Q1_B04a_79310_reclass_verified",
2:"issuer_signed_CTG_2025Q3_original_B02a_B03a_9M_minus_PwC_H1_B04a_FX_exact_verified",
3:"issuer_signed_CTG_2025Q4_original_B02a_B03a_PwC_audited_FY_minus_9M_B04a_material_13824_verified",
6:"issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"}
def verify(a,fy,d):
 assert (a["ticker"],a["period"],a["scope"],a["unit"])==("CTG","2026-Q1","consolidated","triệu VND")
 src=a["source"]
 assert src["url"]=="https://investor.vietinbank.vn/documents/20126/745243/BCTC%20hop%20nhat%20Quy%20I.2026.pdf.pdf/fe475c57-822f-3c6d-5bf1-53e6612969e9"
 assert (src["pdf_sha256"],src["pages"],src["bytes"],src["source_workflow_run"])==(SHA,61,5679820,45346880126)
 assert src["FY2025_PwC_sha256"]==fy["source"]["audited_FY_sha256"]=="b82eeb879b667e80d0b5322969c808089fd39b83835b75dc47f9a890189fc137"
 b,p,c=(a[k] for k in ("B02a_original","B03a_Q1_original","B04a_Q1_original"))
 def S(x,ks):return sum(x[k] for k in ks)
 E={}
 E["B02_assets"]=S(b,("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","investment_securities","long_investments","fixed_assets","other_assets"))-b["assets"]
 E["B02_liabs"]=S(b,("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["liabs"]
 E["B02_equity"]=S(b,("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity"))-b["equity"]
 E["B02_balance"]=b["assets"]-b["liabs"]-b["equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_services"]=p["service_income"]+p["service_expense"]-p["services"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_op"]
 E["B03_revenue"]=S(p,("net_interest","services","FX","trading","investment","other_op","contribution"))-p["revenue"]
 E["B03_preprov"]=p["revenue"]-p["opex"]-p["before_prov"]
 E["B03_pretax"]=p["before_prov"]-p["provision"]-p["pbt"]
 E["B03_tax"]=p["tax_current"]+p["tax_deferred"]-p["tax"]
 E["B03_PAT"]=p["pbt"]-p["tax"]-p["pat"]
 E["B03_parent"]=p["pat"]-p["nci"]-p["parent_pat"]
 E["B04_preWC"]=S(c,("interest_received","interest_paid","service_cash","FX_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["before_wc"]
 E["B04_wcAsset"]=S(c,("wc_asset_interbank","wc_asset_trading","wc_asset_derivatives","wc_asset_loans","wc_asset_credit_provision","wc_asset_other"))-c["wc_assets"]
 E["B04_wcLiabs"]=S(c,("wc_liabs_government","wc_liabs_interbank","wc_liabs_customer_deposits","wc_liabs_valuable_papers","wc_liabs_trust","wc_liabs_derivative","wc_liabs_other","wc_liabs_reserves"))-c["wc_liabs"]
 E["B04_trueCFO"]=c["before_wc"]+c["wc_assets"]+c["wc_liabs"]-c["CFO"]
 E["B04_CFI"]=c["capex"]+c["asset_sales"]+c["asset_disposal_expense"]+c["dividends_invest"]-c["CFI"]
 E["B04_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net"]
 E["B04_FXcash"]=c["opening"]+c["net"]+c["FX_cash"]-c["closing"]
 assert len(E)==20 and E==a["source_zero_residuals_million_vnd"] and all(n==0 for n in E.values()),E
 assert (b["assets"],b["liabs"],b["equity"])==(2924176928,2735484770,188692158)
 assert (p["revenue"],p["before_prov"],p["provision"],p["pbt"],p["pat"],p["parent_pat"])==(25101554,18840291,7700931,11139360,8960041,8916979)
 assert (c["before_wc"],c["wc_assets"],c["wc_liabs"],c["CFO"],c["CFI"],c["CFF"],c["net"],c["FX_cash"],c["opening"],c["closing"])==(9152054,-34509385,152836984,127479653,-315503,0,127164150,85384,451745475,578995009)
 assert c["opening"]==fy["B04a_PwC_audited_FY"]["closing"]
 assert len(d["items"])==7 and [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 for i,status in LOCKS.items():assert d["items"][i]["verification_status"]==status
 assert d["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 row=d["items"][4];v=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert v["original_pdf_hash_verified"] and v["original_pdf_sha256"]==SHA and v["original_pdf_pages"]==61
 assert v["true_CFO_after_WC_127479653_verified"] and v["pre_wc_9152054_not_true_CFO"] and v["original_CFF_zero_verified"] and v["FX_cash_bridge_exact"]
 assert v["source_audit_ledger"]==str(AUD.relative_to(R)) and v["prior_PwC_FY2025_cash_matched"]
 mapped={"total_assets":b["assets"],"total_liabilities":b["liabs"],"equity":b["equity"],
 "revenue":p["revenue"],"pretax_profit":p["pbt"],"net_profit":p["pat"],"net_profit_attributable":p["parent_pat"],
 "bank_pre_provision_operating_profit":p["before_prov"],"bank_provision_expense":p["provision"],"bank_customer_loans":b["customer_loans"],
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],"financing_cash_flow":c["CFF"],"net_cash_change":c["net"],
 "cashflow_fx":c["FX_cash"],"cash_beginning":c["opening"],"cash_ending":c["closing"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],
 "net_cash_change_ytd":c["net"],"cashflow_fx_ytd":c["FX_cash"]}
 for key,amount in mapped.items():assert row[key]==amount,(key,row.get(key),amount)
 for pre,obj in (("b02a",b),("b03a",p),("b04a",c)):
  for key,amount in obj.items():assert row["signed_source_"+pre+"_"+key]==amount,(pre,key)
 assert row["roa"]==1.26 and row["roe"]==19.37 and row["eps"] is None
 assert row["financial_line_items_rejected_values"]=={} and row["financial_line_items_rejected_fields"]==[]
 assert all(x["period"]>="2025-Q1" for x in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(AUD.read_text("utf8"));f=json.loads(FY.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 n,m=verify(a,f,d)
 cases=("source_sha","source_FYsha","source_pages","B02_assets","B02_liabs","B02_equity","B03_interest","B03_services","B03_operating","B03_provision","B03_PAT","B04_preWC","B04_assets","B04_liabs","B04_CFO","B04_CFI","B04_net","B04_FX","Q1_CFO_as_preWC","Q1_CFO_negative","Q1_CFF_as_net","Q1_CFI_wrong","Q1_FX_removed","Q1_closing","FY_opening_cash","prior_Q4_locked","prior_Q3_2026_locked","source_identity_forged","wrong_2024_period","EPS_imputed","status_downgraded","bank_loan_misparsed")
 for case in cases:
  aa,ff,dd=copy.deepcopy(a),copy.deepcopy(f),copy.deepcopy(d)
  b,p,c=(aa[k] for k in ("B02a_original","B03a_Q1_original","B04a_Q1_original"));row=dd["items"][4]
  if case=="source_sha":aa["source"]["pdf_sha256"]="0"*64
  elif case=="source_FYsha":aa["source"]["FY2025_PwC_sha256"]="0"*64
  elif case=="source_pages":aa["source"]["pages"]=60
  elif case=="B02_assets":b["assets"]+=1
  elif case=="B02_liabs":b["liabs"]+=1
  elif case=="B02_equity":b["equity"]+=1
  elif case=="B03_interest":p["net_interest"]+=1
  elif case=="B03_services":p["services"]+=1
  elif case=="B03_operating":p["before_prov"]+=1
  elif case=="B03_provision":p["provision"]+=1
  elif case=="B03_PAT":p["pat"]+=1
  elif case=="B04_preWC":c["before_wc"]+=1
  elif case=="B04_assets":c["wc_assets"]+=1
  elif case=="B04_liabs":c["wc_liabs"]+=1
  elif case=="B04_CFO":c["CFO"]+=1
  elif case=="B04_CFI":c["CFI"]+=1
  elif case=="B04_net":c["net"]+=1
  elif case=="B04_FX":c["FX_cash"]+=1
  elif case=="Q1_CFO_as_preWC":row["operating_cash_flow"]=9152054
  elif case=="Q1_CFO_negative":row["operating_cash_flow"]=-row["operating_cash_flow"]
  elif case=="Q1_CFF_as_net":row["financing_cash_flow"]=127164150
  elif case=="Q1_CFI_wrong":row["investing_cash_flow"]+=1
  elif case=="Q1_FX_removed":row["cashflow_fx"]=0
  elif case=="Q1_closing":row["cash_ending"]+=1
  elif case=="FY_opening_cash":ff["B04a_PwC_audited_FY"]["closing"]+=1
  elif case=="prior_Q4_locked":dd["items"][3]["verification_status"]="pending"
  elif case=="prior_Q3_2026_locked":dd["items"][6]["verification_status"]="pending"
  elif case=="source_identity_forged":aa["source_zero_residuals_million_vnd"]["B04_trueCFO"]=1
  elif case=="wrong_2024_period":dd["items"].append({"period":"2024-Q4"})
  elif case=="EPS_imputed":row["eps"]=11
  elif case=="status_downgraded":row["verification_status"]="pending"
  elif case=="bank_loan_misparsed":row["bank_customer_loans"]+=100
  try:verify(aa,ff,dd)
  except (AssertionError,IndexError,KeyError,TypeError):pass
  else:raise AssertionError("CTG 2026Q1 tamper passed: "+case)
 print(f"PASS CTG signed original 2026Q1 61p: {n} exact source identities, {m} production mappings, {len(cases)} negative tamper tests")
 print("PASS signed true CFO +127,479,653 NOT before-WC +9,152,054; zero CFF NOT net +127,164,150; CFI -315,503 FX +85,384 cash end 578,995,009; audited FY2025 source unchanged")
if __name__=="__main__":main()
