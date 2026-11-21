#!/usr/bin/env python3
"""VCK/VPSS Q1/2025: issuer-signed VPS securities B01/B02/B03 exact VND.

Explicitly NOT a consolidated filing; issuer prospectus says after disposal of
its only subsidiary in Q1/2025, consolidated filings were not required.
Customer brokerage cash is excluded. No 2024 records are retained.
"""
import copy
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2025Q1-VPSS-issuer-signed-standalone-vnd.json"
DATA=ROOT/"data/financials-VCK.json"
M=Decimal("1000000")
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def exact(row,k):
    value=row.get(k)
    assert type(value) in (float,int),(k,value)
    v=Decimal(str(value))*M
    assert v==v.to_integral_value(),(k,value,v)
    return int(v)
def verified_source(source):
    assert source["ticker"]=="VCK" and source["prior_filing_symbol"]=="VPSS"
    assert source["company"]=="Công ty Cổ phần Chứng khoán VPS"
    assert source["period"]=="2025-Q1" and source["report_signed"]=="2025-04-17"
    assert source["signed_report_url"].endswith("VPSS_Baocaotaichinh_Q1_2025.pdf")
    assert "standalone" in source["source_scope"] and "consolidated" not in source["source_document_title"].lower()
    assert source["currency"]=="VND"
    f=source["exact_vnd_fields"]
    assert len(f)==65
    N=lambda k:int(f[k])
    identities={
        "balance_assets":N("current_assets")+N("non_current_assets")-N("total_assets"),
        "balance_equity":N("total_liabilities")+N("equity")-N("total_assets"),
        "current_assets":N("financial_assets_current")+N("other_current_assets")-N("current_assets"),
        "noncurrent_assets":sum(N(k) for k in ("financial_assets_noncurrent","fixed_assets",
          "long_term_construction_in_progress","other_non_current_assets"))-N("non_current_assets"),
        "noncurrent_fixed":N("securities_fixed_tangible")+N("securities_fixed_intangible")-N("fixed_assets"),
        "liability_balance":N("current_liabilities")+N("long_term_liabilities")-N("total_liabilities"),
        "operating_revenue":sum(N(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
          "securities_loan_interest_income","securities_brokerage_revenue","securities_depository_revenue",
          "securities_financial_advice_revenue","securities_other_revenue"))-N("revenue"),
        "operating_expenses":sum(N(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense",
          "securities_brokerage_expense","securities_depository_expense",
          "securities_financial_advice_expense"))-N("securities_operating_expense"),
        "operating_profit":N("revenue")-N("securities_operating_expense")+N("financial_income")
          -N("financial_expense")-N("admin_expense")-N("operating_profit"),
        "profit_before_tax":N("operating_profit")+N("other_profit")-N("pretax_profit"),
        "profit_after_tax":N("pretax_profit")-N("income_tax")-N("net_profit"),
        "company_cash_balance":N("cash_and_equivalents")-N("cash_ending"),
        "investing_items":N("capital_expenditure")+N("capital_investments")+N("investment_recovery")-N("investing_cash_flow"),
        "financing_items":N("financing_borrowing_receipts")+N("financing_loan_repayments")-N("financing_cash_flow"),
        "cash_sections":N("operating_cash_flow")+N("investing_cash_flow")+N("financing_cash_flow")-N("net_cash_change"),
        "cash_beginning_ending":N("cash_beginning")+N("net_cash_change")-N("cash_ending"),
        "financial_income_components":N("financial_income_deposit_interest")+N("financial_income_other_investments")-N("financial_income"),
        "financial_expense_components":N("interest_expense")+N("financial_other_expense")-N("financial_expense"),
        "fvtpl_profit_components":N("securities_fvtpl_disposal_gain")+N("securities_fvtpl_revaluation_gain")+
            N("securities_fvtpl_dividend_interest")-N("securities_fvtpl_gain"),
    }
    assert len(identities)==19 and all(v==0 for v in identities.values()),identities
    assert set(identities)==set(source["exact_vnd_residuals"])
    assert all(source["exact_vnd_residuals"][k]=="0" for k in identities)
    assert source["acquisition_disposal_note"].startswith("Per issuer listing prospectus")
    return f
def verify(source,data):
    fields=verified_source(source)
    assert data["symbol"]=="VCK"
    periods=[r["period"] for r in data["items"]]
    assert periods==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
    assert not data.get("pre_listing_legacy_reports")
    assert data.get("legacy_2024_excluded_from_window") is True
    r=data["items"][0]
    assert r["verification_status"]=="issuer_signed_Q1_2025_B01_B02_B03_original_standalone_no_subs"
    assert r["unit"]=="triệu VND" and r["cashflow_period_basis"]=="quarter"
    assert r["source_url"]==source["signed_report_url"]
    assert "không bắt buộc lập hợp nhất" in r["report_type"]
    sv=r["source_validation"]
    assert sv["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert sv["scope_status"]=="issuer_signed_standalone_no_consolidation_required_since_Q1_2025"
    assert sv["signed_original_report_scope_verified"] is True
    assert sv["client_cash_outside_issuer_balance_sheet"] is True
    assert sv["original_pdf_hash_verified"] is False
    assert sv["manual_review_blocking_automatic_extraction"] is False
    assert sv["accounting_identities_exact_vnd"]==19
    assert "scope_unverified_financial_values" not in r
    allowed=set(r["financial_line_items_manually_verified_fields"])
    for k,amount in fields.items():
        assert k in allowed and exact(r,k)==int(amount),(k,r.get(k),amount)
    aliases={
       "broker_fvtpl_assets":"securities_fvtpl_assets",
       "broker_held_to_maturity_assets":"securities_htm_short",
       "broker_lending_assets":"securities_margin_loans",
       "broker_receivables":"securities_receivables",
       "broker_long_term_bonds":"securities_long_term_bonds",
       "broker_operating_expenses":"securities_operating_expense",
       "broker_total_operating_revenue":"revenue",
       "broker_total_operating_expenses":"securities_operating_expense",
       "broker_brokerage_revenue":"securities_brokerage_revenue",
       "broker_custody_revenue":"securities_depository_revenue",
       "broker_brokerage_expense":"securities_brokerage_expense",
       "broker_custody_expense":"securities_depository_expense",
       "broker_trading_expense":"securities_self_trading_expense",
       "broker_short_term_borrowings":"short_term_borrowings",
       "broker_financial_income":"financial_income",
       "broker_financial_expense":"financial_expense",
       "income_tax_current":"income_tax",
    }
    for k,v in aliases.items():
        assert exact(r,k)==int(fields[v]),(k,exact(r,k),v)
    assert exact(r,"net_profit_attributable")==exact(r,"net_profit")
    assert exact(r,"interest_expense")!=exact(r,"financial_expense"),"Interest and total finance expense must not be conflated"
    assert set(r["cashflow_quarter_manually_verified_fields"])=={"operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","cash_ending"}
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_ending"):
        assert exact(r,k)==exact(r,k+"_ytd")
    assert exact(r,"cash_beginning")==exact(r,"cash_beginning_reported_ytd")
    for other in data["items"][1:]:
        assert other["total_assets"] is None and other["net_profit"] is None
    return len(fields)
def main():
    source,data=read(SRC),read(DATA)
    fields=verify(source,data)
    for corrupted in ("source_asset_1VND","source_CFO_1VND","website_cash_1VND","wrong_finance_expense"):
        a,b=copy.deepcopy(source),copy.deepcopy(data)
        row=b["items"][0]
        if corrupted=="source_asset_1VND":
            a["exact_vnd_fields"]["total_assets"]=str(int(a["exact_vnd_fields"]["total_assets"])+1)
        elif corrupted=="source_CFO_1VND":
            a["exact_vnd_fields"]["operating_cash_flow"]=str(int(a["exact_vnd_fields"]["operating_cash_flow"])+1)
        elif corrupted=="website_cash_1VND":
            row["cash_ending"]+=0.000001
        else:
            row["interest_expense"]=row["financial_expense"]
        try: verify(a,b)
        except (AssertionError,TypeError,ValueError): pass
        else: raise AssertionError("Corruption not rejected: "+corrupted)
    print(f"PASS VPS/VCK Q1/2025: {fields} issuer-signed exact-VND fields, 19 independent accounting identities, 4 corruption controls.")
    print("Signed 2025-Q1 report scope verified, no consolidation requirement; client custody isolated, 2024 records omitted.")
    print("NEXT sequential checkpoint: VCK Q2/2025.")
if __name__=="__main__":
    main()
