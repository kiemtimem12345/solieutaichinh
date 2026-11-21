#!/usr/bin/env python3
"""Fail-closed VIX 2026Q1 signed issuer CTCK form and CORE ONLY VND regression.

VIX 17 Apr 2026 issuer-hosted PDF (B01-CTCK, B02-CTCK, B03b-CTCK,
B09-CTCK, Note 2.1 TT210/2014 TT334/2016 VAS27). This verification checks
selected signed current totals and prior FY original source continuity ONLY.
The full 2026Q1 B01/B02/B03 detail and binary PDF SHA are NOT yet verified.
No general legal-compliance certification is made.
"""
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"reports/source-audits/VIX-2026Q1-issuer-TT334-legal-form-and-headline-vnd.json"
DATA=ROOT/"data/financials-VIX.json"
PREV=ROOT/"reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json"
M=Decimal(1000000)

def exact_million(row,k):
    x=row.get(k)
    assert type(x) in (int,float),(k,x)
    d=Decimal(str(x))*M
    assert d==d.to_integral_value(),(k,d)
    return int(d)

def checks(a,fy):
    v=a["q1_2026_exact_vnd"]
    assert (a["period"],a["report_scope"],a["statement_currency"])==("2026-Q1","separate","VND")
    assert a["issuer_pdf"].startswith("https://vixs.vn/wp-content/uploads/2026/04/")
    assert a["form_facts"]["B01"].startswith("B01-CTCK (TT334")
    assert a["form_facts"]["B02"].startswith("B02-CTCK (TT334")
    assert a["form_facts"]["B03"].startswith("B03b-CTCK indirect method (TT334")
    assert "VAS27" in a["form_facts"]["account_policies_declared"]
    assert a["pdf_sha256"] is None and a["sha256_status"]=="PENDING_FULL_PDF_BINARY_RETRIEVAL"
    assert a["do_not_mark_full_pass"] is True
    assert v["total_assets"]==v["total_liabilities"]+v["equity"]
    assert v["pretax_profit"]==v["income_tax"]+v["net_profit"]
    assert v["income_tax"]==v["income_tax_current"]+v["income_tax_deferred"]
    assert v["income_tax_deferred"] < 0
    assert (v["operating_cash_flow"]+v["investing_cash_flow"]+v["financing_cash_flow"])==v["net_cash_change"]
    assert v["cash_beginning"]+v["net_cash_change"]==v["cash_ending"]
    assert v["cash_and_equivalents"]==v["cash_ending"]
    n=a["note5_cash_crosscheck_vnd"]
    assert n["company_bank_cash"]+n["clearing_cash"]==n["total"]==v["cash_ending"]
    assert n["2025_q4_ending_cash"]==v["cash_beginning"]==fy["b03_original_12m"]["cash_ending"]
    assert a["prior_2025q4_from_verified_signed_source_vnd"]["total_assets"]==fy["b01"]["total_assets"]
    assert a["prior_2025q1_comparative_pat_vnd"]==372276939771
    return v

def main():
    a=json.loads(AUDIT.read_text("utf-8"))
    d=json.loads(DATA.read_text("utf-8"))
    prev=json.loads(PREV.read_text("utf-8"))
    v=checks(a,prev)
    q=next(x for x in d["items"] if x["period"]=="2026-Q1")
    s=q["source_validation"]
    assert q["verification_status"]=="issuer_signed_2026Q1_partial_core_B01_B02_B03_verified_FULL_DETAIL_PENDING"
    assert q["unit"]=="triệu VND"
    assert "riêng" in q["report_type"].lower() and "hợp nhất" not in q["report_type"].lower()
    assert q["eps"] is None and q["eps_ytd"]==90
    assert q["broker_customer_deposits"] is None and q["net_profit_attributable"] is None
    assert q["cashflow_period_basis"]=="quarter" and q["cashflow_ytd_period_basis"]=="three_months"
    assert s["original_issuer_partial_document_url"]==a["issuer_pdf"]
    assert s["accounting_specialist_form_2026_verified"] is True
    assert s["source_scope_verified"] is True and s["source_scope"]=="separate"
    assert s["partial_original_source_core_checked"] is True
    assert s["core_only_is_not_financial_full_pass"] is True
    assert s["full_b01_b02_b03_visual_reviewed"] is False
    assert s["manually_visual_reviewed"] is False
    assert s["manual_review_blocking_automatic_extraction"] is True
    assert s["original_pdf_sha256_pending"] is True and s["source_signed_pdf_sha256"] is None
    assert s["signed_q1_2026_2025q4_cash_continuity_vnd_residual"]=="0"
    assert s["partial_core_source_ledger"]==str(AUDIT.relative_to(ROOT))
    for k,num in v.items():assert exact_million(q,k)==num,(k,num,exact_million(q,k))
    for k in ("pretax_profit","income_tax","income_tax_current","income_tax_deferred",
              "net_profit","operating_cash_flow","investing_cash_flow",
              "financing_cash_flow","net_cash_change"):
        assert exact_million(q,k+"_ytd")==v[k],k
    assert exact_million(q,"cash_beginning_reported_ytd")==v["cash_beginning"]
    assert exact_million(q,"cash_ending_ytd")==v["cash_ending"]

    # Fail-closed: source mismatch and "full pass" must not pass this test.
    wrong=json.loads(json.dumps(a));wrong["q1_2026_exact_vnd"]["cash_ending"]+=1
    try:checks(wrong,prev)
    except AssertionError:pass
    else:raise AssertionError("Bad B03 source cash accepted")
    wrong=json.loads(json.dumps(a));wrong["q1_2026_exact_vnd"]["income_tax_deferred"]=abs(v["income_tax_deferred"])
    try:checks(wrong,prev)
    except AssertionError:pass
    else:raise AssertionError("Bad deferred tax sign accepted")
    assert q["verification_status"].endswith("FULL_DETAIL_PENDING")
    print("PASS PARTIAL SOURCE ONLY: VIX 2026Q1 issuer CTCK specialized TT334 B01/B02/B03 forms "
          "and exact original cash/asset/profit totals; Q4'25 end cash = Q1'26 open "
          "2,049,092,199,336 VND, B01/Note5/B03 end cash 970,994,021,164; "
          "CFO 3,243,431,300,446, CFI -529,478,618, CFF -4,321,000,000,000; "
          "signed 2026 full detail and SHA PENDING, no legal certification.")

if __name__=="__main__":
    main()
