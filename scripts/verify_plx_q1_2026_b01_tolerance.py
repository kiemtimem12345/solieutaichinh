#!/usr/bin/env python3
"""PLX Q1/2026: accept two printed B01 subtotals only with cross-source agreement.

A 0.1% tolerance is NOT evidence that the issuer's component arithmetic is exact.
Secondary feeds are checked at their DISPLAY PRECISION (million VND integers
or billion VND one decimal), never falsely asserted to be exact to the dong.
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import urlsplit

from verify_plx_q1_2026_b01_forensic import parse_ledger

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "reports/source-audits/PLX-2026Q1-B01-cross-source-tolerance.json"
LEDGER_PATH = ROOT / "reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt"
DATA_PATH = ROOT / "data/financials-PLX.json"
THRESHOLD = Decimal("0.1")
FIELD_KEYS = {"130": "short_term_receivables", "310": "current_liabilities"}
COMPONENTS = {
    "130": ("recv_customers", "recv_advances", "recv_other", "recv_provision", "recv_pending"),
    "310": ("current_liab_suppliers", "current_liab_customer_advances",
            "current_liab_dividend_payable", "current_liab_taxes",
            "current_liab_employees", "current_liab_accruals",
            "current_liab_unearned_revenue", "current_liab_other",
            "current_liab_borrowings", "current_liab_provision",
            "current_liab_staff_fund", "current_liab_stabilization"),
}

def at_display_precision(amount_vnd: int, unit: str) -> Decimal:
    raw = Decimal(amount_vnd)
    if unit == "million_VND_integer":
        return (raw / Decimal(1_000_000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    if unit == "billion_VND_1dp":
        return (raw / Decimal(1_000_000_000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    raise AssertionError(f"unsupported display unit: {unit!r}")

def validate_cross_sources(audit, v, d):
    assert (audit["ticker"], audit["period"], audit["scope"], audit["as_of"]) == (
        "PLX", "2026-Q1", "consolidated", "2026-03-31")
    assert audit["issuer"]["sha256"] == (
        "158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9")
    assert audit["issuer"]["unit"] == "VND"
    assert audit["reconciliation"]["threshold_percent"] == str(THRESHOLD)
    assert audit["reconciliation"]["exact_original_component_arithmetic_matches"] is False
    seen = set()
    residuals = {}
    for code, ledger_key in FIELD_KEYS.items():
        printed = v[ledger_key]
        assert int(audit["issuer"]["values"][code]) == printed
        components = sum(d[k] for k in COMPONENTS[code])
        assert int(audit["reconciliation"]["original_component_sum_vnd"][code]) == components
        residual = printed - components
        assert int(audit["reconciliation"]["original_residual_vnd"][code]) == residual
        assert residual != 0, "wrongly treating signed source subtotal as exact"
        pct = abs(Decimal(residual)) * 100 / Decimal(abs(printed))
        assert Decimal("0.01") < pct <= THRESHOLD, (code, pct)
        residuals[code] = (residual, pct)
    for source in audit["secondary"]:
        name = source["provider"]
        domain = urlsplit(source["url"]).hostname
        assert name and name not in seen and domain, source
        seen.add(name)
        for code in FIELD_KEYS:
            expected = at_display_precision(int(audit["issuer"]["values"][code]), source["display_unit"])
            assert Decimal(source["displays"][code]) == expected, (name, code, source["displays"][code], expected)
    assert len(seen) >= 3, "require original issuer and three named public comparisons"
    assert set(seen) == {"Stockbiz", "Cophieu68", "iWinStock"}
    return residuals

def main():
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    sections = parse_ledger(LEDGER_PATH.read_text(encoding="utf-8"))
    residuals = validate_cross_sources(audit, sections["SOURCE_B01_B02_B03"], sections["ORIGINAL_B01_DETAIL"])
    doc = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    q = next(x for x in doc["items"] if x["period"] == "2026-Q1"
             and "hợp nhất" in x["report_type"].lower())
    s = q["source_validation"]
    assert q["verification_status"] == "signed_original_B01_B02_B03_Q1_2026_PASS_WITH_TOLERANCE_0p1"
    assert s["b01_tolerance_status"] == audit["reconciliation"]["financial_use_status"] == "PASS_WITH_TOLERANCE"
    assert s["b01_tolerance_percent"] == "0.1"
    assert s["b01_secondary_crosschecks_at_display_precision_passed"] is True
    assert s["b01_secondary_crosscheck_ledger_path"] == str(AUDIT_PATH.relative_to(ROOT))
    assert s["b01_original_subtotal_discrepancies_still_unexplained"] is True
    assert s["full_b01_component_arithmetic_passed"] is False
    assert s["b01_full_pass_blocked_until_official_correction"] is False
    assert s["b01_2026q1_forensic_status"] == "ISSUER_SOURCE_MISMATCH_ACCEPTED_WITH_0P1_TOLERANCE"
    assert s["b01_forensic_issuer_correction_found"] is False
    assert q.get("eps") is None and q.get("eps_ytd") is None
    for code, (residual, pct) in residuals.items():
        assert s["b01_tolerance_residual_vnd"][code] == str(residual)
        assert Decimal(s["b01_tolerance_residual_percent"][code]) == pct.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    # Synthetic negative tests prove tolerance does not bypass source-identity requirements.
    try:
        clone = json.loads(json.dumps(audit))
        clone["secondary"][0]["displays"]["130"] = "19662068"
        validate_cross_sources(clone, sections["SOURCE_B01_B02_B03"], sections["ORIGINAL_B01_DETAIL"])
    except AssertionError:
        pass
    else:
        raise AssertionError("cross-source mismatch was not rejected")
    try:
        clone = json.loads(json.dumps(audit))
        clone["secondary"] = clone["secondary"][:1]
        validate_cross_sources(clone, sections["SOURCE_B01_B02_B03"], sections["ORIGINAL_B01_DETAIL"])
    except AssertionError:
        pass
    else:
        raise AssertionError("single-source override was not rejected")
    assert audit["reconciliation"]["issuer_source_subtotal_mismatch_remains"] is True
    assert audit["reconciliation"]["unprinted_133_317"] == "no value imputed"
    print("PASS_WITH_TOLERANCE (not exact arithmetic): PLX Q1/2026 signed original B01 "
          "130 residual 9,083,970,186 VND; 310 residual 9,088,965,442 VND; "
          "both <0.1% and same rounded published totals at Stockbiz, Cophieu68, iWinStock. "
          "Signed source values preserved, no invented codes 133/317; signed B02/B03 "
          "and other original exact identities remain protected.")

if __name__ == "__main__":
    main()
