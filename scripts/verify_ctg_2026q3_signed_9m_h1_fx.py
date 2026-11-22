#!/usr/bin/env python3
"""CTG 2026Q3 issuer bank consolidated signed 9M and H1, exact million-VND.

Bank B04a direct method has a distinct exchange-rate adjustment; preserve
9M-minus-6M CFO/CFI/CFF and exchange FX separately. Never use gross
cash interest receipts as CFO, and never conflate parent-only bank reports.
"""
from pathlib import Path
import copy,json
R=Path(__file__).resolve().parents[1]
AUDIT=R/"reports/source-audits/CTG-2026Q3-consolidated-original-9M-minus-H1-million-vnd.json"
FIN=R/"data/financials-CTG.json"
def read(p):return json.loads(p.read_text("utf8"))
def proof(src):
 assert src["ticker"]=="CTG" and src["period"]=="2026-Q3" and src["unit"]=="triệu VND"
 assert "consolidated" in src["scope"]
 for src_id,digest,count,bytes_ in (
  ("original_Q3","0f1a77f5b3e799a6a67175a893727862ea094c8545c3250b2d36f6594b6e038e",62,5892629),
  ("original_H1","f7453816648cac21536621e09d4e52a40e8ce9fcdbaf824981b3b997a8197318",61,6703623)):
  z=src[src_id]
  assert z["pdf_sha256"]==digest and z["pages"]==count and z["bytes"]==bytes_
 assert src["source_workflow"]["run_id"]==45014360407 and src["source_workflow"]["visual_artifact_id"]==14751002244
 f=src["original_source_million_vnd"]
 assert len(f)==104 and all(type(v)==int for v in f.values())
 V=lambda k:f[k]
 S=lambda ks:sum(V(k) for k in ks)
 q={k:V(k+"_9m")-V(k+"_H1") for k in ("cfo","cfi","cff","net")}
 q["fx"]=V("fx_cash_9m")-V("fx_cash_H1")
 q["opening"]=V("close_H1");q["ending"]=V("close_9m")
 assert q==src["quarter_cashflow_million_vnd"]
 checks={
 "B02_balance":V("liabs")+V("equity")-V("assets"),
 "B02_assets":S(("cash_vault","deposits_SBV","interbank_assets","trading","derivative_asset","customer_loans","invest_securities","long_investments","fixed_assets","other_assets"))-V("assets"),
 "B02_liabs":S(("government_liabilities","interbank_liabilities","customer_deposit_liabilities","derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-V("liabs"),
 "B02_equity":S(("owner_capital","owner_funds","FX_equity","retained","noncontrolling_equity"))-V("equity"),
 "H1_balance":V("liabs_H1")+V("equity_H1")-V("assets_H1"),
 "Q3_revenue":S(("net_interest_q3","services_q3","FX_q3","trading_q3","investment_q3","other_op_q3","contribution_q3"))-V("revenue_q3"),
 "Q3_before":V("revenue_q3")-V("opex_q3")-V("before_prov_q3"),
 "Q3_pbt":V("before_prov_q3")-V("provision_q3")-V("pbt_q3"),
 "Q3_PAT":V("pbt_q3")-V("tax_q3")-V("pat_q3"),
 "Q3_nci":V("pat_q3")-V("nci_q3")-V("parent_pat_q3"),
 "H1_revenue":S(("net_interest_H1","services_H1","FX_H1","trading_H1","investment_H1","other_op_H1","contribution_H1"))-V("revenue_H1"),
 "H1_before":V("revenue_H1")-V("opex_H1")-V("before_prov_H1"),
 "H1_PBT":V("before_prov_H1")-V("provision_H1")-V("pbt_H1"),
 "H1_PAT":V("pbt_H1")-V("tax_H1")-V("pat_H1"),
 "Y9_revenue":S(("net_interest_9m","services_9m","FX_9m","trading_9m","investment_9m","other_op_9m","contribution_9m"))-V("revenue_9m"),
 "Y9_before":V("revenue_9m")-V("opex_9m")-V("before_prov_9m"),
 "Y9_PBT":V("before_prov_9m")-V("provision_9m")-V("pbt_9m"),
 "Y9_PAT":V("pbt_9m")-V("tax_9m")-V("pat_9m"),
 "B04_CFO_9m":V("cfo_before_wc_9m")+V("wc_assets_9m")+V("wc_liabs_9m")-V("cfo_9m"),
 "B04_CFO_H1":V("cfo_before_wc_H1")+V("wc_assets_H1")+V("wc_liabs_H1")-V("cfo_H1"),
 "B04_9M_sections":V("cfo_9m")+V("cfi_9m")+V("cff_9m")-V("net_9m"),
 "B04_H1_sections":V("cfo_H1")+V("cfi_H1")+V("cff_H1")-V("net_H1"),
 "B04_Q3_sections":q["cfo"]+q["cfi"]+q["cff"]-q["net"],
 "B04_9M_FX":V("open_9m")+V("net_9m")+V("fx_cash_9m")-V("close_9m"),
 "B04_H1_FX":V("open_H1")+V("net_H1")+V("fx_cash_H1")-V("close_H1"),
 "B04_Q3_FX":q["opening"]+q["net"]+q["fx"]-q["ending"],
 "B04_investing":S(("capex_9m","asset_disposal_9m","disposal_expense_9m","long_invest_cash_9m","dividend_invest_9m"))-V("cfi_9m"),
 "B04_financing":S(("long_term_financing_received_9m","long_term_financing_repaid_9m","dividends_paid_9m"))-V("cff_9m")
 }
 assert len(checks)==28 and set(checks)==set(src["source_zero_residual_million_vnd"])
 assert all(n==0 for n in checks.values()),checks
 assert all(int(src["source_zero_residual_million_vnd"][k])==n for k,n in checks.items())
 bridge_keys=("net_interest","services","FX","trading","investment","other_op","contribution","revenue","opex","before_prov","provision","pbt","tax","pat","nci","parent_pat")
 assert len(bridge_keys)==16 and set(bridge_keys)==set(src["q3_direct_vs_9m_less_h1_income_residual_million_vnd"])
 for k in bridge_keys:
  diff=V(k+"_9m")-V(k+"_H1")-V(k+"_q3")
  assert diff==0 and int(src["q3_direct_vs_9m_less_h1_income_residual_million_vnd"][k])==diff,k
 assert q["cfo"]==-19748243 and q["cfi"]==1804250 and q["cff"]==-4273630
 assert q["net"]==-22217623 and q["fx"]==-67131 and q["ending"]==520137917
 assert V("open_9m")==V("open_H1")==451745475
 return f,q
def verify(src,d):
 f,q=proof(src)
 assert d["symbol"]=="CTG" and len(d["items"])==7
 assert [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 r=d["items"][-1]
 assert r["verification_status"]=="issuer_signed_CTG_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1_FX_verified"
 assert r["unit"]=="triệu VND" and "hợp nhất" in r["report_type"].lower()
 assert r["source_url"]==src["original_Q3"]["url"] and r["cashflow_period_basis"]=="year_to_date"
 v=r["source_validation"]
 assert v["source_audit_ledger"]==str(AUDIT.relative_to(R))
 assert v["original_pdf_sha256"]==src["original_Q3"]["pdf_sha256"]
 assert v["H1_source_pdf_sha256"]==src["original_H1"]["pdf_sha256"]
 assert v["original_pdf_hash_verified"] and v["manually_visual_reviewed"] and v["source_is_consolidated_financial_statements"]
 assert v["original_source_28_bank_equations_zero_million"] and v["B03_Q3_16_direct_income_lines_equal_9M_minus_H1"]
 assert v["bank_B04_FX_aware_cash_bridge_zero_million"] and v["bank_B04_cash_sections_zero_million"]
 for k,num in f.items():assert r["signed_source_"+k]==num,(k,num,r.get("signed_source_"+k))
 a={"total_assets":"assets","total_liabilities":"liabs","equity":"equity","revenue":"revenue_q3",
    "pretax_profit":"pbt_q3","net_profit":"pat_q3","net_profit_attributable":"parent_pat_q3",
    "bank_cash_on_hand":"cash_vault","bank_customer_loans":"customer_loans",
    "bank_customer_deposits":"customer_deposit_liabilities",
    "operating_cash_flow_ytd":"cfo_9m","investing_cash_flow_ytd":"cfi_9m",
    "financing_cash_flow_ytd":"cff_9m","net_cash_change_ytd":"net_9m"}
 for k,key in a.items():assert r[k]==f[key],(k,r[k],f[key])
 for k,col in (("operating_cash_flow","cfo"),("investing_cash_flow","cfi"),("financing_cash_flow","cff"),
    ("net_cash_change","net"),("cashflow_fx","fx"),("cash_beginning","opening"),("cash_ending","ending")):
  assert r[k]==q[col],(k,r.get(k),q[col])
 assert r["cash_beginning"]+r["net_cash_change"]+r["cashflow_fx"]==r["cash_ending"]
 assert r["cash_beginning"]+r["net_cash_change"]!=r["cash_ending"] # FX must not be discarded
 assert r["roa"]==round(4*100*f["pat_q3"]/((f["assets"]+f["assets_H1"])/2),2)
 assert r["roe"]==round(4*100*f["pat_q3"]/((f["equity"]+f["equity_H1"])/2),2)
 assert all(not x["period"].startswith("2024") for x in d["items"])
 return len(f)
def main():
 a,b=read(AUDIT),read(FIN)
 n=verify(a,b)
 for label in ("asset_source_plus1","signed_CFO_plus1","FY_FX_wrong","dashboard_profit"):
  c,d=copy.deepcopy(a),copy.deepcopy(b)
  row=d["items"][-1]
  if label=="asset_source_plus1":c["original_source_million_vnd"]["assets"]+=1
  elif label=="signed_CFO_plus1":c["original_source_million_vnd"]["cfo_9m"]+=1
  elif label=="FY_FX_wrong":row["cashflow_fx"]+=1
  else:row["net_profit"]+=1
  try:verify(c,d)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError("Failed to catch corruption "+label)
 print(f"PASS CTG 2026 Q3: {n} signed million VND source values, 28 source accounting equations zero, 16 direct Q3=9M-H1 income lines zero, 4 corruption tests.")
 print("CTG quarter CFO -19,748,243 CFI +1,804,250 CFF -4,273,630 net -22,217,623 FX -67,131 end 520,137,917 million VND.")
if __name__=="__main__":main()
