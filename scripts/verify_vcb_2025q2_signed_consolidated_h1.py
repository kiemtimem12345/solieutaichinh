#!/usr/bin/env python3
"""VCB 2025Q2 signed consolidated bank B02/B03/B04 exact million-VND checks.

Different bank account 3M Q1 and signed current H1 6M; Q2 standalone corporate
cash = 6M minus 3M; do not mistake B04 interest receipts for bank CFO.
"""
import copy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=R/"reports/source-audits/VCB-2025Q2-original-signed-consolidated-H1-million-vnd.json"
Q1=R/"reports/source-audits/VCB-2025Q1-original-signed-consolidated-million-vnd.json"
D=R/"data/financials-VCB.json"
def read(p):return json.loads(p.read_text("utf-8"))
def sums(N,keys):return sum(N(k) for k in keys)
def audit(s,q1):
 assert s["ticker"]=="VCB" and s["period"]=="2025-Q2"
 z=s["signed_original"]
 assert z["pdf_sha256"]=="789948b37004bdfcb11e56c0efa153bc745e4ec2b79b4336d2a8413ac87f034a"
 assert z["pdf_pages"]==53 and z["pdf_bytes"]==15489752
 assert z["signed_date"]=="2025-07-30"
 assert z["source_workflow_run"]==44970514105 and z["source_artifact_id"]==14733112765
 assert s["original_unit"]=="triệu VND" and "consolidated" in s["source_scope"]
 f=s["source_million_vnd_fields"]
 assert len(f)==136 and all(type(v)==int for v in f.values())
 N=lambda k:f[k]
 p=q1["original_million_vnd_fields"]
 assert q1["period"]=="2025-Q1" and q1["signed_original"]["pdf_sha256"]=="f25bf036ad962541961817d80b49fba2119881d75cbf7abd5c98854a8fad5321"
 P=lambda k:p[k]
 checks={
  "B02_bank_interbank_deposits":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")-N("bank_deposits_and_loans_at_credit_institutions"),
  "B02_trading_net":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
  "B02_loan_net":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
  "B02_securities_net":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
  "B02_long_investment":sums(N,("bank_jv_investments","bank_associates_investments","bank_other_long_term_investments","bank_longterm_investment_impairment"))-N("bank_contributions_and_long_term_investments"),
  "B02_fixed":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
  "B02_other_assets":sums(N,("bank_other_receivables","bank_interest_receivables","bank_deferred_tax_assets","bank_other_assets_misc","bank_other_assets_impairment"))-N("bank_other_assets"),
  "B02_assets":sums(N,("bank_cash_on_hand","bank_deposits_at_state_bank","bank_deposits_and_loans_at_credit_institutions","bank_trading_securities","bank_derivative_assets","bank_customer_loans","bank_investment_securities","bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
  "B02_interbank_funding":N("bank_deposits_from_credit_institutions")+N("bank_borrowings_from_credit_institutions")-N("bank_deposits_and_borrowings_from_credit_institutions"),
  "B02_other_liabilities":N("bank_interest_payable")+N("bank_other_payables")-N("bank_other_liabilities"),
  "B02_liabilities":sums(N,("bank_government_borrowing","bank_deposits_and_borrowings_from_credit_institutions","bank_customer_deposits","bank_derivative_liabilities","bank_funding_and_trust_liabilities","bank_valuable_papers","bank_other_liabilities"))-N("total_liabilities"),
  "B02_capital":N("bank_capital_share")+N("bank_capital_premium")+N("bank_capital_other")-N("bank_capital_and_capital_surplus"),
  "B02_retained_earnings":N("retained_prior_earnings")+N("retained_current_earnings")-N("retained_earnings"),
  "B02_equity":sums(N,("bank_capital_and_capital_surplus","bank_funds","bank_foreign_exchange_equity","retained_earnings","bank_non_controlling_equity"))-N("equity"),
  "B02_total":N("total_liabilities")+N("equity")-N("total_assets"),
  "B03_net_interest":N("bank_interest_income")+N("bank_interest_expense")-N("bank_net_interest_income"),
  "B03_service":N("bank_service_income")+N("bank_service_expense")-N("bank_net_service_income"),
  "B03_other":N("bank_other_operating_income")+N("bank_other_operating_expense")-N("bank_other_operating_net"),
  "B03_revenue":sums(N,("bank_net_interest_income","bank_net_service_income","bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income"))-N("revenue"),
  "B03_operating":N("revenue")+N("bank_operating_expenses")-N("bank_pre_provision_operating_profit"),
  "B03_pretax":N("bank_pre_provision_operating_profit")+N("bank_provision_expense")-N("pretax_profit"),
  "B03_tax":-N("bank_tax_current")-N("bank_tax_deferred")-N("income_tax"),
  "B03_PAT":N("pretax_profit")-N("income_tax")-N("net_profit"),
  "B03_NCI":N("net_profit")+N("bank_non_controlling_profit")-N("net_profit_attributable"),
  "H1_net_interest":N("h1_bank_interest_income")+N("h1_bank_interest_expense")-N("h1_bank_net_interest_income"),
  "H1_net_services":N("h1_bank_service_income")+N("h1_bank_service_expense")-N("h1_bank_net_service_income"),
  "H1_net_other":N("h1_bank_other_operating_income")+N("h1_bank_other_operating_expense")-N("h1_bank_other_operating_net"),
  "H1_revenue":sums(N,("h1_bank_net_interest_income","h1_bank_net_service_income","h1_bank_fx_net_income","h1_bank_trading_securities_net","h1_bank_investment_securities_net","h1_bank_other_operating_net","h1_bank_dividend_and_capital_income"))-N("h1_revenue"),
  "H1_operating":N("h1_revenue")+N("h1_bank_operating_expenses")-N("h1_bank_pre_provision_operating_profit"),
  "H1_pretax":N("h1_bank_pre_provision_operating_profit")+N("h1_bank_provision_expense")-N("h1_pretax_profit"),
  "H1_tax":-N("h1_bank_tax_current")-N("h1_bank_tax_deferred")-N("h1_income_tax"),
  "H1_profit":N("h1_pretax_profit")-N("h1_income_tax")-N("h1_net_profit"),
  "H1_NCI":N("h1_net_profit")+N("h1_bank_non_controlling_profit")-N("h1_net_profit_attributable"),
  "B04_before_wc":sums(N,("bank_cashflow_interest_received_ytd","bank_cashflow_interest_paid_ytd","bank_cashflow_service_net_received_ytd","bank_cashflow_fx_net_ytd","bank_cashflow_other_net_ytd","bank_cashflow_recovered_bad_debt_ytd","bank_cashflow_staff_management_paid_ytd","bank_cashflow_income_tax_paid_ytd"))-N("bank_cfo_before_balance_changes_ytd"),
  "B04_CFO":N("bank_cfo_before_balance_changes_ytd")+sums(N,("bank_wc_deposits_loans_with_banks_ytd","bank_wc_trading_securities_ytd","bank_wc_derivative_assets_ytd","bank_wc_customer_loans_ytd","bank_wc_write_off_ytd","bank_wc_other_assets_ytd","bank_wc_government_funding_ytd","bank_wc_other_bank_funding_ytd","bank_wc_customer_deposits_ytd","bank_wc_debt_securities_ytd","bank_wc_trust_funding_ytd","bank_wc_derivative_liabilities_ytd","bank_wc_other_operating_liabilities_ytd","bank_wc_bank_funds_ytd"))-N("operating_cash_flow_ytd"),
  "B04_CFI":sums(N,("bank_investing_capex_ytd","bank_investing_disposals_received_ytd","bank_investing_disposals_expense_ytd","bank_investing_dividends_received_ytd"))-N("investing_cash_flow_ytd"),
  "B04_sections":N("operating_cash_flow_ytd")+N("investing_cash_flow_ytd")+N("financing_cash_flow_ytd")-N("net_cash_change_ytd"),
  "B04_cashbridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd")
 }
 assert len(checks)==38 and set(checks)==set(s["source_residual_million_vnd"])
 assert all(value==0 for value in checks.values()),checks
 assert all(int(s["source_residual_million_vnd"][key])==checks[key] for key in checks)
 # Preserve issuer B03a signed direct Q2 column and independently recalc 6M-Q1.
 shared=("bank_interest_income","bank_interest_expense","bank_net_interest_income",
         "bank_service_income","bank_service_expense","bank_net_service_income",
         "bank_fx_net_income","bank_trading_securities_net","bank_investment_securities_net",
         "bank_other_operating_income","bank_other_operating_expense","bank_other_operating_net",
         "bank_dividend_and_capital_income","revenue","bank_operating_expenses",
         "bank_pre_provision_operating_profit","bank_provision_expense","pretax_profit",
         "bank_tax_current","bank_tax_deferred","income_tax","net_profit",
         "bank_non_controlling_profit","net_profit_attributable")
 for k in shared:
    assert N("h1_"+k)-P(k)==N(k),k
 assert len(shared)==24
 q={k:N(k+"_ytd")-P(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
 q["cash_beginning"]=P("cash_ending")
 q["cash_ending"]=N("cash_ending_ytd")
 assert q==s["q2_standalone_cashflow_million_vnd"],q
 assert q["operating_cash_flow"]+q["investing_cash_flow"]+q["financing_cash_flow"]==q["net_cash_change"]
 assert q["cash_beginning"]+q["net_cash_change"]==q["cash_ending"]
 assert N("cash_beginning_reported_ytd")==P("cash_beginning")
 assert N("bank_cash_on_hand")!=N("cash_ending_ytd")
 return f,q

def verify(s,q1,d):
    f,quarter=audit(s,q1)
    assert d["symbol"]=="VCB"
    row=next(x for x in d["items"] if x["period"]=="2025-Q2")
    assert row["verification_status"]=="issuer_signed_VCB_2025Q2_consolidated_B02_B03_B04_H1_minus_Q1_exact_million"
    assert "hợp nhất" in row["report_type"].lower()
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
    assert row["source_url"]==s["signed_original"]["url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(S.relative_to(R))
    assert v["source_is_consolidated_financial_statements"] is True
    assert v["original_pdf_sha256"]==s["signed_original"]["pdf_sha256"]
    assert v["quarter_income_H1_minus_Q1_exact_zero_million"] is True
    assert v["quarter_cash_sections_residual_million"]=="0"
    assert v["quarter_cash_openclose_residual_million"]=="0"
    assert v["manually_visual_reviewed"] is True
    approved=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in f.items():
        assert k in approved and row.get(k)==amount,(k,amount,row.get(k))
    for k,amount in quarter.items():
        assert k in approved and row.get(k)==amount,(k,amount,row.get(k))
    assert row["bank_cash_and_equivalents_cashflow_basis"]==row["cash_ending"]
    assert row["bank_cash_on_hand"]!=row["cash_ending"]
    assert row["net_profit_attributable"]!=row["net_profit"]
    assert all(not x["period"].startswith("2024") for x in d["items"])
    return len(f)

def main():
    s,q1,d=read(S),read(Q1),read(D)
    n=verify(s,q1,d)
    for damage in ("bad_assets","bad_h1_cfo","wrong_q2_cash","wrong_interest_as_cfo"):
        a,b,c=copy.deepcopy(s),copy.deepcopy(q1),copy.deepcopy(d)
        row=next(x for x in c["items"] if x["period"]=="2025-Q2")
        if damage=="bad_assets":a["source_million_vnd_fields"]["total_assets"]+=1
        elif damage=="bad_h1_cfo":a["source_million_vnd_fields"]["operating_cash_flow_ytd"]+=1
        elif damage=="wrong_q2_cash":row["cash_ending"]+=1
        else:row["operating_cash_flow"]=row["bank_cashflow_interest_received_ytd"]
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corrupt signed source accepted: "+damage)
    print(f"PASS VCB 2025 Q2: {n} exact source million VND fields, 38 original banking source equations, 24 Q2 earnings identities, 2 quarter cash bridges and 4 negative controls.")
    print("Next VCB Q3/2025, do not reload Q1/Q2 signed PASS.")
if __name__=="__main__":main()
