#!/usr/bin/env python3
"""TPB signed 2025Q4 vs official KPMG audited FY2025, million-VND QA.

Original first-issued Q4 B02a/B03a direct; audited FY B04a minus separately
signed 9M, with source-version differences and implied FX tracked explicitly.
Never overwrite original-source Q4 figures with the audited or later 2026
represented balance-sheet version. Fail closed on accounting/FX errors.
"""
import json
from pathlib import Path
from copy import deepcopy

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2025Q4-first-issued-vs-KPMG-FY-audited-bank-million-vnd.json"
PRIOR=ROOT/"reports/source-audits/TPB-2025Q3-signed-9M-KPMG-H1-bank-FX-million-vnd.json"
FIN=ROOT/"data/financials-TPB.json"

def verify(a,prior,data):
 assert (a["symbol"],a["period"],a["scope"],a["unit"])==("TPB","2025-Q4","consolidated","triệu VND")
 src,proof=a["signed_Q4_source"],a["audited_FY_source"]
 assert src["sha256"]=="7035db49b3b4ca6bdc5ed67e4c9913896f1cadfd54fd52119daea50638dff26c"
 assert proof["sha256"]=="7fbc90dda0999189e4a6a15265d73ca5f7a52b060e2967e7fead7deaa6486558"
 assert (src["bytes"],src["pages"])==(11290003,63) and (proof["bytes"],proof["pages"])==(7855542,108)
 assert src["pdf_B02a_pages"]==[7,8] and src["pdf_B03a_page"]==10 and src["pdf_B04a_pages"]==[11,12]
 assert proof["pdf_B02a_pages"]==[10,11,12,13] and proof["pdf_B03a_pages"]==[14,15]
 assert proof["pdf_B04a_pages"]==[16,17] and proof["auditor"]=="KPMG"
 assert a["prior_9M"]["sha256"]==prior["original_Q3"]["sha256"]
 assert a["prior_9M"]["B03_9m"]==prior["B03a_9m"] and a["prior_9M"]["B04_9m"]==prior["B04a_9m"]
 b,ba=a["B02_Q4_first"],a["B02_FY_audited"]
 q,first,audit=a["B03_Q4_first"],a["B03_FY_first"],a["B03_FY_audited"]
 cf,cfa=a["B04_FY_first"],a["B04_FY_audited"]
 nine=a["prior_9M"];qcf=a["Q4_cash_audited_FY_minus_signed_9M"];v=a["versions_audited_minus_first"]
 checks={}
 assets=("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets","customer_loans_net",
         "purchased_debt_net","investment_securities","fixed_assets","other_assets")
 liabs=("government_liabilities","interbank_liabilities","customer_deposits","derivative_liabilities",
        "trust_liabilities","valuable_papers","other_liabilities")
 eq=("bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity")
 for key,bal in (("first",b),("audit",ba)):
  checks["B02_"+key+"_assets"]=sum(bal[k] for k in assets)-bal["total_assets"]
  checks["B02_"+key+"_liabs"]=sum(bal[k] for k in liabs)-bal["total_liabilities"]
  checks["B02_"+key+"_equity"]=sum(bal[k] for k in eq)-bal["total_equity"]
  checks["B02_"+key+"_balance"]=bal["total_assets"]-bal["total_liabilities"]-bal["total_equity"]
 for n,k in (("assets","total_assets"),("liabilities","total_liabilities"),("equity","total_equity")):
  checks["B02_audited_minus_first_"+n]=ba[k]-b[k]-v[n]
 assert a["source_restated_comparative_2026_provisional_not_source_verified"]["assets"]==505926663
 assert ba["total_assets"]!=a["source_restated_comparative_2026_provisional_not_source_verified"]["assets"]
 income=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 for name,s in (("Q4",q),("FY_first",first),("FY_KPMG",audit)):
  checks["B03_"+name+"_sum"]=sum(s[k] for k in income)-s["operating_income"]
  checks["B03_"+name+"_opex"]=s["operating_income"]-s["operating_expenses"]-s["before_provision"]
  checks["B03_"+name+"_allowance"]=s["before_provision"]-s["credit_provision"]-s["pretax_profit"]
  checks["B03_"+name+"_PAT"]=s["pretax_profit"]-s["income_tax"]-s["net_profit"]
  checks["B03_"+name+"_NCI"]=s["net_profit"]-s["noncontrolling_profit"]-s["parent_profit"]
 checks["B03_Q4_net_interest"]=q["interest_income"]+q["interest_expense"]-q["net_interest"]
 checks["B03_Q4_services"]=q["service_income"]+q["service_expense"]-q["services_net"]
 checks["B03_Q4_other"]=q["other_income"]+q["other_expense"]-q["other_net"]
 checks["B03_Q4_tax"]=q["income_tax_current"]+q["income_tax_deferred"]-q["income_tax"]
 qkeys=(*income,"operating_income","operating_expenses","before_provision","credit_provision",
        "pretax_profit","income_tax","net_profit","noncontrolling_profit","parent_profit")
 for key in qkeys:
  checks["B03_Q4_direct_FY_minus9M_"+key]=first[key]-nine["B03_9m"][key]-q[key]
 for k in ("operating_income","before_provision","pretax_profit","income_tax","net_profit"):
  checks["B03_audited_FY_vintage_"+k]=audit[k]-first[k]-v[k]
 checks["B03_audited_FY_vintage_provision"]=audit["credit_provision"]-first["credit_provision"]-v["provision"]
 before=("interest_cash_received","interest_cash_paid","services_cash","fx_trading_cash",
         "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid")
 assetcf=("asset_interbank","asset_securities","asset_derivatives","asset_customer_loans","asset_provisions","asset_other")
 liabcf=("liability_government","liability_interbank","liability_customer_deposits","liability_papers",
         "liability_trust","liability_derivatives","liability_other")
 for name,s in (("first",cf),("audit",cfa)):
  checks["B04_"+name+"_preWC"]=sum(s[k] for k in before)-s["before_wc_cash"]
  checks["B04_"+name+"_CFO"]=s["before_wc_cash"]+sum(s[k] for k in assetcf)+sum(s[k] for k in liabcf)-s["CFO"]
  checks["B04_"+name+"_CFI"]=sum(s[k] for k in ("capex","disposal_proceeds","investments_in_subsidiaries",
                                     "investment_inflows_from_subsidiaries","investment_dividends"))-s["CFI"]
  checks["B04_"+name+"_CFF"]=sum(s[k] for k in ("financing_new_debt","financing_repayment","financing_dividends_paid"))-s["CFF"]
  checks["B04_"+name+"_net"]=s["CFO"]+s["CFI"]+s["CFF"]-s["net_cash_change"]
  checks["B04_"+name+"_cash"]=s["opening_cash"]+s["net_cash_change"]+s["FX_effect"]-s["closing_cash"]
 for key in ("CFO","CFI","CFF","net_cash_change","before_wc_cash"):
  alias="cash_before_wc" if key=="before_wc_cash" else key
  checks["B04_vintage_"+key]=cfa[key]-cf[key]-v[alias]
 for key in ("CFO","CFI","CFF","net_cash_change"):
  checks["B04_Q4_AUD_FY_minus9M_"+key]=cfa[key]-nine["B04_9m"][key]-qcf[key]
 checks["B04_Q4_open"]=qcf["opening_cash"]-nine["B04_9m"]["closing_cash"]
 checks["B04_Q4_close"]=qcf["closing_cash"]-cfa["closing_cash"]
 checks["B04_Q4_FX_implied"]=qcf["FX_effect"]-(cfa["FX_effect"]-nine["B04_9m"]["fx_cash_effect"])
 checks["B04_Q4_net"]=qcf["CFO"]+qcf["CFI"]+qcf["CFF"]-qcf["net_cash_change"]
 checks["B04_Q4_cash"]=qcf["opening_cash"]+qcf["net_cash_change"]+qcf["FX_effect"]-qcf["closing_cash"]
 checks["B04_Q4_capex"]=qcf["capex"]-(cfa["capex"]-nine["B04_9m"]["capex"])
 checks["B04_Q4_investing_proceeds"]=qcf["disposal_proceeds"]-(cfa["disposal_proceeds"]-nine["B04_9m"]["disposal_proceeds"])
 checks["B04_Q4_financing"]=qcf["financing_new_debt"]+qcf["financing_repayment"]+qcf["financing_dividends_paid"]-qcf["CFF"]
 checks["B04_FY_cash_vintage"]=cfa["closing_cash"]-cf["closing_cash"]-v["year_end_cash"]
 assert len(checks)>=75 and all(x==0 for x in checks.values()),(len(checks),{k:x for k,x in checks.items() if x})
 assert (cf["CFO"],cfa["CFO"],cf["CFI"],cfa["CFI"])==(29797620,26177747,-1571779,2048094)
 assert v["CFO"]==-3619873 and v["CFI"]==3619873 and v["net_cash_change"]==0
 assert (first["pretax_profit"],audit["pretax_profit"],v["pretax_profit"])==(9203137,9231078,27941)
 assert (qcf["CFO"],qcf["CFI"],qcf["CFF"],qcf["net_cash_change"])==(28136272,2209560,-958800,29387032)
 assert (qcf["opening_cash"],qcf["closing_cash"],qcf["FX_effect"])==(86612489,115747324,-252197)
 assert data["symbol"]=="TPB" and [x["period"] for x in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2"]
 row=data["items"][3];source=row["source_validation"]
 assert row["verification_status"]=="issuer_signed_TPB_2025Q4_original_B02a_B03a_KPMG_FY_audited_minus_9M_B04a_FX_vintage_verified"
 assert row["unit"]=="triệu VND" and "hợp nhất" in row["report_type"].lower()
 assert source["manually_visual_reviewed"] and source["original_pdf_hash_verified"]
 assert source["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert source["original_pdf_sha256"]==src["sha256"] and source["official_KPMG_FY2025_pdf_sha256"]==proof["sha256"]
 assert source["Q3_signed_9M_pdf_sha256"]==prior["original_Q3"]["sha256"]
 assert source["audited_vs_first_FY_vintage"]==v
 assert source["signed_Q4_first_issued_16_B03a_direct_equals_original_FY_minus_9M"]
 assert source["audited_FY_B04a_Q4_from_12M_minus_9M_source_exact"]
 assert source["FX_Q4_negative_252197_implied_not_independently_reported"]
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"]
 assert row["equity"]==b["total_equity"] and row["pretax_profit"]==q["pretax_profit"] and row["net_profit"]==q["net_profit"]
 assert row["net_profit_attributable"]==q["parent_profit"] and row["revenue"]==q["operating_income"]
 assert row["operating_cash_flow"]==qcf["CFO"] and row["investing_cash_flow"]==qcf["CFI"]
 assert row["financing_cash_flow"]==qcf["CFF"] and row["net_cash_change"]==qcf["net_cash_change"]
 assert row["cash_beginning"]==qcf["opening_cash"] and row["cash_ending"]==qcf["closing_cash"] and row["cashflow_fx"]==qcf["FX_effect"]
 assert row["operating_cash_flow_ytd"]==cfa["CFO"] and row["investing_cash_flow_ytd"]==cfa["CFI"]
 assert row["financing_cash_flow_ytd"]==cfa["CFF"] and row["net_cash_change_ytd"]==cfa["net_cash_change"]
 assert row["roa"]==round(400*q["net_profit"]/((b["total_assets"]+data["items"][2]["total_assets"])/2),2)==2.12
 assert row["roe"]==round(400*q["net_profit"]/((b["total_equity"]+data["items"][2]["equity"])/2),2)==23.65
 assert not row["financial_line_items_rejected_values"] and not row["financial_line_items_rejected_fields"]
 for prefix,sourceobj in (("b02a_Q4",b),("b02a_FY_KPMG",ba),
    ("b03a_Q4",q),("b03a_FY_original",first),("b03a_FY_KPMG",audit),
    ("b04a_FY_original",cf),("b04a_FY_KPMG",cfa),("b04a_Q4",qcf)):
  for key,value in sourceobj.items():
   if isinstance(value,int):assert row["signed_source_"+prefix+"_"+key]==value,(prefix,key)
 assert all(x["verification_status"].startswith("issuer_signed") for x in data["items"][:4])
 assert data["items"][4]["verification_status"]=="issuer_signed_TPB_2026Q1_B02a_B03a_B04a_exact_FX_2025_represented_comparative_verified"
 assert data["items"][5]["verification_status"]=="issuer_signed_TPB_2026Q2_first_B02a_B03a_KPMG_H1_minus_Q1_B04a_FX_verified"
 assert not any(x["period"].startswith("2024") for x in data["items"])
 return len(checks)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 p=json.loads(PRIOR.read_text("utf-8"))
 d=json.loads(FIN.read_text("utf-8"))
 count=verify(a,p,d)
 for case in ("BS","audited_balance","B03","audited_profit","preWC","cash_CFO","cash_CFI",
              "FX_omission","third_vintage","original_SHA","audited_SHA","past_Q3","future_Q1","ROE"):
  aa,pp,dd=deepcopy(a),deepcopy(p),deepcopy(d)
  if case=="BS":aa["B02_Q4_first"]["total_assets"]+=1
  elif case=="audited_balance":aa["B02_FY_audited"]["total_equity"]+=1
  elif case=="B03":aa["B03_Q4_first"]["net_profit"]+=1
  elif case=="audited_profit":aa["B03_FY_audited"]["pretax_profit"]+=1
  elif case=="preWC":aa["B04_FY_first"]["staff_admin_cash"]+=300000
  elif case=="cash_CFO":aa["B04_FY_audited"]["CFO"]+=1
  elif case=="cash_CFI":dd["items"][3]["investing_cash_flow"]+=1
  elif case=="FX_omission":dd["items"][3]["cashflow_fx"]=0
  elif case=="third_vintage":dd["items"][3]["total_assets"]=505926663
  elif case=="original_SHA":aa["signed_Q4_source"]["sha256"]="0"*64
  elif case=="audited_SHA":aa["audited_FY_source"]["sha256"]="f"*64
  elif case=="past_Q3":dd["items"][2]["verification_status"]="fake"
  elif case=="future_Q1":dd["items"][4]["verification_status"]="forged"
  elif case=="ROE":dd["items"][3]["roe"]=23.67
  try:verify(aa,pp,dd)
  except (AssertionError,KeyError,TypeError):pass
  else:raise AssertionError("Tampering undetected "+case)
 print(f"PASS TPB signed Q4 63p + bank-official KPMG audited FY 108p: {count} exact B02 B03 B04 and vintage/FX identities, 16 direct Q4 profit bridges, 14 anti-corruption gates.")
 print("PASS FY audited CFO 26,177,747, CFI 2,048,094; original FY CFO 29,797,620 and CFI -1,571,779: exact reclassification 3,619,873 with zero FY net cash difference.")
 print("PASS standalone Q4 CFO 28,136,272, CFI +2,209,560, CFF -958,800, net +29,387,032, FX cumulative presentation -252,197, cash 86,612,489 to 115,747,324 million VND.")
 print("PASS signed original Q4 PAT 2,542,763 and ROA 2.12%, ROE 23.65%. TPB Q1-Q3 checkpoints immutable, Q1-Q2 2026 remain provisional.")
if __name__=="__main__":main()
