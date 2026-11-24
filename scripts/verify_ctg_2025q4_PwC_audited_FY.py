#!/usr/bin/env python3
"""CTG 2025Q4 signed issuer original vs independently PwC audited FY:
material audit adjustment 13,824 million PAT/equity > 0.01% → audited FY less signed 9M.
Verify bank original and audited B02 B03 B04, FY cash and FX Q4 bridge without plugs.
"""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/CTG-2025Q4-original-PwC-audited-FY-million-vnd.json"
Q3=ROOT/"reports/source-audits/CTG-2025Q3-original-9M-PwC-H1-million-vnd.json"
FIN=ROOT/"data/financials-CTG.json"
SHA="4021fffc0b009734f2092a976c81a0dd91213b9735deb12aaf38087e5540e219"
PWC="b82eeb879b667e80d0b5322969c808089fd39b83835b75dc47f9a890189fc137"
Q3SHA="255b340f3eb40e53e641e661d688671bd9cb3b0cfb86df155b77960424bd7543"
STATUS="issuer_signed_CTG_2025Q4_original_B02a_B03a_PwC_audited_FY_minus_9M_B04a_material_13824_verified"
LOCKS={"2025-Q1":"issuer_signed_CTG_2025Q1_consolidated_B02a_B03a_B04a_true_CFO_FX_exact_verified",
"2025-Q2":"issuer_signed_CTG_2025Q2_original_B02a_B03a_PwC_H1_minus_Q1_B04a_79310_reclass_verified",
"2025-Q3":"issuer_signed_CTG_2025Q3_original_B02a_B03a_9M_minus_PwC_H1_B04a_FX_exact_verified",
"2026-Q3":"issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"}
def verify(a,prior,data):
 assert (a["ticker"],a["period"],a["scope"],a["unit"])==("CTG","2025-Q4","consolidated","triệu VND")
 s=a["source"]
 assert (s["original_Q4_sha256"],s["original_Q4_pages"],s["original_Q4_bytes"])==(SHA,60,5802979)
 assert (s["audited_FY_sha256"],s["audited_FY_pages"],s["audited_FY_bytes"])==(PWC,85,11853560)
 assert s["source_inspection_run"]==45345237202 and s["reviewer"]=="PwC (Vietnam) Limited"
 assert s["prior_signed_9M_pdf_sha256"]==prior["original_source"]["pdf_sha256"]==Q3SHA
 b,bo,p,po,y,yo,q=(a[k] for k in ("B02a_PwC_audited_FY","B02a_first_issued_Q4",
 "B03a_PwC_audited_standalone_Q4","B03a_first_issued_direct_Q4","B04a_PwC_audited_FY",
 "B04a_first_issued_FY","B04a_standalone_Q4_audited_FY_minus_9M"))
 real9m=prior["B04a_9M_original_signed"]
 for k,v in a["B04a_signed_prior_9M"].items():assert real9m[k]==v,(k,real9m.get(k),v)
 assert a["B03a_prior_signed_9M"]==prior["B03a_original_9M_ytd"]
 A=("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","investment_securities","long_investments","fixed_assets","other_assets")
 L=("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities")
 EQ=("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity")
 P=("net_interest","services","FX","trading","investment","other_op","contribution")
 PRE=("interest_received","interest_paid","service_cash","FX_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid")
 CA=("wc_asset_interbank","wc_asset_trading","wc_asset_derivatives","wc_asset_loans","wc_asset_credit_provision","wc_asset_other")
 CL=("wc_liabs_government","wc_liabs_interbank","wc_liabs_customer_deposits","wc_liabs_valuable_papers","wc_liabs_trust","wc_liabs_derivative","wc_liabs_other","wc_liabs_reserves")
 def S(x,keys):return sum(x[k] for k in keys)
 E={}
 for name,x in (("original",bo),("PwC",b)):
  E[name+"_B02assets"]=S(x,A)-x["assets"]
  E[name+"_B02liabs"]=S(x,L)-x["liabs"]
  E[name+"_B02equity"]=S(x,EQ)-x["equity"]
  E[name+"_B02balance"]=x["assets"]-x["liabs"]-x["equity"]
 for name,x in (("original",po),("PwC",p)):
  E[name+"_interest"]=x["interest_income"]+x["interest_expense"]-x["net_interest"]
  E[name+"_service"]=x["service_income"]+x["service_expense"]-x["services"]
  E[name+"_other"]=x["other_income"]+x["other_expense"]-x["other_op"]
  E[name+"_revenue"]=S(x,P)-x["revenue"]
  E[name+"_preprovision"]=x["revenue"]-x["opex"]-x["before_prov"]
  E[name+"_pretax"]=x["before_prov"]-x["provision"]-x["pbt"]
  E[name+"_tax"]=x["tax_current"]+x["tax_deferred"]-x["tax"]
  E[name+"_PAT"]=x["pbt"]-x["tax"]-x["pat"]
  E[name+"_parentPAT"]=x["pat"]-x["nci"]-x["parent_pat"]
 for name,x in (("original",yo),("PwC",y)):
  E[name+"_preWC"]=S(x,PRE)-x["before_wc"]
  E[name+"_wcAssets"]=S(x,CA)-x["wc_assets"]
  E[name+"_wcLiabs"]=S(x,CL)-x["wc_liabs"]
  E[name+"_CFO"]=x["before_wc"]+x["wc_assets"]+x["wc_liabs"]-x["CFO"]
  E[name+"_CFI"]=x["capex"]+x["asset_sales"]+x["asset_disposal_expense"]+x["dividends_invest"]-x["CFI"]
  E[name+"_net"]=x["CFO"]+x["CFI"]+x["CFF"]-x["net"]
  E[name+"_FXcash"]=x["opening"]+x["net"]+x["FX_cash"]-x["closing"]
 delta=a["PwC_adjustments_to_first_issued_million_vnd"]
 EXPECT={"B02_liabilities":-13824,"B02_equity":13824,"B03_expense":2145,"B03_preprovision":-2145,
 "B03_pretax":-2145,"B03_tax":-15969,"B03_PAT":13824,"B03_parent_PAT":13824,
 "B04_preWC":-2145,"B04_liabs":2145,"B04_CFO":0,"B04_CFI":0,"B04_CFF":0,
 "B04_net":0,"B04_FX_cash":0,"B04_close":0}
 assert delta==EXPECT
 E["vintage_equity"]=b["equity"]-bo["equity"]-delta["B02_equity"]
 E["vintage_liab"]=b["liabs"]-bo["liabs"]-delta["B02_liabilities"]
 E["vintage_expense"]=p["opex"]-po["opex"]-delta["B03_expense"]
 E["vintage_pretax"]=p["pbt"]-po["pbt"]-delta["B03_pretax"]
 E["vintage_tax"]=p["tax"]-po["tax"]-delta["B03_tax"]
 E["vintage_PAT"]=p["pat"]-po["pat"]-delta["B03_PAT"]
 E["vintage_cashWC"]=y["before_wc"]-yo["before_wc"]-delta["B04_preWC"]
 E["vintage_cfo_liab"]=y["wc_liabs"]-yo["wc_liabs"]-delta["B04_liabs"]
 E["vintage_CFO"]=y["CFO"]-yo["CFO"]
 for k in ("CFO","CFI","CFF","net","FX_cash","capex"):
  E["quarter_"+k]=y[k]-real9m[k]-q[k]
 E["quarter_start"]=q["opening"]-real9m["closing"]
 E["quarter_finish"]=q["closing"]-y["closing"]
 E["quarter_cashflows"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net"]
 E["quarter_FXcash"]=q["opening"]+q["net"]+q["FX_cash"]-q["closing"]
 nine=prior["B03a_original_9M_ytd"]
 auditedFY,firstFY=(a[k] for k in ("B03a_PwC_audited_FY_2025","B03a_first_issued_FY_2025"))
 E["Q4_PBT"]=auditedFY["pretax_profit"]-nine["pretax_profit"]-p["pbt"]
 E["Q4_PAT"]=auditedFY["net_profit"]-nine["net_profit"]-p["pat"]
 E["Q4_parent"]=auditedFY["parent_profit"]-nine["parent_profit"]-p["parent_pat"]
 E["Q4_beforeProvision"]=auditedFY["before_provision"]-46481879-p["before_prov"]
 E["Q4_provision"]=auditedFY["credit_provision"]-16947139-p["provision"]
 assert len(E)==64 and E==a["source_zero_residuals_million_vnd"] and all(v==0 for v in E.values()),E
 assert (bo["liabs"],bo["equity"],b["liabs"],b["equity"],b["assets"])==(2588058119,179641181,2588044295,179655005,2767699300)
 assert (po["pbt"],po["pat"],p["pbt"],p["pat"],p["parent_pat"])==(13911214,11093587,13909069,11107411,11066937)
 assert (firstFY["pretax_profit"],firstFY["net_profit"],auditedFY["pretax_profit"],auditedFY["net_profit"])==(43445954,34857442,43443809,34871266)
 assert (y["CFO"],y["CFI"],y["CFF"],y["net"],y["FX_cash"],y["closing"])==(82644000,-1915192,-2416496,78312312,113607,451745475)
 assert (yo["CFO"],yo["CFI"],yo["CFF"],yo["net"],yo["FX_cash"],yo["closing"])==(82644000,-1915192,-2416496,78312312,113607,451745475)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net"],q["FX_cash"],q["opening"],q["closing"])==(-2378836,-760506,-2416496,-5555838,-60661,457361974,451745475)
 assert abs(p["pat"]-po["pat"])/abs(po["pat"])*100 > a["rules"]["source_tolerance_pct"]
 assert a["rules"]["material_audit_adjustment_requires_audited_override"]
 assert [x["period"] for x in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 for i in (0,1,2,6):assert data["items"][i]["verification_status"]==LOCKS[data["items"][i]["period"]]
 assert data["items"][6]["source_validation"]["original_pdf_sha256"]=="0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e"
 row=data["items"][3];v=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert v["original_pdf_hash_verified"] and v["original_pdf_sha256"]==SHA and v["PwC_audited_FY_pdf_sha256"]==PWC
 assert v["source_accounting_64_zero_identities"] and v["material_audit_adjustment_above_0_01pct_replaced_first_issue_PBT_PAT"]
 assert v["cashflow_FY_minus_signed_9M_FX_exact"] and v["original_and_PwC_FY_CFO_CFI_CFF_net_cash_identical"]
 assert v["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 mapped={"total_assets":b["assets"],"total_liabilities":b["liabs"],"equity":b["equity"],
 "revenue":p["revenue"],"pretax_profit":p["pbt"],"net_profit":p["pat"],"net_profit_attributable":p["parent_pat"],
 "bank_pre_provision_operating_profit":p["before_prov"],"bank_provision_expense":p["provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],"financing_cash_flow":q["CFF"],
 "net_cash_change":q["net"],"cashflow_fx":q["FX_cash"],"cash_beginning":q["opening"],
 "cash_ending":q["closing"],"operating_cash_flow_ytd":y["CFO"],"investing_cash_flow_ytd":y["CFI"],
 "financing_cash_flow_ytd":y["CFF"],"net_cash_change_ytd":y["net"],"cashflow_fx_ytd":y["FX_cash"]}
 for k,amount in mapped.items():assert row[k]==amount,(k,row.get(k),amount)
 for prefix,obj in (("b02a_PwC_FY",b),("b03a_Q4_PwC_FY_minus_9M",p),("b04a_PwC_FY",y)):
  for k,amount in obj.items():assert row["signed_source_"+prefix+"_"+k]==amount,(prefix,k)
 assert row["roa"]==1.61 and row["roe"]==25.33 and row["eps"] is None
 assert all(x["period"]>="2025-Q1" for x in data["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(LEDGER.read_text("utf8"));prev=json.loads(Q3.read_text("utf8"));d=json.loads(FIN.read_text("utf8"))
 n,m=verify(a,prev,d)
 tests=("issuerSHA","PwCSHA","priorQ3SHA","audited_asset","signed_asset","audited_liabs",
 "audit_equity","source_vintage_equity","source_tax_vintage","source_pretax_vintage",
 "audited_PBT","source_original_PBT","audited_PAT","source_original_PAT","audited_opex",
 "audited_before_prov","original_beforeWC","PwC_beforeWC","audited_other_liabs",
 "original_other_liabs","audited_CFO","original_CFO","audited_CFI","audited_CFF",
 "FY_net","FY_FX","Q4_CFO","Q4_CFI","Q4_CFF","Q4_net","Q4_FX","Q4_open","Q4_end",
 "prior9M_CFO","prior9M_PBT","first_issue_as_audited_PAT","first_issue_as_audited_equity",
 "ignore_material_threshold","prior2025Q3_locked","prior2025Q1_locked","2026Q3_locked",
 "EPS_unverified","2024_dashboard","audit_liability_reclass_wrong","identity_forgery")
 for case in tests:
  aa,pp,dd=copy.deepcopy(a),copy.deepcopy(prev),copy.deepcopy(d)
  b,bo,p,po,y,yo,q=(aa[k] for k in ("B02a_PwC_audited_FY","B02a_first_issued_Q4",
 "B03a_PwC_audited_standalone_Q4","B03a_first_issued_direct_Q4","B04a_PwC_audited_FY",
 "B04a_first_issued_FY","B04a_standalone_Q4_audited_FY_minus_9M"))
  row=dd["items"][3]
  if case=="issuerSHA":aa["source"]["original_Q4_sha256"]="0"*64
  elif case=="PwCSHA":aa["source"]["audited_FY_sha256"]="0"*64
  elif case=="priorQ3SHA":aa["source"]["prior_signed_9M_pdf_sha256"]="0"*64
  elif case=="audited_asset":b["assets"]+=1
  elif case=="signed_asset":bo["assets"]+=1
  elif case=="audited_liabs":b["liabs"]+=1
  elif case=="audit_equity":row["equity"]+=1
  elif case=="source_vintage_equity":aa["PwC_adjustments_to_first_issued_million_vnd"]["B02_equity"]+=1
  elif case=="source_tax_vintage":aa["PwC_adjustments_to_first_issued_million_vnd"]["B03_tax"]+=1
  elif case=="source_pretax_vintage":aa["PwC_adjustments_to_first_issued_million_vnd"]["B03_pretax"]+=1
  elif case=="audited_PBT":p["pbt"]+=1
  elif case=="source_original_PBT":po["pbt"]+=1
  elif case=="audited_PAT":row["net_profit"]+=1
  elif case=="source_original_PAT":po["pat"]+=1
  elif case=="audited_opex":p["opex"]+=1
  elif case=="audited_before_prov":p["before_prov"]+=1
  elif case=="original_beforeWC":yo["before_wc"]+=1
  elif case=="PwC_beforeWC":y["before_wc"]+=1
  elif case=="audited_other_liabs":y["wc_liabs_other"]+=1
  elif case=="original_other_liabs":yo["wc_liabs_other"]+=1
  elif case=="audited_CFO":y["CFO"]+=1
  elif case=="original_CFO":yo["CFO"]+=1
  elif case=="audited_CFI":y["CFI"]+=1
  elif case=="audited_CFF":y["CFF"]+=1
  elif case=="FY_net":y["net"]+=1
  elif case=="FY_FX":y["FX_cash"]+=1
  elif case=="Q4_CFO":row["operating_cash_flow"]+=1
  elif case=="Q4_CFI":row["investing_cash_flow"]+=1
  elif case=="Q4_CFF":row["financing_cash_flow"]+=1
  elif case=="Q4_net":q["net"]+=1
  elif case=="Q4_FX":q["FX_cash"]+=1
  elif case=="Q4_open":row["cash_beginning"]+=1
  elif case=="Q4_end":row["cash_ending"]+=1
  elif case=="prior9M_CFO":pp["B04a_9M_original_signed"]["CFO"]+=1
  elif case=="prior9M_PBT":pp["B03a_original_9M_ytd"]["pretax_profit"]+=1
  elif case=="first_issue_as_audited_PAT":row["net_profit"]=11093587
  elif case=="first_issue_as_audited_equity":row["equity"]=179641181
  elif case=="ignore_material_threshold":aa["rules"]["source_tolerance_pct"]=1
  elif case=="prior2025Q3_locked":dd["items"][2]["verification_status"]="pending"
  elif case=="prior2025Q1_locked":dd["items"][0]["verification_status"]="pending"
  elif case=="2026Q3_locked":dd["items"][6]["verification_status"]="pending"
  elif case=="EPS_unverified":row["eps"]=2
  elif case=="2024_dashboard":dd["items"].append({"period":"2024-Q4"})
  elif case=="audit_liability_reclass_wrong":aa["PwC_adjustments_to_first_issued_million_vnd"]["B02_liabilities"]+=1
  elif case=="identity_forgery":aa["source_zero_residuals_million_vnd"]["PwC_CFO"]=1
  try:verify(aa,pp,dd)
  except (AssertionError,KeyError,TypeError,IndexError,ValueError):pass
  else:raise AssertionError("CTG Q4 2025 audited source tamper escaped: "+case)
 print(f"PASS CTG Q4 2025 signed issuer 60p vs PwC audited FY 85p: {n} exact source accounting identities, {m} mapped key fields, {len(tests)} source tamper checks")
 print("PASS material audited FY 2025 delta PAT+13,824, equity+13,824, liabilities-13,824 and PBT-2,145; production Q4 audited PBT 13,909,069, PAT 11,107,411")
 print("PASS audited FY-minus-signed 9M Q4 CFO -2,378,836 CFI -760,506 CFF -2,416,496 net -5,555,838 FX -60,661 cash 457,361,974 -> 451,745,475; prior CTG checkpoints locked")
if __name__=="__main__":main()
