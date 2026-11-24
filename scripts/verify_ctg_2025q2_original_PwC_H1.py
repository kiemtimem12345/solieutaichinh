#!/usr/bin/env python3
"""CTG Q2 2025 original signed issuer B02/B03 and independently PwC-reviewed H1 B04.
Keep 79,310m CFO/CFI vintage reclassification, true quarter FX cash, and locked CTG Q3/2026.
"""
from pathlib import Path
import copy,json
R=Path(__file__).resolve().parents[1]
AUDIT=R/"reports/source-audits/CTG-2025Q2-original-PwC-H1-bank-million-vnd.json"
Q1=R/"reports/source-audits/CTG-2025Q1-original-signed-bank-million-vnd.json"
FIN=R/"data/financials-CTG.json"
ORIGINAL="6fafb5d70e3dc9ca99518b632ea44c8d75d5d57908bdf56b2221bc212e9b2aa7"
PWC="6dd260b0197fc4994ded9f42e60d24acc49b6c86755b09012e5b67ccfa41bcaa"
Q1_SHA="244171fc77a8ab7e8685b90a74ea8a52f00f3ad622864b591affcea21f953065"
STATUS="issuer_signed_CTG_2025Q2_original_B02a_B03a_PwC_H1_minus_Q1_B04a_79310_reclass_verified"
LOCKED_Q3="issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"
def check(a,q1,data):
 assert (a["ticker"],a["period"],a["unit"],a["scope"])==("CTG","2025-Q2","triệu VND","consolidated")
 src=a["sources"]
 issuer,review=src["issuer_Q2_original"],src["PwC_H1_reviewed"]
 assert (issuer["pdf_sha256"],issuer["bytes"],issuer["pages"])==(ORIGINAL,5373307,62)
 assert (review["pdf_sha256"],review["bytes"],review["pages"])==(PWC,11776646,76)
 assert src["source_workflow_run"]==45343490708
 assert src["prior_Q1_original_pdf_sha256"]==q1["source"]["pdf_sha256"]==Q1_SHA
 b,p,o,e,prior,q=(a[k] for k in ("B02a_PwC_H1","B03a_Q2_signed_direct","B04a_Q2_original_H1",
 "B04a_PwC_reviewed_H1","B04a_Q1_issuer_signed_prior","B04a_Q2_PwC_reviewed_H1_minus_Q1"))
 q1_b04=q1["B04a_Q1_original_million_vnd"]
 for k,v in prior.items():assert v==q1_b04[k],("Q1 frozen",k,v,q1_b04[k])
 def S(obj,keys):return sum(obj[k] for k in keys)
 C={}
 C["B02_assets"]=S(b,("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","investment_securities","long_investments","fixed_assets","other_assets"))-b["assets"]
 C["B02_liabs"]=S(b,("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["liabs"]
 C["B02_equity"]=S(b,("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity"))-b["equity"]
 C["B02_bal"]=b["assets"]-b["liabs"]-b["equity"]
 C["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 C["B03_service"]=p["service_income"]+p["service_expense"]-p["services"]
 C["B03_other"]=p["other_income"]+p["other_expense"]-p["other_op"]
 C["B03_income"]=S(p,("net_interest","services","FX","trading","investment","other_op","contribution"))-p["revenue"]
 C["B03_preprov"]=p["revenue"]-p["opex"]-p["before_prov"]
 C["B03_pbt"]=p["before_prov"]-p["provision"]-p["pbt"]
 C["B03_tax"]=p["tax_current"]+p["tax_deferred"]-p["tax"]
 C["B03_PAT"]=p["pbt"]-p["tax"]-p["pat"]
 C["B03_nci"]=p["pat"]-p["nci"]-p["parent_pat"]
 C["B03_pbt_H1_bridge"]=p["pbt"]+q1["B03a_Q1_original_million_vnd"]["pbt"]-a["B03a_H1_comparator"]["pretax_profit"]
 C["B03_PAT_H1_bridge"]=p["pat"]+q1["B03a_Q1_original_million_vnd"]["pat"]-a["B03a_H1_comparator"]["net_profit"]
 for name,c in (("original",o),("PwC",e)):
  C[name+"_preWC"]=S(c,("interest_received","interest_paid","service_cash","FX_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["before_wc"]
  C[name+"_assets"]=S(c,("wc_asset_interbank","wc_asset_trading","wc_asset_derivatives","wc_asset_loans","wc_asset_credit_provision","wc_asset_other"))-c["wc_assets"]
  C[name+"_liabs"]=S(c,("wc_liabs_government","wc_liabs_interbank","wc_liabs_customer_deposits","wc_liabs_valuable_papers","wc_liabs_trust","wc_liabs_derivative","wc_liabs_other","wc_liabs_reserves"))-c["wc_liabs"]
  C[name+"_trueCFO"]=c["before_wc"]+c["wc_assets"]+c["wc_liabs"]-c["CFO"]
  C[name+"_CFI"]=S(c,("capex","asset_sales","asset_disposal_expense","dividends_invest"))-c["CFI"]
  C[name+"_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net"]
  C[name+"_FXcash"]=c["opening"]+c["net"]+c["FX_cash"]-c["closing"]
 C["classification_CFO"]=e["CFO"]-o["CFO"]+79310
 C["classification_CFI"]=e["CFI"]-o["CFI"]-79310
 C["classification_liabs"]=e["wc_liabs_other"]-o["wc_liabs_other"]+79310
 C["classification_capex"]=e["capex"]-o["capex"]-79310
 C["classification_net"]=e["net"]-o["net"]
 C["classification_FX"]=e["FX_cash"]-o["FX_cash"]
 for k in ("CFO","CFI","CFF","net","FX_cash","capex"):
  C["Q2_"+k]=e[k]-q1_b04[k]-q[k]
 C["Q2_open"]=q1_b04["closing"]-q["opening"]
 C["Q2_end"]=e["closing"]-q["closing"]
 C["Q2_cashflow"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net"]
 C["Q2_fx_cash"]=q["opening"]+q["net"]+q["FX_cash"]-q["closing"]
 assert len(C)==45 and C==a["source_accounting_zero_residual_million_vnd"] and all(v==0 for v in C.values()),C
 assert a["source_vintage_PwC_less_issuer"]=={"CFO":-79310,"CFI":79310,"CFF":0,"net":0,"FX_cash":0,"closing":0,"wc_liabs_other":-79310,"capex":79310}
 assert (b["assets"],b["liabs"],b["equity"])==(2609788006,2445961810,163826196)
 assert (p["pbt"],p["pat"],p["parent_pat"],p["provision"],p["before_prov"])==(12097152,9752005,9669885,2972768,15069920)
 assert (o["CFO"],o["CFI"],o["CFF"],o["net"],o["FX_cash"],o["closing"])==(18334950,-661227,0,17673723,181069,391174348)
 assert (e["CFO"],e["CFI"],e["CFF"],e["net"],e["FX_cash"],e["closing"])==(18255640,-581917,0,17673723,181069,391174348)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net"],q["FX_cash"],q["opening"],q["closing"])==(27016581,-358420,0,26658161,200739,364315448,391174348)
 assert data["symbol"]=="CTG" and len(data["items"])==7
 assert [x["period"] for x in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert data["items"][0]["verification_status"]=="issuer_signed_CTG_2025Q1_consolidated_B02a_B03a_B04a_true_CFO_FX_exact_verified"
 assert data["items"][6]["verification_status"]==LOCKED_Q3 and data["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 row=data["items"][1];sv=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert sv["original_pdf_hash_verified"] and sv["original_pdf_sha256"]==ORIGINAL and sv["PwC_reviewed_H1_pdf_sha256"]==PWC
 assert sv["original_source_run"]==45343490708 and sv["source_audit_ledger"]==str(AUDIT.relative_to(R))
 assert sv["bank_PwC_H1_minus_signed_Q1_FX_cash_exact"] and sv["PwC_reviewed_H1_CFO_reclassification_million"]==-79310 and sv["PwC_reviewed_H1_CFI_reclassification_million"]==79310
 assert sv["PwC_other_liabs_reclass_million"]==-79310 and sv["PwC_capex_reclass_million"]==79310
 mapped={"total_assets":b["assets"],"total_liabilities":b["liabs"],"equity":b["equity"],
 "revenue":p["revenue"],"pretax_profit":p["pbt"],"net_profit":p["pat"],"net_profit_attributable":p["parent_pat"],
 "bank_pre_provision_operating_profit":p["before_prov"],"bank_provision_expense":p["provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net"],"cashflow_fx":q["FX_cash"],"cash_beginning":q["opening"],"cash_ending":q["closing"],
 "operating_cash_flow_ytd":e["CFO"],"investing_cash_flow_ytd":e["CFI"],
 "financing_cash_flow_ytd":e["CFF"],"net_cash_change_ytd":e["net"],"cashflow_fx_ytd":e["FX_cash"]}
 for field,val in mapped.items():assert row[field]==val,(field,row.get(field),val)
 for prefix,obj in (("b02a",b),("b03a",p),("b04a_PwC_H1",e)):
  for k,v in obj.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["roa"]==1.54 and row["roe"]==24.34 and row["eps"] is None
 assert row["financial_line_items_rejected_fields"]==[] and row["financial_line_items_rejected_values"]=={}
 assert all(x["period"]>="2025-Q1" for x in data["items"])
 return len(C),len(mapped)
def main():
 a=json.loads(AUDIT.read_text("utf8"));p=json.loads(Q1.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 n,m=check(a,p,d)
 cases=("origSHA","PwCSHA","source_Q1SHA","B02asset","B02liab","B02equity","B03revenue","B03provision","B03pat","H1profit","B04_preWC","B04_assets","B04_liabs","B04_orig_CFO","B04_PwC_CFO","B04_PwC_CFI","B04_CFF_2024_comparator","B04_net","B04_FX","capex_vintage","other_liabs_vintage","reclass_source_mismatch","reclass_ledger_mismatch","Q2_CFO_preWC_error","Q2_CFI_wrong","Q2_CFF_comparator","Q2_fx_wrong","Q2_end","Q1_CFO_locked","Q3_2026_locked","EPS_YTD_as_quarter","2024_dashboard")
 for kind in cases:
  aa,pp,dd=copy.deepcopy(a),copy.deepcopy(p),copy.deepcopy(d)
  b,pbt,o,e,q=(aa[k] for k in ("B02a_PwC_H1","B03a_Q2_signed_direct","B04a_Q2_original_H1","B04a_PwC_reviewed_H1","B04a_Q2_PwC_reviewed_H1_minus_Q1"))
  row=dd["items"][1]
  if kind=="origSHA":aa["sources"]["issuer_Q2_original"]["pdf_sha256"]="0"*64
  elif kind=="PwCSHA":aa["sources"]["PwC_H1_reviewed"]["pdf_sha256"]="0"*64
  elif kind=="source_Q1SHA":aa["sources"]["prior_Q1_original_pdf_sha256"]="0"*64
  elif kind=="B02asset":b["assets"]+=1
  elif kind=="B02liab":b["liabs"]+=1
  elif kind=="B02equity":b["equity"]+=1
  elif kind=="B03revenue":pbt["revenue"]+=1
  elif kind=="B03provision":pbt["provision"]+=1
  elif kind=="B03pat":row["net_profit"]+=1
  elif kind=="H1profit":aa["B03a_H1_comparator"]["pretax_profit"]+=1
  elif kind=="B04_preWC":o["before_wc"]+=1
  elif kind=="B04_assets":o["wc_assets"]+=1
  elif kind=="B04_liabs":e["wc_liabs"]+=1
  elif kind=="B04_orig_CFO":o["CFO"]+=1
  elif kind=="B04_PwC_CFO":e["CFO"]+=1
  elif kind=="B04_PwC_CFI":e["CFI"]+=1
  elif kind=="B04_CFF_2024_comparator":e["CFF"]=1537
  elif kind=="B04_net":e["net"]+=1
  elif kind=="B04_FX":e["FX_cash"]+=1
  elif kind=="capex_vintage":e["capex"]+=1
  elif kind=="other_liabs_vintage":e["wc_liabs_other"]+=1
  elif kind=="reclass_source_mismatch":aa["source_vintage_PwC_less_issuer"]["CFO"]=0
  elif kind=="reclass_ledger_mismatch":aa["source_accounting_zero_residual_million_vnd"]["classification_CFO"]=1
  elif kind=="Q2_CFO_preWC_error":row["operating_cash_flow"]=e["before_wc"]
  elif kind=="Q2_CFI_wrong":row["investing_cash_flow"]+=1
  elif kind=="Q2_CFF_comparator":row["financing_cash_flow"]=1537
  elif kind=="Q2_fx_wrong":row["cashflow_fx"]+=1
  elif kind=="Q2_end":row["cash_ending"]+=1
  elif kind=="Q1_CFO_locked":pp["B04a_Q1_original_million_vnd"]["CFO"]+=1
  elif kind=="Q3_2026_locked":dd["items"][6]["verification_status"]="pending"
  elif kind=="EPS_YTD_as_quarter":row["eps"]=1
  elif kind=="2024_dashboard":dd["items"].append({"period":"2024-Q4"})
  try:check(aa,pp,dd)
  except (AssertionError,KeyError,IndexError,TypeError):pass
  else:raise AssertionError("CTG 2025Q2 reclassification tamper escaped: "+kind)
 print(f"PASS CTG Q2 2025 signed original 62p vs PwC-reviewed H1 76p, {n} zero source identities, {m} normalized mappings, {len(cases)} negative tamper checks")
 print("PASS reclass +79,310 CFI/-79,310 CFO from fixed asset capex and other operating liabilities, same net and FX, true Q2 CFO +27,016,581 CFI -358,420 CFF 0 FX +200,739 cash 391,174,348; locked Q1 and Q3/2026")
if __name__=="__main__":main()
