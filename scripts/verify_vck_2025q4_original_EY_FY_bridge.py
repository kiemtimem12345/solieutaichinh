#!/usr/bin/env python3
"""VPS/VCK Q4 2025 signed issuer original, EY audited FY version comparison.

Must not conflate 2025Q4 as-filed B02 revenue with audited FY revenue:
EY FY reduces both full-year operating revenues and expenses by same exact VND.
Q4 B02 comes directly from signed issuer's standalone quarter column, while
Q4 B03 is 12M-9M same scope and is unchanged by EY audit.
"""
import json, copy
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/source-audits/VCK-2025Q4-original-EY-FY2025-exact-vnd.json"
PREV=ROOT/"reports/source-audits/VCK-2025Q3-VPS-original-signed-EY-H1-vnd.json"
DATA=ROOT/"data/financials-VCK.json"
M=Decimal("1000000")
CASH_KEYS=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change")
def read(path):
    return json.loads(path.read_text("utf-8"))
def actual(row,key):
    value=row.get(key)
    assert type(value) in (float,int),(key,value)
    scaled=Decimal(str(value))*M
    assert scaled==scaled.to_integral_value(),(key,value,scaled)
    return int(scaled)
def source_check(src,prior):
    assert src["ticker"]=="VCK" and src["period"]=="2025-Q4"
    assert src["Q4_signed_source"]["original_pdf_sha256"]=="3c3c95bace73bd3c880f77bc299bd61f3e4a887e43dd0f65c6280aff01c2f265"
    assert src["Q4_signed_source"]["archive_sha256"]=="6b8623b993d35eb43f04ee6feb8583b3cafc29f3a7dc8ea4449da8af10c37e43"
    assert src["Q4_signed_source"]["original_pdf_pages"]==43
    assert src["Q4_signed_source"]["original_pdf_bytes"]==2427951
    assert src["Q4_signed_source"]["inspection_workflow_run"]==44933535018
    assert src["Q4_signed_source"]["visual_artifact"]==14718995174
    assert "baocaotaichinh" in src["Q4_signed_source"]["member_name"].lower()
    assert "consolidated" not in src["scope"]
    original=src["original_Q4_exact_vnd_fields"]
    prior9=prior["original_exact_vnd_fields"]
    audit=src["FY2025_EY_audit"]["current_year_matched_issuer_source_fields"]
    assert len(original)==80 and len(src["exact_vnd_equations"])==32
    F=lambda k:int(original[k])
    P=lambda k:int(prior9[k])
    q={k:F(k+"_ytd")-P(k+"_ytd") for k in CASH_KEYS}
    q["cash_beginning"]=P("cash_ending_ytd")
    q["cash_ending"]=F("cash_ending_ytd")
    assert {k:int(v) for k,v in src["quarter_2025Q4_B03_vnd"].items()}==q
    check={
      "assets":F("current_assets")+F("non_current_assets")-F("total_assets"),
      "balance":F("total_assets")-F("total_liabilities")-F("equity"),
      "liabs":F("current_liabilities")+F("long_term_liabilities")-F("total_liabilities"),
      "current_assets":F("financial_assets_current")+F("other_current_assets")-F("current_assets"),
      "noncurrent_assets":sum(F(k) for k in ("financial_assets_noncurrent","fixed_assets",
            "long_term_construction_in_progress","other_non_current_assets"))-F("non_current_assets"),
      "fixed_assets":F("securities_fixed_tangible")+F("securities_fixed_intangible")-F("fixed_assets"),
      "cash_components":F("cash_only")+F("cash_equivalents_only")-F("cash_and_equivalents"),
      "equity_components":sum(F(k) for k in ("capital_share","capital_premium","afs_fair_value_equity","retained_earnings"))-F("equity"),
      "revenue_components":sum(F(k) for k in ("securities_fvtpl_gain","securities_htm_interest_income",
          "securities_loan_interest_income","securities_afs_interest_income",
          "securities_brokerage_revenue","securities_depository_revenue",
          "securities_financial_advice_revenue","securities_other_revenue"))-F("revenue"),
      "operating_expenses":sum(F(k) for k in ("securities_fvtpl_loss","securities_self_trading_expense",
          "securities_brokerage_expense","securities_depository_expense",
          "securities_financial_advice_expense"))-F("securities_operating_expense"),
      "financial_expense":F("interest_expense")+F("financial_other_expense")-F("financial_expense"),
      "quarter_operating":F("revenue")-F("securities_operating_expense")+F("financial_income")
          -F("financial_expense")-F("admin_expense")-F("operating_profit"),
      "quarter_other":F("other_income")-F("other_expense")-F("other_profit"),
      "quarter_pretax":F("operating_profit")+F("other_profit")-F("pretax_profit"),
      "quarter_pat":F("pretax_profit")-F("income_tax")-F("net_profit"),
      "FY_operating":F("revenue_ytd")-F("securities_operating_expense_ytd")
          +F("financial_income_ytd")-F("financial_expense_ytd")-F("admin_expense_ytd")-F("operating_profit_ytd"),
      "FY_pretax":F("operating_profit_ytd")+F("other_profit_ytd")-F("pretax_profit_ytd"),
      "FY_pat":F("pretax_profit_ytd")-F("income_tax_ytd")-F("net_profit_ytd"),
      "Q4_profit_bridge":F("net_profit_ytd")-P("net_profit_ytd")-F("net_profit"),
      "Q4_pretax_bridge":F("pretax_profit_ytd")-P("pretax_profit_ytd")-F("pretax_profit"),
      "Q4_rev_asfiled_bridge":F("revenue_ytd")-P("revenue_ytd")-F("revenue"),
      "FY_cash_sections":sum(F(k+"_ytd") for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))-F("net_cash_change_ytd"),
      "FY_cash_openclose":F("cash_beginning_reported_ytd")+F("net_cash_change_ytd")-F("cash_ending_ytd"),
      "FY_B01_B03_cash":F("cash_and_equivalents")-F("cash_ending_ytd"),
      "quarter_cash_sections":sum(q[k] for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"))-q["net_cash_change"],
      "quarter_cash_openclose":q["cash_beginning"]+q["net_cash_change"]-q["cash_ending"],
      "FY_investing_items":sum(F(k) for k in ("capital_expenditure_ytd","capital_disposals_proceeds_ytd",
          "capital_investments_ytd","capital_investment_recoveries_ytd","dividends_received_ytd"))-F("investing_cash_flow_ytd"),
      "FY_financing_items":sum(F(k) for k in ("share_issue_financing_proceeds_ytd","borrowing_receipts_ytd","loan_repayments_ytd"))-F("financing_cash_flow_ytd"),
      "audit_revenue_minus_expense_effect":F("revenue_ytd")-int(audit["revenue_ytd"])-F("securities_operating_expense_ytd")+int(audit["securities_operating_expense_ytd"]),
      "audit_pretax_match":F("pretax_profit_ytd")-int(audit["pretax_profit_ytd"]),
      "audit_net_match":F("net_profit_ytd")-int(audit["net_profit_ytd"]),
      "audit_cash_match":F("cash_ending_ytd")-int(audit["cash_ending_ytd"])
    }
    assert len(check)==32 and set(check)==set(src["exact_vnd_equations"])
    assert all(v==0 for v in check.values()),check
    assert all(src["exact_vnd_equations"][k]=="0" for k in check)
    for k,v in audit.items():
        if k in ("revenue_ytd","securities_operating_expense_ytd"):continue
        assert F(k)==int(v),(k,F(k),v)
    audited_diff=F("revenue_ytd")-int(audit["revenue_ytd"])
    assert audited_diff==6600452055
    assert audited_diff==F("securities_operating_expense_ytd")-int(audit["securities_operating_expense_ytd"])
    assert audited_diff>0,"audit version must be distinguishable from original"
    assert src["FY2025_EY_audit"]["version_difference"]["offsetting_amount_vnd"]==str(audited_diff)
    assert F("cash_beginning_reported_ytd")==P("cash_beginning_reported_ytd")
    return q
def verify(src,prev,data):
    q=source_check(src,prev)
    assert data["symbol"]=="VCK" and len(data["items"])==7
    row=next(x for x in data["items"] if x["period"]=="2025-Q4")
    assert row["unit"]=="triệu VND" and row["cashflow_period_basis"]=="year_to_date"
    assert row["verification_status"]=="issuer_signed_VCK_Q4_2025_B01_B02_B03_original_EY_FY_bridge"
    assert "không phát hành BCTC hợp nhất" in row["report_type"]
    assert row["source_url"]==src["Q4_signed_source"]["url"]
    v=row["source_validation"]
    assert v["source_audit_ledger"]==str(SRC.relative_to(ROOT))
    assert v["original_signed_pdf_sha256"]==src["Q4_signed_source"]["original_pdf_sha256"]
    assert v["original_pdf_hash_verified"] is True
    assert v["EY_FY2025_company_cash_net_profit_PBT_match_signed_Q4"] is True
    assert v["EY_FY2025_operating_revenue_expense_reclassification_logged"] is True
    assert v["source_is_not_an_explicit_consolidated_report"] is True
    assert v["client_cash_outside_company_B01_verified"] is True
    assert v["q4_cash_bridge_residual_vnd"]=="0"
    approved=set(row["financial_line_items_manually_verified_fields"])
    for k,amount in src["original_Q4_exact_vnd_fields"].items():
        assert k in approved and actual(row,k)==int(amount),(k,actual(row,k),amount)
    for k,amount in q.items():
        assert k in approved and actual(row,k)==amount,(k,actual(row,k),amount)
    assert set(row["cashflow_quarter_manually_verified_fields"])==set(q)
    for alias,source in (("broker_fvtpl_assets","securities_fvtpl_assets"),
       ("broker_lending_assets","securities_margin_loans"),
       ("broker_brokerage_revenue","securities_brokerage_revenue"),
       ("broker_financial_expense","financial_expense")):
        assert actual(row,alias)==actual(row,source)
    assert actual(row,"net_profit_attributable")==actual(row,"net_profit")
    assert actual(row,"cash_ending")==actual(row,"cash_ending_ytd")
    assert not data.get("pre_listing_legacy_reports")
    q2=next(x for x in data["items"] if x["period"]=="2025-Q2")
    assert q2["net_profit"] is None
    assert q2["source_validation"]["unreconciled_vintage_queued"] is True
    return q
if __name__=="__main__":
    src,prev,data=map(read,(SRC,PREV,DATA))
    q=verify(src,prev,data)
    for case in ("asset_source_1VND","net_cash_source_1VND","website_cff_1VND","audited_revenue_wrongly_overwritten"):
        a,b,c=copy.deepcopy(src),copy.deepcopy(prev),copy.deepcopy(data)
        row=next(x for x in c["items"] if x["period"]=="2025-Q4")
        if case=="asset_source_1VND":
            a["original_Q4_exact_vnd_fields"]["total_assets"]=str(int(a["original_Q4_exact_vnd_fields"]["total_assets"])+1)
        elif case=="net_cash_source_1VND":
            a["original_Q4_exact_vnd_fields"]["net_cash_change_ytd"]=str(int(a["original_Q4_exact_vnd_fields"]["net_cash_change_ytd"])+1)
        elif case=="website_cff_1VND":
            row["financing_cash_flow"]+=0.000001
        else:
            row["revenue"]=(int(a["FY2025_EY_audit"]["current_year_matched_issuer_source_fields"]["revenue_ytd"])-int(b["original_exact_vnd_fields"]["revenue_ytd"]))/1e6
        try:verify(a,b,c)
        except (AssertionError,ValueError,TypeError):pass
        else:raise AssertionError("Failed to stop corrupted case: "+case)
    print("PASS VCK Q4 2025 signed Vietnamese 43p source, 80 exact VND fields, 32 accounting/cash checks; EY 18-field audited matched core and explicit offsetting revenue+expense vintage, 4 negative controls.")
    print("Q4 company CFO CFI CFF net:",*(q[k] for k in CASH_KEYS))
    print("Next VCK Q1 2026; VCK signed Q1 and Q3 2025 preserved, no 2024.")
