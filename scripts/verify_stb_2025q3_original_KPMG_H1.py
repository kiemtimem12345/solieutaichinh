#!/usr/bin/env python3
"""STB 2025Q3 signed issuer B02/B03 and 9M-minus-KPMG-reviewed-H1 bank B04 exact FX.
Original 9M B04 component source has a +200 million OCR/print residual (0.000574% of CFO);
DO NOT balance-force it. Validate against source CFO, acceptance threshold <=0.01%.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/source-audits/STB-2025Q3-original-9M-KPMG-reviewed-H1-million-vnd.json"
PRIOR=ROOT/"reports/source-audits/STB-2025Q2-original-KPMG-reviewed-H1-million-vnd.json"
DATA=ROOT/"data/financials-STB.json"
STATUS="issuer_signed_STB_2025Q3_original_B02a_B03a_9M_minus_KPMG_H1_B04a_FX_tolerance_verified"
SHA="653a4124dc782bc56ff3dd95a7d4f51ff14d7fcfcbac65e504947cc62cac8518"
def test(a,prev,d):
 assert (a["symbol"],a["period"],a["unit"],a["scope"])==("STB","2025-Q3","triệu VND","consolidated")
 assert a["source"]["original_sha256"]==SHA and a["source"]["original_bytes"]==3192234
 assert a["source"]["original_pages"]==47 and a["source"]["original_workflow_run"]==45266774366
 assert a["source"]["KPMG_H1_sha256"]==prev["source"]["KPMG_H1_reviewed"]["sha256"]
 b,p,c,q,h=(a[k] for k in ("B02a_original","B03a_Q3_direct","B04a_original_9M","B04a_Q3_9M_less_KPMG_H1","KPMG_H1_comparator"))
 h0=prev["B04a_6M_KPMG_reviewed"]
 assert all(h[k]==h0[k] for k in h)
 def sm(o,keys):return sum(o[k] for k in keys)
 E={}
 E["assets"]=sm(b,("cash_vault","deposits_SBV","interbank_assets","trading_securities",
 "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
 "longterm_investments","fixed_assets","investment_property","other_assets"))-b["total_assets"]
 E["liab"]=sm(b,("gov_liabs","interbank_liabs","customer_deposits","derivative_liabs",
 "trust_liabs","valuable_papers","other_liabs"))-b["total_liabilities"]
 E["equity"]=sm(b,("capital","reserves","fx_reserve","retained","minority"))-b["total_equity"]
 E["balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 E["operating"]=sm(p,("net_interest","services_net","FX_net","trading_net",
 "invest_net","other_net","contribution_income"))-p["operating_income"]
 E["preprov"]=p["operating_income"]-p["operating_expenses"]-p["before_provision"]
 E["provision"]=p["before_provision"]-p["credit_provision"]-p["pretax_profit"]
 E["tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["PAT"]=p["pretax_profit"]-p["income_tax"]-p["net_profit"]
 E["parent"]=p["net_profit"]-p["noncontrolling_profit"]-p["parent_profit"]
 E["9M_preWC"]=sm(c,("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
 "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["9M_CFO_component_residual"]=c["pre_wc_cash"]+sm(c,("assets_interbank","assets_securities",
 "assets_derivatives","assets_customer_loans","assets_credit_provisions","assets_other",
 "liabs_government","liabs_interbank","liabs_customer_deposits","liabs_valuable_papers",
 "liabs_trust","liabs_derivatives","liabs_other","payments_from_bank_reserves"))-c["CFO"]
 E["9M_CFI"]=sm(c,("capex","asset_disposals","investment_distributions"))-c["CFI"]
 E["9M_CFF"]=c["financing_bonds_issued"]+c["financing_bonds_repaid"]-c["CFF"]
 E["9M_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["9M_cash_FX"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 for k in ("CFO","CFI","CFF","net_cash_change","FX_effect","capex"):
  E["Q3_"+k]=c[k]-h[k]-q[k]
 E["Q3_open"]=h["closing_cash"]-q["opening_cash"]
 E["Q3_close"]=c["closing_cash"]-q["closing_cash"]
 E["Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["Q3_cash_FX"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 assert len(E)>=28
 assert all(v==0 for k,v in E.items() if k!="9M_CFO_component_residual"), E
 assert E["9M_CFO_component_residual"]==200,E
 assert a["source_identity_residuals"]["source_CFO_components"]==200
 assert all(v==0 for k,v in a["source_identity_residuals"].items() if k!="source_CFO_components")
 assert 100*abs(E["9M_CFO_component_residual"])/abs(c["CFO"])<=0.01
 assert a["rules"]["accepted_source_component_residual_pct_max"]==0.01
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(848942045,786237253,62704792)
 assert (p["operating_income"],p["pretax_profit"],p["net_profit"])==(8796519,3656898,2901283)
 assert a["B03a_original_9M_YTD"]["pretax_profit"]-7331272==p["pretax_profit"]
 assert a["B03a_original_9M_YTD"]["net_profit"]-5790290==p["net_profit"]
 assert (c["CFO"],c["CFI"],c["CFF"],c["net_cash_change"],c["FX_effect"])==(34871233,-409902,-3386136,31075195,166291)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"],q["FX_effect"],q["opening_cash"],q["closing_cash"])==(11877929,-114593,499397,12262733,-18648,125490456,137734541)
 assert [x["period"] for x in d["items"]]==[
 "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 assert all(d["items"][k]["verification_status"].startswith("issuer_signed_STB_2025Q") for k in range(3))
 assert d["items"][2]["verification_status"]==STATUS
 assert [x["verification_status"] for x in d["items"]][3:]==[
 "issuer_signed_STB_2025Q4_original_B02a_B03a_KPMG_FY_minus_9M_B04a_FX_verified","issuer_signed_STB_2026Q1_original_B02a_B03a_B04a_FX_exact_verified","issuer_signed_STB_2026Q2_original_B02a_B03a_EY_H1_minus_Q1_B04a_FX_vintage_verified"]
 row=d["items"][2];sv=row["source_validation"]
 assert sv["original_pdf_sha256"]==SHA and sv["original_pdf_hash_verified"]
 assert sv["B04_original_source_components_CFO_residual_million_vnd"]==200
 assert sv["B04_original_residual_accepted_within_0_01pct"] and sv["no_balancing_plug"]
 assert sv["bank_9M_minus_KPMG_H1_FX_cash_exact"]
 assert sv["source_audit_ledger"]==str(SOURCE.relative_to(ROOT))
 mapped={"total_assets":b["total_assets"],"total_liabilities":b["total_liabilities"],
 "equity":b["total_equity"],"revenue":p["operating_income"],"pretax_profit":p["pretax_profit"],
 "net_profit":p["net_profit"],"net_profit_attributable":p["parent_profit"],
 "bank_pre_provision_operating_profit":p["before_provision"],"bank_provision_expense":p["credit_provision"],
 "operating_cash_flow":q["CFO"],"investing_cash_flow":q["CFI"],
 "financing_cash_flow":q["CFF"],"net_cash_change":q["net_cash_change"],
 "cashflow_fx":q["FX_effect"],"cash_beginning":q["opening_cash"],"cash_ending":q["closing_cash"],
 "operating_cash_flow_ytd":c["CFO"],"investing_cash_flow_ytd":c["CFI"],
 "financing_cash_flow_ytd":c["CFF"],"net_cash_change_ytd":c["net_cash_change"],
 "cashflow_fx_ytd":c["FX_effect"],"capital_expenditure":q["capex"]}
 for k,v in mapped.items():assert row[k]==v,(k,row.get(k),v)
 for prefix,ob in (("b02a",b),("b03a",p),("b04a_original_9M",c)):
  for k,v in ob.items():assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert row["roa"]==1.4 and row["roe"]==18.94
 assert row["eps"] is None and row["eps_ytd"]==6519
 assert not any(v["period"].startswith("2024") for v in d["items"])
 return len(E),len(mapped)
def main():
 a=json.loads(SOURCE.read_text("utf8"));prior=json.loads(PRIOR.read_text("utf8"));d=json.loads(DATA.read_text("utf8"))
 n,m=test(a,prior,d)
 cases=("asset","liabs","equity","income","pretax","pat","credit_provision",
 "CFO_not_preWC","9M_CFO","9M_CFI","9M_CFF","9M_fx","cash_end",
 "quarter_CFO","quarter_CFI","quarter_CFF","quarter_net","quarter_fx","quarter_open",
 "KPMG_H1_CFO","KPMG_H1_FX","200m_residual_replaced","tolerance_forged",
 "source_SHA","prior_H1_SHA","Q1_status","Q2_status","premature_Q4",
 "EPS_source_9M_as_quarter","2024_period")
 for name in cases:
  aa,pp,dd=copy.deepcopy(a),copy.deepcopy(prior),copy.deepcopy(d)
  if name=="asset":aa["B02a_original"]["total_assets"]+=1
  elif name=="liabs":dd["items"][2]["total_liabilities"]+=1
  elif name=="equity":dd["items"][2]["equity"]+=1
  elif name=="income":aa["B03a_Q3_direct"]["operating_income"]+=1
  elif name=="pretax":aa["B03a_Q3_direct"]["pretax_profit"]+=1
  elif name=="pat":dd["items"][2]["net_profit"]+=1
  elif name=="credit_provision":aa["B03a_Q3_direct"]["credit_provision"]+=1
  elif name=="CFO_not_preWC":dd["items"][2]["operating_cash_flow"]=13008377
  elif name=="9M_CFO":aa["B04a_original_9M"]["CFO"]+=1
  elif name=="9M_CFI":aa["B04a_original_9M"]["CFI"]+=1
  elif name=="9M_CFF":aa["B04a_original_9M"]["CFF"]+=1
  elif name=="9M_fx":aa["B04a_original_9M"]["FX_effect"]+=1
  elif name=="cash_end":dd["items"][2]["cash_ending"]+=1
  elif name=="quarter_CFO":dd["items"][2]["operating_cash_flow"]+=1
  elif name=="quarter_CFI":dd["items"][2]["investing_cash_flow"]+=1
  elif name=="quarter_CFF":dd["items"][2]["financing_cash_flow"]+=1
  elif name=="quarter_net":aa["B04a_Q3_9M_less_KPMG_H1"]["net_cash_change"]+=1
  elif name=="quarter_fx":aa["B04a_Q3_9M_less_KPMG_H1"]["FX_effect"]+=1
  elif name=="quarter_open":dd["items"][2]["cash_beginning"]+=1
  elif name=="KPMG_H1_CFO":pp["B04a_6M_KPMG_reviewed"]["CFO"]+=1
  elif name=="KPMG_H1_FX":pp["B04a_6M_KPMG_reviewed"]["FX_effect"]+=1
  elif name=="200m_residual_replaced":aa["B04a_original_9M"]["liabs_other"]-=200
  elif name=="tolerance_forged":aa["rules"]["accepted_source_component_residual_pct_max"]=1
  elif name=="source_SHA":aa["source"]["original_sha256"]="0"*64
  elif name=="prior_H1_SHA":aa["source"]["KPMG_H1_sha256"]="0"*64
  elif name=="Q1_status":dd["items"][0]["verification_status"]="pending"
  elif name=="Q2_status":dd["items"][1]["verification_status"]="pending"
  elif name=="premature_Q4":dd["items"][3]["verification_status"]="verified"
  elif name=="EPS_source_9M_as_quarter":dd["items"][2]["eps"]=6519
  elif name=="2024_period":dd["items"].append({"period":"2024-Q4"})
  try:test(aa,pp,dd)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("STB 2025 Q3 source corruption escaped: "+name)
 print(f"PASS STB 2025 Q3 signed original 9M vs KPMG H1: {n-1} zero identities, 1 retained 200-million VND B04 component residual (0.000574% CFO), {m} normalized checks, {len(cases)} negative tamper cases")
 print("PASS Q3 CFO +11,877,929 CFI -114,593 CFF +499,397 net +12,262,733 FX -18,648 opening 125,490,456 ending 137,734,541; Q1/Q2 unchanged")
if __name__=="__main__":main()
