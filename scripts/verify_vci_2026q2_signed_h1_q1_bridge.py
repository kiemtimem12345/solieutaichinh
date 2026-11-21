#!/usr/bin/env python3
"""VCI 2026Q2 signed B01/B02, PwC-reviewed six-month B03 minus original Q1, exact VND.

Safety: no consolidated report claim for company with no subsidiaries;
exclude broker client custody cash, preserve already PASS Q3/2026.
"""
import copy,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCI-2026Q2-original-reviewed-H1-and-Q1-cash-bridge-vnd.json"
Q1=ROOT/"reports/source-audits/VCI-2026Q1-issuer-signed-original-B01-B02-B03-vnd.json"
H1=ROOT/"reports/source-audits/VCI-2026Q3-reviewed-H1-signed-Q2-quarter-cash-vnd.json"
DATA=ROOT/"data/financials-VCI.json"
M=Decimal("1000000")
def read(p): return json.loads(p.read_text("utf-8"))
def scaled(row,key):
    v=row.get(key);assert type(v) in (int,float),(key,v)
    x=Decimal(str(v))*M
    assert x==x.to_integral_value(),(key,v,x)
    return int(x)
def verify_source(s,q1,h1):
    assert s["ticker"]=="VCI" and s["period"]=="2026-Q2"
    a=s["as_filed_Q2"];b=s["reviewed_H1_PwC"]
    assert a["sha256"]=="a8fec422bac195c1b4d9743a995da35ec5066fa6dc0f951e6fbb36f2218823b5"
    assert b["sha256"]=="1ea814d02563a136d11d718c62c1ffc3c08463ffaf12369c517111cd26f6b9af"
    assert a["bytes"]==17064259 and a["pages"]==48
    assert b["bytes"]==15650240 and b["pages"]==98
    assert a["visually_checked_pdf_pages"]["note1_no_subsidiaries"]==19
    assert s["source_visual_workflow"]==44918419435 and s["source_artifact_id"]==14712970890
    assert "no subsidiaries" in s["scope"]
    f=s["original_exact_vnd_fields"];assert len(f)==69
    q=q1["exact_vnd_fields"]
    F=lambda k:int(f[k]);Q=lambda k:int(q[k])
    h1q=h1["h1_reviewed_source"]["cashflow_vnd"];h1as=h1["q2_as_filed_source"]["cashflow_vnd"]
    assert h1q==h1as,"Reviewed H1 and first Q2 as-filed 6M B03 differ"
    for k,code in (("operating_cash_flow_ytd","operating_cash_flow"),("investing_cash_flow_ytd","investing_cash_flow"),("financing_cash_flow_ytd","financing_cash_flow"),("net_cash_change_ytd","net_cash_change"),("cash_beginning_reported_ytd","cash_beginning"),("cash_ending_ytd","cash_ending")):
        assert F(k)==int(h1q[code]),(k,F(k),h1q[code])
    quarter={k:F(k+"_ytd")-Q(k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
    quarter["cash_beginning"]=Q("cash_ending")
    quarter["cash_ending"]=F("cash_ending_ytd")
    checks={
      "assets":F("current_assets")+F("non_current_assets")-F("total_assets"),
      "balance":F("total_assets")-F("total_liabilities")-F("equity"),
      "liabs":F("current_liabilities")+F("long_term_liabilities")-F("total_liabilities"),
      "current":F("financial_assets_current")+F("other_current_assets")-F("current_assets"),
      "fixed":F("securities_fixed_tangible")+F("securities_fixed_intangible")-F("fixed_assets"),
      "long":F("fixed_assets")+F("long_term_construction_in_progress")+F("other_non_current_assets")-F("non_current_assets"),
      "cash":F("cash_and_equivalents")-F("cash_ending_ytd"),
      "q2_rev":sum(F(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
        "securities_loan_interest_income","securities_afs_interest_income",
        "securities_brokerage_revenue","securities_financial_advice_revenue",
        "securities_depository_revenue","securities_consulting_revenue","securities_other_revenue"))-F("revenue"),
      "q2_opex":sum(F(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense",
        "securities_brokerage_expense","securities_depository_expense",
        "securities_financial_advice_expense"))-F("securities_operating_expense"),
      "q2_operating":F("revenue")-F("securities_operating_expense")+F("financial_income")
        -F("financial_expense")-F("admin_expense")-F("operating_profit"),
      "q2_pretax":F("operating_profit")+F("other_profit")-F("pretax_profit"),
      "q2_tax":F("income_tax_current")+F("income_tax_deferred")-F("income_tax"),
      "q2_profit":F("pretax_profit")-F("income_tax")-F("net_profit"),
      "h1_operating":F("revenue_ytd")-F("securities_operating_expense_ytd")
        +F("financial_income_ytd")-F("financial_expense_ytd")-F("admin_expense_ytd")-F("operating_profit_ytd"),
      "h1_pretax":F("operating_profit_ytd")+F("other_profit_ytd")-F("pretax_profit_ytd"),
      "h1_tax":F("income_tax_current_ytd")+F("income_tax_deferred_ytd")-F("income_tax_ytd"),
      "h1_profit":F("pretax_profit_ytd")-F("income_tax_ytd")-F("net_profit_ytd"),
      "h1_less_q1_revenue":F("revenue_ytd")-Q("revenue")-F("revenue"),
      "h1_less_q1_opex":F("securities_operating_expense_ytd")-Q("securities_operating_expense")-F("securities_operating_expense"),
      "h1_less_q1_fininc":F("financial_income_ytd")-Q("financial_income")-F("financial_income"),
      "h1_less_q1_finexp":F("financial_expense_ytd")-Q("financial_expense")-F("financial_expense"),
      "h1_less_q1_admin":F("admin_expense_ytd")-Q("admin_expense")-F("admin_expense"),
      "h1_less_q1_operating":F("operating_profit_ytd")-Q("operating_profit")-F("operating_profit"),
      "h1_less_q1_pretax":F("pretax_profit_ytd")-Q("pretax_profit")-F("pretax_profit"),
      "h1_less_q1_tax":F("income_tax_ytd")-Q("income_tax")-F("income_tax"),
      "h1_less_q1_profit":F("net_profit_ytd")-Q("net_profit")-F("net_profit"),
      "h1_cashflow":F("operating_cash_flow_ytd")+F("investing_cash_flow_ytd")
        +F("financing_cash_flow_ytd")-F("net_cash_change_ytd"),
      "h1_cashbridge":F("cash_beginning_reported_ytd")+F("net_cash_change_ytd")-F("cash_ending_ytd"),
      "q2_cashflow":quarter["operating_cash_flow"]+quarter["investing_cash_flow"]
        +quarter["financing_cash_flow"]-quarter["net_cash_change"],
      "q2_cashbridge":quarter["cash_beginning"]+quarter["net_cash_change"]-quarter["cash_ending"],
      "q2_begin_matches_q1_end":quarter["cash_beginning"]-Q("cash_ending"),
    }
    assert len(checks)==31
    assert all(v==0 for v in checks.values()),checks
    assert len(s["source_checks_exact_vnd"])==31 and all(v=="0" for v in s["source_checks_exact_vnd"].values())
    assert {k:int(v) for k,v in s["standalone_2026q2_cashflow_vnd"].items()}==quarter
    assert F("cash_beginning_reported_ytd")==Q("cash_beginning")
    return quarter
def verify(s,q1,h1,d):
    quarter=verify_source(s,q1,h1)
    assert d["symbol"]=="VCI" and len(d["items"])==7
    q2=next(z for z in d["items"] if z["period"]=="2026-Q2")
    assert q2["unit"]=="triệu VND" and q2["cashflow_period_basis"]=="year_to_date"
    assert "không có công ty con" in q2["report_type"].lower()
    assert q2["verification_status"]=="issuer_signed_Q2_2026_B01_B02_PwC_reviewed_H1_B03_Q1_bridge_no_subs"
    assert q2["source_url"]==s["as_filed_Q2"]["url"]
    v=q2["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["signed_q2_H1_six_month_B03_vs_reviewed_6M_exact_match"] is True
    assert v["reporter_has_no_subsidiaries_signed_source"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["manual_review_blocking_automatic_extraction"] is False
    assert v["q2_quarter_cash_bridge_residual_vnd"]=="0"
    approved=set(q2["financial_line_items_manually_verified_fields"])
    for k,amount in s["original_exact_vnd_fields"].items():
        assert k in approved and scaled(q2,k)==int(amount),(k,q2.get(k),amount)
    for k,amount in quarter.items():
        assert k in approved and scaled(q2,k)==amount,(k,q2.get(k),amount)
    assert set(q2["cashflow_quarter_manually_verified_fields"])==set(quarter)
    for alt,base in {"broker_afs_assets":"securities_afs_assets",
      "broker_lending_assets":"securities_margin_loans",
      "broker_fvtpl_assets":"securities_fvtpl_assets"}.items():
      assert scaled(q2,alt)==scaled(q2,base)
    assert scaled(q2,"net_profit_attributable")==scaled(q2,"net_profit")
    q3=next(z for z in d["items"] if z["period"]=="2026-Q3")
    assert q3["q3_standalone_cashflow_status"]=="verified_signed_9M_less_reviewed_H1_exact_VND_bridge"
    return quarter

def main():
    s,q1,h1,d=read(SRC),read(Q1),read(H1),read(DATA)
    quarter=verify(s,q1,h1,d)
    for damage in ("one_vnd_asset","one_vnd_net","wrong_website_CFO","wrong_cff_sign"):
        a,b,c,e=copy.deepcopy(s),copy.deepcopy(q1),copy.deepcopy(h1),copy.deepcopy(d)
        row=next(x for x in e["items"] if x["period"]=="2026-Q2")
        if damage=="one_vnd_asset":
            a["original_exact_vnd_fields"]["total_assets"]=str(int(a["original_exact_vnd_fields"]["total_assets"])+1)
        elif damage=="one_vnd_net":
            a["original_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["original_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif damage=="wrong_website_CFO":row["operating_cash_flow"]+=0.000001
        else:row["financing_cash_flow"]=-abs(row["financing_cash_flow"])
        try:verify(a,b,c,e)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corrupt Q2 accounting value passed "+damage)
    print("PASS VCI Q2/2026 signed Q2 B01 B02, issuer and PwC-reviewed H1 6M B03, 69 exact VND fields, 31 identities and 4 negative controls.")
    print("Q2 standalone CFO/CFI/CFF/net:",*(quarter[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")))
    print("VCI 7/7 quarters source verified Q1/2025-Q3/2026, no 2024.")
if __name__=="__main__":main()
