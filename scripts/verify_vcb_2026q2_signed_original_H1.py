#!/usr/bin/env python3
"""VCB 2026Q2 bank consolidated original: 40 independent issuer equations.

Original million VND, direct Q2 B03 earnings check vs 6M−signed Q1,
standalone Q2 bank B04 cash from signed H1 less original Q1, no interest
receipts/capex substitution, bank B02 vault cash != bank B04 cash.
"""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCB-2026Q2-issuer-signed-H1-sixmonth-million-vnd.json"
PRIOR=ROOT/"reports/source-audits/VCB-2026Q1-consolidated-original-29april-million-vnd.json"
FIN=ROOT/"data/financials-VCB.json"
def read(path):return json.loads(path.read_text("utf-8"))
def verify_source(src,prior):
 assert src["ticker"]=="VCB" and src["period"]=="2026-Q2" and src["unit"]=="triệu VND"
 assert "consolidated" in src["scope"] and prior["period"]=="2026-Q1"
 z=src["issuer_source_original"]
 assert z["signed_date"]=="2026-07-30"
 assert z["pdf_sha256"]=="fb0bc8ebbad76c175e61f7c2a7b78ae67608623a8d715d5470a08dbac00ff223"
 assert z["pages"]==55 and z["bytes"]==6028106
 assert z["workflow_run"]==45011853335 and z["artifact_id"]==14750210893
 assert z["url"].endswith("VCB_Baocaotaichinh_Q2_2026_Hopnhat.pdf")
 f=src["original_source_million_vnd_fields"]
 assert len(f)==141 and all(type(v)==int for v in f.values())
 N=lambda k:f[k]
 S=lambda ks:sum(N(k) for k in ks)
 identity={
  "balance":N("total_assets")-N("total_liabilities")-N("equity"),
  "interbank":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")+N("bank_interbank_impairment")-N("bank_deposits_and_loans_at_credit_institutions"),
  "trading":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
  "customer_loans":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
  "investment_sec":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
  "long_invest":S(("bank_jv_investments","bank_associates_investments","bank_other_long_term_investments","bank_longterm_investment_impairment"))-N("bank_contributions_and_long_term_investments"),
  "fixed":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
  "tang_depr":N("bank_fixed_tangible_gross")+N("bank_fixed_tangible_depreciation")-N("bank_fixed_assets_tangible"),
  "intang_depr":N("bank_fixed_intangible_gross")+N("bank_fixed_intangible_depreciation")-N("bank_fixed_assets_intangible"),
  "other_assets":S(("bank_other_receivables","bank_interest_receivables","bank_deferred_tax_assets","bank_other_assets_misc","bank_other_assets_impairment"))-N("bank_other_assets"),
  "assets":S(("bank_cash_on_hand","bank_deposits_at_state_bank","bank_deposits_and_loans_at_credit_institutions","bank_trading_securities","bank_derivative_assets","bank_customer_loans","bank_investment_securities","bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
  "interbank_funding":N("bank_deposits_from_credit_institutions")+N("bank_borrowings_from_credit_institutions")-N("bank_deposits_and_borrowings_from_credit_institutions"),
  "other_liabilities":N("bank_interest_payable")+N("bank_other_payables")-N("bank_other_liabilities"),
  "liabs":S(("bank_government_borrowing","bank_deposits_and_borrowings_from_credit_institutions","bank_customer_deposits","bank_derivative_liabilities","bank_funding_and_trust_liabilities","bank_valuable_papers","bank_other_liabilities"))-N("total_liabilities"),
  "capital":N("bank_capital_share")+N("bank_capital_premium")+N("bank_capital_other")-N("bank_capital_and_capital_surplus"),
  "retained":N("retained_prior_earnings")+N("retained_current_earnings")-N("retained_earnings"),
  "equity":S(("bank_capital_and_capital_surplus","bank_funds","bank_foreign_exchange_equity","retained_earnings","bank_non_controlling_equity"))-N("equity"),
  "net_interest":N("bank_interest_income")+N("bank_interest_expense")-N("bank_net_interest_income"),
  "net_service":N("bank_service_income")+N("bank_service_expense")-N("bank_net_service_income"),
  "net_other":N("bank_other_operating_income")+N("bank_other_operating_expense")-N("bank_other_operating_net"),
  "revenue":S(("bank_net_interest_income","bank_net_service_income","bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income"))-N("revenue"),
  "operating_profit":N("revenue")+N("bank_operating_expenses")-N("bank_pre_provision_operating_profit"),
  "pretax":N("bank_pre_provision_operating_profit")+N("bank_provision_expense")-N("pretax_profit"),
  "income_tax":-N("bank_tax_current")-N("bank_tax_deferred")-N("income_tax"),
  "net_profit":N("pretax_profit")-N("income_tax")-N("net_profit"),
  "NCI":N("net_profit")+N("bank_non_controlling_profit")-N("net_profit_attributable"),
  "h1_net_interest":N("h1_bank_interest_income")+N("h1_bank_interest_expense")-N("h1_bank_net_interest_income"),
  "h1_net_service":N("h1_bank_service_income")+N("h1_bank_service_expense")-N("h1_bank_net_service_income"),
  "h1_net_other":N("h1_bank_other_operating_income")+N("h1_bank_other_operating_expense")-N("h1_bank_other_operating_net"),
  "h1_revenue":S(("h1_bank_net_interest_income","h1_bank_net_service_income","h1_bank_fx_net_income","h1_bank_trading_securities_net","h1_bank_investment_securities_net","h1_bank_other_operating_net","h1_bank_dividend_and_capital_income"))-N("h1_revenue"),
  "h1_operating_profit":N("h1_revenue")+N("h1_bank_operating_expenses")-N("h1_bank_pre_provision_operating_profit"),
  "h1_pretax":N("h1_bank_pre_provision_operating_profit")+N("h1_bank_provision_expense")-N("h1_pretax_profit"),
  "h1_income_tax":-N("h1_bank_tax_current")-N("h1_bank_tax_deferred")-N("h1_income_tax"),
  "h1_net":N("h1_pretax_profit")-N("h1_income_tax")-N("h1_net_profit"),
  "h1_NCI":N("h1_net_profit")+N("h1_bank_non_controlling_profit")-N("h1_net_profit_attributable"),
  "cash_before_wc":S(("bank_cashflow_interest_received_ytd","bank_cashflow_interest_paid_ytd","bank_cashflow_service_net_received_ytd","bank_cashflow_fx_net_ytd","bank_cashflow_other_net_ytd","bank_cashflow_recovered_bad_debt_ytd","bank_cashflow_staff_management_paid_ytd","bank_cashflow_income_tax_paid_ytd"))-N("bank_cfo_before_balance_changes_ytd"),
  "CFO":N("bank_cfo_before_balance_changes_ytd")+S(("bank_wc_deposits_loans_with_banks_ytd","bank_wc_trading_securities_ytd","bank_wc_derivative_assets_ytd","bank_wc_customer_loans_ytd","bank_wc_write_off_ytd","bank_wc_other_assets_ytd","bank_wc_government_funding_ytd","bank_wc_other_bank_funding_ytd","bank_wc_customer_deposits_ytd","bank_wc_debt_securities_ytd","bank_wc_trust_funding_ytd","bank_wc_derivative_liabilities_ytd","bank_wc_other_operating_liabilities_ytd","bank_wc_bank_funds_ytd"))-N("operating_cash_flow_ytd"),
  "CFI":S(("bank_investing_capex_ytd","bank_investing_disposals_received_ytd","bank_investing_disposals_expense_ytd","bank_investing_dividends_received_ytd"))-N("investing_cash_flow_ytd"),
  "cash_sections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
  "cash_bridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd")
 }
 assert len(identity)==40 and set(identity)==set(src["source_checks_million_vnd"])
 assert all(v==0 for v in identity.values()),identity
 assert all(int(src["source_checks_million_vnd"][k])==identity[k] for k in identity)
 p=prior["original_source_million_vnd_fields"]
 assert len(p)==116
 assert prior["signed_original"]["source_pdf_sha256"]=="fd4d634f10478caa9f5f1e0b2b85f3dbae86d1f619e20f2e797ffb6ede244879"
 direct=("bank_interest_income","bank_interest_expense","bank_net_interest_income",
  "bank_service_income","bank_service_expense","bank_net_service_income",
  "bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net",
  "bank_other_operating_income","bank_other_operating_expense","bank_other_operating_net",
  "bank_dividend_and_capital_income","revenue","bank_operating_expenses",
  "bank_pre_provision_operating_profit","bank_provision_expense","pretax_profit",
  "bank_tax_current","bank_tax_deferred","income_tax","net_profit",
  "bank_non_controlling_profit","net_profit_attributable")
 assert len(direct)==24
 for k in direct:
  assert N("h1_"+k)-p[k]==N(k),(k,N("h1_"+k),p[k],N(k))
 quarter={k:N(k+"_ytd")-p[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
 quarter["cash_beginning"]=p["cash_ending"]
 quarter["cash_ending"]=N("cash_ending_ytd")
 assert quarter==src["quarter_only_bank_cashflow_million_vnd"],quarter
 assert quarter["operating_cash_flow"]+quarter["investing_cash_flow"]+quarter["financing_cash_flow"]==quarter["net_cash_change"]
 assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
 assert N("cash_beginning_reported_ytd")==p["cash_beginning"]==541688802
 assert N("bank_cash_on_hand")!=N("cash_ending_ytd")
 assert N("operating_cash_flow_ytd")==130996443 and N("bank_cashflow_interest_received_ytd")==67450619
 assert N("investing_cash_flow_ytd")==-645581 and N("bank_investing_capex_ytd")==-680065
 return f,quarter
def verify(src,prior,data):
 f,quarter=verify_source(src,prior)
 assert data["symbol"]=="VCB" and all(not i["period"].startswith("2024") for i in data["items"])
 row=next(x for x in data["items"] if x["period"]=="2026-Q2")
 assert row["verification_status"]=="issuer_signed_VCB_2026Q2_consolidated_B02_B03_B04_signed_6M_minus_Q1"
 assert "hợp nhất" in row["report_type"].lower() and row["unit"]=="triệu VND"
 assert row["source_url"]==src["issuer_source_original"]["url"]
 v=row["source_validation"]
 assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
 assert v["original_pdf_sha256"]==src["issuer_source_original"]["pdf_sha256"] and v["original_pdf_hash_verified"] is True
 assert v["manually_visual_reviewed"] is True and v["source_is_consolidated_financial_statements"] is True
 assert v["source_40_accounting_checks_zero_million"] is True
 assert v["source_B03_Q2_direct_matches_6M_minus_Q1_24_lines"] is True
 assert v["source_quarter_cashflow_zero_residual"] is True
 assert row["cashflow_period_basis"]=="year_to_date"
 verified=set(row["financial_line_items_manually_verified_fields"])
 for k,value in f.items():
  assert k in verified and row.get(k)==value,(k,value,row.get(k))
 for k,value in quarter.items():
  assert k in verified and row.get(k)==value,(k,value,row.get(k))
 assert row["bank_cash_and_equivalents_cashflow_basis"]==row["cash_ending"]
 assert row["bank_cash_on_hand"]!=row["cash_ending"]
 assert row["net_profit_attributable"]!=row["net_profit"]
 return len(f)
def main():
 s,p,d=read(SRC),read(PRIOR),read(FIN)
 n=verify(s,p,d)
 for which in ("source_assets","source_h1_cfo","website_q2_cfo","interest_receipt_as_cfo"):
  a,b,c=copy.deepcopy(s),copy.deepcopy(p),copy.deepcopy(d)
  r=next(x for x in c["items"] if x["period"]=="2026-Q2")
  if which=="source_assets":a["original_source_million_vnd_fields"]["total_assets"]+=1
  elif which=="source_h1_cfo":a["original_source_million_vnd_fields"]["operating_cash_flow_ytd"]+=1
  elif which=="website_q2_cfo":r["operating_cash_flow"]+=1
  else:r["operating_cash_flow"]=r["bank_cashflow_interest_received_ytd"]
  try:verify(a,b,c)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError("Bank statement corruption undetected: "+which)
 print(f"PASS VCB 2026-Q2: {n} signed bank source million-VND fields, 40 equations zero residual, all 24 H1-minus-Q1 Q2 earnings lines exact, 4 mutation controls.")
 print("Bank Q2 CFO +95,598,249 CFI -351,473 CFF 0 net +95,246,776 cash end 672,039,664 million VND.")
if __name__=="__main__":main()
