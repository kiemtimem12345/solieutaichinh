#!/usr/bin/env python3
"""VCI issuer-signed 2025Q4 B01 B02 B03 vs PwC audited FY2025.

Do not mix brokerage client custody money with issuer cash, Q4 as-filed with
unexamined audit restatements, or VND with million VND.
"""
import copy
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCI-2025Q4-asfiled-PwC-audited-2025-source-vnd.json"
Q3=ROOT/"reports/source-audits/VCI-2025Q3-issuer-signed-9M-minus-H1-vnd.json"
DATA=ROOT/"data/financials-VCI.json"
M=Decimal("1000000")
FLOW=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def scaled(row,key):
    v=row.get(key)
    assert type(v) in (int,float),(key,v)
    a=Decimal(str(v))*M
    assert a==a.to_integral_value(),(key,v,a)
    return int(a)
def source_checks(src,q3):
    assert src["ticker"]=="VCI" and src["period"]=="2025-Q4"
    original,aud=src["q4_asfiled"],src["fy2025_audited"]
    assert original["sha256"]=="eacfd66b3e90cb64f197a2b3c6a353adb6781793f00bef7038c04b7445bbea5f"
    assert original["bytes"]==8046323 and original["pages"]==48
    assert aud["sha256"]=="9035205081b85170e7fbf71aa1bdb8fb7052f6461b6feacffa989788d08c12ee"
    assert aud["bytes"]==33936991 and aud["pages"]==101
    assert src["visual_source_workflow_run"]==44923331586
    assert src["source_artifact_id"]==14714577893
    assert "no_subsidiaries" in src["scope"]
    assert len(src["q4_asfiled_exact_vnd_fields"])==73
    f=src["q4_asfiled_exact_vnd_fields"];S=lambda k:int(f[k])
    p=q3["exact_vnd_fields"];P=lambda k:int(p[k])
    checks={
     "assets":S("current_assets")+S("non_current_assets")-S("total_assets"),
     "balance":S("total_assets")-S("total_liabilities")-S("equity"),
     "liabilities":S("current_liabilities")+S("long_term_liabilities")-S("total_liabilities"),
     "current_assets":S("financial_assets_current")+S("other_current_assets")-S("current_assets"),
     "cash_components":S("cash_only")+S("cash_equivalents_only")-S("cash_and_equivalents"),
     "fixed":S("securities_fixed_tangible")+S("securities_fixed_intangible")-S("fixed_assets"),
     "q4_revenue":sum(S(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
         "securities_loan_interest_income","securities_afs_interest_income",
         "securities_brokerage_revenue","securities_financial_advice_revenue",
         "securities_depository_revenue","securities_consulting_revenue",
         "securities_other_revenue"))-S("revenue"),
     "q4_op_expenses":sum(S(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense",
         "securities_brokerage_expense","securities_depository_expense",
         "securities_financial_advice_expense"))-S("securities_operating_expense"),
     "q4_operating":S("revenue")-S("securities_operating_expense")+S("financial_income")
         -S("financial_expense")-S("admin_expense")-S("operating_profit"),
     "q4_other":S("other_income")-S("other_expense")-S("other_profit"),
     "q4_pretax":S("operating_profit")+S("other_profit")-S("pretax_profit"),
     "q4_tax":S("income_tax_current")+S("income_tax_deferred")-S("income_tax"),
     "q4_net":S("pretax_profit")-S("income_tax")-S("net_profit"),
     "fy_operating":S("revenue_ytd")-S("securities_operating_expense_ytd")
         +S("financial_income_ytd")-S("financial_expense_ytd")
         -S("admin_expense_ytd")-S("operating_profit_ytd"),
     "fy_pretax":S("operating_profit_ytd")+S("other_profit_ytd")-S("pretax_profit_ytd"),
     "fy_tax":S("income_tax_current_ytd")+S("income_tax_deferred_ytd")-S("income_tax_ytd"),
     "fy_net":S("pretax_profit_ytd")-S("income_tax_ytd")-S("net_profit_ytd"),
     "fy_less_9m_revenue":S("revenue_ytd")-P("revenue_ytd")-S("revenue"),
     "fy_less_9m_pretax":S("pretax_profit_ytd")-P("pretax_profit_ytd")-S("pretax_profit"),
     "fy_less_9m_profit":S("net_profit_ytd")-P("net_profit_ytd")-S("net_profit"),
     "fy_cash_sections":S("operating_cash_flow_ytd")+S("investing_cash_flow_ytd")
        +S("financing_cash_flow_ytd")-S("net_cash_change_ytd"),
     "fy_cash_bridge":S("cash_beginning_reported_ytd")+S("net_cash_change_ytd")-S("cash_ending_ytd"),
     "fy_investing":S("capital_expenditure_ytd")+S("capital_disposals_proceeds_ytd")-S("investing_cash_flow_ytd"),
     "fy_financing":4006506240000+39299956000000-35809270000000
        +S("dividends_paid_ytd")-S("financing_cash_flow_ytd")
    }
    q={k:S(k+"_ytd")-P(k+"_ytd") for k in FLOW}
    q["cash_beginning"]=P("cash_ending_ytd")
    q["cash_ending"]=S("cash_ending_ytd")
    checks["quarter_cashflow_sections"]=q["operating_cash_flow"]+q["investing_cash_flow"]+q["financing_cash_flow"]-q["net_cash_change"]
    checks["quarter_cash_bridge"]=q["cash_beginning"]+q["net_cash_change"]-q["cash_ending"]
    assert len(checks)==26 and all(v==0 for v in checks.values()),checks
    assert len(src["exact_vnd_checks"])==26 and all(v=="0" for v in src["exact_vnd_checks"].values())
    assert {k:int(v) for k,v in src["quarter_2025q4_standalone_vnd"].items()}==q
    assert len(src["fy_audited_checked_fields"])==19
    for key,v in src["fy_audited_checked_fields"].items():
        assert key in f and int(f[key])==int(v),(key,v,f.get(key))
    assert q["cash_ending"]==S("cash_and_equivalents")
    assert S("cash_beginning_reported_ytd")==P("cash_beginning_reported_ytd")
    assert S("cash_equivalents_only")==0
    return q

def verify(src,prior,data):
    quarter=source_checks(src,prior)
    assert data["symbol"]=="VCI" and len(data["items"])==7
    row=next(r for r in data["items"] if r["period"]=="2025-Q4")
    assert row["unit"]=="triệu VND"
    assert "không có công ty con" in row["report_type"].lower()
    assert row["verification_status"]=="issuer_signed_Q4_2025_B01_B02_B03_PwC_FY_source_reconciled_no_subs"
    assert row["cashflow_period_basis"]=="year_to_date"
    assert row["q4_standalone_cashflow_status"]=="verified_signed_12M_minus_9M_zero_VND_bridge"
    assert row["source_url"]==src["q4_asfiled"]["url"]
    v=row["source_validation"]
    assert v["issuer_original_pdf_sha256"]==src["q4_asfiled"]["sha256"]
    assert v["audited_FY2025_pdf_sha256"]==src["fy2025_audited"]["sha256"]
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["reporter_has_no_subsidiaries_signed_source"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["year_end_audited_FY2025_checked_current_year_fields_match"] is True
    assert v["q4_quarter_cashflow_zero_residual_vnd"]=="0"
    assert v["manual_review_blocking_automatic_extraction"] is False
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    accepted=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in src["q4_asfiled_exact_vnd_fields"].items():
        assert k in accepted and scaled(row,k)==int(amount),(k,row.get(k),amount)
    for k,amount in quarter.items():
        assert k in accepted and scaled(row,k)==amount,(k,amount,row.get(k))
    assert set(row["cashflow_quarter_manually_verified_fields"])==set(quarter)
    assert scaled(row,"cash_ending")==scaled(row,"cash_ending_ytd")
    assert scaled(row,"net_profit_attributable")==scaled(row,"net_profit")
    for alias,base in {"broker_fvtpl_assets":"securities_fvtpl_assets",
       "broker_held_to_maturity_assets":"securities_htm_short",
       "broker_lending_assets":"securities_margin_loans",
       "broker_afs_assets":"securities_afs_assets",
       "broker_custody_revenue":"securities_depository_revenue"}.items():
        assert scaled(row,alias)==scaled(row,base),(alias,base)
    return quarter

def main():
    src,previous,data=read(SRC),read(Q3),read(DATA)
    q=verify(src,previous,data)
    for damage in ("bad_asset_source","bad_fy_cash","wrong_website_profit","wrong_cff_sign"):
        a,b,c=copy.deepcopy(src),copy.deepcopy(previous),copy.deepcopy(data)
        row=next(r for r in c["items"] if r["period"]=="2025-Q4")
        if damage=="bad_asset_source":
            a["q4_asfiled_exact_vnd_fields"]["total_assets"]=str(int(a["q4_asfiled_exact_vnd_fields"]["total_assets"])+1)
        elif damage=="bad_fy_cash":
            a["q4_asfiled_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["q4_asfiled_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif damage=="wrong_website_profit":row["net_profit"]+=0.000001
        else:row["financing_cash_flow"]=-abs(row["financing_cash_flow"])
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Corrupt source/report passed "+damage)
    print("PASS VCI 2025Q4 73 signed VND fields, 19 audited source comparisons, 26 exact-VND accounting/quarter cash checks, 4 corruption controls.")
    print("Q4 standalone company cash:",*[str(q[k]) for k in FLOW],
          "begin",q["cash_beginning"],"end",q["cash_ending"])
    print("Remaining VCI: Q1/2026 then Q2/2026; Q3/2026 already PASS.")
if __name__=="__main__": main()
