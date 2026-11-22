#!/usr/bin/env python3
"""VCK Q2 2026: issuer signed B01/B02, reviewed H1 B03 minus signed Q1.

Use exact VND, zero-VND company cash residual; preserve direct Q2 B02 and
a small documented YTD/Q1 comparison variance, no balancing plug.
"""
from pathlib import Path
from decimal import Decimal
import copy,json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2026Q2-issuer-signed-original-and-Q1-quarter-vnd.json"
Q1=ROOT/"reports/source-audits/VCK-2026Q1-issuer-signed-original-vnd.json"
FIN=ROOT/"data/financials-VCK.json"
M=Decimal("1000000")
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def asvnd(row,k):
    v=row.get(k)
    assert type(v) in (float,int),(k,v)
    x=Decimal(str(v))*M
    assert x==x.to_integral_value(),(k,x)
    return int(x)
def verify_source(s,q1):
    assert s["ticker"]=="VCK" and s["period"]=="2026-Q2"
    signed=s["issuer_q2_source"]
    assert signed["pdf_sha256"]=="6652ed69f6a3c666194d5594813234e5458d45fc40691dd1a97736143dc0bfa9"
    assert signed["pdf_pages"]==61 and signed["pdf_bytes"]==3588837
    assert signed["inspection_workflow"]==44968719866
    assert signed["signed_date"]=="2026-07-17"
    assert signed["url"].endswith("VCK_Baocaotaichinh_Q2_2026.pdf")
    review=s["reviewed_H1_2026"]
    assert review["visual_seen"] and review["document_pages"]==72
    assert review["signed_report_date"]=="2026-08-12"
    assert review["reconciles_exactly_with_asfiled_Q2_B03"] is True
    assert s["source_policy"]["customer_cash_is_separate"] is True
    f=s["original_exact_vnd_fields"]
    assert len(f)==84 and len(s["source_checks_vnd"])==34
    V=lambda k:int(f[k])
    Q=lambda k:int(q1["source_current_vnd_fields"][k])
    for lhs,other in (("operating_cash_flow_ytd","operating_cash_flow"),
                      ("investing_cash_flow_ytd","investing_cash_flow"),
                      ("financing_cash_flow_ytd","financing_cash_flow"),
                      ("net_cash_change_ytd","net_cash_change"),
                      ("cash_beginning_reported_ytd","cash_beginning"),
                      ("cash_ending_ytd","cash_ending")):
        assert V(lhs)==int(review["source_cashflow_6m_vnd"][other]),lhs
    q2={k:V(k+"_ytd")-Q(k) for k in ("operating_cash_flow","investing_cash_flow",
        "financing_cash_flow","net_cash_change")}
    q2["cash_beginning"]=Q("cash_ending")
    q2["cash_ending"]=V("cash_ending_ytd")
    assert {k:int(v) for k,v in s["q2_standalone_company_cashflow_vnd"].items()}==q2
    equations={
      "assets":V("current_assets")+V("non_current_assets")-V("total_assets"),
      "balance":V("total_assets")-V("total_liabilities")-V("equity"),
      "liabs":V("current_liabilities")+V("long_term_liabilities")-V("total_liabilities"),
      "current":V("financial_assets_current")+V("other_current_assets")-V("current_assets"),
      "noncurrent":V("financial_assets_noncurrent")+V("fixed_assets")+
         V("long_term_construction_in_progress")+V("other_non_current_assets")-V("non_current_assets"),
      "fixed":V("securities_fixed_tangible")+V("securities_fixed_intangible")-V("fixed_assets"),
      "cash":V("cash_only")+V("cash_equivalents_only")-V("cash_and_equivalents"),
      "revenue":sum(V(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
          "securities_loan_interest_income","securities_afs_interest_income",
          "securities_brokerage_revenue","securities_depository_revenue",
          "securities_financial_advice_revenue","securities_other_revenue"))-V("revenue"),
      "expenses":sum(V(k) for k in ("securities_fvtpl_loss","securities_htm_loss",
          "securities_afs_reclass_loss","securities_self_trading_expense",
          "securities_brokerage_expense","securities_depository_expense",
          "securities_financial_advice_expense"))-V("securities_operating_expense"),
      "financial_income":V("financial_income_deposit_interest")+V("financial_income_other_investments")-V("financial_income"),
      "financial_expense":V("interest_expense")+V("financial_fx_loss")+V("financial_other_expense")-V("financial_expense"),
      "quarter_profit":V("revenue")-V("securities_operating_expense")+V("financial_income")-
          V("financial_expense")-V("admin_expense")-V("operating_profit"),
      "quarter_pretax":V("operating_profit")+V("other_profit")-V("pretax_profit"),
      "quarter_net":V("pretax_profit")-V("income_tax")-V("net_profit"),
      "H1_operating":V("revenue_ytd")-V("securities_operating_expense_ytd")+
          V("financial_income_ytd")-V("financial_expense_ytd")-V("admin_expense_ytd")-V("operating_profit_ytd"),
      "H1_pretax":V("operating_profit_ytd")+V("other_profit_ytd")-V("pretax_profit_ytd"),
      "H1_net":V("pretax_profit_ytd")-V("income_tax_ytd")-V("net_profit_ytd"),
      "H1_b03":V("operating_cash_flow_ytd")+V("investing_cash_flow_ytd")+
          V("financing_cash_flow_ytd")-V("net_cash_change_ytd"),
      "H1_open_to_close":V("cash_beginning_reported_ytd")+V("net_cash_change_ytd")-V("cash_ending_ytd"),
      "H1_B01_B03_company_cash":V("cash_and_equivalents")-V("cash_ending_ytd"),
      "Q2_b03":q2["operating_cash_flow"]+q2["investing_cash_flow"]+
          q2["financing_cash_flow"]-q2["net_cash_change"],
      "Q2_open_to_close":q2["cash_beginning"]+q2["net_cash_change"]-q2["cash_ending"],
      "Q2_begin_equals_Q1_end":q2["cash_beginning"]-Q("cash_ending"),
      "H1_investing":V("capital_expenditure_ytd")-V("investing_cash_flow_ytd"),
      "H1_financing":V("issued_equity_cash_ytd")+V("borrowing_receipts_ytd")+
          V("loan_repayments_ytd")-V("financing_cash_flow_ytd")
    }
    assert all(v==0 for v in equations.values()),equations
    # The signed 2025/2026 B02 quarter is authoritative; independent Q1
    # comparison shows a 29,595,000 VND charge difference (0.017% of admin).
    delta=29595000
    assert V("pretax_profit_ytd")-Q("pretax_profit")-V("pretax_profit")==delta
    assert V("net_profit_ytd")-Q("net_profit")-V("net_profit")==delta
    assert V("admin_expense_ytd")-Q("admin_expense")-V("admin_expense")==-delta
    assert V("operating_profit_ytd")-Q("operating_profit")-V("operating_profit")==delta
    assert Decimal(delta)/Decimal(V("admin_expense"))<Decimal("0.001") # 0.1% latest exception acceptance
    assert Decimal(delta)/Decimal(V("pretax_profit"))<Decimal("0.0001") # 0.01% for PBT
    for k,v in s["source_checks_vnd"].items():
        assert int(v)==(delta if k in ("q2_op_vintage","q2_pbt_vintage","q2_net_vintage")
            else (-delta if k=="q2_admin_vintage" else 0)),(k,v)
    assert V("cash_and_equivalents")!=V("client_brokerage_cash_ending_ytd")
    return q2

def verify(s,sourceq1,d):
    q=verify_source(s,sourceq1)
    assert d["symbol"]=="VCK" and len(d["items"])==7
    row=next(x for x in d["items"] if x["period"]=="2026-Q2")
    assert row["verification_status"]=="issuer_signed_VCK_Q2_2026_B01_B02_reviewed_H1_B03_Q1_cash_bridge"
    assert row["source_url"]==s["issuer_q2_source"]["url"]
    assert "không phải báo cáo hợp nhất" in row["report_type"].lower()
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["issuer_original_pdf_sha256"]==s["issuer_q2_source"]["pdf_sha256"]
    assert v["reviewed_H1_6M_B03_matches_first_signed_B03_exact_vnd"] is True
    assert v["company_and_brokerage_cash_isolated"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["q2_company_cash_residual_vnd"]=="0"
    assert v["manual_review_blocking_automatic_extraction"] is False
    accepted=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in s["original_exact_vnd_fields"].items():
        assert k in accepted and asvnd(row,k)==int(amount),(k,amount,row.get(k))
    for k,amount in q.items():
        assert k in accepted and asvnd(row,k)==amount,(k,amount,row.get(k))
    for a,b in {"broker_customer_deposits":"client_brokerage_cash_ending_ytd",
                "broker_fvtpl_assets":"securities_fvtpl_assets",
                "broker_afs_assets":"securities_afs_assets",
                "broker_lending_assets":"securities_margin_loans"}.items():
        assert asvnd(row,a)==asvnd(row,b)
    assert asvnd(row,"cash_ending")==asvnd(row,"cash_ending_ytd")
    assert asvnd(row,"net_profit_attributable")==asvnd(row,"net_profit")
    assert not d.get("pre_listing_legacy_reports")
    return q

def main():
    a,b,c=read(SRC),read(Q1),read(FIN)
    q=verify(a,b,c)
    for kind in ("assets_1vnd","netcash_1vnd","source_income_1vnd","client_as_company"):
        s,p,d=copy.deepcopy(a),copy.deepcopy(b),copy.deepcopy(c)
        row=next(r for r in d["items"] if r["period"]=="2026-Q2")
        if kind=="assets_1vnd":
            s["original_exact_vnd_fields"]["total_assets"]=str(int(s["original_exact_vnd_fields"]["total_assets"])+1)
        elif kind=="netcash_1vnd":
            s["original_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(s["original_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif kind=="source_income_1vnd":row["net_profit"]+=0.000001
        else:row["cash_ending"]=row["broker_customer_deposits"]
        try:verify(s,p,d)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corruption not detected: "+kind)
    print("PASS VCK 2026-Q2: 84 signed VND cells, 34 stored source checks (30 exact zero), 25 fresh zero-residual equations, 4 negative controls.")
    print("Cash Q2 CFO CFI CFF net:",*[q[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")])
    print("Next VCK Q3/2026. No completed period revisited.")
if __name__=="__main__":main()
