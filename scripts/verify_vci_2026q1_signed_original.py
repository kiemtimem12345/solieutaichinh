#!/usr/bin/env python3
"""VCI 2026Q1 signed issuer-original securities-company B01 B02 B03, exact VND."""
from pathlib import Path
from decimal import Decimal
import copy,json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCI-2026Q1-issuer-signed-original-B01-B02-B03-vnd.json"
FIN=ROOT/"data/financials-VCI.json"
FY=ROOT/"reports/source-audits/VCI-2025Q4-asfiled-PwC-audited-2025-source-vnd.json"
M=Decimal("1000000")
def read(p):return json.loads(p.read_text("utf-8"))
def val(row,k):
    v=row.get(k)
    assert type(v) in (int,float),(k,v)
    a=Decimal(str(v))*M
    assert a==a.to_integral_value(),(k,a)
    return int(a)
def source_checks(z,fy):
    assert z["ticker"]=="VCI" and z["period"]=="2026-Q1"
    assert z["pdf_sha256"]=="b5562dc6db6a785388e8e2de6e4ea5c10d5c759448de22f27e6d2fcfdcbad2a1"
    assert z["pdf_bytes"]==15121284 and z["pdf_pages"]==48
    assert z["source_inspection_workflow"]==44924314308 and z["source_artifact_id"]==14714518427
    assert z["visually_checked_pdf_pages"]["note1_no_subsidiaries"]==19
    f=z["exact_vnd_fields"]
    assert len(f)==59
    N=lambda k:int(f[k])
    c={
       "assets":N("current_assets")+N("non_current_assets")-N("total_assets"),
       "balance":N("total_assets")-N("total_liabilities")-N("equity"),
       "liabs":N("current_liabilities")+N("long_term_liabilities")-N("total_liabilities"),
       "current":N("financial_assets_current")+N("other_current_assets")-N("current_assets"),
       "cash":N("cash_only")+N("cash_equivalents_only")-N("cash_and_equivalents"),
       "fixed":N("securities_fixed_tangible")+N("securities_fixed_intangible")-N("fixed_assets"),
       "revenue":sum(N(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
           "securities_loan_interest_income","securities_afs_interest_income",
           "securities_brokerage_revenue","securities_financial_advice_revenue",
           "securities_depository_revenue","securities_consulting_revenue",
           "securities_other_revenue"))-N("revenue"),
       "expense":sum(N(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense",
           "securities_brokerage_expense","securities_depository_expense","securities_financial_advice_expense"))-N("securities_operating_expense"),
       "operating":N("revenue")-N("securities_operating_expense")+N("financial_income")-
           N("financial_expense")-N("admin_expense")-N("operating_profit"),
       "pbt":N("operating_profit")+N("other_profit")-N("pretax_profit"),
       "tax":N("income_tax_current")+N("income_tax_deferred")-N("income_tax"),
       "profit":N("pretax_profit")-N("income_tax")-N("net_profit"),
       "sections":N("operating_cash_flow")+N("investing_cash_flow")+N("financing_cash_flow")-N("net_cash_change"),
       "cash_bridge":N("cash_beginning")+N("net_cash_change")-N("cash_ending"),
       "B01_B03_cash":N("cash_and_equivalents")-N("cash_ending"),
       "cash_FY2025_opening":N("cash_beginning")-int(fy["q4_asfiled_exact_vnd_fields"]["cash_ending_ytd"]),
       "CFI":N("capital_expenditure")-N("investing_cash_flow"),
       "CFF":12203971000000-10025000000000+N("dividends_paid")-N("financing_cash_flow"),
    }
    assert len(c)==18 and all(v==0 for v in c.values()),c
    assert len(z["checks_exact_vnd"])==18 and all(int(v)==0 for v in z["checks_exact_vnd"].values())
    assert "no subsidiaries" in z["scope"]
    return c
def verify(z,fy,d):
    c=source_checks(z,fy)
    assert len(d["items"])==7 and d["symbol"]=="VCI"
    row=next(r for r in d["items"] if r["period"]=="2026-Q1")
    assert row["verification_status"]=="issuer_signed_2026Q1_B01_B02_B03_original_exact_vnd_no_subs"
    assert "không có công ty con" in row["report_type"].lower()
    assert row["cashflow_period_basis"]=="quarter" and row["unit"]=="triệu VND"
    assert row["source_url"]==z["source_url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["issuer_original_pdf_sha256"]==z["pdf_sha256"]
    assert v["reporter_has_no_subsidiaries_signed_source"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["manual_review_blocking_automatic_extraction"] is False
    allowed=set(row["financial_line_items_manually_verified_fields"])
    for k,source in z["exact_vnd_fields"].items():
        assert k in allowed and val(row,k)==int(source),(k,row.get(k),source)
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","cash_ending"):
        ytd="cash_beginning_reported_ytd" if k=="cash_beginning" else k+"_ytd"
        assert val(row,k)==val(row,ytd),(k,ytd)
    for alt,field in {"broker_afs_assets":"securities_afs_assets",
       "broker_fvtpl_assets":"securities_fvtpl_assets",
       "broker_lending_assets":"securities_margin_loans"}.items():
        assert val(row,alt)==val(row,field),(alt,field)
    assert val(row,"net_profit_attributable")==val(row,"net_profit")
    return c
def main():
    z,fy,d=read(SRC),read(FY),read(FIN)
    checks=verify(z,fy,d)
    for corruption in ("one_vnd_asset","one_vnd_CFO","source_cash","wrong_sign"):
        a,b,c=copy.deepcopy(z),copy.deepcopy(fy),copy.deepcopy(d)
        row=next(r for r in c["items"] if r["period"]=="2026-Q1")
        if corruption=="one_vnd_asset":
            a["exact_vnd_fields"]["total_assets"]=str(int(a["exact_vnd_fields"]["total_assets"])+1)
        elif corruption=="one_vnd_CFO":
            a["exact_vnd_fields"]["operating_cash_flow"]=str(int(a["exact_vnd_fields"]["operating_cash_flow"])+1)
        elif corruption=="source_cash":row["cash_ending"]+=0.000001
        else:row["financing_cash_flow"]=-abs(row["financing_cash_flow"])
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Source/report corruption not rejected: "+corruption)
    print("PASS VCI Q1/2026 59 signed-original VND values, 18 exact identities, 4 negative controls and 2025FY opening bridge.")
    print("Remaining Q2/2026; Q3/2026 already verified.")
if __name__=="__main__": main()
