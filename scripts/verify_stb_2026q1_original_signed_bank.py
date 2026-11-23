#!/usr/bin/env python3
"""STB Q1 2026 issuer signed consolidated source B02/B03/B04 exact identities.
Protect 2025 frozen verified periods, source SHA256, negative CFO vs pre-WC and bank FX.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"reports/source-audits/STB-2026Q1-original-signed-bank-million-vnd.json"
OLD=ROOT/"reports/source-audits/STB-2025Q4-original-KPMG-FY-bank-million-vnd.json"
DATA=ROOT/"data/financials-STB.json"
SHA="9bdfef933a655d731b26f51daf831971eb87498eaf570ed8872240ae7064cdbc"
STATUS="issuer_signed_STB_2026Q1_original_B02a_B03a_B04a_FX_exact_verified"
def check(a,old,data):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("STB","2026-Q1","consolidated","triệu VND")
 assert a["source"]["sha256"]==SHA and a["source"]["pages"]==45 and a["source"]["bytes"]==2966556
 assert a["source"]["source_inspection_run"]==45272591891
 b,p,c=(a[k] for k in ("B02a","B03a","B04a"))
 def sm(x,ks):return sum(x[k] for k in ks)
 E={}
 E["assets"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","investment_property","other_assets"))-b["total_assets"]
 E["liabs"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs","trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
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
 E["preWC"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["true_CFO"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities","assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other","liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers","liabs_trust","liabs_derivatives","liabs_other","payments_from_bank_reserves"))-c["CFO"]
 E["CFI"]=sm(c,("capex","asset_disposals","investment_distributions"))-c["CFI"]
 E["CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
 E["net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["FX"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 assert len(E)==19 and all(v==0 for v in E.values()), E
 assert a["source_identity_residuals"]==dict.fromkeys(E,0) or (len(a["source_identity_residuals"])==19 and all(v==0 for v in a["source_identity_residuals"].values()))
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(859571527,798094916,61476611)
 assert (p["before_provision"],p["credit_provision"],p["pretax_profit"],p["net_profit"])==(4130068,2023863,2106205,1584404)
 assert (c["pre_wc_cash"],c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"],c["opening_cash"],c["closing_cash"])==(3664141,-58545352,-128122,-24412,-58697886,10352,194472583,135785049)
 assert c["opening_cash"]==old["B04a_FY_KPMG_audited"]["closing_cash"]
 assert [r["period"] for r in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 assert all(x["verification_status"].startswith("issuer_signed_STB") for x in data["items"][:5])
 assert data["items"][4]["verification_status"]==STATUS
 assert data["items"][5]["verification_status"]=="issuer_signed_STB_2026Q2_original_B02a_B03a_EY_H1_minus_Q1_B04a_FX_vintage_verified"
 row=data["items"][4];v=row["source_validation"]
 assert v["original_pdf_hash_verified"] and v["original_pdf_sha256"]==SHA and v["original_pdf_pages"]==45
 assert v["source_audit_ledger"]==str(A.relative_to(ROOT)) and v["original_B04_FX_cash_bridge_exact"]
 map={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],"equity":b["total_equity"],
 "revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],"net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
 "bank_pre_provision_operating_profit":p["before_provision"],"bank_provision_expense":p["credit_provision"],
 "operating_cash_flow":c["CFO"],"investing_cash_flow":c["CFI"],"financing_cash_flow":c["CFF"],
 "net_cash_change":c["net_cash_change"],"cashflow_fx":c["FX_effect"],"cash_beginning":c["opening_cash"],"cash_ending":c["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],"financing_cash_flow_ytd":c["CFF"],
 "net_cash_change_ytd":c["net_cash_change"],"cashflow_fx_ytd":c["FX_effect"]}
 for k,value in map.items():assert row[k]==value,(k,row.get(k),value)
 for prefix,obj in (("b02a",b),("b03a",p),("b04a",c)):
  for k,val in obj.items():assert row["signed_source_"+prefix+"_"+k]==val,(prefix,k)
 assert row["roa"]==0.71 and row["roe"]==10.45 and row["eps"] is None and row["eps_ytd"]==2454
 assert not any(x["period"].startswith("2024") for x in data["items"])
 return len(E),len(map)
def main():
 a=json.loads(A.read_text("utf8"));o=json.loads(OLD.read_text("utf8"));d=json.loads(DATA.read_text("utf8"))
 n,m=check(a,o,d)
 cases=("SHA","assets","liabilities","equity","interest","service","FX_income","income",
 "provision","pretax","PAT","CFO_preWC","CFO","CFI","CFF","net","cash_FX",
 "source_CFO","source_CFI","source_CFF","source_cash","FY_cash_open","prior_Q4_locked",
 "premature_Q2","EPS_not_quarter","2024_quarter","reserve_sign","workcap_loan_flow")
 for case in cases:
  aa,oo,dd=copy.deepcopy(a),copy.deepcopy(o),copy.deepcopy(d)
  b,p,c=(aa[k] for k in ("B02a","B03a","B04a"));row=dd["items"][4]
  if case=="SHA":aa["source"]["sha256"]="0"*64
  elif case=="assets":b["total_assets"]+=1
  elif case=="liabilities":b["total_liabilities"]+=1
  elif case=="equity":b["total_equity"]+=1
  elif case=="interest":p["net_interest"]+=1
  elif case=="service":p["services_net"]+=1
  elif case=="FX_income":p["FX_net"]+=1
  elif case=="income":row["revenue"]+=1
  elif case=="provision":p["credit_provision"]+=1
  elif case=="pretax":p["pretax_profit"]+=1
  elif case=="PAT":row["net_profit"]+=1
  elif case=="CFO_preWC":row["operating_cash_flow"]=c["pre_wc_cash"]
  elif case=="CFO":row["operating_cash_flow"]+=1
  elif case=="CFI":row["investing_cash_flow"]+=1
  elif case=="CFF":row["financing_cash_flow"]+=1
  elif case=="net":c["net_cash_change"]+=1
  elif case=="cash_FX":c["FX_effect"]+=1
  elif case=="source_CFO":c["CFO"]+=1
  elif case=="source_CFI":c["CFI"]+=1
  elif case=="source_CFF":c["CFF"]+=1
  elif case=="source_cash":c["closing_cash"]+=1
  elif case=="FY_cash_open":oo["B04a_FY_KPMG_audited"]["closing_cash"]+=1
  elif case=="prior_Q4_locked":dd["items"][3]["verification_status"]="tampered"
  elif case=="premature_Q2":dd["items"][5]["verification_status"]="verified"
  elif case=="EPS_not_quarter":row["eps"]=2454
  elif case=="2024_quarter":dd["items"].append({"period":"2024-Q4"})
  elif case=="reserve_sign":b["fx_reserve"]=-b["fx_reserve"]
  elif case=="workcap_loan_flow":c["assets_customer_loans"]=-c["assets_customer_loans"]
  try:check(aa,oo,dd)
  except (AssertionError,KeyError,IndexError,TypeError):pass
  else:raise AssertionError("STB 2026Q1 source tamper escaped: "+case)
 print(f"PASS STB 2026Q1 source signed original 45p: {n} exact identities, {m} mapped fields, {len(cases)} negative tests")
 print("PASS true CFO -58,545,352 NOT pre-WC +3,664,141, CFI -128,122 CFF -24,412 FX +10,352, end 135,785,049; 2025 locked")
if __name__=="__main__":main()
