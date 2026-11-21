#!/usr/bin/env python3
"""VIX 2025-Q4 original signed RIÊNG B01/B02/B03 and 9M→12M source-vintage QA.

Quarters 2025-Q1..Q3 have already passed exact original signed source checks
and MUST NOT be recomputed from the FY audited/reissued FY2025 statements.
Signed original Q4 PDF 12 Jan 2026 is the primary source. The 10 Feb 2026
erratum corrects a typographic loan cell on a separate YEAR-END self-filed
report; it does not rewrite the earlier signed Q4 source.
"""
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/source-audits/VIX-2025Q4-original-B01-B02-B03-exact-vnd.json"
PREV=ROOT/"reports/source-audits/VIX-2025Q3-original-B01-B02-B03-exact-vnd.json"
DATA=ROOT/"data/financials-VIX.json"
VND=Decimal("1000000")
FLOW=("operating_cash_flow","investing_cash_flow","financing_cash_flow",
      "net_cash_change","capital_expenditure")
B01_EXTRA={
 "current_financial_assets","current_other_assets","financial_assets_provision",
 "financial_assets_prepay","financial_services_receivables",
 "financial_other_receivables","financial_receivables_provision",
 "long_term_financial_assets","other_non_current_assets"
}

def source_checks(z):
    b,c,m=z["b01"],z["b02_q4"],z["b03_original_12m"]
    checks={
      "b01_full_balance":b["total_liabilities"]+b["equity"]-b["total_assets"],
      "b01_asset_classes":b["current_assets"]+b["non_current_assets"]-b["total_assets"],
      "b01_liability_classes":b["current_liabilities"]+b["long_term_liabilities"]-b["total_liabilities"],
      "b01_current_assets":b["current_financial_assets"]+b["current_other_assets"]-b["current_assets"],
      "b01_noncurrent_assets":b["fixed_assets"]+b["long_term_financial_assets"]+b["other_non_current_assets"]-b["non_current_assets"],
      "b01_current_financial_components":sum(b[k] for k in (
          "cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets",
          "broker_lending_assets","financial_assets_provision","broker_receivables",
          "financial_assets_prepay","financial_services_receivables",
          "financial_other_receivables","financial_receivables_provision"))-b["current_financial_assets"],
      "b02_operating_revenue":sum(c[k] for k in (
          "broker_fvtpl_gain","broker_held_to_maturity_income",
          "broker_lending_income","broker_brokerage_revenue",
          "broker_underwriting_revenue","broker_custody_revenue",
          "broker_financial_advisory_revenue"))-c["revenue"],
      "b02_operating_expenses":sum(c[k] for k in (
          "broker_fvtpl_loss","broker_trading_expense","broker_brokerage_expense",
          "broker_custody_expense","broker_advisory_expense",
          "broker_other_operating_expense"))-c["broker_total_operating_expenses"],
      "b02_operating_profit":c["revenue"]-c["broker_total_operating_expenses"]
          +c["financial_income"]-c["financial_expense"]-c["admin_expense"]-c["broker_net_operating_profit"],
      "b02_other":c["other_income"]-c["other_expense"]-c["other_profit"],
      "b02_pretax":c["broker_net_operating_profit"]+c["other_profit"]-c["pretax_profit"],
      "b02_tax":c["income_tax_current"]+c["income_tax_deferred"]-c["income_tax"],
      "b02_net":c["pretax_profit"]-c["income_tax"]-c["net_profit"],
      "b03_cfo_cfi_cff":sum(m[k] for k in FLOW[:3])-m["net_cash_change"],
      "b03_cash_bridge":m["cash_beginning"]+m["net_cash_change"]-m["cash_ending"],
      "b03_closing_b01":m["cash_ending"]-b["cash_and_equivalents"],
      "fy_b02_tax":z["b02_original_12m"]["income_tax_current"]+z["b02_original_12m"]["income_tax_deferred"]-z["b02_original_12m"]["income_tax"]
    }
    assert len(checks)==17 and all(v==0 for v in checks.values()),checks
    assert b["broker_short_term_borrowings"]==11332000000000
    assert z["provenance"]["fy_erratum_scope"].startswith("separate_FY2025_self_prepared")
    assert z["b02_original_12m"]["eps_ytd"]==3533
    assert c["broker_fvtpl_loss"]>0, "Q4 FVTPL loss is positive 276b, Q3 signed row negative"
    return checks

def money(q,k):
    v=q.get(k)
    assert type(v) in (float,int),(k,v)
    n=Decimal(str(v))*VND
    assert n==n.to_integral_value(),(k,n)
    return int(n)

def main():
    z=json.loads(SOURCE.read_text("utf-8"))
    prev=json.loads(PREV.read_text("utf-8"))
    all_data=json.loads(DATA.read_text("utf-8"))
    row=next(q for q in all_data["items"] if q["period"]=="2025-Q4")
    assert (z["ticker"],z["period"],z["scope"],z["unit"])==("VIX","2025-Q4","separate","VND")
    assert z["provenance"]["q4_pdf_sha256"]=="d5a6e87eeac220951bcbe35c5359940092f58e4080d40f94c6bbd2ab99717408"
    assert (z["provenance"]["q4_pdf_bytes"],z["provenance"]["q4_pdf_pages"])==(1743460,43)
    assert z["provenance"]["fy2025_self_filed_corrected_pdf_sha256"]=="74d89731ce8efbb393f5f94a39cec377d9031c8889568a49aaaa8176133e22d8"
    assert source_checks(z)
    assert row["unit"]=="triệu VND"
    assert "riêng" in row["report_type"].lower() and "hợp nhất" not in row["report_type"].lower()
    assert row["source_url"]==z["provenance"]["q4_issuer_url"]
    assert row["verification_status"]=="issuer_signed_2025Q4_separate_B01_B02_B03_exact_vnd_and_12m_minus_9m_cash"
    src=row["source_validation"]
    assert src["original_issuer_pdf_sha256"]==z["provenance"]["q4_pdf_sha256"]
    assert src["source_scope"]=="separate" and src["source_scope_verified"]
    assert src["original_vnd_ledger"]==str(SOURCE.relative_to(ROOT))
    assert src["full_b01_b02_b03_visual_reviewed"] and src["manually_visual_reviewed"]
    assert src["exact_accounting_identity_count"]==17
    assert src["exact_accounting_identity_max_residual_vnd"]==0
    assert src["original_q4_vs_fy2025_self_filed_erratum_versions_kept_separate"]
    assert src["fy2025_self_filed_loan_code312_typo_corrected_vnd"]=="11332000000000"
    assert src["original_q4_loan_code312_vnd"]=="11332000000000"
    assert src["fy2025_erratum_does_not_revise_q4_original"] is True
    assert row["net_profit_attributable"] is None
    assert row["broker_customer_deposits"] is None
    assert src["client_cash_off_balance_separate_from_company_B01"] is True
    assert row["eps"] is None and row["eps_ytd"]==3533
    for k,v in z["b01"].items():
        if k in B01_EXTRA:continue
        assert money(row,k)==v,("B01",k,money(row,k),v)
    for k,v in z["b02_q4"].items():
        assert money(row,k)==v,("B02",k,money(row,k),v)
    assert money(row,"client_brokerage_cash_off_balance")==z["b01"]["client_brokerage_cash_off_balance"]
    for k,v in z["b02_original_12m"].items():
        if k!="eps_ytd":assert money(row,k+"_ytd")==v,("B02 12M",k)
    m9=prev["b03_9m_ytd"]
    m12=z["b03_original_12m"]
    quarter={k:m12[k]-m9[k] for k in FLOW}
    quarter["cash_beginning"]=m9["cash_ending"]
    quarter["cash_ending"]=m12["cash_ending"]
    assert quarter["operating_cash_flow"]==102816912722
    assert quarter["investing_cash_flow"]==-12627320000
    assert quarter["financing_cash_flow"]==1049000000000
    assert quarter["net_cash_change"]==1139189592722
    assert sum(quarter[k] for k in FLOW[:3])==quarter["net_cash_change"]
    assert quarter["cash_beginning"]+quarter["net_cash_change"]==quarter["cash_ending"]
    assert row["cashflow_period_basis"]=="quarter"
    assert row["cashflow_ytd_period_basis"]=="twelve_months"
    for k,v in quarter.items():assert money(row,k)==v,("Q4",k,money(row,k),v)
    for k,v in m12.items():
        dest=("cash_beginning_reported_ytd" if k=="cash_beginning" else
              "cash_ending_ytd" if k=="cash_ending" else k+"_ytd")
        assert money(row,dest)==v,("12M",dest)
    assert money(row,"cash_and_equivalents")==m12["cash_ending"]
    for k in ("revenue","pretax_profit","net_profit","income_tax","income_tax_current","income_tax_deferred"):
        assert z["b02_q4"][k]+prev["b02_9m_ytd"][k]==z["b02_original_12m"][k],k
    assert src["b03_q4_standalone_source_vnd"]=={k:str(v) for k,v in quarter.items()}
    assert src["b03_12m_original_source_vnd"]=={k:str(v) for k,v in m12.items()}
    # Source-tamper negatives: source arithmetic errors must never use a tolerant shortcut.
    bad=json.loads(json.dumps(z));bad["b01"]["total_assets"]+=1
    try:source_checks(bad)
    except AssertionError:pass
    else:raise AssertionError("Accepted tampered B01 total")
    bad=json.loads(json.dumps(z));bad["b02_q4"]["income_tax_deferred"]+=1
    try:source_checks(bad)
    except AssertionError:pass
    else:raise AssertionError("Accepted tampered B02 tax")
    print("PASS VIX separate Q4 2025 signed issuer 43p, B01/B02/B03 17 exact-VND identities; "
          "Q4 CFO 102,816,912,722, CFI -12,627,320,000, CFF +1,049,000,000,000 "
          "and cash 909,902,606,614 -> 2,049,092,199,336. "
          "12M FY original Q4 minus signed Q3 9M exact 0 VND; "
          "FY self-filed 2026-02-10 correction isolated by source vintage.")
if __name__=="__main__":
    main()
