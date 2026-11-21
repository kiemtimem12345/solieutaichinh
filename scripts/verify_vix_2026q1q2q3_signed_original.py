#!/usr/bin/env python3
"""Exact-VND original-signature accounting QA for VIX Q1/Q2/Q3 2026 RIÊNG.

Source: signed issuer Q1/Q2 PDFs, Q3 Vietstock signed company-parent
Vietnamese PDF + corresponding English translation of SAME statement.
Do not treat translation as an independent issuer. This validator is
independent of the 0.1% tolerance used for eligible source subtotal errors.
Fails closed on source scope, signs, VND/million VND, 3M/6M/9M basis,
off-balance client money and quarter-only EPS.
"""
from pathlib import Path
from decimal import Decimal
import json
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/source-audits/VIX-2026Q1Q2Q3-original-signed-VND.json"
DATA=ROOT/"data/financials-VIX.json"
PRIOR=ROOT/"reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json"
POLICY=ROOT/"reports/accounting-legal-validation-framework.json"
M=Decimal("1000000")
PERIODS=("2026-Q1","2026-Q2","2026-Q3")
FLOW=("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","capital_expenditure")
B01_EXTRA={"current_financial_assets","current_other_assets","financial_assets_provision",
           "financial_assets_prepay","financial_services_receivables","financial_other_receivables",
           "financial_receivables_provision","long_term_financial_assets","other_non_current_assets",
           "cash_and_equivalents_breakdown"}
B01_COMPONENTS=("cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets",
                "broker_lending_assets","financial_assets_provision","broker_receivables",
                "financial_assets_prepay","financial_services_receivables",
                "financial_other_receivables","financial_receivables_provision")
B02_REVENUE=("broker_fvtpl_gain","broker_held_to_maturity_income","broker_lending_income",
             "broker_brokerage_revenue","broker_underwriting_revenue",
             "broker_custody_revenue","broker_financial_advisory_revenue")
B02_EXPENSE=("broker_fvtpl_loss","broker_trading_expense","broker_brokerage_expense",
             "broker_custody_expense","broker_advisory_expense","broker_other_operating_expense")
PANDL=("revenue","pretax_profit","net_profit","income_tax","income_tax_current","income_tax_deferred")

def million(row,k):
    x=row.get(k)
    assert type(x) in (int,float),(k,x)
    d=Decimal(str(x))*M
    assert d==d.to_integral_value(),(k,d)
    return int(d)

def source_math(original):
    b=original["b01"];c=original["b02_quarter"];y=original["b02_ytd"];m=original["b03_ytd"]
    checks={
      "B01_assets":b["current_assets"]+b["non_current_assets"]-b["total_assets"],
      "B01_full_balance":b["total_liabilities"]+b["equity"]-b["total_assets"],
      "B01_liabilities":b["current_liabilities"]+b["long_term_liabilities"]-b["total_liabilities"],
      "B01_current_assets":b["current_financial_assets"]+b["current_other_assets"]-b["current_assets"],
      "B01_noncurrent":b["fixed_assets"]+b["long_term_financial_assets"]+b["other_non_current_assets"]-b["non_current_assets"],
      "B01_financial_detail":sum(b[k] for k in B01_COMPONENTS)-b["current_financial_assets"],
      "B02_revenue_detail":sum(c[k] for k in B02_REVENUE)-c["revenue"],
      "B02_expense_detail":sum(c[k] for k in B02_EXPENSE)-c["broker_total_operating_expenses"],
      "B02_operating_profit":c["revenue"]-c["broker_total_operating_expenses"]+c["financial_income"]-c["financial_expense"]-c["admin_expense"]-c["broker_net_operating_profit"],
      "B02_other":c["other_income"]-c["other_expense"]-c["other_profit"],
      "B02_pretax":c["broker_net_operating_profit"]+c["other_profit"]-c["pretax_profit"],
      "B02_tax":c["income_tax_current"]+c["income_tax_deferred"]-c["income_tax"],
      "B02_net":c["pretax_profit"]-c["income_tax"]-c["net_profit"],
      "B03_CFO_CFI_CFF":m["operating_cash_flow"]+m["investing_cash_flow"]+m["financing_cash_flow"]-m["net_cash_change"],
      "B03_cash_bridge":m["cash_beginning"]+m["net_cash_change"]-m["cash_ending"],
      "B03_B01_cash":m["cash_ending"]-b["cash_and_equivalents"],
      "B01_B03_cash_components":b["cash_and_equivalents_breakdown"]["bank_cash_vnd"]+b["cash_and_equivalents_breakdown"]["cash_equivalents_vnd"]-b["cash_and_equivalents"],
      "B02_YTD_tax":y["income_tax_current"]+y["income_tax_deferred"]-y["income_tax"]
    }
    assert len(checks)==18,checks
    assert set(checks.values())=={0},checks
    assert c["broker_total_operating_revenue"]==c["revenue"]
    assert c["broker_operating_expenses"]==c["broker_total_operating_expenses"]
    assert c["income_tax"]==c["income_tax_current"]+c["income_tax_deferred"]
    assert y["pretax_profit"]-y["income_tax"]==y["net_profit"]
    return checks

def validate(doc,ledger,year_open):
    assert doc["symbol"]=="VIX" and ledger["symbol"]=="VIX"
    assert ledger["scope"]=="separate_company_parent" and ledger["unit"]=="VND"
    assert set(ledger["periods"])==set(PERIODS)
    rows={x["period"]:x for x in doc["items"]}
    assert len(rows)==len(doc["items"])
    assert set(PERIODS).issubset(rows)
    assert len(rows)<=20
    assert all("2025-Q1"<=k<="2026-Q3" for k in rows)
    assert year_open==2049092199336
    expected_status={
     "2026-Q1":"issuer_signed_2026Q1__separate_B01_B02_B03_exact_vnd",
     "2026-Q2":"issuer_signed_2026Q2__separate_B01_B02_B03_exact_vnd_H1_minus_Q1_quarter",
     "2026-Q3":"issuer_signed_2026Q3__separate_B01_B02_B03_exact_vnd_9M_minus_H1_quarter",
    }
    previous=None
    for period in PERIODS:
        original=ledger["periods"][period]
        p=original["provenance"]
        o=original["signed_source_VND"]
        b=o["b01"];c=o["b02_quarter"];y=o["b02_ytd"];m=o["b03_ytd"]
        checks=source_math(o)
        assert original["independent_source_arithmetic_checks"]==18
        assert original["original_source_arithmetic_max_residual_vnd"]==0
        row=rows[period];s=row["source_validation"]
        assert row["verification_status"]==expected_status[period]
        assert "riêng" in row["report_type"].lower() and "hợp nhất" not in row["report_type"].lower()
        assert row["unit"]=="triệu VND"
        assert s["source_scope"]=="separate" and s["source_scope_verified"] is True
        assert s["full_b01_b02_b03_visual_reviewed"] is True
        assert s["manually_visual_reviewed"] is True
        assert s["original_issuer_pdf_sha256"]==p["pdf_sha256"]
        assert s["original_issuer_pdf_pages"]==p["pdf_pages"]
        assert s["original_signed_source_exact_VND_identity_count"]==18
        assert s["original_signed_source_identity_max_residual_vnd"]==0
        assert s["same_scope_2026_quarter_and_YTD_bridge"] is True
        assert s["same_scope_cash_2025_Q4_continuity_verified"] is True
        assert s["client_cash_off_balance_separate_from_company_B01"] is True
        assert s["legal_compliance_certified"] is False
        assert s["signed_original_vnd_ledger"]==str(SOURCE.relative_to(ROOT))
        assert row["net_profit_attributable"] is None and row["broker_customer_deposits"] is None
        assert row["eps"] is None and row["eps_ytd"]==y["eps_ytd"]
        assert row["cashflow_period_basis"]=="quarter"
        assert row["cashflow_ytd_period_basis"]==({"2026-Q1":"three_months","2026-Q2":"six_months","2026-Q3":"nine_months"}[period])
        assert million(row,"client_brokerage_cash_off_balance")==b["client_brokerage_cash_off_balance"]
        for k,v in b.items():
            if k not in B01_EXTRA and k!="client_brokerage_cash_off_balance":
                assert million(row,k)==v,(period,"B01",k,v,million(row,k))
        for k,v in c.items():
            assert million(row,k)==v,(period,"B02",k,v,million(row,k))
        for k,v in y.items():
            if k!="eps_ytd":
                assert million(row,k+"_ytd")==v,(period,"B02 YTD",k)
        assert million(row,"cash_and_equivalents")==m["cash_ending"]
        for k,v in m.items():
            dest="cash_beginning_reported_ytd" if k=="cash_beginning" else "cash_ending_ytd" if k=="cash_ending" else k+"_ytd"
            assert million(row,dest)==v,(period,"B03 YTD",k)
        quarter={k:m[k]-(previous[k] if previous else 0) for k in FLOW}
        quarter["cash_beginning"]=previous["cash_ending"] if previous else year_open
        quarter["cash_ending"]=m["cash_ending"]
        assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
        assert quarter["operating_cash_flow"]+quarter["investing_cash_flow"]+quarter["financing_cash_flow"]==quarter["net_cash_change"]
        for k,v in quarter.items():
            assert million(row,k)==v,(period,"B03 QTR",k,v,million(row,k))
        assert s["signed_ytd_B03_vnd"]=={k:str(v) for k,v in m.items()}
        assert s["derived_quarter_B03_vnd"]=={k:str(v) for k,v in quarter.items()}
        for k in PANDL:
            assert y[k]==c[k]+(ledger["periods"][{"2026-Q2":"2026-Q1","2026-Q3":"2026-Q2"}[period]]["signed_source_VND"]["b02_ytd"][k] if previous else 0),(period,k)
        if period=="2026-Q1":
            assert m["cash_beginning"]==year_open
            assert p["source_kind"]=="issuer_signed_original" and p["pdf_pages"]==43
            assert p["pdf_sha256"]=="90845a76928739230468c0f8ea3f3890e29475fe91239cbb51c5e9b28aab852f"
            assert s["original_pdf_sha256_pending"] is False and s["source_signed_pdf_sha256"]==p["pdf_sha256"]
        elif period=="2026-Q2":
            assert m["cash_beginning"]==year_open
            assert p["source_kind"]=="issuer_signed_original" and p["pdf_pages"]==43
            assert p["pdf_sha256"]=="41ea9b8482afff88b81297139afac8fd9c2075aa01ecea350992beda23e622c0"
        else:
            assert m["cash_beginning"]==year_open
            assert p["source_kind"]=="Vietstock_hosted_signed_company_parent_original"
            assert p["pdf_pages"]==44 and p["english_translation_pages"]==47
            assert p["pdf_sha256"]=="088c2fed91cee527f33e898f43b67b94ca4db404636841fbc963cb8c0c6acfbd"
            assert p["english_translation_pdf_sha256"]=="64ef26327d91aea75f699337efe86e7c3580701fa3dd66cbd6025e1e20d847f4"
            assert p["english_translation_independent_provider"] is False
            assert s["signed_source_language_variants"]["english_is_translated_same_separate_reporting_scope"] is True
        previous=m
    assert len([p for p in rows if p.startswith("2025-Q")])==4
    return True

def negative_tests(doc,ledger,year_open):
    def deny(fn):
        try:fn()
        except AssertionError:return
        raise AssertionError("ACCEPTED incorrect source, unit, scope, sign or period")
    q=ledger["periods"]["2026-Q1"]
    bad=json.loads(json.dumps(q["signed_source_VND"]));bad["b01"]["total_assets"]+=1
    deny(lambda:source_math(bad))
    bad=json.loads(json.dumps(q["signed_source_VND"]));bad["b02_quarter"]["income_tax_deferred"]=abs(bad["b02_quarter"]["income_tax_deferred"])
    deny(lambda:source_math(bad))
    mutated=json.loads(json.dumps(doc))
    next(x for x in mutated["items"] if x["period"]=="2026-Q2")["operating_cash_flow"]=75253
    deny(lambda:validate(mutated,ledger,year_open))
    mutated=json.loads(json.dumps(doc))
    next(x for x in mutated["items"] if x["period"]=="2026-Q3")["broker_customer_deposits"]=123
    deny(lambda:validate(mutated,ledger,year_open))
    mutated=json.loads(json.dumps(doc))
    next(x for x in mutated["items"] if x["period"]=="2026-Q1")["unit"]="VND"
    deny(lambda:validate(mutated,ledger,year_open))
    mutated=json.loads(json.dumps(doc))
    next(x for x in mutated["items"] if x["period"]=="2026-Q3")["report_type"]="BCTC hợp nhất"
    deny(lambda:validate(mutated,ledger,year_open))
    mutated=json.loads(json.dumps(doc))
    next(x for x in mutated["items"] if x["period"]=="2026-Q2")["eps"]=114
    deny(lambda:validate(mutated,ledger,year_open))
    return 7

def main():
    doc=json.loads(DATA.read_text("utf-8"))
    ledger=json.loads(SOURCE.read_text("utf-8"))
    fy=json.loads(PRIOR.read_text("utf-8"))
    policy=json.loads(POLICY.read_text("utf-8"))
    year_open=fy["b03_original_12m"]["cash_ending"]
    assert policy["tolerances"]["user_accepted_relative_subtotal_percent"]=="0.1"
    validate(doc,ledger,year_open)
    count=negative_tests(doc,ledger,year_open)
    print("PASS: VIX RIENG 2026 Q1 Q2 Q3: each 18 signed-source exact VND accounting checks,"
          " signed original SHA Q1+Q2 + Q3 signed Vietstock Vietnamese parent and matching"
          " English translation (not independent), B02 3M+Q2=6M and 6M+Q3=9M exact,"
          " B03 Q2=6M-3M and Q3=9M-6M, cash bridges exact."
          f" {count} negative fail-closed cases. No 0.1% tolerance invoked, legal compliance not certified.")

if __name__=="__main__":
    main()
