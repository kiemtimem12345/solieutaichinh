#!/usr/bin/env python3
"""VCB 2025Q1 original consolidated bank issuer B02 B03 B04 financial pages.

Reported unit is triệu VND; do NOT infer underlying 1VND precision.
Bank B04 operating cashflow is not gross interest cash received; bank
B04 cash equivalents differ from B02 vault cash. Read-only exact controls.
"""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1]
SRC=R/"reports/source-audits/VCB-2025Q1-original-signed-consolidated-million-vnd.json"
FIN=R/"data/financials-VCB.json"
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def source_checks(s):
    assert s["ticker"]=="VCB" and s["period"]=="2025-Q1"
    assert "consolidated" in s["scope"] and "separate parent-only" in s["scope"]
    assert s["reporting_currency"]=="triệu VND"
    z=s["signed_original"]
    assert z["signed_date"]=="2025-04-29"
    assert z["pdf_sha256"]=="f25bf036ad962541961817d80b49fba2119881d75cbf7abd5c98854a8fad5321"
    assert z["pdf_pages"]==53 and z["pdf_bytes"]==14951723
    assert z["source_workflow_run"]==44969925241 and z["source_visual_artifact_id"]==14733132694
    assert len(s["original_million_vnd_fields"])==110
    f=s["original_million_vnd_fields"]
    assert all(type(v)==int for v in f.values())
    N=lambda k:f[k]
    checks={
       "B01_bank_deposits_credit_inst":N("bank_deposits_at_credit_institutions")+N("bank_loans_to_credit_institutions")-N("bank_deposits_and_loans_at_credit_institutions"),
       "B01_trading":N("bank_trading_securities_gross")+N("bank_trading_securities_impairment")-N("bank_trading_securities"),
       "B01_customer_loans":N("bank_customer_loans_gross")+N("bank_customer_loans_impairment")-N("bank_customer_loans"),
       "B01_investment_sec":N("bank_investment_available_for_sale")+N("bank_investment_held_to_maturity")+N("bank_investment_securities_impairment")-N("bank_investment_securities"),
       "B01_long_investment":N("bank_jv_investments")+N("bank_associates_investments")+N("bank_other_long_term_investments")+N("bank_longterm_investment_impairment")-N("bank_contributions_and_long_term_investments"),
       "B01_fixed_assets":N("bank_fixed_assets_tangible")+N("bank_fixed_assets_intangible")-N("fixed_assets"),
       "B01_other_assets":N("bank_other_receivables")+N("bank_interest_receivables")+N("bank_deferred_tax_assets")+N("bank_other_assets_misc")+N("bank_other_assets_impairment")-N("bank_other_assets"),
       "B01_assets_sum":sum(N(k) for k in ("bank_cash_on_hand","bank_deposits_at_state_bank",
           "bank_deposits_and_loans_at_credit_institutions","bank_trading_securities",
           "bank_derivative_assets","bank_customer_loans","bank_investment_securities",
           "bank_contributions_and_long_term_investments","fixed_assets","bank_other_assets"))-N("total_assets"),
       "B01_bank_funding":N("bank_deposits_from_credit_institutions")+N("bank_borrowings_from_credit_institutions")-N("bank_deposits_and_borrowings_from_credit_institutions"),
       "B01_liabilities_sum":sum(N(k) for k in ("bank_government_borrowing",
           "bank_deposits_and_borrowings_from_credit_institutions","bank_customer_deposits",
           "bank_derivative_liabilities","bank_funding_and_trust_liabilities",
           "bank_valuable_papers","bank_other_liabilities"))-N("total_liabilities"),
       "B01_equity_capital":N("bank_capital_share")+N("bank_capital_premium")+N("bank_capital_other")-N("bank_capital_and_capital_surplus"),
       "B01_equity_sum":sum(N(k) for k in ("bank_capital_and_capital_surplus","bank_funds",
           "bank_foreign_exchange_equity","retained_earnings","bank_non_controlling_equity"))-N("equity"),
       "B01_total_balance":N("total_liabilities")+N("equity")-N("total_assets"),
       "B02_net_interest":N("bank_interest_income")+N("bank_interest_expense")-N("bank_net_interest_income"),
       "B02_net_services":N("bank_service_income")+N("bank_service_expense")-N("bank_net_service_income"),
       "B02_net_other":N("bank_other_operating_income")+N("bank_other_operating_expense")-N("bank_other_operating_net"),
       "B02_total_operating_income":sum(N(k) for k in ("bank_net_interest_income",
           "bank_net_service_income","bank_fx_net_income","bank_trading_securities_net",
           "bank_investment_securities_net","bank_other_operating_net","bank_dividend_and_capital_income"))-N("revenue"),
       "B02_before_provision":N("revenue")+N("bank_operating_expenses")-N("bank_pre_provision_operating_profit"),
       "B02_after_provision":N("bank_pre_provision_operating_profit")+N("bank_provision_expense")-N("pretax_profit"),
       "B02_income_tax":N("bank_tax_current")+N("bank_tax_deferred")+N("income_tax"),
       "B02_PAT":N("pretax_profit")-N("income_tax")-N("net_profit"),
       "B02_noncontrolling":N("net_profit")+N("bank_non_controlling_profit")-N("net_profit_attributable"),
       "B03_cash_before_wc":sum(N(k) for k in ("bank_cashflow_interest_received",
           "bank_cashflow_interest_paid","bank_cashflow_service_net_received","bank_cashflow_fx_net",
           "bank_cashflow_other_net","bank_cashflow_recovered_bad_debt",
           "bank_cashflow_staff_management_paid","bank_cashflow_income_tax_paid"))-N("bank_cfo_before_balance_changes"),
       "B03_CFO_components":N("bank_cfo_before_balance_changes")+
          sum(N(k) for k in ("bank_wc_deposits_loans_with_banks","bank_wc_trading_securities",
           "bank_wc_derivative_assets","bank_wc_customer_loans","bank_wc_write_off",
           "bank_wc_other_assets","bank_wc_government_funding","bank_wc_other_bank_funding",
           "bank_wc_customer_deposits","bank_wc_debt_securities","bank_wc_trust_funding",
           "bank_wc_derivative_liabilities","bank_wc_other_operating_liabilities",
           "bank_wc_bank_funds"))-N("operating_cash_flow"),
       "B03_CFI":N("bank_investing_capex")+N("bank_investing_disposals_received")+
          N("bank_investing_disposals_expense")+N("bank_investing_dividends_received")-N("investing_cash_flow"),
       "B03_sections":N("operating_cash_flow")+N("investing_cash_flow")+
          N("financing_cash_flow")-N("net_cash_change"),
       "B03_open_close":N("cash_beginning")+N("net_cash_change")-N("cash_ending"),
       "B03_not_B01_cash":int(N("bank_cash_on_hand")==N("cash_ending"))
    }
    assert len(checks)==28 and set(checks)==set(s["source_check_residual_million_vnd"])
    assert all(v==0 for v in checks.values()),checks
    assert all(int(s["source_check_residual_million_vnd"][k])==checks[k] for k in checks)
    assert N("operating_cash_flow")==-13180595 and N("bank_cashflow_interest_received")==23692971
    assert N("investing_cash_flow")==-174898 and N("financing_cash_flow")==0
    assert N("cash_beginning")==430614185 and N("cash_ending")==417258692
    return f

def verify(s,d):
    f=source_checks(s)
    assert d["symbol"]=="VCB"
    row=next(x for x in d["items"] if x["period"]=="2025-Q1")
    assert row["verification_status"]=="issuer_signed_VCB_2025Q1_consolidated_B01_B02_B04_exact_million_VND"
    assert row["unit"]=="triệu VND"
    assert "hợp nhất" in row["report_type"]
    assert row["source_url"]==s["signed_original"]["url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(R))
    assert v["manually_visual_reviewed"] is True
    assert v["source_is_consolidated_financial_statements"] is True
    assert v["source_accounting_unit"]=="triệu VND"
    assert v["original_pdf_sha256"]==s["signed_original"]["pdf_sha256"]
    assert v["original_pdf_hash_verified"] is True
    assert v["source_28_identities_all_zero_million"] is True
    allowed=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in f.items():
        assert k in allowed and row.get(k)==amount,(k,amount,row.get(k))
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change"):
        assert row[k]==row[k+"_ytd"],(k,row[k],row[k+"_ytd"])
    assert row["cash_beginning"]==row["cash_beginning_reported_ytd"]
    assert row["cash_ending"]==row["cash_ending_ytd"]
    assert row["bank_cash_and_equivalents_cashflow_basis"]==row["cash_ending"]
    assert row["net_profit_attributable"]!=row["net_profit"]
    assert row["operating_cash_flow"]!=row["bank_cashflow_interest_received"]
    assert len(d["items"])>=6 and all(not x["period"].startswith("2024") for x in d["items"])
    for other in d["items"]:
        if other["period"]!="2025-Q1": assert other["verification_status"]!="issuer_signed_VCB_2025Q1_consolidated_B01_B02_B04_exact_million_VND"
    return len(f)
if __name__=="__main__":
    s,d=read(SRC),read(FIN)
    count=verify(s,d)
    for damaged in ("source_asset_1million","source_cfo_1million","web_cash_1million","misclassified_interest_receipts"):
        a,b=copy.deepcopy(s),copy.deepcopy(d)
        r=next(x for x in b["items"] if x["period"]=="2025-Q1")
        if damaged=="source_asset_1million":a["original_million_vnd_fields"]["total_assets"]+=1
        elif damaged=="source_cfo_1million":a["original_million_vnd_fields"]["operating_cash_flow"]+=1
        elif damaged=="web_cash_1million":r["cash_ending"]+=1
        else:r["operating_cash_flow"]=r["bank_cashflow_interest_received"]
        try:verify(a,b)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corruption not caught: "+damaged)
    print(f"PASS VCB 2025Q1 signed consolidated banking: {count} source million-VND fields, 28 zero-residual equations, 4 corruption controls.")
    print("Actual B04 CFO -13,180,595, CFI -174,898, CFF zero; cash 430,614,185 -> 417,258,692 million VND.")
