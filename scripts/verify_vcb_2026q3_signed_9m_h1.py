#!/usr/bin/env python3
"""VCB 2026Q3 consolidated issuer signed bank financial B02a/B03a/B04a.

Original source units = million VND. Validate 43 independently recomputed
source equations, 24 exact direct-Q3 vs 9M-minus-signed-H1 earnings lines, and
zero company B04 cash residuals; do not substitute interest receipts for CFO.
"""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCB-2026Q3-original-signed-consolidated-9M-million-vnd.json"
H1=ROOT/"reports/source-audits/VCB-2026Q2-issuer-signed-H1-sixmonth-million-vnd.json"
DATA=ROOT/"data/financials-VCB.json"
QUEUE=ROOT/"reports/financial-exception-queue.json"
def load(p):return json.loads(p.read_text(encoding="utf8"))
def source_verify(src,h1):
 assert src["ticker"]=="VCB" and src["period"]=="2026-Q3" and src["unit"]=="triệu VND"
 assert "consolidated" in src["scope"]
 z=src["original_signed_source"]
 assert z["signed_date"]=="2026-10-30" and z["pdf_sha256"]=="9c69b62c629e7c4d586535c99277bbc6c4ba785d04ff765371fea07ece5daa08"
 assert z["pages"]==66 and z["bytes"]==9988936
 assert z["source_workflow_run"]==45012503358 and z["source_artifact_id"]==14749929820
 assert z["url"].endswith("VCB_Baocaotaichinh_Q3_2026_Hopnhat.pdf")
 assert "2510515" in z["official_HOSE_reference_url"]
 f=src["source_million_vnd_fields"]
 assert len(f)==148 and all(type(v)==int for v in f.values())
 N=lambda k:f[k]
 S=lambda keys:sum(N(k) for k in keys)
 eq={
 "balance":N("total_assets")-N("total_liabilities")-N("equity"),
 "interbank":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")+N("bank_interbank_impairment")-N("bank_deposits_and_loans_at_credit_institutions"),
 "trading":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
 "customer_loans":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
 "investment_sec":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
 "long_invest":S(("bank_jv_investments","bank_associates_investments","bank_other_long_term_investments","bank_longterm_investment_impairment"))-N("bank_contributions_and_long_term_investments"),
 "fixed":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
 "tangible":N("bank_fixed_tangible_gross")+N("bank_fixed_tangible_depreciation")-N("bank_fixed_assets_tangible"),
 "intangible":N("bank_fixed_intangible_gross")+N("bank_fixed_intangible_depreciation")-N("bank_fixed_assets_intangible"),
 "other_assets":S(("bank_other_receivables","bank_interest_receivables","bank_deferred_tax_assets","bank_other_assets_misc","bank_other_assets_impairment"))-N("bank_other_assets"),
 "assets":S(("bank_cash_on_hand","bank_deposits_at_state_bank","bank_deposits_and_loans_at_credit_institutions","bank_trading_securities","bank_derivative_assets","bank_customer_loans","bank_investment_securities","bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
 "government":N("bank_government_deposits_and_borrowings")+N("bank_government_repo_agreements")-N("bank_government_borrowing"),
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
 "ytd_net_interest":N("ytd_bank_interest_income")+N("ytd_bank_interest_expense")-N("ytd_bank_net_interest_income"),
 "ytd_net_service":N("ytd_bank_service_income")+N("ytd_bank_service_expense")-N("ytd_bank_net_service_income"),
 "ytd_net_other":N("ytd_bank_other_operating_income")+N("ytd_bank_other_operating_expense")-N("ytd_bank_other_operating_net"),
 "ytd_revenue":S(("ytd_bank_net_interest_income","ytd_bank_net_service_income","ytd_bank_fx_net_income","ytd_bank_trading_securities_net","ytd_bank_investment_securities_net","ytd_bank_other_operating_net","ytd_bank_dividend_and_capital_income"))-N("ytd_revenue"),
 "ytd_operating_profit":N("ytd_revenue")+N("ytd_bank_operating_expenses")-N("ytd_bank_pre_provision_operating_profit"),
 "ytd_pretax":N("ytd_bank_pre_provision_operating_profit")+N("ytd_bank_provision_expense")-N("ytd_pretax_profit"),
 "ytd_income_tax":-N("ytd_bank_tax_current")-N("ytd_bank_tax_deferred")-N("ytd_income_tax"),
 "ytd_net_profit":N("ytd_pretax_profit")-N("ytd_income_tax")-N("ytd_net_profit"),
 "ytd_NCI":N("ytd_net_profit")+N("ytd_bank_non_controlling_profit")-N("ytd_net_profit_attributable"),
 "before_wc":S(("bank_cashflow_interest_received_ytd","bank_cashflow_interest_paid_ytd","bank_cashflow_service_net_received_ytd","bank_cashflow_fx_net_ytd","bank_cashflow_other_net_ytd","bank_cashflow_recovered_bad_debt_ytd","bank_cashflow_staff_management_paid_ytd","bank_cashflow_income_tax_paid_ytd"))-N("bank_cfo_before_balance_changes_ytd"),
 "CFO":N("bank_cfo_before_balance_changes_ytd")+S(("bank_wc_deposits_loans_with_banks_ytd","bank_wc_trading_securities_ytd","bank_wc_derivative_assets_ytd","bank_wc_customer_loans_ytd","bank_wc_write_off_ytd","bank_wc_other_assets_ytd","bank_wc_government_funding_ytd","bank_wc_other_bank_funding_ytd","bank_wc_customer_deposits_ytd","bank_wc_debt_securities_ytd","bank_wc_trust_funding_ytd","bank_wc_derivative_liabilities_ytd","bank_wc_other_operating_liabilities_ytd","bank_wc_bank_funds_ytd"))-N("operating_cash_flow_ytd"),
 "CFI":S(("bank_investing_capex_ytd","bank_investing_disposals_received_ytd","bank_investing_disposals_expense_ytd","bank_investing_longterm_contributions_ytd","bank_investing_dividends_received_ytd"))-N("investing_cash_flow_ytd"),
 "CFF":N("bank_dividends_paid_ytd")-N("financing_cash_flow_ytd"),
 "sections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
 "cashbridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd"),
 "FY_comparative_balance":N("revised_FY2025_comparison_assets")-N("revised_FY2025_comparison_liabilities")-N("revised_FY2025_comparison_equity")
 }
 assert len(eq)==43 and set(eq)==set(src["source_check_residual_million_vnd"])
 assert all(x==0 for x in eq.values()),eq
 assert all(int(src["source_check_residual_million_vnd"][k])==v for k,v in eq.items())
 assert h1["ticker"]=="VCB" and h1["period"]=="2026-Q2"
 assert h1["issuer_source_original"]["pdf_sha256"]=="fb0bc8ebbad76c175e61f7c2a7b78ae67608623a8d715d5470a08dbac00ff223"
 prior=h1["original_source_million_vnd_fields"]
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
  assert N("ytd_"+k)-prior["h1_"+k]==N(k),(k,N("ytd_"+k),prior["h1_"+k],N(k))
 quarter={k:N(k+"_ytd")-prior[k+"_ytd"] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
 quarter["cash_beginning"]=prior["cash_ending_ytd"]
 quarter["cash_ending"]=N("cash_ending_ytd")
 assert quarter==src["q3_company_B04_quarter_cashflow_million_vnd"]
 assert sum(quarter[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))==quarter["net_cash_change"]
 assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
 assert N("cash_beginning_reported_ytd")==prior["cash_beginning_reported_ytd"]==541688802
 assert N("bank_cash_on_hand")!=N("cash_ending_ytd")
 assert N("operating_cash_flow_ytd")==81448510 and N("bank_cashflow_interest_received_ytd")==106822239
 assert N("investing_cash_flow_ytd")==-1374720 and N("financing_cash_flow_ytd")==-3760054
 return f,quarter
def verify(src,h1,data,queue):
 f,q=source_verify(src,h1)
 assert data["symbol"]=="VCB" and len(data["items"])==7
 assert [x["period"] for x in data["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
 r=data["items"][-1]
 assert r["verification_status"]=="issuer_signed_VCB_2026Q3_consolidated_B02a_B03a_B04a_9M_minus_H1"
 assert r["unit"]=="triệu VND" and "hợp nhất" in r["report_type"]
 assert r["source_url"]==src["original_signed_source"]["url"] and r["cashflow_period_basis"]=="year_to_date"
 v=r["source_validation"]
 assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
 assert v["original_pdf_sha256"]==src["original_signed_source"]["pdf_sha256"] and v["original_pdf_hash_verified"] is True
 assert v["manually_visual_reviewed"] and v["source_is_consolidated_financial_statements"]
 assert v["source_43_accounting_checks_exact_zero_million"] and v["Q3_B03_direct_equals_9M_minus_H1_24_source_lines"]
 assert v["B04_Q3_sections_residual_million"]=="0" and v["B04_Q3_begin_end_residual_million"]=="0"
 approved=set(r["financial_line_items_manually_verified_fields"])
 for k,num in f.items():
  assert k in approved and r.get(k)==num,(k,num,r.get(k))
 for k,num in q.items():
  assert k in approved and r.get(k)==num,(k,num,r.get(k))
 assert r["bank_cash_and_equivalents_cashflow_basis"]==r["cash_ending"]
 assert r["bank_cash_on_hand"]!=r["cash_ending"]
 assert r["net_profit_attributable"]!=r["net_profit"]
 e=next(x for x in queue["items"] if x["id"]=="VCB-2026Q3-2025FY-comparative-trinh-bay-lai-vs-2026H1")
 assert e["production_eligible"] and not e["blocks_sequential_processing"]
 assert e["user_visibility"]=="only_if_user_explicitly_asks_for_missing_ticker_or_period_list"
 assert all(not x["period"].startswith("2024") for x in data["items"])
 return len(f)
def main():
 src,h1,data,queue=load(SRC),load(H1),load(DATA),load(QUEUE)
 n=verify(src,h1,data,queue)
 for damage in ("assets_1million","B04_9M_CFO_1million","direct_q3_profit_1million","client_cash_confusion"):
  a,b,c,e=copy.deepcopy(src),copy.deepcopy(h1),copy.deepcopy(data),copy.deepcopy(queue)
  row=c["items"][-1]
  if damage=="assets_1million":a["source_million_vnd_fields"]["total_assets"]+=1
  elif damage=="B04_9M_CFO_1million":a["source_million_vnd_fields"]["operating_cash_flow_ytd"]+=1
  elif damage=="direct_q3_profit_1million":row["net_profit"]+=1
  else:row["cash_ending"]=row["bank_cash_on_hand"]
  try:verify(a,b,c,e)
  except (AssertionError,ValueError,TypeError):pass
  else:raise AssertionError("Corrupt financial content not detected: "+damage)
 print(f"PASS VCB 2026Q3 consolidated: {n} issuer signed source million-VND fields, 43 zero accounting equations, 24 signed Q3=9M-H1 profit bridges, cash section/balance zero and 4 mutation tests.")
 print("Q3 corporate bank cash CFO -49,547,933 CFI -729,139 CFF -3,760,054 net -54,037,126 cash end 618,002,538 million VND.")
if __name__=="__main__":main()
