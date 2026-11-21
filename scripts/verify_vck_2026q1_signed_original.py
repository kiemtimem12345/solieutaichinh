#!/usr/bin/env python3
"""VCK 2026Q1 issuer-signed securities firm B01/B02/B03 exact VND.

PDF 61 pages from original HOSE ZIP, Vietnamese signed company report;
no client custody cash in issuer B01/B03 and no 2024 data.
"""
import copy,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2026Q1-issuer-signed-original-vnd.json"
FY=ROOT/"reports/source-audits/VCK-2025Q4-original-EY-FY2025-exact-vnd.json"
DATA=ROOT/"data/financials-VCK.json"
M=Decimal("1000000")
def read(x):return json.loads(x.read_text("utf-8"))
def scaled(row,key):
    v=row.get(key)
    assert type(v) in (float,int),(key,v)
    x=Decimal(str(v))*M
    assert x==x.to_integral_value(),(key,x)
    return int(x)
def verify_source(s,fy):
    assert s["ticker"]=="VCK" and s["period"]=="2026-Q1"
    x=s["source_signed"]
    assert x["archive_sha256"]=="4529f9f8c8bec23ebc49cf1ba7f66f3e8b9dcb9923f67f46a5989fb2063ef829"
    assert x["original_pdf_sha256"]=="0710073b8f6ef2d6ba1268d5831a6627b380b1a5359ff78c72d77fd3753a51d9"
    assert x["original_pdf_pages"]==61 and x["original_pdf_bytes"]==3481834
    assert x["source_workflow_run"]==44934211169
    assert x["source_artifact_id"]==14718867573
    assert "vi_baocaotaichinh_q1_2026" in x["original_member"]
    assert s["unit"]=="VND" and "standalone" in s["scope"]
    f=s["source_current_vnd_fields"];assert len(f)==73
    F=lambda k:int(f[k])
    old=fy["original_Q4_exact_vnd_fields"]
    assert F("cash_beginning")==int(old["cash_ending_ytd"])
    checks={
       "assets":F("current_assets")+F("non_current_assets")-F("total_assets"),
       "balance":F("total_assets")-F("total_liabilities")-F("equity"),
       "liabs":F("current_liabilities")+F("long_term_liabilities")-F("total_liabilities"),
       "financial_current_plus_other":F("financial_assets_current")+F("other_current_assets")-F("current_assets"),
       "noncurrent_components":sum(F(k) for k in ("financial_assets_noncurrent","fixed_assets","long_term_construction_in_progress","other_non_current_assets"))-F("non_current_assets"),
       "fixed":F("securities_fixed_tangible")+F("securities_fixed_intangible")-F("fixed_assets"),
       "cash":F("cash_only")+F("cash_equivalents_only")-F("cash_and_equivalents"),
       "equity_components":sum(F(k) for k in ("capital_share","capital_premium","afs_fair_value_equity","retained_earnings"))-F("equity"),
       "revenue_breakdown":sum(F(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
           "securities_loan_interest_income","securities_afs_interest_income","securities_brokerage_revenue",
           "securities_depository_revenue","securities_financial_advice_revenue","securities_other_revenue"))-F("revenue"),
       "expense_breakdown":sum(F(k) for k in ("securities_fvtpl_loss","securities_htm_loss",
           "securities_afs_reclass_loss","securities_self_trading_expense","securities_brokerage_expense",
           "securities_depository_expense","securities_financial_advice_expense"))-F("securities_operating_expense"),
       "financial_income_components":F("financial_income_deposit_interest")+F("financial_income_other_investments")-F("financial_income"),
       "financial_expense_components":sum(F(k) for k in ("financial_expense_fx_loss","interest_expense",
           "securities_financial_investment_impairment","financial_other_expense"))-F("financial_expense"),
       "operating_profit":F("revenue")-F("securities_operating_expense")+F("financial_income")-F("financial_expense")-F("admin_expense")-F("operating_profit"),
       "other_profit":F("other_income")-F("other_expense")-F("other_profit"),
       "pretax":F("operating_profit")+F("other_profit")-F("pretax_profit"),
       "aftertax":F("pretax_profit")-F("income_tax")-F("net_profit"),
       "cash_sections":F("operating_cash_flow")+F("investing_cash_flow")+F("financing_cash_flow")-F("net_cash_change"),
       "cash_openend":F("cash_beginning")+F("net_cash_change")-F("cash_ending"),
       "company_cash_B01_B03":F("cash_and_equivalents")-F("cash_ending"),
       "opening_FY2025":F("cash_beginning")-int(old["cash_ending_ytd"]),
       "investing_items":F("capital_expenditure")-F("investing_cash_flow"),
       "financing_items":F("borrowing_receipts")+F("loan_repayments")-F("financing_cash_flow"),
       "client_cash_not_company":int(F("client_brokerage_cash_ending")==F("cash_ending")),
    }
    assert len(checks)==23 and set(checks)==set(s["source_exact_vnd_checks"])
    assert all(v==0 for v in checks.values()),checks
    assert all(s["source_exact_vnd_checks"][k]=="0" for k in checks)
    return f
def verify(s,fy,data):
    f=verify_source(s,fy)
    assert data["symbol"]=="VCK" and len(data["items"])==7
    row=next(z for z in data["items"] if z["period"]=="2026-Q1")
    assert row["verification_status"]=="issuer_signed_VCK_Q1_2026_original_B01_B02_B03_no_subs"
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="quarter"
    assert "không phải hợp nhất" in row["report_type"]
    assert row["source_url"]==s["source_signed"]["url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["original_pdf_sha256"]==s["source_signed"]["original_pdf_sha256"]
    assert v["original_pdf_hash_verified"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["cashflow_residual_exact_vnd"]=="0"
    approved=set(row["financial_line_items_manually_verified_fields"])
    for k,raw in f.items():
        assert k in approved and scaled(row,k)==int(raw),(k,row.get(k),raw)
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_ending"):
        assert scaled(row,k)==scaled(row,k+"_ytd")
    assert scaled(row,"cash_beginning")==scaled(row,"cash_beginning_reported_ytd")
    assert scaled(row,"net_profit_attributable")==scaled(row,"net_profit")
    assert scaled(row,"broker_customer_deposits")==scaled(row,"client_brokerage_cash_ending")
    assert scaled(row,"broker_customer_deposits")!=scaled(row,"cash_ending")
    assert not data.get("pre_listing_legacy_reports")
    assert next(z for z in data["items"] if z["period"]=="2025-Q2")["net_profit"] is None
    return len(f)
if __name__=="__main__":
    src,fy,data=map(read,(SRC,FY,DATA))
    n=verify(src,fy,data)
    for mutation in ("asset_1VND","cash_1VND","website_PAT_1VND","client_deposit_as_cash"):
        a,b,c=copy.deepcopy(src),copy.deepcopy(fy),copy.deepcopy(data)
        r=next(z for z in c["items"] if z["period"]=="2026-Q1")
        if mutation=="asset_1VND":a["source_current_vnd_fields"]["total_assets"]=str(int(a["source_current_vnd_fields"]["total_assets"])+1)
        elif mutation=="cash_1VND":a["source_current_vnd_fields"]["cash_ending"]=str(int(a["source_current_vnd_fields"]["cash_ending"])+1)
        elif mutation=="website_PAT_1VND":r["net_profit"]+=0.000001
        else:r["cash_ending"]=r["client_brokerage_cash_ending"]
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corruption undetected "+mutation)
    print(f"PASS VCK Q1/2026: {n} signed-original exact-VND source fields, 23 independently calculated checks, 4 negative controls, 2025FY opening, no customer custody money.")
