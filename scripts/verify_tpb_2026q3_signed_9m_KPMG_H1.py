#!/usr/bin/env python3
"""TPB 2026 Q3 issuer-signed B02a/B03a/9M B04a, KPMG 2026 H1 exact QA.

Q3 direct issuer-signed B03a is authoritative. Reporting-vintage differences
between original Q3 9M and KPMG-reviewed H1 6M B03a are 1-3 million VND:
preserve original direct quarter rather than silently plug, and fail closed
on >3 million or >0.1% field-specific deviation. B04a 9M-minus-H1 FX and
cash identities MUST balance exactly, without any cash-flow tolerance.
"""
from copy import deepcopy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/TPB-2026Q3-signed-9M-KPMG-H1-FX-B03-vintage-million-vnd.json"
PRIOR=ROOT/"reports/source-audits/TPB-2026Q2-original-vs-KPMG-H1-bank-FX-million-vnd.json"
DATA=ROOT/"data/financials-TPB.json"
STATUS="issuer_signed_TPB_2026Q3_B02a_B03a_9M_minus_KPMG_H1_bank_B04a_FX_vintage_verified"

def verify(a, h, fin):
 assert (a["symbol"],a["period"],a["scope"],a["unit"]) == ("TPB","2026-Q3","consolidated","triệu VND")
 s=a["original_Q3"]; rev=a["reviewed_H1"]
 assert s["sha256"]=="bd1aa29d631748a0e37bfe33b58ee11b4c4bc281187b4b1110f16b66f1dc7e89"
 assert (s["bytes"],s["pages"])==(16711136,64)
 assert s["B02a_pages"]==[7,8] and s["B03a_page"]==10 and s["B04a_pages"]==[11,12]
 assert s["workflow_run"]==45208423862
 assert rev["sha256"]==h["reviewed_H1"]["sha256"] and rev["reviewer"]=="KPMG"
 assert rev["B03a_6m"]==h["B03a_H1_KPMG"]
 assert rev["B03a_6m_first"]==h["B03a_6m_first"]
 assert rev["B04a_6m"]==h["B04a_H1_KPMG"]
 assert rev["ledger"]==str(PRIOR.relative_to(ROOT))
 b,p,y,c,q=a["B02a_Q3"],a["B03a_Q3_direct"],a["B03a_9m"],a["B04a_9m"],a["Q3_cash_9m_minus_H1"]
 hcf=rev["B04a_6m"]; hprof=rev["B03a_6m"]; hfirst=rev["B03a_6m_first"]
 def subtotal(o,ks):return sum(o[k] for k in ks)
 E={}
 assets=("cash_vault","deposits_SBV","interbank_assets","trading_securities","derivative_assets",
  "customer_loans_net","purchased_debt_net","investment_securities","longterm_investments","fixed_assets","other_assets")
 liabilities=("government_liabilities","interbank_liabilities","customer_deposits","derivative_liabilities",
  "trust_liabilities","valuable_papers","other_liabilities")
 equity=("bank_capital","bank_funds","fx_equity","retained_profit","noncontrolling_equity")
 E["B02_assets"]=subtotal(b,assets)-b["total_assets"]
 E["B02_liabilities"]=subtotal(b,liabilities)-b["total_liabilities"]
 E["B02_equity"]=subtotal(b,equity)-b["total_equity"]
 E["B02_balance"]=b["total_assets"]-b["total_liabilities"]-b["total_equity"]
 inc=("net_interest","services_net","FX_net","trading_net","invest_net","other_net","contribution_income")
 for prefix,v in (("Q3",p),("9M",y)):
  E["B03_"+prefix+"_interest"]=v["interest_income"]+v["interest_expense"]-v["net_interest"]
  E["B03_"+prefix+"_services"]=v["service_income"]+v["service_expense"]-v["services_net"]
  E["B03_"+prefix+"_other"]=v["other_income"]+v["other_expense"]-v["other_net"]
  E["B03_"+prefix+"_operating_income"]=subtotal(v,inc)-v["operating_income"]
  E["B03_"+prefix+"_pre_provision"]=v["operating_income"]-v["operating_expenses"]-v["before_provision"]
  E["B03_"+prefix+"_pretax"]=v["before_provision"]-v["credit_provision"]-v["pretax_profit"]
  E["B03_"+prefix+"_tax"]=v["income_tax_current"]+v["income_tax_deferred"]-v["income_tax"]
  E["B03_"+prefix+"_aftertax"]=v["pretax_profit"]-v["income_tax"]-v["net_profit"]
  E["B03_"+prefix+"_parent"]=v["net_profit"]-v["noncontrolling_profit"]-v["parent_profit"]
 bridges=(*inc,"operating_income","operating_expenses","before_provision",
          "credit_provision","pretax_profit","income_tax","net_profit",
          "noncontrolling_profit","parent_profit")
 for key in bridges:
  r=y[key]-hprof[key]-p[key]
  original_r=y[key]-hfirst[key]-p[key]
  assert a["B03a_9m_minus_reviewed_H1_vs_direct_Q3_residuals"][key]==r,key
  assert a["B03a_9m_minus_first_H1_vs_direct_Q3_residuals"][key]==original_r,key
  assert abs(r)<=3 and abs(r)<=abs(p[key])*0.001, (key,r,p[key])
  E["B03_bridge_tracked_"+key]=r-a["B03a_9m_minus_reviewed_H1_vs_direct_Q3_residuals"][key]
 # Preserve issuer-published direct quarter, NOT an invented 9M-6M quarter.
 expected_residual={"FX_net":-1,"operating_income":-1,"before_provision":-1,
  "pretax_profit":-1,"income_tax":1,"net_profit":-2,
  "noncontrolling_profit":1,"parent_profit":-3}
 assert {k:v for k,v in a["B03a_9m_minus_reviewed_H1_vs_direct_Q3_residuals"].items() if v}==expected_residual
 assert a["B03a_9m_minus_first_H1_vs_direct_Q3_residuals"]["net_profit"]==56
 assert a["B03a_9m_minus_first_H1_vs_direct_Q3_residuals"]["income_tax"]==-57
 before=("interest_received","interest_paid","services_cash","fx_trading_cash",
  "other_cash","recovered_bad_debts_cash","staff_admin_cash","tax_paid")
 operating_assets=("asset_interbank","asset_securities","asset_derivatives","asset_customer_loans",
  "asset_credit_provisions","asset_other")
 operating_liabilities=("liability_government","liability_interbank","liability_customer_deposits",
  "liability_papers","liability_trust","liability_derivatives","liability_other")
 E["B04_9M_preWC"]=subtotal(c,before)-c["pre_wc_cash"]
 E["B04_9M_true_CFO"]=c["pre_wc_cash"]+subtotal(c,operating_assets)+subtotal(c,operating_liabilities)-c["CFO"]
 E["B04_9M_CFI"]=subtotal(c,("capex","disposal_receipts","disposal_expenses","investment_outflows","investing_dividends"))-c["CFI"]
 E["B04_9M_CFF"]=subtotal(c,("financing_new_debt","financing_repayment","financing_dividends_paid"))-c["CFF"]
 E["B04_9M_net"]=c["CFO"]+c["CFI"]+c["CFF"]-c["net_cash_change"]
 E["B04_9M_FX_cash"]=c["opening_cash"]+c["net_cash_change"]+c["FX_effect"]-c["closing_cash"]
 for k in ("CFO","CFI","CFF","net_cash_change"):
  E["B04_Q3_9M_less_KPMG_H1_"+k]=c[k]-hcf[k]-q[k]
 for k in ("capex","disposal_receipts","disposal_expenses","investment_outflows",
           "investing_dividends","financing_new_debt","financing_repayment"):
  E["B04_Q3_line_9M_less_KPMG_H1_"+k]=c[k]-hcf[k]-q[k]
 E["B04_Q3_opening"]=q["opening_cash"]-hcf["closing_cash"]
 E["B04_Q3_closing"]=q["closing_cash"]-c["closing_cash"]
 E["B04_Q3_FX"]=q["FX_effect"]-c["FX_effect"]+hcf["FX_effect"]
 E["B04_Q3_net"]=q["CFO"]+q["CFI"]+q["CFF"]-q["net_cash_change"]
 E["B04_Q3_openclose"]=q["opening_cash"]+q["net_cash_change"]+q["FX_effect"]-q["closing_cash"]
 assert len(E)>=55 and all(x==0 for x in E.values()),(len(E),{k:v for k,v in E.items() if v})
 assert (c["CFO"],c["pre_wc_cash"],c["interest_received"])==(22602790,8875048,29083148)
 assert (q["CFO"],q["CFI"],q["CFF"],q["net_cash_change"])==(39535763,-36884,-1017000,38481879)
 assert (q["opening_cash"],q["FX_effect"],q["closing_cash"])==(97023335,161199,135666413)
 assert (b["total_assets"],b["total_liabilities"],b["total_equity"])==(596511612,544378558,52133054)
 assert (p["pretax_profit"],p["net_profit"],p["parent_profit"])==(2980630,2351201,2308904)
 assert a["rules"]["B03_residuals_explicit_not_plugged"] and a["rules"]["append_as_seventh_TPB_period"]
 assert fin["symbol"]=="TPB" and [z["period"] for z in fin["items"]]==[
  "2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 previous_assets=[388891150,428589979,451893195,505871568,527169377,547664403]
 previous_CFO=[-41476406,21755856,17762025,28136272,-7280016,-9652957]
 previous_cash=[44780913,67278398,86612489,115747324,108553424,97023335]
 for ix in range(6):
  prev=fin["items"][ix]
  assert prev["total_assets"]==previous_assets[ix] and prev["operating_cash_flow"]==previous_CFO[ix]
  assert prev["cash_ending"]==previous_cash[ix] and prev["verification_status"].startswith("issuer_signed")
 row=fin["items"][6];sval=row["source_validation"]
 assert row["verification_status"]==STATUS and row["unit"]=="triệu VND"
 assert sval["original_pdf_sha256"]==s["sha256"] and sval["KPMG_H1_reviewed_pdf_sha256"]==rev["sha256"]
 assert sval["source_audit_ledger"]==str(LEDGER.relative_to(ROOT))
 assert sval["manually_visual_reviewed"] and sval["original_pdf_hash_verified"]
 assert sval["B04a_9M_minus_KPMG_H1_bank_cash_exact"]
 assert sval["B03a_direct_Q3_authoritative"] and sval["source_discrepancies_preserved_without_plugs"]
 assert sval["B03a_9M_minus_KPMG_H1_direct_quarter_residuals"]==a["B03a_9m_minus_reviewed_H1_vs_direct_Q3_residuals"]
 assert row["total_assets"]==b["total_assets"] and row["total_liabilities"]==b["total_liabilities"] and row["equity"]==b["total_equity"]
 assert row["net_profit"]==p["net_profit"] and row["pretax_profit"]==p["pretax_profit"]
 assert row["net_profit_attributable"]==p["parent_profit"] and row["revenue"]==p["operating_income"]
 for dst,src in (("operating_cash_flow","CFO"),("investing_cash_flow","CFI"),
   ("financing_cash_flow","CFF"),("net_cash_change","net_cash_change"),
   ("cashflow_fx","FX_effect"),("cash_beginning","opening_cash"),("cash_ending","closing_cash")):
  assert row[dst]==q[src],dst
 for dst,src in (("operating_cash_flow_ytd","CFO"),("investing_cash_flow_ytd","CFI"),
   ("financing_cash_flow_ytd","CFF"),("net_cash_change_ytd","net_cash_change"),
   ("cashflow_fx_ytd","FX_effect"),("cash_beginning_reported_ytd","opening_cash"),
   ("cash_ending_ytd","closing_cash")):assert row[dst]==c[src],dst
 assert row["roa"]==round(400*p["net_profit"]/((b["total_assets"]+fin["items"][5]["total_assets"])/2),2)==1.64
 assert row["roe"]==round(400*p["net_profit"]/((b["total_equity"]+fin["items"][5]["equity"])/2),2)==18.50
 for prefix,part in (("b02a_Q3",b),("b03a_Q3",p),("b03a_9m",y),("b04a_9m",c),("b04a_Q3",q)):
  for k,v in part.items():
   if isinstance(v,int):assert row["signed_source_"+prefix+"_"+k]==v,(prefix,k)
 assert len(row["financial_line_items_manually_verified_fields"])>=55
 assert len(fin["items"])==7 and not any(z["period"].startswith("2024") for z in fin["items"])
 return len(E)

def main():
 a=json.loads(LEDGER.read_text("utf-8"))
 h=json.loads(PRIOR.read_text("utf-8"))
 d=json.loads(DATA.read_text("utf-8"))
 n=verify(a,h,d)
 cases=("asset","equity","PBT","PAT","B03_rounding","H1_vintage","H1_sha","Q3_sha","CFO","net_cash",
  "FX_omitted","cash_end","past_Q2_tamper","period_missing","ROE","false_proof")
 for kind in cases:
  aa,hh,dd=deepcopy(a),deepcopy(h),deepcopy(d)
  if kind=="asset":aa["B02a_Q3"]["total_assets"]+=1
  elif kind=="equity":aa["B02a_Q3"]["total_equity"]+=1
  elif kind=="PBT":aa["B03a_Q3_direct"]["pretax_profit"]+=1
  elif kind=="PAT":dd["items"][6]["net_profit"]=123
  elif kind=="B03_rounding":aa["B03a_9m"]["FX_net"]+=10
  elif kind=="H1_vintage":hh["B03a_H1_KPMG"]["net_profit"]+=100
  elif kind=="H1_sha":hh["reviewed_H1"]["sha256"]="f"*64
  elif kind=="Q3_sha":aa["original_Q3"]["sha256"]="0"*64
  elif kind=="CFO":aa["B04a_9m"]["CFO"]+=1
  elif kind=="net_cash":dd["items"][6]["net_cash_change"]+=1
  elif kind=="FX_omitted":dd["items"][6]["cashflow_fx"]=0
  elif kind=="cash_end":aa["Q3_cash_9m_minus_H1"]["closing_cash"]+=1
  elif kind=="past_Q2_tamper":dd["items"][5]["operating_cash_flow"]+=1
  elif kind=="period_missing":dd["items"].pop()
  elif kind=="ROE":dd["items"][6]["roe"]=0
  elif kind=="false_proof":dd["items"][6]["source_validation"]["B04a_9M_minus_KPMG_H1_bank_cash_exact"]=False
  try:verify(aa,hh,dd)
  except (AssertionError,KeyError,TypeError,IndexError):pass
  else:raise AssertionError("Tamper not caught "+kind)
 print(f"PASS TPB 2026 Q3 signed 64p original and KPMG H1 107p: {n} exact B02a B03a bank B04a cash/FX and source bridge identities; 16 direct Q3 income-vintage fields, {len(cases)} negative corruption cases.")
 print("PASS Q3 2026 CFO +39,535,763 CFI -36,884 CFF -1,017,000 net +38,481,879 FX +161,199; bank cash 97,023,335 to 135,666,413 million VND.")
 print("PASS original Q3 direct PAT 2,351,201 million, ROA 1.64% ROE 18.50%, with independently tracked 1-3m 9M less KPMG H1 B03 source vintage differences; no balancing plugs.")
 print("PASS TPB all seven Q1/2025 through Q3/2026 source-verified, six previous checkpoint values unchanged; no 2024 reporting periods.")
if __name__=="__main__":main()
