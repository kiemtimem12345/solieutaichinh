#!/usr/bin/env python3
"""Fail-closed forensic regression for PLX consolidated B01 Q1 2026.

A PASS from this test means the ISSUER-SOURCE mismatch is correctly detected and
quarantined. It MUST NEVER be mistaken for complete B01 financial approval.
Source: signed 29 Apr 2026 original PDF (pages 2-3; note pages 20-22),
SHA256 158547073d7cd10f8c16e3ce599795b0fe159c70bf1fd7490fff242b5f4bc5f9.
"""
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/PLX-2026Q1-consolidated-signed-original-vnd.txt"
DATA = ROOT / "data/financials-PLX.json"
TOLERANCE = Decimal("0.01")  # percent, NOT absolute VND


def parse_ledger(text):
    sections, group = {}, None
    for line in text.splitlines():
        if line.startswith("# BEGIN "):
            group = line[len("# BEGIN "):].strip()
            assert group not in sections
            sections[group] = {}
        elif line.startswith("# END "):
            group = None
        elif line and not line.startswith("#"):
            key, val = line.split()
            assert group in sections and key not in sections[group]
            sections[group][key] = int(val)
    return sections


def pct_of_subtotal(residual, subtotal):
    return abs(Decimal(residual)) / abs(Decimal(subtotal)) * 100


def tolerance_pass(printed, components):
    return pct_of_subtotal(printed - components, printed) <= TOLERANCE


def main():
    sections = parse_ledger(LEDGER.read_text(encoding="utf-8"))
    v = sections["SOURCE_B01_B02_B03"]
    d = sections["ORIGINAL_B01_DETAIL"]
    f = sections["B01_FORENSIC_OPENING_AND_SIGNED_NOTES"]
    q = next(x for x in json.loads(DATA.read_text(encoding="utf-8"))["items"]
             if x["period"] == "2026-Q1" and "hợp nhất" in x["report_type"].lower())
    s = q["source_validation"]

    # The signed source printed the 01/01/2026 components and BOTH totals:
    opening_receivables = sum(f[k] for k in (
        "recv_open_131_customers", "recv_open_132_advances", "recv_open_135_other",
        "recv_open_136_provision", "recv_open_137_pending"))
    opening_liabilities = sum(f[k] for k in (
        "liab_open_311_suppliers", "liab_open_312_advances", "liab_open_313_dividend",
        "liab_open_314_tax", "liab_open_315_employees", "liab_open_316_accruals",
        "liab_open_319_unearned", "liab_open_320_other", "liab_open_321_borrowings",
        "liab_open_322_provision", "liab_open_323_staff_fund",
        "liab_open_324_stabilization"))
    assert (f["recv_open_subtotal_130"], opening_receivables) == (15969900845614,) * 2
    assert (f["liab_open_subtotal_310"], opening_liabilities) == (55354328118906,) * 2
    assert s["b01_forensic_01jan2026_printed_components_zero_residual_vnd"] == {
        "code_130": "0", "code_310": "0"}

    # The signed Q1 notes independently validate several of the visible figures.
    # Note 3 customer receivables includes 275,000,000 long-term (B01 211).
    note_checks = {
        "note3_customer_current_plus_long":
            d["recv_customers"] + d["long_receivables_customer"],
        "note4_other_receivables_current": d["recv_other"],
        "note5_current_pending_assets": d["recv_pending"],
        "note18_suppliers_current": d["current_liab_suppliers"],
        "note21_accruals_current": d["current_liab_accruals"],
        "note22_other_payables_current": d["current_liab_other"],
        "note23_unearned_current": d["current_liab_unearned_revenue"],
        "note26_provision_current": d["current_liab_provision"],
    }
    assert all(f[k] == val for k, val in note_checks.items()), note_checks

    recv_detail = sum(d[k] for k in (
        "recv_customers", "recv_advances", "recv_other", "recv_provision", "recv_pending"))
    liab_detail = sum(d[k] for k in (
        "current_liab_suppliers", "current_liab_customer_advances",
        "current_liab_dividend_payable", "current_liab_taxes",
        "current_liab_employees", "current_liab_accruals",
        "current_liab_unearned_revenue", "current_liab_other",
        "current_liab_borrowings", "current_liab_provision",
        "current_liab_staff_fund", "current_liab_stabilization"))
    recv_resid = v["short_term_receivables"] - recv_detail
    liab_resid = v["current_liabilities"] - liab_detail
    assert (recv_resid, liab_resid) == (9083970186, 9088965442)
    assert pct_of_subtotal(recv_resid, v["short_term_receivables"]) > TOLERANCE
    assert pct_of_subtotal(liab_resid, v["current_liabilities"]) > TOLERANCE
    assert not tolerance_pass(v["short_term_receivables"], recv_detail)
    assert not tolerance_pass(v["current_liabilities"], liab_detail)

    # Do NOT claim the residuals are internal offsetting balances: they differ.
    assert (liab_resid - recv_resid) == int(s["b01_forensic_residuals_not_equal_vnd"]) == 4995256
    assert "amount_not_inferable" in s["b01_forensic_unprinted_codes_133_317"]["code_133"]
    assert "amount_not_inferable" in s["b01_forensic_unprinted_codes_133_317"]["code_317"]

    # Guard test against false PASS; sample exact data can pass a mathematical
    # test, but the issuer-original record above still MUST remain blocked.
    assert tolerance_pass(1000000, 1000000)
    assert tolerance_pass(1000000, 999900)  # exactly 0.01%
    assert not tolerance_pass(1000000, 999899)
    assert s["b01_2026q1_forensic_status"] == (
        "SIGNED_ORIGINAL_SOURCE_SUBTOTAL_MISMATCH_VERIFIED_NOT_FINANCIAL_PASS")
    assert s["full_b01_component_arithmetic_passed"] is False
    assert s["b01_subgroups_exceed_001percent_tolerance"] is True
    assert s["b01_full_pass_blocked_until_official_correction"] is True
    assert s["b01_forensic_issuer_correction_found"] is False
    assert s["signed_original_b01_short_receivables_unexplained_difference_vnd"] == str(recv_resid)
    assert s["signed_original_b01_current_liabilities_unexplained_difference_vnd"] == str(liab_resid)
    assert q["verification_status"].find("B01_subgroup_and_opening_cash_vintage_exceptions") >= 0

    print("PASS FORENSIC GUARD ONLY — NOT FINANCIAL B01 PASS: signed notes "
          "crosschecked, BOTH opening subtotals exact 0 VND, Q1 closing residuals "
          f"130={recv_resid:,} and 310={liab_resid:,} VND exceed 0.01%; codes "
          "133/317 not printed, no invented amount; preserve source BLOCKED.")


if __name__ == "__main__":
    main()
