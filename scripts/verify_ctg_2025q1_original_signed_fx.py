#!/usr/bin/env python3
"""CTG 2025Q1 signed 61-page consolidated bank B02a/B03a/B04a true CFO and FX cash.
Quarantine historic OCR pre-WC-as-CFO and net-as-CFF mislabels; preserve CTG 2026Q3.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"reports/source-audits/CTG-2025Q1-original-signed-bank-million-vnd.json"
FIN=ROOT/"data/financials-CTG.json"
SHA="244171fc77a8ab7e8685b90a74ea8a52f00f3ad622864b591affcea21f953065"
STATUS="issuer_signed_CTG_2025Q1_consolidated_B02a_B03a_B04a_true_CFO_FX_exact_verified"
LOCKED_Q3="issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"
def check(a,d):
 assert a["ticker"]=="CTG" and a["period"]=="2025-Q1" and "consolidated" in a["scope"]
 assert a["unit"]=="triệu VND"
 src=a["source"]
 assert src["url"]=="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/CTG_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
 assert (src["pdf_sha256"],src["pages"],src["bytes"],src["source_workflow_run"])==(SHA,61,6535983,45342348257)
 b,p,c=(a[k] for k in ("B02a_original_million_vnd","B03a_Q1_original_million_vnd","B04a_Q1_original_million_vnd"))
 def S(obj,names):return sum(obj[n] for n in names)
 E={}
 E["B02_asset"]=S(b,("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","investment_securities","long_investments","fixed_assets","other_assets"))-b["assets"]
 E["B02_liab"]=S(b,("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["liabs"]
 E["B02_equity"]=S(b,("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity"))-b["equity"]
 E["B02_balance"]=b["assets"]-b["liabs"]-b["equity"]
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_op"]
 E["B03_revenue"]=S(p,("net_interest","services","FX","trading","investment","other_op","contribution"))-p["revenue"]
 E["B03_operating"]=p["revenue"]-p["opex"]-p["before_prov"]
 E["B03_pretax"]=p["before_prov"]-p["provision"]-p["pbt"]
 E["B03_tax"]=p["tax_current"]+p["tax_deferred"]-p["tax"]
 E["B03_PAT"]=p["pbt"]-p["tax"]-p["pat"]
 E["B03_parent"]=p["pat"]-p["nci"]-p["parent_pat"]
 E["B04_preWC"]=S(c,("interest_received","interest_paid","service_cash","FX_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["before_wc"]
 E["B04_wc_assets"]=S(c,("wc_asset_interbank","wc_asset_trading","wc_asset_derivatives","wc_asset_loans","wc_asset_credit_provision","wc_asset_other"))-c["wc_assets"]
 E["B04_wc_liabs"]=S(c,("wc_liabs_government","wc_liabs_interbank","wc_liabs_customer_deposits","wc_liabs_valuable_papers","wc_liabs_trust","wc_liabs_derivative","wc_liabs_other","wc_liabs_reserves"))-c["wc_liabs"]
 E["B04_trueCFO"]=c["before_wc"]+c["wc_assets"]+c["wc_liabs"]-c["CFO"]
 E["B04_CFI"]=S(c,("capex","asset_sales","asset_disposal_expense","dividends_invest"))-c["CFI"]
 E["B04_cashflows"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net"]
 E["B04_FXcash"]=c["opening"]+c["net"]+c["FX_cash"]-c["closing"]
 assert len(E)==20 and E==a["source_zero_residual_million_vnd"] and all(v==0 for v in E.values()),E
 assert (b["assets"],b["liabs"],b["equity"])==(2469863401,2315881229,153982172)
 assert (p["revenue"],p["pbt"],p["pat"],p["nci"],p["parent_pat"],p["provision"],p["before_prov"])==(20453383,6823198,5499387,80512,5418875,8110962,14934160)
 assert (c["before_wc"],c["wc_assets"],c["wc_liabs"],c["CFO"],c["CFI"],c["CFF"],c["net"],c["FX_cash"],c["opening"],c["closing"])==(8159069,-99312123,82392113,-8760941,-223497,0,-8984438,-19670,373319556,364315448)
 assert a["source_corrected_legacy_parser"]["incorrect_pre_wc_as_CFO"]==8159069
 assert a["source_corrected_legacy_parser"]["true_signed_CFO"]==-8760941
 assert a["source_corrected_legacy_parser"]["legacy_rejected_CFF"]==-8984438
 assert a["source_corrected_legacy_parser"]["true_CFF"]==0
 assert d["symbol"]=="CTG" and [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert d["items"][6]["verification_status"]==LOCKED_Q3
 assert d["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 row=d["items"][0]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 sv=row["source_validation"]
 assert sv["original_pdf_hash_verified"] and sv["original_pdf_sha256"]==SHA
 assert sv["original_pdf_pages"]==61 and sv["original_pdf_bytes"]==6535983
 assert sv["source_20_zero_accounting_identities"] and sv["original_negative_CFO_true_after_WC"] and sv["original_CFF_zero"]
 assert sv["FX_cash_bridge_exact"] and sv["legacy_OCR_bank_CFO_CFF_provision_misclassification_repaired"]
 assert sv["source_audit_ledger"]==str(AUDIT.relative_to(ROOT))
 source_fields={"total_assets":b["assets"],"total_liabilities":b["liabs"],"equity":b["equity"],"revenue":p["revenue"],
 "pretax_profit":p["pbt"],"net_profit":p["pat"],"net_profit_attributable":p["parent_pat"],
 "bank_customer_loans":b["customer_loans"],"bank_customer_loans_gross":1800459242,"bank_customer_loan_loss_allowance":-38269013,
 "bank_pre_provision_operating_profit":p["before_prov"],"bank_provision_expense":p["provision"],
 "bank_service_income":p["service_income"],"bank_service_expense":p["service_expense"],
 "bank_net_service_income":p["services"],"income_tax":p["tax"],
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],"financing_cash_flow":c["CFF"],
 "net_cash_change":c["net"],"cashflow_fx":c["FX_cash"],"cash_beginning":c["opening"],"cash_ending":c["closing"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],
 "net_cash_change_ytd":c["net"],"cashflow_fx_ytd":c["FX_cash"]}
 for k,val in source_fields.items():assert row[k]==val,(k,row.get(k),val)
 for prefix,obj in (("b02a",b),("b03a",p),("b04a",c)):
  for k,v in obj.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["roa"]==0.91 and row["roe"]==14.33 and row["eps"] is None
 assert row["financial_line_items_rejected_values"]=={} and row["financial_line_items_rejected_fields"]==[]
 assert all(not x["period"].startswith("2024") for x in d["items"])
 return len(E),len(source_fields)
def main():
 a=json.loads(AUDIT.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 identities,mappings=check(a,d)
 cases=("source_SHA","source_B02_asset","row_B02_asset","source_liabs","source_equity","source_interest","source_service",
 "source_operating","source_provision","source_PAT","source_parent","source_cash_preWC",
 "source_cash_assetWC","source_cash_liabWC","source_true_CFO","source_CFI","source_cash_FX",
 "dashboard_bad_CFO_preWC","dashboard_bad_CFF_as_net","dashboard_true_CFI","dashboard_close",
 "dashboard_provision","dashboard_preprovision","dashboard_loan_OCR","source_version_old_CFF",
 "source_20_residual_tamper","ratio_parent_PAT","source_SHA_in_row","Q3_locked","EPS_fabrication",
 "2024_period","change_bank_currency")
 for label in cases:
  aa,dd=copy.deepcopy(a),copy.deepcopy(d)
  b,p,c=(aa[x] for x in ("B02a_original_million_vnd","B03a_Q1_original_million_vnd","B04a_Q1_original_million_vnd"))
  row=dd["items"][0]
  if label=="source_SHA":aa["source"]["pdf_sha256"]="0"*64
  elif label=="source_B02_asset":b["assets"]+=1
  elif label=="row_B02_asset":row["total_assets"]+=1
  elif label=="source_liabs":b["liabs"]+=1
  elif label=="source_equity":b["equity"]+=1
  elif label=="source_interest":p["net_interest"]+=1
  elif label=="source_service":p["services"]+=1
  elif label=="source_operating":p["revenue"]+=1
  elif label=="source_provision":p["provision"]+=1
  elif label=="source_PAT":p["pat"]+=1
  elif label=="source_parent":p["parent_pat"]+=1
  elif label=="source_cash_preWC":c["before_wc"]+=1
  elif label=="source_cash_assetWC":c["wc_assets"]+=1
  elif label=="source_cash_liabWC":c["wc_liabs"]+=1
  elif label=="source_true_CFO":c["CFO"]+=1
  elif label=="source_CFI":c["CFI"]+=1
  elif label=="source_cash_FX":c["FX_cash"]+=1
  elif label=="dashboard_bad_CFO_preWC":row["operating_cash_flow"]=8159069
  elif label=="dashboard_bad_CFF_as_net":row["financing_cash_flow"]=-8984438
  elif label=="dashboard_true_CFI":row["investing_cash_flow"]+=1
  elif label=="dashboard_close":row["cash_ending"]+=1
  elif label=="dashboard_provision":row["bank_provision_expense"]=14934160
  elif label=="dashboard_preprovision":row["bank_pre_provision_operating_profit"]=21757358
  elif label=="dashboard_loan_OCR":row["bank_customer_loans"]=1762190220
  elif label=="source_version_old_CFF":aa["source_corrected_legacy_parser"]["true_CFF"]=-8984438
  elif label=="source_20_residual_tamper":aa["source_zero_residual_million_vnd"]["B04_trueCFO"]=1
  elif label=="ratio_parent_PAT":row["roe"]+=0.01
  elif label=="source_SHA_in_row":row["source_validation"]["original_pdf_sha256"]="0"*64
  elif label=="Q3_locked":dd["items"][6]["verification_status"]="pending"
  elif label=="EPS_fabrication":row["eps"]=1
  elif label=="2024_period":dd["items"].append({"period":"2024-Q4"})
  elif label=="change_bank_currency":row["unit"]="VND"
  try:check(aa,dd)
  except (AssertionError,KeyError,IndexError,TypeError,ValueError):pass
  else:raise AssertionError("CTG 2025Q1 source tamper escaped: "+label)
 print(f"PASS CTG Q1 2025 original signed bank 61p: {identities} zero accounting/source identities, {mappings} mapped key fields, {len(cases)} negative tests")
 print("PASS CFO -8,760,941 not beforeWC +8,159,069, CFI -223,497, CFF 0, net -8,984,438, FX -19,670, bank cash end 364,315,448; original CTG 2026Q3 preserved")
if __name__=="__main__":main()
