#!/usr/bin/env python3
"""Source-proof SHS 2026Q3 signed original + AASC reviewed H1, exact VND.

Company B01/B02/B03, segregated client brokerage cash. Quarter bank cash
9M−AASC H1; do not project 9M CFO onto standalone Q3 or use client money.
"""
from pathlib import Path
from decimal import Decimal
import copy,json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/SHS-2026Q3-issuer-signed-AASC-reviewed-H1-exact-vnd.json"
FIN=ROOT/"data/financials-SHS.json"
M=Decimal("1000000")
def read(p):return json.loads(p.read_text(encoding="utf8"))
def vnd(row,key):
 val=row.get(key);assert isinstance(val,(float,int)) and not isinstance(val,bool),(key,val)
 n=Decimal(str(val))*M
 assert n==n.to_integral_value(),(key,val,n)
 return int(n)
def proof(src):
 assert src["ticker"]=="SHS" and src["period"]=="2026-Q3"
 assert src["unit"]=="VND" and "segregated customer money" in src["scope"]
 o,h=src["Q3_original_issuer"],src["H1_independently_reviewed"]
 assert o["signed_date"]=="2026-10-20" and o["pages"]==40 and o["bytes"]==29580249
 assert o["pdf_sha256"]=="78622b1eb767b4cbefa53836bde45ece8f8feb6baa55d6bac1d155667f80acc8"
 assert h["signed_date"]=="2026-08-13" and h["auditor"]=="AASC"
 assert h["pages"]==56 and h["bytes"]==37951575
 assert h["pdf_sha256"]=="6511a79ba024ffa3070b2739c634c9a88f45236ec7d716de0a7fe932a4d2c2f0"
 assert src["source_proof"]["github_workflow_run"]==45013391624
 assert src["source_proof"]["visual_artifact_id"]==14750393671
 s=src["original_exact_vnd"]
 assert len(s)==62 and all(isinstance(x,str) for x in s.values())
 V=lambda k:int(s[k])
 S=lambda names:sum(V(k) for k in names)
 q={k:(V(k+"_9m")-V(k+"_H1")) for k in ("cfo","cfi","cff","net")}
 q["cash_beginning"]=V("close_H1");q["cash_ending"]=V("close_9m")
 assert {k:int(v) for k,v in src["quarter_standalone_cashflow_vnd"].items()}==q
 checks={
 "assets":V("short_assets")+V("long_assets")-V("total_assets"),
 "current":V("financial_short")+V("other_short")-V("short_assets"),
 "financial_short":S(("cash","fvtpl","htm","loans","afs","receivables","advances","service_receivables","other_receivables","impairment"))-V("financial_short"),
 "liabilities":V("current_liabs")+V("long_liabs")-V("liabs"),
 "balance":V("liabs")+V("equity")-V("total_assets"),
 "equity":S(("share_capital","share_premium","afs_fv_equity","retained"))-V("equity"),
 "q_profit":V("revenue_q3")-V("cost_q3")+V("finance_rev_q3")-V("finance_exp_q3")-V("admin_q3")-V("operating_profit_q3"),
 "q_beforetax":V("operating_profit_q3")+V("other_profit_q3")-V("pbt_q3"),
 "q_aftertax":V("pbt_q3")-V("tax_q3")-V("pat_q3"),
 "bridge_revenue":V("reven_9m")-V("reven_H1")-V("revenue_q3"),
 "bridge_pbt":V("pbt_9m")-V("pbt_H1")-V("pbt_q3"),
 "bridge_pat":V("pat_9m")-V("pat_H1")-V("pat_q3"),
 "cash_9m":V("cfo_9m")+V("cfi_9m")+V("cff_9m")-V("net_9m"),
 "cash_H1":V("cfo_H1")+V("cfi_H1")+V("cff_H1")-V("net_H1"),
 "cash_q3":q["cfo"]+q["cfi"]+q["cff"]-q["net"],
 "cash_bridge_9m":V("open_9m")+V("net_9m")-V("close_9m"),
 "cash_bridge_H1":V("open_H1")+V("net_H1")-V("close_H1"),
 "cash_bridge_q3":q["cash_beginning"]+q["net"]-q["cash_ending"],
 "cash_B01_B03":V("cash")-V("close_9m"),
 "cfi_items":V("cfi_capex_9m")+V("cfi_disposal_9m")+V("cfi_dividends_9m")-V("cfi_9m"),
 "cff_items":V("cff_borrow_9m")+V("cff_repayment_9m")-V("cff_9m"),
 "customer_not_company":int(V("customer_cash_9m")==V("cash")),
 "reviewed_H1_balance":V("assets_H1")-V("liabs_H1")-V("equity_H1"),
 "H1_reported_independent_cash_opening_equals_Q3_cash_opening":V("open_H1")-V("open_9m")
 }
 assert len(checks)==24 and set(checks)==set(src["source_check_residual_vnd"])
 assert all(v==0 for v in checks.values()),checks
 assert all(int(src["source_check_residual_vnd"][k])==v for k,v in checks.items())
 assert q["cfo"]==1010086597336 and q["cfi"]==-15663429228
 assert q["cff"]==1439580814265 and q["net"]==2434003982373
 assert q["cash_ending"]==3392364033103
 assert V("customer_cash_9m")==1211124622076 and V("customer_cash_9m")!=V("cash")
 return s,q

def verify(src,d):
 s,quarter=proof(src)
 assert d["symbol"]=="SHS" and len(d["items"])==7
 assert [x["period"] for x in d["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 row=d["items"][-1]
 assert row["verification_status"]=="issuer_signed_SHS_2026Q3_B01a_B02a_B03b_AASC_reviewed_H1_exact_vnd"
 assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
 assert row["source_url"]==src["Q3_original_issuer"]["url"]
 v=row["source_validation"]
 assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
 assert v["original_pdf_sha256"]==src["Q3_original_issuer"]["pdf_sha256"]
 assert v["reviewed_H1_pdf_sha256"]==src["H1_independently_reviewed"]["pdf_sha256"]
 assert v["original_pdf_hash_verified"] and v["manually_visual_reviewed"] and v["AASC_H1_source_visually_verified"]
 assert v["broker_client_cash_segregated"] and v["accounting_checks_24_exact_zero_vnd"]
 assert v["source_cashflow_zero_residual_vnd"]=="0" and v["quarter_cashflow_zero_residual_vnd"]=="0"
 f={
  "total_assets":"total_assets","total_liabilities":"liabs","equity":"equity",
  "revenue":"revenue_q3","pretax_profit":"pbt_q3","net_profit":"pat_q3",
  "net_profit_attributable":"pat_q3","income_tax":"tax_q3",
  "cash_and_equivalents":"close_9m","cash_ending_ytd":"close_9m",
  "current_assets":"short_assets","non_current_assets":"long_assets",
  "current_liabilities":"current_liabs","long_term_liabilities":"long_liabs",
  "broker_fvtpl_assets":"fvtpl","broker_held_to_maturity_assets":"htm",
  "broker_lending_assets":"loans","broker_afs_assets":"afs",
  "broker_customer_deposits":"customer_cash_9m",
  "operating_cash_flow_ytd":"cfo_9m","investing_cash_flow_ytd":"cfi_9m",
  "financing_cash_flow_ytd":"cff_9m","net_cash_change_ytd":"net_9m",
  "cash_beginning_reported_ytd":"open_9m",
  "financial_income":"finance_rev_q3","financial_expense":"finance_exp_q3",
  "broker_operating_expenses":"cost_q3"
 }
 for field,src_name in f.items():
  assert vnd(row,field)==int(s[src_name]),(field,row.get(field),s[src_name])
 for field,src_name in (("operating_cash_flow","cfo"),("investing_cash_flow","cfi"),
                        ("financing_cash_flow","cff"),("net_cash_change","net"),
                        ("cash_beginning","cash_beginning"),("cash_ending","cash_ending")):
  assert vnd(row,field)==quarter[src_name],(field,quarter[src_name],row.get(field))
 assert vnd(row,"bank_cash_and_equivalents_cashflow_basis")==int(s["cash"])
 expected_roa=round(int(s["pat_q3"])/(int(s["assets_H1"])+int(s["total_assets"]))*800,2)
 expected_roe=round(int(s["pat_q3"])/(int(s["equity_H1"])+int(s["equity"]))*800,2)
 assert row["roa"]==expected_roa and row["roe"]==expected_roe,(expected_roa,expected_roe)
 assert vnd(row,"broker_customer_deposits")!=vnd(row,"cash_ending")
 assert vnd(row,"cash_beginning")+vnd(row,"net_cash_change")==vnd(row,"cash_ending")
 assert not any(x["period"].startswith("2024") for x in d["items"])
 return len(s)
def main():
 src,d=read(SRC),read(FIN)
 count=verify(src,d)
 for bad in ("balance_1vnd","source_9M_cfo_1vnd","dashboard_profit_1vnd","broker_cash_not_issuer_cash"):
  a,b=copy.deepcopy(src),copy.deepcopy(d)
  row=b["items"][-1]
  if bad=="balance_1vnd":a["original_exact_vnd"]["total_assets"]=str(int(a["original_exact_vnd"]["total_assets"])+1)
  elif bad=="source_9M_cfo_1vnd":a["original_exact_vnd"]["cfo_9m"]=str(int(a["original_exact_vnd"]["cfo_9m"])+1)
  elif bad=="dashboard_profit_1vnd":row["net_profit"]+=0.000001
  else:row["cash_ending"]=row["broker_customer_deposits"]
  try:verify(a,b)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError("Tampered SHS source/data passed: "+bad)
 print(f"PASS SHS 2026Q3: {count} issuer signed exact VND source values, 24 exact-zero source equations including AASC reviewed H1 B03, 4 source mutation controls.")
 print("Source Q3 cash CFO +1,010,086,597,336 CFI -15,663,429,228 CFF +1,439,580,814,265 net +2,434,003,982,373 end 3,392,364,033,103 VND.")
if __name__=="__main__":main()
