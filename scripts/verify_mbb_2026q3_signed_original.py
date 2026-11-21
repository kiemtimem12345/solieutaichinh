#!/usr/bin/env python3
"""MBB consolidated 2026 Q3 signed B02a, B03a Q3 and B04a 9M-minus-H1.

All currency in bank signed source is *million VND*, not VND; signs exactly
as original. 61-page source PDFs each fully recovered and SHA-256 hashed,
original page renders p3,p4,p6,p7,p8 reviewed. 0.1% tolerance not used.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"reports/source-audits/MBB-2026Q3-signed-consolidated-B02a-B03a-B04a-million-vnd.json"
DATA=ROOT/"data/financials-MBB.json"
REQUIRED_PNL=("bank_interest_income","bank_interest_expense","bank_net_interest_income",
"bank_service_income","bank_service_expense","bank_net_service_income",
"bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net",
"bank_other_operating_net","bank_dividend_and_capital_income","revenue",
"bank_operating_expenses","bank_pre_provision_operating_profit","bank_provision_expense",
"pretax_profit","income_tax_current","income_tax_deferred","income_tax",
"net_profit","bank_non_controlling_profit","net_profit_attributable")
P_AND_L_COMPONENTS=("bank_net_interest_income","bank_net_service_income",
"bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net",
"bank_other_operating_net","bank_dividend_and_capital_income")
B01_ASSETS=("bank_cash_on_hand","bank_deposits_at_state_bank",
"bank_deposits_and_loans_to_credit_institutions","bank_trading_securities",
"bank_customer_loans","bank_debt_purchases_net","bank_investment_securities",
"bank_contributions_and_long_term_investments","fixed_assets",
"bank_investment_property","bank_other_assets")
B01_LIABS=("bank_government_and_state_bank_liabilities",
"bank_deposits_and_borrowings_from_credit_institutions",
"bank_customer_deposits","bank_derivatives_and_other_financial_liabilities",
"bank_funding_and_trust_liabilities","bank_valuable_papers","bank_other_liabilities")
B01_CAPITAL=("bank_capital_and_funds","bank_reserves",
"bank_fx_difference","retained_earnings","bank_non_controlling_equity")

def eq(original):
 b=original["Q3_B02a_VND_millions"]
 p=original["Q3_B03a_quarter_VND_millions"]
 h=original["Q2_B04a_6M_YTD_VND_millions"]
 y=original["Q3_B04a_9M_YTD_VND_millions"]
 z=original["Q3_B04a_standalone_quarter_derived_VND_millions"]
 v={
  "b01_assets":sum(b[k] for k in B01_ASSETS)-b["total_assets"],
  "b01_debt":sum(b[k] for k in B01_LIABS)-b["total_liabilities"],
  "b01_debt_equity":b["total_liabilities"]+b["equity"]-b["total_assets"],
  "b01_capital":sum(b[k] for k in B01_CAPITAL)-b["equity"],
  "b01_customer_loans":b["bank_customer_loans_gross"]+b["bank_customer_loan_loss_allowance"]-b["bank_customer_loans"],
  "b01_debt_purchases":b["bank_debt_purchases_gross"]+b["bank_debt_purchases_provision"]-b["bank_debt_purchases_net"],
  "b01_trading_securities":b["bank_trading_securities_gross"]+b["bank_trading_securities_provision"]-b["bank_trading_securities"],
  "b01_investment_securities":b["bank_available_for_sale_securities"]+b["bank_held_to_maturity_securities"]+b["bank_investment_securities_allowance"]-b["bank_investment_securities"],
  "b01_other_liabilities":b["bank_interest_payable"]+b["bank_other_payables_and_liabilities"]+b["bank_other_provisions"]-b["bank_other_liabilities"],
  "b03_interest":p["bank_interest_income"]+p["bank_interest_expense"]-p["bank_net_interest_income"],
  "b03_service":p["bank_service_income"]+p["bank_service_expense"]-p["bank_net_service_income"],
  "b03_revenue":sum(p[k] for k in P_AND_L_COMPONENTS)-p["revenue"],
  "b03_preprovision":p["revenue"]+p["bank_operating_expenses"]-p["bank_pre_provision_operating_profit"],
  "b03_provision":p["bank_pre_provision_operating_profit"]+p["bank_provision_expense"]-p["pretax_profit"],
  "b03_income_tax":p["income_tax_current"]+p["income_tax_deferred"]+p["income_tax"],
  "b03_profit":p["pretax_profit"]-p["income_tax"]-p["net_profit"],
  "b03_parent_profit":p["net_profit"]-p["bank_non_controlling_profit"]-p["net_profit_attributable"],
  "b04_six_month_sections":h["CFO"]+h["CFI"]+h["CFF"]-h["net"],
  "b04_six_month_cash":h["cash_beginning"]+h["net"]-h["cash_ending"],
  "b04_nine_month_sections":y["CFO"]+y["CFI"]+y["CFF"]-y["net"],
  "b04_nine_month_cash":y["cash_beginning"]+y["net"]-y["cash_ending"],
  "b04_year_open":y["cash_beginning"]-h["cash_beginning"],
  "b04_q3_sections":z["CFO"]+z["CFI"]+z["CFF"]-z["net"],
  "b04_q3_cash":z["cash_beginning"]+z["net"]-z["cash_ending"],
  "b04_q3_net_change":z["cash_ending"]-h["cash_ending"]-z["net"],
  "b04_capex":z["capex"]-y["capex"]+h["capex"],
  "b04_dividends":z["dividends_paid"]-y["dividends_paid"]+h["dividends_paid"]
 }
 assert len(v)==27
 # Independently rederive all 27 identities while retaining the audit
 # ledger's source-side descriptive labels. Match each category one-to-one.
 labels={
 "b01_assets":"B01_assets_topline","b01_debt":"B01_liabilities_topline",
 "b01_debt_equity":"B01_total_balance","b01_capital":"B01_equity",
 "b01_customer_loans":"B01_loan_net","b01_debt_purchases":"B01_debt_buy_net",
 "b01_trading_securities":"B01_trading_net","b01_investment_securities":"B01_investment_net",
 "b01_other_liabilities":"B01_other_liabilities","b03_interest":"B03_interest",
 "b03_service":"B03_service","b03_revenue":"B03_operating_income",
 "b03_preprovision":"B03_preprovision","b03_provision":"B03_provision",
 "b03_income_tax":"B03_income_tax","b03_profit":"B03_profit",
 "b03_parent_profit":"B03_attributable",
 "b04_six_month_sections":"B04_Q2_sections","b04_six_month_cash":"B04_Q2_cash",
 "b04_nine_month_sections":"B04_Q3YTD_sections","b04_nine_month_cash":"B04_Q3YTD_cash",
 "b04_year_open":"B04_same_opening","b04_q3_sections":"B04_quarter_sections",
 "b04_q3_cash":"B04_quarter_cash","b04_q3_net_change":"B04_quarter_net_delta",
 "b04_capex":"B04_capex","b04_dividends":"B04_dividend"
 }
 assert set(labels)==set(v)
 assert set(labels.values())==set(original["source_accounting_identity_residuals_million_vnd"])
 assert {labels[k]:val for k,val in v.items()}==original["source_accounting_identity_residuals_million_vnd"],v
 assert set(v.values())=={0},v
 for k in ("CFO","CFI","CFF","net","capex","dividends_paid"):
  assert z[k]==y[k]-h[k],k
 assert z["cash_beginning"]==h["cash_ending"]
 assert z["cash_ending"]==y["cash_ending"]
 return (b,p,h,y,z)

def check(a,d):
 assert a["symbol"]=="MBB" and a["scope"]=="consolidated"
 assert a["original_currency"]=="triệu VND"
 assert a["specialist_forms"]=={"balance":"B02a/TCTD-HN","income":"B03a/TCTD-HN","cashflow":"B04a/TCTD-HN direct cash flow"}
 assert a["signed_pdf"]["Q2"]["sha256"]=="a86757a4499953264ca22dd57ae2e3257057631107742e1d04ad1ecd0e2c23d1"
 assert a["signed_pdf"]["Q3"]["sha256"]=="bd5b2bad6c4c0669f16e9673c9a076d100fa6eb51bc7085bf66db89053d618ce"
 for period in ("Q2","Q3"):
  assert a["signed_pdf"][period]["pages"]==61
  assert a["signed_pdf"][period]["visual_pages"]==[3,4,6,7,8]
 assert a["source_checks_count"]==27 and a["source_checks_max_abs_residual_million_vnd"]==0
 b,p,h,y,z=eq(a)
 rows={r["period"]:r for r in d["items"]}
 assert len(rows)==7 and set(rows)==set(["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"])
 row=rows["2026-Q3"];q1=rows["2026-Q1"];q2=rows["2026-Q2"]
 assert row["report_type"].startswith("BCTC hợp nhất MBB Q3/2026")
 assert row["unit"]=="triệu VND" and row["symbol"]=="MBB"
 assert row["verification_status"]=="issuer_signed_original_visual_verified_B02a_B03a_B04a_Q3_9M_minus_H1_27_exact_million_vnd_checks"
 assert row["roa"] is None and row["roe"] is None and row["eps"] is None
 assert row["eps_ytd"]==2563
 assert row["source_url"]==a["signed_pdf"]["Q3"]["url"]
 sv=row["source_validation"]
 assert sv["source_ledger_path"]==str(LEDGER.relative_to(ROOT))
 assert sv["issuer_signed_pdf_q3_2026_sha256"]==a["signed_pdf"]["Q3"]["sha256"]
 assert sv["issuer_signed_pdf_q2_2026_sha256"]==a["signed_pdf"]["Q2"]["sha256"]
 assert sv["source_ledger_identity_count"]==27 and sv["verified_cash_bridge_million_vnd_residual"]==0
 assert sv["source_scope"]=="consolidated" and sv["source_scope_verified"] is True
 assert sv["human_original_visual_reviewed"] is True
 assert sv["signed_eps_current_q3_cell_blank"] is True
 assert sv["legal_disclosure_compliance_certified"] is False
 assert row["cashflow_period_basis"]=="quarter" and row["cashflow_ytd_period_basis"]=="nine_months"
 verified=set(row["financial_line_items_manually_verified_fields"])
 assert set(REQUIRED_PNL)<=verified
 assert set(REQUIRED_PNL)<=set(row["financial_line_items_extracted_fields"])
 for k,val in b.items():
  if k in row:
   assert type(row[k])==int and row[k]==val,("B02a",k)
 for k,val in p.items():
  assert type(row.get(k))==int and row[k]==val,("B03a",k)
 for src,target in (("CFO","operating_cash_flow"),("CFI","investing_cash_flow"),
 ("CFF","financing_cash_flow"),("net","net_cash_change"),
 ("capex","capital_expenditure"),("dividends_paid","dividends_paid"),
 ("cash_beginning","cash_beginning"),("cash_ending","cash_ending")):
  assert row[target]==z[src],target
  key=target+"_ytd" if target not in ("cash_beginning","cash_ending") else "cash_beginning_reported_ytd" if target=="cash_beginning" else "cash_ending_ytd"
  assert row[key]==y[src],key
 assert q2["period"]=="2026-Q2" and q2["source_url"]==a["signed_pdf"]["Q2"]["url"]
 assert q2["operating_cash_flow_ytd"]==h["CFO"]
 for k in ("revenue","pretax_profit","net_profit","net_profit_attributable"):
  assert q1[k]+q2[k]+p[k]==a["Q3_B03a_9M_VND_millions"][k],k
  assert row[k+"_ytd"]==a["Q3_B03a_9M_VND_millions"][k],k
 assert all(row[k]<0 for k in ("bank_interest_expense","bank_service_expense","bank_operating_expenses","bank_provision_expense","income_tax_current","income_tax_deferred"))
 return True

def main():
 a=json.loads(LEDGER.read_text("utf-8"));d=json.loads(DATA.read_text("utf-8"))
 check(a,d)
 # Negative controls: never absorb a cash/period/scope/unit mistake into 0.1% waiver.
 def deny(changed):
  try:check(a,changed)
  except AssertionError:return
  raise AssertionError("Bad signed source data accepted")
 x=json.loads(json.dumps(d))
 next(z for z in x["items"] if z["period"]=="2026-Q3")["operating_cash_flow"]=-65264905
 deny(x)
 x=json.loads(json.dumps(d))
 next(z for z in x["items"] if z["period"]=="2026-Q3")["unit"]="VND"
 deny(x)
 x=json.loads(json.dumps(d))
 next(z for z in x["items"] if z["period"]=="2026-Q3")["report_type"]="BCTC riêng"
 deny(x)
 x=json.loads(json.dumps(d))
 next(z for z in x["items"] if z["period"]=="2026-Q3")["eps"]=2563
 deny(x)
 x=json.loads(json.dumps(d))
 next(z for z in x["items"] if z["period"]=="2026-Q3")["cash_beginning"]=239259989
 deny(x)
 print("PASS MBB consolidated Q3 2026 signed specialist B02a/B03a/B04a bank model; "
       "27/27 exact million-VND accounting identities, 9M-minus-H1 standalone cash "
       "CFO -12,063,094 CFI -789,880 CFF +5,047,866, Q3 PAT 8,251,873, "
       "MBB seven financial periods in scope; 5 negative tests.")
if __name__=="__main__":
 main()
