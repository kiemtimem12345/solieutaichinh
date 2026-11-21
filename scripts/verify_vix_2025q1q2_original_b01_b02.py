#!/usr/bin/env python3
"""VIX Q1 and Q2 2025 signed separate (NOT consolidated) original B01/B02/B03 QA.

The original issuer PDF is scan-only. B01 pages 8-10, customer off-balance
p11, B02 pp13-15 and B03 pp16-17 have been inspected as rendered images.
Exact source numbers in the read-only audit ledger are in VND; web data are
stored in millions VND. Reject unit, sign, category, period, scope and EPS
mistakes; tolerance is NOT a license to remap accounting fields.
"""
import json
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-B01-B02-exact-vnd.json"
CASH=ROOT/"reports/source-audits/VIX-2025Q1Q2-original-cash-vnd.json"
DATA=ROOT/"data/financials-VIX.json"
M=Decimal("1000000")
B01_EXTRA={"current_financial_assets","current_other_assets","financial_assets_provision",
           "financial_assets_prepay","financial_services_receivables","financial_other_receivables",
           "financial_receivables_provision","long_term_financial_assets","other_non_current_assets"}

def money(item,key):
    v=item.get(key)
    assert type(v) in (int,float),(key,type(v),v)
    exact=Decimal(str(v))*M
    assert exact==exact.to_integral_value(),(key,exact)
    return int(exact)

def check_signed(src):
    b=src["b01"]; c=src["b02"]
    assert b["total_assets"]==b["total_liabilities"]+b["equity"]
    assert b["total_assets"]==b["current_assets"]+b["non_current_assets"]
    assert b["total_liabilities"]==b["current_liabilities"]+b["long_term_liabilities"]
    assert b["current_assets"]==b["current_financial_assets"]+b["current_other_assets"]
    assert b["non_current_assets"]==b["long_term_financial_assets"]+b["fixed_assets"]+b["other_non_current_assets"]
    assert b["current_financial_assets"]==sum(b[k] for k in (
        "cash_and_equivalents","broker_fvtpl_assets","broker_held_to_maturity_assets",
        "broker_lending_assets","financial_assets_provision","broker_receivables",
        "financial_assets_prepay","financial_services_receivables",
        "financial_other_receivables","financial_receivables_provision"))
    assert c["revenue"]==c["broker_total_operating_revenue"]
    assert c["broker_total_operating_expenses"]==c["broker_operating_expenses"]
    assert c["broker_net_operating_profit"]==(
        c["broker_total_operating_revenue"]-c["broker_total_operating_expenses"]
        +c["financial_income"]-c["financial_expense"]-c["admin_expense"])
    assert c["pretax_profit"]==c["broker_net_operating_profit"]+c["other_profit"]
    assert c["other_profit"]==c["other_income"]-c["other_expense"]
    assert c["income_tax"]==c["income_tax_current"]+c["income_tax_deferred"]
    assert c["net_profit"]==c["pretax_profit"]-c["income_tax"]
    assert b["client_brokerage_cash_off_balance"]!=b["cash_and_equivalents"]
    assert b["broker_short_term_borrowings"]>0
    return True

def main():
    source=json.loads(SOURCE.read_text("utf-8"))
    doc=json.loads(DATA.read_text("utf-8"))
    cash=json.loads(CASH.read_text("utf-8"))
    assert (source["symbol"],source["scope"],source["original_currency"])==("VIX","separate","VND")
    assert source["storage_currency"]=="triệu VND"
    rows={x["period"]:x for x in doc["items"]}
    for period in ("2025-Q1","2025-Q2"):
        signed=source["sources"][period]
        assert check_signed(signed)
        row=rows[period]
        assert row["unit"]=="triệu VND"
        assert "riêng" in row["report_type"].lower()
        assert "hợp nhất" not in row["report_type"].lower()
        assert row["source_validation"]["source_scope"]=="separate"
        assert row["source_validation"]["source_scope_verified"] is True
        assert row["source_validation"]["full_b01_b02_b03_visual_reviewed"] is True
        assert row["source_validation"]["manually_visual_reviewed"] is True
        assert row["source_validation"]["b01_b02_original_signed_visual_verified"] is True
        assert row["source_validation"]["signed_b01_b02_exact_vnd_identity_count"]==10
        assert row["source_validation"]["signed_b01_b02_exact_vnd_identity_max_residual"]==0
        assert row["source_validation"]["original_issuer_pdf_sha256"]==signed["issuer_sha256"]
        assert row["source_validation"]["signed_b01_b02_audit_ledger"]==str(SOURCE.relative_to(ROOT))
        assert row["source_validation"]["client_cash_off_balance_code_026_vnd"]==str(signed["b01"]["client_brokerage_cash_off_balance"])
        assert row["source_validation"]["client_cash_off_balance_separate_from_B01_and_CFO"]
        assert row["broker_customer_deposits"] is None
        assert row["net_profit_attributable"] is None
        assert row["eps"]==signed["eps_quarter"]
        assert row["eps_ytd"]==signed["eps_ytd"]
        assert row["verification_status"]==(
            "issuer_signed_2025Q1_separate_B01_B02_B03_exact_vnd"
            if period=="2025-Q1" else "issuer_signed_2025Q2_separate_B01_B02_B03_exact_vnd_and_H1_bridge")
        assert row["source_validation"]["b03_2025_cashflow_verification_status"].endswith("0_VND_residual")
        assert money(row,"client_brokerage_cash_off_balance")==signed["b01"]["client_brokerage_cash_off_balance"]
        for key,val in signed["b01"].items():
            if key in B01_EXTRA or key=="client_brokerage_cash_off_balance":continue
            assert money(row,key)==val,(period,"B01",key,money(row,key),val)
        for key,val in signed["b02"].items():
            assert money(row,key)==val,(period,"B02",key,money(row,key),val)
        assert money(row,"cash_and_equivalents")==cash["signed_q1_vnd" if period=="2025-Q1" else "signed_h1_vnd"]["cash_ending"]
        # Prevent resurrecting the old severe bug: CFO pretax_profit as an OCR placeholder.
        assert money(row,"operating_cash_flow")!=money(row,"pretax_profit")
        assert row["cashflow_period_basis"]=="quarter"
    q1=source["sources"]["2025-Q1"]
    q2=source["sources"]["2025-Q2"]
    for key in ("revenue","pretax_profit","net_profit"):
        assert q1["b02"][key]+q2["b02"][key]==q2["official_b02_ytd_"+key],key
        assert money(rows["2025-Q2"],key+"_ytd")==q2["official_b02_ytd_"+key]
    assert money(rows["2025-Q1"],"net_profit_ytd")==q1["b02"]["net_profit"]
    assert money(rows["2025-Q2"],"cash_beginning")==money(rows["2025-Q1"],"cash_ending")
    assert q2["eps_quarter"] is None, "Quarter-specific EPS is not printed in signed B02"
    assert q1["eps_ytd"]==255 and q2["eps_ytd"]==1093

    # Negative test: catch wrong B01 subtotal regardless of how small the change is.
    bad=json.loads(json.dumps(q1))
    bad["b01"]["total_assets"]+=1000
    try:check_signed(bad)
    except AssertionError:pass
    else:raise AssertionError("Modified total assets bypassed exact signed-source reconciliation")
    bad=json.loads(json.dumps(q2))
    bad["b02"]["income_tax_deferred"]+=1
    try:check_signed(bad)
    except AssertionError:pass
    else:raise AssertionError("Deferred tax mismatch bypassed exact B02 source reconciliation")
    print("PASS VIX 2025 Q1-Q2 signed separate B01/B02: 2 x 10 exact-VND identities; "
          "plus cross-quarter signed H1 B02 bridges; signed B03 prior regression intact; "
          "2025Q2 quarter EPS intentionally blank; client cash exclusively OFF B01; "
          "no mixing consolidated and separate reports.")

if __name__=="__main__":
    main()
