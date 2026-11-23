#!/usr/bin/env python3
"""BID Q2/2026 issuer first-issued B01/B03 and independently reviewed H1 B04.

Exact million-VND reconciliations, same-consolidated-scope Q2 6M–Q1 bank cash,
and explicitly preserved source vintages. Reviewed H1 source previously
verified in signed Q3 checkpoint; do NOT repeat source extraction.
"""
from pathlib import Path
from copy import deepcopy
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/BID-2026Q2-original-vs-reviewedH1-quarter-million-vnd.json"
Q1=ROOT/"reports/source-audits/BID-2026Q1-signed-consolidated-exact-million-vnd.json"
Q3=ROOT/"reports/source-audits/BID-2026Q3-official-web-excerpt-preliminary-million-vnd.json"
FIN=ROOT/"data/financials-BID.json"

def verify(a:dict,q1:dict,q3:dict,fin:dict)->int:
 assert a["symbol"]=="BID" and a["period"]=="2026-Q2"
 assert a["scope"]=="consolidated" and a["unit"]=="triệu VND"
 source=a["original_q2"]
 assert source["sha256"]=="73d9ead38e4e60b2241ae7d41a6e5382f8f2e5cc59f2e7a70ca0bedb95792003"
 assert source["pages"]==37 and source["bytes"]==13263197
 assert source["B01_pdf_pages"]==[4,5] and source["B03_pdf_page"]==7 and source["B04_pdf_pages"]==[8,9]
 h=a["reviewed_H1"];p=a["signed_Q1"]
 assert h["sha256"]=="3c3f6c39c9ca9f737c3d8d52893d7320be29dbb1a4bcecfdf062fad2b45106d2"
 assert h["sha256"]==q3["h1_reviewed_consolidated_original"]["pdf_sha256"]
 assert h["B01"]==q3["b01_H1_reviewed_2026_06_30_million_vnd"]
 assert h["B03_6m"]==q3["b03_H1_reviewed_6m_million_vnd"]
 assert h["B04_6m"]==q3["b04_H1_reviewed_6m_million_vnd"]
 assert p["sha256"]==q1["signed_q1_source"]["sha256"]
 assert p["B01"]==q1["B01_q1"] and p["B03_q1"]==q1["B03_q1"] and p["B04_q1"]==q1["B04_q1"]
 b,q,s6,cf1,cf2=a["B01_original_Q2"],a["B03_Q2_original_direct"],a["B03_6m_first_issued"],a["B04_6m_first_issued"],a["Q2_quarter_reviewed_H1_minus_Q1"]
 sr=h["B04_6m"];p1=p["B04_q1"];v=a["version_difference_reviewed_H1_minus_original_H1"]
 e={}
 e["b01_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 e["b01_assets"]=sum(b[k] for k in (
  "cash_vault","deposits_SBV","interbank_assets","trading_securities",
  "derivative_assets","customer_loans_net","investment_securities",
  "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 e["b01_liabs"]=sum(b[k] for k in (
  "government_liabilities","interbank_liabilities","customer_deposits",
  "derivative_liabilities","trust_liabilities","valuable_papers","other_liabilities"))-b["total_liabilities"]
 e["b01_equity"]=sum(b[k] for k in (
  "bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity"))-b["total_equity"]
 e["b01_reviewed_balance"]=h["B01"]["total_assets"]-h["B01"]["total_liabilities"]-h["B01"]["equity"]
 for name,orig,reviewed in (
   ("assets",b["total_assets"],h["B01"]["total_assets"]),
   ("liabilities",b["total_liabilities"],h["B01"]["total_liabilities"]),
   ("equity",b["total_equity"],h["B01"]["equity"])
 ):
  e["b01_vintage_"+name]=reviewed-orig-v[name]
 e["Q2_net_interest"]=q["gross_interest_income"]+q["interest_expense"]-q["net_interest"]
 e["Q2_services"]=q["gross_service_income"]+q["service_expense"]-q["services_net"]
 e["Q2_other"]=q["other_income"]+q["other_expense"]-q["other_net"]
 income=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 e["Q2_op_income"]=sum(q[k] for k in income)-q["operating_income"]
 e["first_6m_income"]=sum(s6[k] for k in income)-s6["operating_income"]
 e["Q2_before_provision"]=q["operating_income"]-q["operating_expenses"]-q["before_provision"]
 e["first_6m_before_provision"]=s6["operating_income"]-s6["operating_expenses"]-s6["before_provision"]
 e["Q2_PBT"]=q["before_provision"]-q["credit_provision"]-q["pretax_profit"]
 e["first_6m_PBT"]=s6["before_provision"]-s6["credit_provision"]-s6["pretax_profit"]
 e["Q2_tax"]=q["income_tax_current"]+q["income_tax_deferred"]-q["income_tax"]
 e["Q2_PAT"]=q["pretax_profit"]-q["income_tax"]-q["net_profit"]
 e["first_6m_PAT"]=s6["pretax_profit"]-s6["income_tax"]-s6["net_profit"]
 e["Q2_parent"]=q["net_profit"]-q["noncontrolling_profit"]-q["parent_profit"]
 e["first_6m_parent"]=s6["net_profit"]-s6["noncontrolling_profit"]-s6["parent_profit"]
 b03=("net_interest","services_net","FX_net","trading_net","invest_net","other_net",
      "contribution_income","operating_income","operating_expenses","before_provision",
      "credit_provision","pretax_profit","income_tax","net_profit","noncontrolling_profit","parent_profit")
 for k in b03:
  # First-issued Q2 signed directly prints current quarter B03 columns;
  # Q1 signed original and first-issued 6M must produce exactly Q2.
  e["q2_direct_first_6m_minus_q1_"+k]=s6[k]-p["B03_q1"][k]-q[k] if k not in ("income_tax", "noncontrolling_profit") else (
     s6[k]-p["B03_q1"][{"income_tax":"income_tax","noncontrolling_profit":"noncontrolling_profit"}[k]]-q[k]
  )
 e["B04_original_6M_sum"]=cf1["CFO"]+cf1["CFI"]+cf1["CFF"]-cf1["net_cash_change"]
 e["B04_original_6M_cash"]=cf1["opening_cash"]+cf1["net_cash_change"]-cf1["closing_cash"]
 e["B04_original_6M_investing"]=sum(cf1[k] for k in ("capex","disposal_proceeds","disposal_expenses","dividends_investing"))-cf1["CFI"]
 e["B04_original_6M_financing"]=sum(cf1[k] for k in ("equity_issuance","longterm_new","longterm_repaid"))-cf1["CFF"]
 e["B04_reviewed_6M_sum"]=sr["operating"]+sr["investing"]+sr["financing"]-sr["net_cash_change"]
 e["B04_reviewed_6M_cash"]=sr["year_open_cash"]+sr["net_cash_change"]-sr["ending_cash"]
 e["B04_reviewed_6M_investing"]=sum(sr[k] for k in ("investing_capex","investing_sale_proceeds","investing_disposal_cost","investing_dividends"))-sr["investing"]
 e["B04_reviewed_6M_financing"]=sum(sr[k] for k in ("financing_new_equity","financing_new_longterm","financing_repaid_longterm"))-sr["financing"]
 for name,key in (("CFO","operating"),("CFI","investing"),("CFF","financing"),("net_cash_change","net_cash_change")):
  e["Q2_cash_6M_minus_Q1_"+name]=sr[key]-p1[name]-cf2[name]
  e["B04_vintage_"+name]=sr[key]-cf1[name]-v[name]
 e["B04_vintage_close"]=sr["ending_cash"]-cf1["closing_cash"]-v["closing_cash"]
 e["Q2_cash_open"]=cf2["opening_cash"]-p1["closing_cash"]
 e["Q2_cash_close"]=cf2["closing_cash"]-sr["ending_cash"]
 e["Q2_cash_sum"]=cf2["CFO"]+cf2["CFI"]+cf2["CFF"]-cf2["net_cash_change"]
 e["Q2_cash_open_close"]=cf2["opening_cash"]+cf2["net_cash_change"]-cf2["closing_cash"]
 for key,review_key in (
  ("pretax_profit","pretax_profit"),("net_profit","net_profit"),("parent_profit","parent_profit"),
  ("services_net","services"),("operating_expenses","operating_expenses")
 ):
  e["B03_reviewed_6M_vintage_"+key]=h["B03_6m"][review_key]-s6[key]-v[key]
 assert len(e)>=55 and all(x==0 for x in e.values()),(len(e),{k:v for k,v in e.items() if v})
 assert cf1["before_working_capital_not_CFO"]==26220386 and cf1["before_working_capital_not_CFO"]!=cf1["CFO"]
 assert cf2["CFO"]==-24471221 and cf2["CFI"]==-747536 and cf2["CFF"]==2840220
 assert cf2["net_cash_change"]==-22378537 and cf2["opening_cash"]==544528992 and cf2["closing_cash"]==522150455
 assert v["CFO"]==226 and v["net_cash_change"]==226 and v["assets"]==-2683
 assert fin["symbol"]=="BID" and [x["period"] for x in fin["items"]]==[
   "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 row=fin["items"][5]
 assert row["verification_status"]=="issuer_signed_BID_2026Q2_first_issued_B01_B03_reviewed_H1_minus_signed_Q1_B04_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 sv=row["source_validation"]
 assert sv["manually_visual_reviewed"] and sv["original_pdf_hash_verified"]
 assert sv["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sv["original_pdf_sha256"]==source["sha256"]
 assert sv["H1_reviewed_source_pdf_sha256"]==h["sha256"]
 assert sv["signed_Q1_pdf_sha256"]==p["sha256"]
 assert sv["source_version_differences"]==v and sv["cash_Q2_from_reviewed_H1_minus_signed_Q1_same_scope_exact"]
 assert sv["bank_direct_B04_6M_preWC_26220386_NOT_CFO"]
 assert row["total_assets"]==b["total_assets"] and row["equity"]==b["total_equity"]
 assert row["pretax_profit"]==q["pretax_profit"] and row["net_profit"]==q["net_profit"]
 assert row["net_profit_attributable"]==q["parent_profit"]
 assert row["revenue"]==q["operating_income"]
 assert row["operating_cash_flow"]==cf2["CFO"] and row["investing_cash_flow"]==cf2["CFI"]
 assert row["financing_cash_flow"]==cf2["CFF"] and row["net_cash_change"]==cf2["net_cash_change"]
 assert row["operating_cash_flow_ytd"]==sr["operating"] and row["investing_cash_flow_ytd"]==sr["investing"]
 assert row["financing_cash_flow_ytd"]==sr["financing"] and row["net_cash_change_ytd"]==sr["net_cash_change"]
 assert row["cash_beginning"]==cf2["opening_cash"] and row["cash_ending"]==cf2["closing_cash"]
 assert row["roa"]==round(400*q["net_profit"]/((b["total_assets"]+fin["items"][4]["total_assets"])/2),2)==0.97
 assert row["roe"]==round(400*q["net_profit"]/((b["total_equity"]+fin["items"][4]["equity"])/2),2)==17.04
 for prefix,rec in (
  ("b01_Q2",b),("b03_Q2",q),("b03_6m_first",s6),("b03_6m_reviewed",h["B03_6m"]),
  ("b04_Q2",cf2),("b04_6m_first",cf1),("b04_6m_reviewed",sr),("b01_6m_reviewed",h["B01"])
 ):
  for k,value in rec.items():
   assert row["signed_source_"+prefix+"_"+k]==value,(prefix,k)
 assert all(x["verification_status"].startswith("issuer_signed") for x in fin["items"])
 assert not any(x["period"].startswith("2024") for x in fin["items"])
 return len(e)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 p=json.loads(Q1.read_text("utf-8"))
 h=json.loads(Q3.read_text("utf-8"))
 data=json.loads(FIN.read_text("utf-8"))
 n=verify(a,p,h,data)
 for name in ("Q2_asset","Q2_profit","H1_reviewed_CFO","Q2_cash","vintage","signed_sha","Q1_prior","Q3_prior","preWC","ROE"):
  l,q,r,d=deepcopy(a),deepcopy(p),deepcopy(h),deepcopy(data)
  if name=="Q2_asset":l["B01_original_Q2"]["total_assets"]+=1
  elif name=="Q2_profit":l["B03_Q2_original_direct"]["net_profit"]+=1
  elif name=="H1_reviewed_CFO":r["b04_H1_reviewed_6m_million_vnd"]["operating"]+=1
  elif name=="Q2_cash":d["items"][5]["operating_cash_flow"]+=1
  elif name=="vintage":l["version_difference_reviewed_H1_minus_original_H1"]["CFO"]+=1
  elif name=="signed_sha":l["original_q2"]["sha256"]="0"*64
  elif name=="Q1_prior":d["items"][4]["verification_status"]="unverified"
  elif name=="Q3_prior":d["items"][6]["verification_status"]="unverified"
  elif name=="preWC":l["B04_6m_first_issued"]["before_working_capital_not_CFO"]=l["B04_6m_first_issued"]["CFO"]
  elif name=="ROE":d["items"][5]["roe"]+=1
  try:verify(l,q,r,d)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Q2 tamper case not rejected "+name)
 print(f"PASS BID 2026-Q2 37p original signed + reviewed 57p H1 plus Q1 signed: {n} bank identities/quarter and vintage gates; 16 first-6M minus Q1 B03; 10 corruption cases.")
 print("PASS reviewed H1 less signed Q1 quarterly CFO -24,471,221 CFI -747,536 CFF +2,840,220 net -22,378,537 and bank cash 544,528,992 → 522,150,455 million VND.")
 print("PASS BID all 7/7 quarters Q1/2025 to Q3/2026 source-verified; no 2024 dashboard rows.")
if __name__=="__main__":main()
