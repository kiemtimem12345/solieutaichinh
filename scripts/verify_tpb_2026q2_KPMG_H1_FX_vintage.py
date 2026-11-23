#!/usr/bin/env python3
"""TPB Q2 2026 first-issued signed + KPMG reviewed H1 exact bank accounting.

Review source-vintage differences rather than hide them; reported 6M FX line
absent (zero) but 2026Q1 B04a signed +373,117. Implied Q2 carry -373,117
is NOT independently reported FX charge nor a plug to bank CFO.
"""
from pathlib import Path
from copy import deepcopy
import json

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2026Q2-original-vs-KPMG-H1-bank-FX-million-vnd.json"
Q1=ROOT/"reports/source-audits/TPB-2026Q1-signed-B02a-B03a-B04a-three-FY-vintages-million-vnd.json"
FIN=ROOT/"data/financials-TPB.json"

def validate(a,old,fin):
 assert a["symbol"]=="TPB" and a["period"]=="2026-Q2" and a["scope"]=="consolidated"
 assert a["unit"]=="triệu VND"
 s=a["signed_Q2"];h=a["reviewed_H1"]
 assert s["sha256"]=="36160cdcecbd2382d1501ee3a65ab5a33f75f413c06a39858d8a49f4b4c93023"
 assert h["sha256"]=="b375177862bd6c6da03e55b5c39958341d0ae13232c353dd2d55a7c7bff4e80f"
 assert (s["bytes"],s["pages"])==(16307265,67)
 assert (h["bytes"],h["pages"])==(10294903,107)
 assert s["B02a_pages"]==[7,8] and s["B03a_page"]==10 and s["B04a_pages"]==[11,12]
 assert h["B02a_pages"]==[10,11,12,13] and h["B03a_pages"]==[14,15] and h["B04a_pages"]==[16,17]
 assert h["reviewer"]=="KPMG"
 assert a["Q1_signed_2026"]["sha256"]==old["source"]["sha256"]
 assert a["Q1_signed_2026"]["B02a"]==old["B02a_current"]
 assert a["Q1_signed_2026"]["B03a"]==old["B03a_current"]
 assert a["Q1_signed_2026"]["B04a"]==old["B04a_current"]
 b,br=a["B02a_Q2_first"],a["B02a_H1_KPMG"]
 p,y,yr=a["B03a_Q2_first"],a["B03a_6m_first"],a["B03a_H1_KPMG"]
 c,cr,q=a["B04a_6m_first"],a["B04a_H1_KPMG"],a["Q2_cash_H1_minus_Q1"]
 v=a["H1_KPMG_minus_first_vintage"]
 oldp,oldc=old["B03a_current"],old["B04a_current"]
 E={}
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 E["B02_assets"]=sum(b[k] for k in ("cash_vault","deposits_SBV","interbank_assets","trading_securities",
 "derivative_assets","customer_loans_net","purchased_debt_net","investment_securities",
 "longterm_investments","fixed_assets","other_assets"))-b["total_assets"]
 E["B02_liabilities"]=sum(b[k] for k in ("government_liabilities","interbank_liabilities",
 "customer_deposits","derivative_liabilities","trust_liabilities","valuable_papers",
 "other_liabilities"))-b["total_liabilities"]
 E["B02_equity"]=sum(b[k] for k in ("bank_capital","bank_funds","fx_equity",
 "retained_profit","noncontrolling_equity"))-b["total_equity"]
 E["B02_reviewed_balance"]=br["total_assets"]-br["total_liabilities"]-br["total_equity"]
 for name,current,rev in (("assets",b["total_assets"],br["total_assets"]),
  ("liabilities",b["total_liabilities"],br["total_liabilities"]),
  ("equity",b["total_equity"],br["total_equity"])):
  E["B02_vintage_"+name]=rev-current-v[name]
 E["B02_reviewed_other_liabilities"]=br["other_liabilities"]-b["other_liabilities"]+59
 E["B02_reviewed_retained"]=br["retained_profit"]-b["retained_profit"]-31
 E["B02_reviewed_NCI"]=br["noncontrolling_equity"]-b["noncontrolling_equity"]-28
 E["B03_interest"]=p["interest_income"]+p["interest_expense"]-p["net_interest"]
 E["B03_service"]=p["service_income"]+p["service_expense"]-p["services_net"]
 E["B03_other"]=p["other_income"]+p["other_expense"]-p["other_net"]
 income=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 for name,rec in (("Q2",p),("first_6M",y),("reviewed_6M",yr)):
  E["B03_income_"+name]=sum(rec[k] for k in income)-rec["operating_income"]
  E["B03_opex_"+name]=rec["operating_income"]-rec["operating_expenses"]-rec["before_provision"]
  E["B03_PBT_"+name]=rec["before_provision"]-rec["credit_provision"]-rec["pretax_profit"]
  E["B03_PAT_"+name]=rec["pretax_profit"]-rec["income_tax"]-rec["net_profit"]
  E["B03_NCI_"+name]=rec["net_profit"]-rec["noncontrolling_profit"]-rec["parent_profit"]
 E["B03_Q2_tax"]=p["income_tax_current"]+p["income_tax_deferred"]-p["income_tax"]
 E["B03_6M_KPMG_tax"]=yr["income_tax_current"]+yr["income_tax_deferred"]-yr["income_tax"]
 quarter_fields=(*income,"operating_income","operating_expenses","before_provision",
    "credit_provision","pretax_profit","income_tax","net_profit","noncontrolling_profit","parent_profit")
 for k in quarter_fields:
  E["B03_Q2_first6M_minus_Q1_"+k]=y[k]-oldp[k]-p[k]
 for k,delta_key in (("pretax_profit","PBT"),("net_profit","PAT"),
  ("parent_profit","parent_PAT"),("noncontrolling_profit","NCI_PAT")):
  E["B03_KPMG_vintage_"+k]=yr[k]-y[k]-v[delta_key]
 E["B03_KPMG_tax_delta"]=yr["income_tax"]-y["income_tax"]+58
 E["B04_preWC"]=sum(c[k] for k in ("interest_received","interest_paid",
  "services_cash","fx_trading_cash","other_cash","recovered_bad_debts_cash",
  "staff_admin_cash","tax_paid"))-c["pre_wc_cash"]
 E["B04_true_CFO"]=c["pre_wc_cash"]+sum(c[k] for k in (
  "asset_interbank","asset_securities","asset_derivatives","asset_customer_loans",
  "asset_credit_provisions","asset_other","liability_government","liability_interbank",
  "liability_customer_deposits","liability_papers","liability_trust","liability_derivatives",
  "liability_other"))-c["CFO"]
 E["B04_CFI"]=sum(c[k] for k in (
  "capex","disposal_receipts","disposal_expenses","investment_outflows",
  "investing_dividends"))-c["CFI"]
 E["B04_CFF"]=c["financing_new_debt"]+c["financing_repayment"]-c["CFF"]
 E["B04_6M_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["B04_6M_cash"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 for key in ("CFO","CFI","CFF","net_cash_change","opening_cash","closing_cash",
             "FX_effect","capex","disposal_receipts","disposal_expenses",
             "investment_outflows","investing_dividends","financing_new_debt",
             "financing_repayment","pre_wc_cash"):
  E["B04_6M_first_vs_KPMG_"+key]=c[key]-cr[key]
 for key in ("CFO","CFI","CFF","net_cash_change"):
  E["B04_Q2_6M_less_Q1_"+key]=cr[key]-oldc[key]-q[key]
  E["B04_version_delta_"+key]=cr[key]-c[key]-v[key]
 E["B04_Q2_start"]=q["opening_cash"]-oldc["closing_cash"]
 E["B04_Q2_end"]=q["closing_cash"]-cr["closing_cash"]
 E["B04_Q2_FX"]=q["FX_effect_implied"]-(cr["FX_effect"]-oldc["FX_effect"])
 E["B04_Q2_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["B04_Q2_cash"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect_implied"]-q["closing_cash"]
 E["B04_Q2_capex"]=q["capex"]-(cr["capex"]-oldc["capex"])
 assert len(E)>=65 and all(v==0 for v in E.values()),(len(E),{k:v for k,v in E.items() if v})
 assert c["CFO"]==-16932973 and c["pre_wc_cash"]==4921774 and c["interest_received"]==18171212
 assert c["CFO"]!=c["pre_wc_cash"] and c["CFO"]!=c["interest_received"]
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"])==(-9652957,-32815,-1471200,-11156972)
 assert (q["opening_cash"],q["closing_cash"],q["FX_effect_implied"])==(108553424,97023335,-373117)
 assert v=={"assets":0,"liabilities":-59,"equity":59,"PBT":0,
  "PAT":58,"parent_PAT":30,"NCI_PAT":28,"CFO":0,"CFI":0,"CFF":0,"net_cash_change":0}
 assert fin["symbol"]=="TPB" and [z["period"] for z in fin["items"]]==[
  "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 row=fin["items"][5];source=row["source_validation"]
 assert row["verification_status"]=="issuer_signed_TPB_2026Q2_first_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 assert source["original_pdf_sha256"]==s["sha256"] and source["reviewed_H1_pdf_sha256"]==h["sha256"]
 assert source["signed_Q1_pdf_sha256"]==old["source"]["sha256"]
 assert source["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert source["manually_visual_reviewed"] and source["original_pdf_hash_verified"]
 assert source["KPMG_H1_bank_B04a_minus_signed_Q1_cash_exact"]
 assert source["Q2_2026_direct_B03a_16_6M_minus_Q1_first_exact"]
 assert source["source_vintage_H1_audited_vs_first"]==v
 assert source["KPMG_H1_FX_blank_vs_Q1_FX_373117_implied"]
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"]
 assert row["equity"]==b["total_equity"] and row["revenue"]==p["operating_income"]
 assert row["pretax_profit"]==p["pretax_profit"] and row["net_profit"]==p["net_profit"]
 assert row["net_profit_attributable"]==p["parent_profit"]
 assert row["operating_cash_flow"]==q["CFO"] and row["investing_cash_flow"]==q["CFI"]
 assert row["financing_cash_flow"]==q["CFF"] and row["net_cash_change"]==q["net_cash_change"]
 assert row["cashflow_fx"]==q["FX_effect_implied"]
 assert row["cash_beginning"]==q["opening_cash"] and row["cash_ending"]==q["closing_cash"]
 assert row["operating_cash_flow_ytd"]==cr["CFO"] and row["investing_cash_flow_ytd"]==cr["CFI"]
 assert row["financing_cash_flow_ytd"]==cr["CFF"] and row["net_cash_change_ytd"]==cr["net_cash_change"]
 assert row["roa"]==round(400*p["net_profit"]/((b["total_assets"]+fin["items"][4]["total_assets"])/2),2)==1.41
 assert row["roe"]==round(400*p["net_profit"]/((b["total_equity"]+fin["items"][4]["equity"])/2),2)==15.50
 assert row["financial_line_items_rejected_values"]=={} and row["financial_line_items_rejected_fields"]==[]
 for prefix,record in (("b02a_Q2",b),("b02a_H1_reviewed",br),
  ("b03a_Q2",p),("b03a_6m_original",y),("b03a_H1_reviewed",yr),
  ("b04a_6m_original",c),("b04a_H1_reviewed",cr),("b04a_Q2",q)):
  for k,v in record.items():
   if isinstance(v,int):assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert all(z["verification_status"].startswith("issuer_signed") for z in fin["items"])
 assert fin["items"][6]["verification_status"]=="issuer_signed_TPB_2026Q3_B02a_B03a_9M_minus_KPMG_H1_bank_B04a_FX_vintage_verified"
 assert not any(z["period"].startswith("2024") for z in fin["items"])
 return len(E)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 q=json.loads(Q1.read_text("utf-8"))
 d=json.loads(FIN.read_text("utf-8"))
 n=validate(a,q,d)
 mutations=("B02","B03","reviewed_B02","reviewed_PAT","source_CFO","wrong_interest",
   "FX_removed","source_original_hash","KPMG_hash","old_Q1_changed","prior_Q4_changed","ROE","false_complete")
 for name in mutations:
  ledger,first,data=deepcopy(a),deepcopy(q),deepcopy(d)
  if name=="B02":ledger["B02a_Q2_first"]["total_assets"]+=1
  elif name=="B03":ledger["B03a_Q2_first"]["net_profit"]+=1
  elif name=="reviewed_B02":ledger["B02a_H1_KPMG"]["total_liabilities"]+=1
  elif name=="reviewed_PAT":ledger["B03a_H1_KPMG"]["net_profit"]+=1
  elif name=="source_CFO":ledger["B04a_6m_first"]["CFO"]+=1
  elif name=="wrong_interest":data["items"][5]["operating_cash_flow"]=18171212
  elif name=="FX_removed":data["items"][5]["cashflow_fx"]=0
  elif name=="source_original_hash":ledger["signed_Q2"]["sha256"]="0"*64
  elif name=="KPMG_hash":ledger["reviewed_H1"]["sha256"]="0"*64
  elif name=="old_Q1_changed":first["B04a_current"]["CFO"]+=1
  elif name=="prior_Q4_changed":data["items"][3]["verification_status"]="forged"
  elif name=="ROE":data["items"][5]["roe"]=88
  elif name=="false_complete":data["items"][5]["source_validation"]["KPMG_H1_bank_B04a_minus_signed_Q1_cash_exact"]=False
  try:validate(ledger,first,data)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Tamper case not blocked: "+name)
 print(f"PASS TPB 2026 Q2 signed original 67p and KPMG H1 reviewed 107p: {n} exact bank accounts and source-vintage checks, 16 original direct income bridges, {len(mutations)} tamper controls.")
 print("PASS 6M-H1 minus source-verified Q1 CFO -9,652,957 CFI -32,815 CFF -1,471,200 net -11,156,972, implied FX -373,117; bank cash 108,553,424 -> 97,023,335 million VND.")
 print("PASS first Q2 assets 547,664,403 and equity 49,565,825; reviewed H1 assets same, equity +59 / liabilities -59, PAT +58 million VND; no balancing plug.")
 print("PASS TPB six 2025Q1-2026Q2 source-verified rows; Q3/2026 source to be added as seventh period.")
if __name__=="__main__":main()
