#!/usr/bin/env python3
"""VCB 2026Q1 consolidated bank signed B02/B03/B04 source integrity.

Thirty independent exact million-VND equations plus tamper tests. Bank B04
CFO is not gross interest receipts and cash equivalent is not B02 vault cash.
Audited FY2025 opening version is NOT identical to first-issued 2025 Q4.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"reports/source-audits/VCB-2026Q1-consolidated-original-29april-million-vnd.json"
Q4=ROOT/"reports/source-audits/VCB-2025Q4-original-signed-consolidated-FY-million-vnd.json"
FIN=ROOT/"data/financials-VCB.json"
QUEUE=ROOT/"reports/financial-exception-queue.json"
def read(p):return json.loads(p.read_text("utf8"))
def source_checks(a,prior):
 assert a["ticker"]=="VCB" and a["period"]=="2026-Q1" and a["unit"]=="triệu VND"
 assert "consolidated" in a["scope"]
 z=a["signed_original"]
 assert z["signed_date"]=="2026-04-29" and z["source_pdf_sha256"]=="fd4d634f10478caa9f5f1e0b2b85f3dbae86d1f619e20f2e797ffb6ede244879"
 assert z["pdf_pages"]==53 and z["pdf_bytes"]==8505770
 assert z["source_proof_action_run"]==44972227179 and z["artifact_id"]==14733699149
 assert z["url"].endswith("VCB_Baocaotaichinh_Q1_2026_Hopnhat.pdf")
 f=a["original_source_million_vnd_fields"]
 assert len(f)==116 and all(type(v)==int for v in f.values())
 N=lambda k:f[k]
 S=lambda ks:sum(N(k) for k in ks)
 eq={
 "balance":N("total_assets")-N("total_liabilities")-N("equity"),
 "bank_interbank":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")+N("bank_interbank_impairment")-N("bank_deposits_and_loans_at_credit_institutions"),
 "trading":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
 "customer_loans":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
 "invest_securities":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
 "long_invest":S(("bank_jv_investments","bank_associates_investments","bank_other_long_term_investments","bank_longterm_investment_impairment"))-N("bank_contributions_and_long_term_investments"),
 "fixed":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
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
 "NCI_profit":N("net_profit")+N("bank_non_controlling_profit")-N("net_profit_attributable"),
 "cfo_before_wc":S(("bank_cashflow_interest_received","bank_cashflow_interest_paid","bank_cashflow_service_net_received","bank_cashflow_fx_net","bank_cashflow_other_net","bank_cashflow_recovered_bad_debt","bank_cashflow_staff_management_paid","bank_cashflow_income_tax_paid"))-N("bank_cfo_before_balance_changes"),
 "CFO":N("bank_cfo_before_balance_changes")+S(("bank_wc_deposits_loans_with_banks","bank_wc_trading_securities","bank_wc_derivative_assets","bank_wc_customer_loans","bank_wc_write_off","bank_wc_other_assets","bank_wc_government_funding","bank_wc_other_bank_funding","bank_wc_customer_deposits","bank_wc_debt_securities","bank_wc_trust_funding","bank_wc_derivative_liabilities","bank_wc_other_operating_liabilities","bank_wc_bank_funds"))-N("operating_cash_flow"),
 "CFI":S(("bank_investing_capex","bank_investing_disposals_received","bank_investing_disposals_expense","bank_investing_dividends_received"))-N("investing_cash_flow"),
 "cash_sections":N("operating_cash_flow")+N("investing_cash_flow")+N("financing_cash_flow")-N("net_cash_change"),
 "cash_bridge":N("cash_beginning")+N("net_cash_change")-N("cash_ending"),
 "audited_FY2025_compare_balance":N("audited_FY2025_comparison_total_assets")-N("audited_FY2025_comparison_total_liabilities")-N("audited_FY2025_comparison_equity")
 }
 assert len(eq)==30 and set(eq)==set(a["source_accounting_checks_million_vnd"])
 assert all(z==0 for z in eq.values()),eq
 assert all(int(a["source_accounting_checks_million_vnd"][k])==eq[k] for k in eq)
 assert N("bank_cashflow_interest_received")==31437617 and N("operating_cash_flow")==35398194
 assert N("cash_beginning")+N("net_cash_change")==N("cash_ending")==576792888
 assert N("bank_cash_on_hand")!=N("cash_ending")
 assert N("financing_cash_flow")==0
 assert prior["period"]=="2025-Q4" and prior["original_report"]["pdf_sha256"]=="1f71919eae463bd24e6978e4ebb89d54c5c53f5b0645adf0fd439e71bdb86aa8"
 old=prior["signed_original_million_vnd_fields"]
 assert N("audited_FY2025_comparison_total_assets")-old["total_assets"]==350221
 assert N("audited_FY2025_comparison_total_liabilities")-old["total_liabilities"]==3327371
 assert N("audited_FY2025_comparison_equity")-old["equity"]==-2977150
 assert N("cash_beginning")-old["cash_ending_ytd"]==889334
 assert a["source_audited_comparative_vs_original_asfiled_2025FY_million_vnd"]["audited_start_vs_asfiled_FY2025_cash_million"]==889334
 return f
def verify(a,p,d,queue):
 f=source_checks(a,p)
 assert d["symbol"]=="VCB"
 q=next(x for x in d["items"] if x["period"]=="2026-Q1")
 assert q["verification_status"]=="issuer_signed_VCB_2026Q1_consolidated_B02_B03_B04_signed_30_exact_checks"
 assert "hợp nhất" in q["report_type"] and q["unit"]=="triệu VND"
 assert q["source_url"]==a["signed_original"]["url"]
 v=q["source_validation"]
 assert v["source_audit_ledger"]==str(AUDIT.relative_to(ROOT))
 assert v["original_pdf_sha256"]==a["signed_original"]["source_pdf_sha256"] and v["original_pdf_hash_verified"] is True
 assert v["manually_visual_reviewed"] is True and v["source_is_consolidated_financial_statements"] is True
 assert v["source_30_accounting_checks_zero_million"] and v["FY2025_comparative_vintage_reviewed_separate_from_original_Q4"] is True
 assert v["FY2025_cross_version_opening_cash_million_difference"]==889334
 fields=set(q["financial_line_items_manually_verified_fields"])
 for k,n in f.items():
  assert k in fields and q.get(k)==n,(k,n,q.get(k))
 for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change"):
  assert q[k]==q[k+"_ytd"],k
 assert q["bank_cash_and_equivalents_cashflow_basis"]==q["cash_ending"]
 assert q["cash_beginning"]==q["cash_beginning_reported_ytd"]
 assert q["cash_ending"]==q["cash_ending_ytd"]
 assert q["bank_cash_on_hand"]!=q["cash_ending"]
 x=next(v for v in queue["items"] if v["id"]=="VCB-2026Q1-FY2025-audited-comparative-vs-first-asfiled-vintage")
 assert x["blocks_sequential_processing"] is False and x["production_eligible"] is True
 assert x["user_visibility"]=="only_if_user_explicitly_asks_for_missing_ticker_or_periods"
 assert all(not r["period"].startswith("2024") for r in d["items"])
 return len(f)
def main():
 a,p,d,q=read(AUDIT),read(Q4),read(FIN),read(QUEUE)
 count=verify(a,p,d,q)
 for scenario in ("wrong_assets","wrong_source_cfo","interest_as_cfo","cash_not_balanced"):
  aa,pp,dd,qq=copy.deepcopy(a),copy.deepcopy(p),copy.deepcopy(d),copy.deepcopy(q)
  row=next(x for x in dd["items"] if x["period"]=="2026-Q1")
  if scenario=="wrong_assets":aa["original_source_million_vnd_fields"]["total_assets"]+=1
  elif scenario=="wrong_source_cfo":aa["original_source_million_vnd_fields"]["operating_cash_flow"]+=1
  elif scenario=="interest_as_cfo":row["operating_cash_flow"]=row["bank_cashflow_interest_received"]
  else:row["cash_ending"]+=1
  try:verify(aa,pp,dd,qq)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError("Tampered financial data undetected: "+scenario)
 print(f"PASS VCB consolidated signed Q1 2026: {count} original million-VND fields, 30 zero checks, 4 corruption controls, separately preserved FY2025 audited comparison vintage.")
 print("Q1 CFO +35,398,194 CFI -294,108 CFF 0 net +35,104,086 ending bank cash 576,792,888 million VND.")
if __name__=="__main__":main()
