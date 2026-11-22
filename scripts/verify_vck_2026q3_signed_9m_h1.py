#!/usr/bin/env python3
"""VCK 2026 Q3 original HOSE signed issuer B01 B02 B03 and reviewed H1 bridge.

Fail closed on VND, issuer corporate-vs-client cash, period/scope, Q3 vs 9M,
signed B02 source totals. Keep original small component variances explicit and
within current user 0.1% tolerance: no balancing plugs.
"""
from pathlib import Path
from decimal import Decimal
import copy, json
R=Path(__file__).resolve().parents[1]
SOURCE=R/"reports/source-audits/VCK-2026Q3-issuer-signed-9M-reviewed-H1-exact-vnd.json"
PRIOR=R/"reports/source-audits/VCK-2026Q2-issuer-signed-original-and-Q1-quarter-vnd.json"
QUEUE=R/"reports/financial-exception-queue.json"
FIN=R/"data/financials-VCK.json"
M=Decimal("1000000")
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def vnd(row,k):
    n=row.get(k)
    assert type(n) in (float,int),(k,n)
    x=Decimal(str(n))*M
    assert x==x.to_integral_value(),(k,n,x)
    return int(x)
def source_verify(s,pr):
    assert s["ticker"]=="VCK" and s["period"]=="2026-Q3"
    assert s["signed_date"]=="2026-10-19" and s["published_date"]=="2026-10-20"
    assert s["verified_original_at_HOSE_PDF"] is True
    assert "2505926" in s["official_original_url"] and s["unit"]=="VND"
    assert "consolidated report" in s["scope"] and "client custody" in s["scope"]
    f=s["original_exact_vnd_fields"]
    assert len(f)==89
    N=lambda k:int(f[k])
    p=pr["original_exact_vnd_fields"]
    P=lambda k:int(p[k])
    assert pr["ticker"]=="VCK" and pr["period"]=="2026-Q2"
    assert pr["reviewed_H1_2026"]["reconciles_exactly_with_asfiled_Q2_B03"] is True
    for k,prior_key in (("operating_cash_flow_ytd","operating_cash_flow_ytd"),
                        ("investing_cash_flow_ytd","investing_cash_flow_ytd"),
                        ("financing_cash_flow_ytd","financing_cash_flow_ytd"),
                        ("net_cash_change_ytd","net_cash_change_ytd"),
                        ("cash_ending_ytd","cash_ending_ytd")):
        assert P(prior_key)==int(pr["reviewed_H1_2026"]["source_cashflow_6m_vnd"][
            {"operating_cash_flow_ytd":"operating_cash_flow",
             "investing_cash_flow_ytd":"investing_cash_flow",
             "financing_cash_flow_ytd":"financing_cash_flow",
             "net_cash_change_ytd":"net_cash_change",
             "cash_ending_ytd":"cash_ending"}[k]])
    q3={k:N(k+"_ytd")-P(k+"_ytd") for k in
        ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")}
    q3["cash_beginning"]=P("cash_ending_ytd")
    q3["cash_ending"]=N("cash_ending_ytd")
    assert {k:int(x) for k,x in s["standalone_2026Q3_cashflow_vnd"].items()}==q3
    identities={
       "B01_assets":N("current_assets")+N("non_current_assets")-N("total_assets"),
       "B01_balance":N("total_assets")-N("total_liabilities")-N("equity"),
       "B01_liabilities":N("current_liabilities")+N("long_term_liabilities")-N("total_liabilities"),
       "B01_current_financial_other":N("financial_assets_current")+N("other_current_assets")-N("current_assets"),
       "B01_noncurrent":N("financial_assets_noncurrent")+N("fixed_assets")+
           N("long_term_construction_in_progress")+N("other_non_current_assets")-N("non_current_assets"),
       "B01_financial_noncurrent":N("long_term_receivables")+N("long_term_investments")+
           N("long_term_financial_impairment")-N("financial_assets_noncurrent"),
       "B01_fixed":N("securities_fixed_tangible")+N("securities_fixed_intangible")-N("fixed_assets"),
       "B01_cash":N("cash_only")+N("cash_equivalents_only")-N("cash_and_equivalents"),
       "B01_equity":sum(N(k) for k in ("capital_share","capital_premium",
                      "afs_fair_value_equity","retained_earnings"))-N("equity"),
       "B02_fvtpl":N("securities_fvtpl_disposal_gain")+N("securities_fvtpl_revaluation_gain")+
           N("securities_fvtpl_dividend_interest")-N("securities_fvtpl_gain"),
       "B02_revenue_components":sum(N(k) for k in
         ("securities_fvtpl_gain","securities_htm_interest_income","securities_loan_interest_income",
          "securities_afs_interest_income","securities_brokerage_revenue",
          "securities_depository_revenue","securities_financial_advice_revenue",
          "securities_other_revenue"))-N("revenue"),
       "B02_expense_components":sum(N(k) for k in
         ("securities_fvtpl_loss","securities_htm_loss","securities_afs_reclass_loss",
          "securities_self_trading_expense","securities_brokerage_expense",
          "securities_depository_expense","securities_financial_advice_expense"))-N("securities_operating_expense"),
       "B02_finance_income":N("financial_income_deposit_interest")+
           N("financial_income_other_investments")-N("financial_income"),
       "B02_finance_expense":N("interest_expense")+N("financial_fx_loss")+
           N("financial_other_expense")-N("financial_expense"),
       "B02_operating":N("revenue")-N("securities_operating_expense")+
           N("financial_income")-N("financial_expense")-N("admin_expense")-N("operating_profit"),
       "B02_other":N("other_income")-N("other_expense")-N("other_profit"),
       "B02_pretax":N("operating_profit")+N("other_profit")-N("pretax_profit"),
       "B02_tax":N("pretax_profit")-N("income_tax")-N("net_profit"),
       "B02_ytd_operating":N("revenue_ytd")-N("securities_operating_expense_ytd")+
           N("financial_income_ytd")-N("financial_expense_ytd")-
           N("admin_expense_ytd")-N("operating_profit_ytd"),
       "B02_ytd_pretax":N("operating_profit_ytd")+N("other_profit_ytd")-N("pretax_profit_ytd"),
       "B02_ytd_tax":N("pretax_profit_ytd")-N("income_tax_ytd")-N("net_profit_ytd"),
       "B02_q3_revenue_bridge":N("revenue_ytd")-P("revenue_ytd")-N("revenue"),
       "B02_q3_expenses_bridge":N("securities_operating_expense_ytd")-
           P("securities_operating_expense_ytd")-N("securities_operating_expense"),
       "B02_q3_finance_income_bridge":N("financial_income_ytd")-
           P("financial_income_ytd")-N("financial_income"),
       "B02_q3_finance_expense_bridge":N("financial_expense_ytd")-
           P("financial_expense_ytd")-N("financial_expense"),
       "B02_q3_admin_bridge":N("admin_expense_ytd")-P("admin_expense_ytd")-N("admin_expense"),
       "B02_q3_operating_bridge":N("operating_profit_ytd")-
           P("operating_profit_ytd")-N("operating_profit"),
       "B02_q3_pretax_bridge":N("pretax_profit_ytd")-P("pretax_profit_ytd")-N("pretax_profit"),
       "B02_q3_tax_bridge":N("income_tax_ytd")-P("income_tax_ytd")-N("income_tax"),
       "B02_q3_profit_bridge":N("net_profit_ytd")-P("net_profit_ytd")-N("net_profit"),
       "B03_9M_sections":sum(N(k+"_ytd") for k in
          ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))-
          N("net_cash_change_ytd"),
       "B03_9M_bridge":N("cash_beginning_reported_ytd")+N("net_cash_change_ytd")-N("cash_ending_ytd"),
       "B03_9M_B01_cash":N("cash_and_equivalents")-N("cash_ending_ytd"),
       "B03_9M_CFI":N("capital_expenditure_ytd")-N("investing_cash_flow_ytd"),
       "B03_9M_CFF":N("issued_equity_cash_ytd")+N("borrowing_receipts_ytd")+
           N("loan_repayments_ytd")-N("financing_cash_flow_ytd"),
       "B03_Q3_sections":q3["operating_cash_flow"]+q3["investing_cash_flow"]+
           q3["financing_cash_flow"]-q3["net_cash_change"],
       "B03_Q3_bridge":q3["cash_beginning"]+q3["net_cash_change"]-q3["cash_ending"],
       "B03_Q3_previous_6M_cash":q3["cash_beginning"]-P("cash_ending_ytd")
    }
    assert len(identities)==38 and set(identities)==set(s["exact_vnd_source_checks"])
    for k,value in identities.items():
        assert int(s["exact_vnd_source_checks"][k])==value,(k,value)
        if k not in ("B02_revenue_components","B02_expense_components"):
            assert value==0,(k,value)
    assert identities["B02_revenue_components"]==-500000000
    assert identities["B02_expense_components"]==-400000
    # 0.1% source-details acceptance: do not tamper with signed source totals.
    assert Decimal(500000000)/Decimal(N("revenue")) < Decimal("0.001")
    assert Decimal(400000)/Decimal(N("securities_operating_expense")) < Decimal("0.001")
    assert N("cash_and_equivalents")!=N("client_brokerage_cash_ending_ytd")
    assert sum(q3[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))==q3["net_cash_change"]
    return q3

def verify(s,prior,fin,queue):
    quarter=source_verify(s,prior)
    assert fin["symbol"]=="VCK" and len(fin["items"])==7
    assert [x["period"] for x in fin["items"]]==["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
    assert not fin.get("pre_listing_legacy_reports")
    r=next(x for x in fin["items"] if x["period"]=="2026-Q3")
    assert r["verification_status"]=="issuer_signed_VCK_Q3_2026_HOSE_B01_B02_B03_reviewed_H1_cash_verified"
    assert "không phải hợp nhất" in r["report_type"].lower()
    assert r["unit"]=="triệu VND" and r["cashflow_period_basis"]=="year_to_date"
    assert r["source_url"]==s["official_original_url"]
    v=r["source_validation"]
    assert v["source_audit_ledger"]==str(SOURCE.relative_to(R))
    assert v["source_verified_B01_B02_B03"] and v["broker_client_cash_excluded_from_company_CFO_CFI_CFF"]
    assert v["B02_direct_quarter_income_vs_9M_minus_H1_exact_zero_vnd"]
    assert v["B02_component_subtotal_variance_within_latest_0_1pct"]
    assert v["reviewed_H1_quarter_cash_bridge_exact_zero_vnd"]=="0"
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["manual_review_blocking_automatic_extraction"] is False
    accepted=set(r["financial_line_items_manually_verified_fields"])
    for k,amount in s["original_exact_vnd_fields"].items():
        assert k in accepted and vnd(r,k)==int(amount),(k,r.get(k),amount)
    for k,amount in quarter.items():
        assert k in accepted and vnd(r,k)==amount,(k,r.get(k),amount)
    for alias,base in {"broker_customer_deposits":"client_brokerage_cash_ending_ytd",
        "broker_fvtpl_assets":"securities_fvtpl_assets","broker_afs_assets":"securities_afs_assets",
        "broker_lending_assets":"securities_margin_loans","broker_interest_expense":"interest_expense"}.items():
        assert vnd(r,alias)==vnd(r,base)
    assert vnd(r,"net_profit_attributable")==vnd(r,"net_profit")
    assert vnd(r,"cash_ending")==vnd(r,"cash_ending_ytd")
    e=next(x for x in queue["items"] if x["id"]=="VCK-2026Q3-signed-B02-component-subtotal-500m")
    assert e["production_eligible"] is True and e["blocks_sequential_processing"] is False
    assert e["user_visibility"]=="only_if_user_explicitly_asks_for_missing_ticker_or_period_list"
    return quarter

def main():
    s,p,d,q=read(SOURCE),read(PRIOR),read(FIN),read(QUEUE)
    quarter=verify(s,p,d,q)
    for bad in ("change_cash_source_1vnd","change_profit_source_1vnd","website_net_1vnd","broker_cash_as_company"):
        a,b,c,e=copy.deepcopy(s),copy.deepcopy(p),copy.deepcopy(d),copy.deepcopy(q)
        r=next(x for x in c["items"] if x["period"]=="2026-Q3")
        if bad=="change_cash_source_1vnd":a["original_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["original_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif bad=="change_profit_source_1vnd":a["original_exact_vnd_fields"]["net_profit"]=str(int(a["original_exact_vnd_fields"]["net_profit"])+1)
        elif bad=="website_net_1vnd":r["net_cash_change"]+=0.000001
        else:r["cash_ending"]=r["broker_customer_deposits"]
        try:verify(a,b,c,e)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corrupted source/data not detected "+bad)
    print("PASS VPS/VCK 2026Q3 issuer signed HOSE 89 VND values, 38 equations, 36 zero, 2 immaterial component-source differences, 4 negative controls.")
    print("Standalone Q3 issuer cash CFO CFI CFF net:",*[str(quarter[k]) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")])
    print("Next ticker according newest checkpoint, no 2024 and no rerun of PASS source periods.")
if __name__=="__main__":main()
