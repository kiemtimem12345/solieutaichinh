#!/usr/bin/env python3
"""Signed as-filed VCB 2025Q4 bank consolidated FY B02/B03/B04 exact million-VND.

Q4 B04 standalone 12M minus signed original 9M, not audited FY unless audited
version separately validated. Do not equate B04 bank cash equivalent to B02 vault.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCB-2025Q4-original-signed-consolidated-FY-million-vnd.json"
Q3=ROOT/"reports/source-audits/VCB-2025Q3-original-signed-consolidated-9M-million-vnd.json"
DATA=ROOT/"data/financials-VCB.json"
def read(p):return json.loads(p.read_text("utf-8"))
def source(s,p):
 assert s["ticker"]=="VCB" and s["period"]=="2025-Q4"
 assert "consolidated" in s["scope"] and s["source_unit"]=="triệu VND"
 a=s["original_report"]
 assert a["signed_date"]=="2026-01-30"
 assert a["pdf_sha256"]=="1f71919eae463bd24e6978e4ebb89d54c5c53f5b0645adf0fd439e71bdb86aa8"
 assert a["bytes"]==18635021 and a["pages"]==71
 assert a["inspection_workflow"]==44971548969 and a["artifact_id"]==14734205695
 f=s["signed_original_million_vnd_fields"]
 assert len(f)==138 and all(type(v)==int for v in f.values())
 N=lambda k:f[k]
 P=lambda k:p["signed_original_million_vnd_fields"][k]
 S=lambda ks:sum(N(k) for k in ks)
 residuals={
 "B02_balance":N("total_assets")-N("total_liabilities")-N("equity"),
 "B02_assets":S(("bank_cash_on_hand","bank_deposits_at_state_bank","bank_deposits_and_loans_at_credit_institutions","bank_trading_securities","bank_derivative_assets","bank_customer_loans","bank_investment_securities","bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
 "B02_liabs":S(("bank_government_borrowing","bank_deposits_and_borrowings_from_credit_institutions","bank_customer_deposits","bank_derivative_liabilities","bank_funding_and_trust_liabilities","bank_valuable_papers","bank_other_liabilities"))-N("total_liabilities"),
 "B02_equity":S(("bank_capital_and_capital_surplus","bank_funds","bank_foreign_exchange_equity","retained_earnings","bank_non_controlling_equity"))-N("equity"),
 "B02_interbank":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")-N("bank_deposits_and_loans_at_credit_institutions"),
 "B02_trading":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
 "B02_customer_loans":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
 "B02_securities":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
 "B02_long_investment":S(("bank_jv_investments","bank_associates_investments","bank_other_long_term_investments","bank_longterm_investment_impairment"))-N("bank_contributions_and_long_term_investments"),
 "B02_fixed":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
 "B02_other_assets":S(("bank_other_receivables","bank_interest_receivables","bank_deferred_tax_assets","bank_other_assets_misc","bank_other_assets_impairment"))-N("bank_other_assets"),
 "B02_other_liabilities":N("bank_interest_payable")+N("bank_other_payables")-N("bank_other_liabilities"),
 "B02_capital":N("bank_capital_share")+N("bank_capital_premium")+N("bank_capital_other")-N("bank_capital_and_capital_surplus"),
 "B02_earnings":N("retained_prior_earnings")+N("retained_current_earnings")-N("retained_earnings"),
 "B03_q4_revenue":S(("bank_net_interest_income","bank_net_service_income","bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income"))-N("revenue"),
 "B03_q4_op":N("revenue")+N("bank_operating_expenses")-N("bank_pre_provision_operating_profit"),
 "B03_q4_pbt":N("bank_pre_provision_operating_profit")+N("bank_provision_expense")-N("pretax_profit"),
 "B03_q4_tax":-N("bank_tax_current")-N("bank_tax_deferred")-N("income_tax"),
 "B03_q4_net":N("pretax_profit")-N("income_tax")-N("net_profit"),
 "B03_FY_revenue":S(("ytd_bank_net_interest_income","ytd_bank_net_service_income","ytd_bank_fx_net_income","ytd_bank_trading_securities_net","ytd_bank_investment_securities_net","ytd_bank_other_operating_net","ytd_bank_dividend_and_capital_income"))-N("ytd_revenue"),
 "B03_FY_op":N("ytd_revenue")+N("ytd_bank_operating_expenses")-N("ytd_bank_pre_provision_operating_profit"),
 "B03_FY_pbt":N("ytd_bank_pre_provision_operating_profit")+N("ytd_bank_provision_expense")-N("ytd_pretax_profit"),
 "B03_FY_tax":-N("ytd_bank_tax_current")-N("ytd_bank_tax_deferred")-N("ytd_income_tax"),
 "B03_FY_net":N("ytd_pretax_profit")-N("ytd_income_tax")-N("ytd_net_profit"),
 "B04_beforeWC":S(("bank_cashflow_interest_received_ytd","bank_cashflow_interest_paid_ytd","bank_cashflow_service_net_received_ytd","bank_cashflow_fx_net_ytd","bank_cashflow_other_net_ytd","bank_cashflow_recovered_bad_debt_ytd","bank_cashflow_staff_management_paid_ytd","bank_cashflow_income_tax_paid_ytd"))-N("bank_cfo_before_balance_changes_ytd"),
 "B04_CFO":N("bank_cfo_before_balance_changes_ytd")+S(("bank_wc_deposits_loans_with_banks_ytd","bank_wc_trading_securities_ytd","bank_wc_derivative_assets_ytd","bank_wc_customer_loans_ytd","bank_wc_write_off_ytd","bank_wc_other_assets_ytd","bank_wc_government_funding_ytd","bank_wc_other_bank_funding_ytd","bank_wc_customer_deposits_ytd","bank_wc_debt_securities_ytd","bank_wc_trust_funding_ytd","bank_wc_derivative_liabilities_ytd","bank_wc_other_operating_liabilities_ytd","bank_wc_bank_funds_ytd"))-N("operating_cash_flow_ytd"),
 "B04_CFI":S(("bank_investing_capex_ytd","bank_investing_disposals_received_ytd","bank_investing_disposals_expense_ytd","bank_investing_longterm_contributions_ytd","bank_investing_dividends_received_ytd"))-N("investing_cash_flow_ytd"),
 "B04_CFF":N("bank_dividends_paid_ytd")-N("financing_cash_flow_ytd"),
 "B04_cashSections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
 "B04_cashBalance":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd")
 }
 assert len(residuals)==30 and set(residuals)==set(s["source_check_residual_million_vnd"])
 assert all(v==0 for v in residuals.values()),residuals
 assert all(int(s["source_check_residual_million_vnd"][k])==residuals[k] for k in residuals)
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
    assert N("ytd_"+k)-P("ytd_"+k)==N(k),(k,N("ytd_"+k),P("ytd_"+k),N(k))
 assert N("ytd_net_profit_attributable")==N("ytd_net_profit")+N("ytd_bank_non_controlling_profit")
 assert N("net_profit_attributable")==N("net_profit")+N("bank_non_controlling_profit")
 quarter={k:N(k+"_ytd")-P(k+"_ytd") for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
 quarter["cash_beginning"]=P("cash_ending_ytd")
 quarter["cash_ending"]=N("cash_ending_ytd")
 assert quarter==s["q4_standalone_bank_cashflow_million_vnd"]
 assert sum(quarter[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))==quarter["net_cash_change"]
 assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
 assert N("cash_beginning_reported_ytd")==P("cash_beginning_reported_ytd")
 assert N("bank_cash_on_hand")!=N("cash_ending_ytd")
 assert N("financing_cash_flow_ytd")==-3776798
 return f,quarter

def verify(s,p,d):
    f,q=source(s,p)
    assert d["symbol"]=="VCB"
    r=next(x for x in d["items"] if x["period"]=="2025-Q4")
    assert r["verification_status"]=="issuer_signed_VCB_2025Q4_consolidated_B02_B03_B04_FY_minus_9M"
    assert r["unit"]=="triệu VND" and "hợp nhất" in r["report_type"]
    assert r["cashflow_period_basis"]=="year_to_date"
    assert r["source_url"]==s["original_report"]["url"]
    v=r["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["original_pdf_sha256"]==s["original_report"]["pdf_sha256"]
    assert v["original_pdf_hash_verified"] is True
    assert v["source_is_consolidated_financial_statements"] is True
    assert v["year_end_report_asfiled_not_later_audit"] is True
    assert v["Q4_direct_income_FY_minus_9M_all_24_lines_exact_million"] is True
    assert v["quarter_B04_net_cash_residual_million"]=="0"
    assert v["quarter_B04_openclose_residual_million"]=="0"
    allowed=set(r["financial_line_items_manually_verified_fields"])
    for k,a in f.items():
        assert k in allowed and r.get(k)==a,(k,a,r.get(k))
    for k,a in q.items():
        assert k in allowed and r.get(k)==a,(k,a,r.get(k))
    assert r["bank_cash_and_equivalents_cashflow_basis"]==r["cash_ending"]
    assert r["bank_cash_on_hand"]!=r["cash_ending"]
    assert r["net_profit_attributable"]!=r["net_profit"]
    assert all(not x["period"].startswith("2024") for x in d["items"])
    return len(f)

if __name__=="__main__":
    a,b,c=read(SRC),read(Q3),read(DATA)
    n=verify(a,b,c)
    for damaged in ("total_assets_1million","FY_CFO_1million","Q4_CFF_1million","web_cash_1million"):
        s,p,d=copy.deepcopy(a),copy.deepcopy(b),copy.deepcopy(c)
        r=next(x for x in d["items"] if x["period"]=="2025-Q4")
        if damaged=="total_assets_1million":s["signed_original_million_vnd_fields"]["total_assets"]+=1
        elif damaged=="FY_CFO_1million":s["signed_original_million_vnd_fields"]["operating_cash_flow_ytd"]+=1
        elif damaged=="Q4_CFF_1million":r["financing_cash_flow"]+=1
        else:r["cash_ending"]+=1
        try:verify(s,p,d)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Undetected bank source corruption "+damaged)
    print(f"PASS signed VCB FY2025/Q4: {n} original bank million-VND fields, 30 bank accounting equations, 24 FY-minus-Q3 income bridges, exact Q4 B04 cash, 4 corruption tests.")
    print("Q4 CFO +9,057,928; CFI -660,767; CFF -3,776,798; net +4,620,363; end 540,799,468 million VND.")
