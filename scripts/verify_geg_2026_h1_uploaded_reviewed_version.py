#!/usr/bin/env python3
"""GEG uploaded signed 2026 reviewed H1 B03 vs original Q2 and Q1 cash bridge.

Exact-VND source-ledger checks, not a substitute for re-reading an uploaded PDF.
Never automatically promote reviewed H1 to production Q2 without rechecking
Q3 signed nine-month/Q3 standalone version arithmetic and Q1 restatement.
"""
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports/source-audits/GEG-2026H1-user-uploaded-reviewed-note37-current-cashflow-version.json"
ORIGINAL = ROOT / "reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json"
FIN = ROOT / "data/financials-GEG.json"
N = Decimal("1000000")
CASH = ("CFO", "CFI", "CFF", "net_cash_flow", "opening_cash", "fx", "ending_cash")


def integer_vnd(value):
    n = int(value)
    assert str(n) == str(value), value
    return n


def source_numbers(d):
    reviewed = {key: integer_vnd(d["reviewed_h1_2026_vnd"][key]) for key in CASH}
    original = {key: integer_vnd(d["originally_reported_q2_2026_vnd"][key]) for key in CASH}
    differences = {key: integer_vnd(d["reviewed_minus_original_q2_2026_vnd"][key]) for key in CASH}
    for item in (reviewed, original):
        assert item["CFO"] + item["CFI"] + item["CFF"] == item["net_cash_flow"]
        assert item["opening_cash"] + item["net_cash_flow"] + item["fx"] == item["ending_cash"]
    for key in CASH:
        assert reviewed[key] - original[key] == differences[key], (key, differences[key])
    assert reviewed["ending_cash"] == integer_vnd(d["reviewed_h1_2026_vnd"]["b01_ending_cash"])
    assert reviewed["ending_cash"] == 100322233328
    assert differences == {
        "CFO": -14255225113, "CFI": -2018027237, "CFF": 16268307145,
        "net_cash_flow": -4945205, "opening_cash": 0, "fx": 0, "ending_cash": -4945205,
    }
    note = d["signed_reviewed_note37_2026_year_open_vnd"]
    assert integer_vnd(note["pre_reclass_cash_and_equivalents"]) + integer_vnd(note["reclass_from_cash_to_other_current_assets"]) == integer_vnd(note["post_reclass_cash_and_equivalents"]) == reviewed["opening_cash"]
    assert integer_vnd(note["other_current_asset_reclass_code165"]) == -integer_vnd(note["reclass_from_cash_to_other_current_assets"]) == 11422218903
    prior = d["signed_reviewed_note37_2025_comparatives_vnd"]
    assert prior["note_is_prior_year_not_2026_current_q1"] is True
    for target in ("cash_beginning", "net_cash", "cash_ending"):
        assert (integer_vnd(prior[target+"_pre_reclass"]) +
                integer_vnd(prior[target+"_reclass"]) ==
                integer_vnd(prior[target+"_restated"]))
    # 2025 restatement cash opening + flow + FX = ending: reclassification itself balances.
    assert (integer_vnd(prior["cash_beginning_reclass"]) +
            integer_vnd(prior["net_cash_reclass"]) ==
            integer_vnd(prior["cash_ending_reclass"]))
    return reviewed, original


def main():
    a = json.loads(LEDGER.read_text(encoding="utf-8"))
    prior = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    rowset = json.loads(FIN.read_text(encoding="utf-8"))["items"]
    q1 = next(r for r in rowset if r["period"] == "2026-Q1" and "hợp nhất" in r["report_type"].lower())
    q2 = next(r for r in rowset if r["period"] == "2026-Q2" and "hợp nhất" in r["report_type"].lower())
    assert a["ticker"] == "GEG" and a["scope"] == "consolidated" and a["period"] == "2026-Q2"
    upload = a["reviewed_h1_uploaded_source"]
    assert upload["sha256"] == "c5fcba1374cea2e2fc6e82eb66ccd4cf49320bd4a412c4c3f834d60c16ba700e"
    assert upload["pages"] == 74 and upload["b03_pdf_pages"] == [16, 17]
    assert upload["note37_pdf_page"] == 73 and upload["accounting_policy_tt43_pdf_page"] == 23
    assert upload["assurance"].startswith("EY limited review")
    assert a["q1_consolidated_uploaded_original"]["sha256"] == prior["version_facts"]["q1_signed_original"]["sha256"]
    assert a["separate_parent_uploaded_sources"]["h1_reviewed"]["sha256"] != upload["sha256"]
    reviewed, originally = source_numbers(a)
    eq = {"CFO": "operating_cash_flow_ytd", "CFI": "investing_cash_flow_ytd",
          "CFF": "financing_cash_flow_ytd", "net_cash_flow": "net_cash_change_ytd",
          "opening_cash": "cash_beginning_reported_ytd", "fx": "foreign_exchange_effect_ytd",
          "ending_cash": "cash_ending"}
    for key, field in eq.items():
        value = q2[field]
        assert type(value) in (int, float), (field, value)
        assert Decimal(str(value))*N == Decimal(originally[key]), (field, value)
    assert q2["source_url"] == prior["version_facts"]["q2_signed_original"]["url"]
    assert q2["cashflow_period_basis"] == "year_to_date"
    for field in ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
                  "net_cash_change", "cash_beginning", "capital_expenditure",
                  "dividends_paid", "foreign_exchange_effect"):
        assert q2[field] is None, (field, q2[field])
    # Original Q1 matches signed source, but its March-end cash was never
    # re-presented to the later signed reviewed H1 cash definition.
    assert Decimal(str(q1["cash_ending"]))*N == 105856793049
    assert q1["source_url"] == prior["version_facts"]["q1_signed_original"]["url"]
    candidate = a["quarter_candidate_source_arithmetic_only_vnd"]
    for key, field in (("CFO", "operating_cash_flow_ytd"), ("CFI", "investing_cash_flow_ytd"),
                       ("CFF", "financing_cash_flow_ytd"), ("net_cash_flow", "net_cash_change_ytd"),
                       ("fx", "foreign_exchange_effect_ytd")):
        derived = reviewed[key] - int(Decimal(str(q1[field]))*N)
        assert derived == integer_vnd(candidate[key]), (key, derived)
    residual = (reviewed["ending_cash"] - int(Decimal(str(q1["cash_ending"]))*N)
                - integer_vnd(candidate["net_cash_flow"]) - integer_vnd(candidate["fx"]))
    assert residual == integer_vnd(candidate["standalone_q2_cash_bridge_residual"]) == -11422218903
    assert a["decision"]["standalone_q2_cashflow_still_blocked"] is True
    assert a["decision"]["q1_mar31_restricted_deposit_amount_signed_and_confirmed"] is False
    assert a["decision"]["q1_2026_restated_same_basis_current_b03_signed_and_confirmed"] is False
    assert a["decision"]["do_not_overwrite_original_q2_or_verified_q3_without_full_version_reconciliation"] is True
    assert a["signed_reviewed_policy"]["tt43_2026_adoption_explicit"] is True
    assert a["signed_reviewed_policy"]["note37_reclassification_under_tt99_2025_explicit"] is True
    # Negative test: an altered source line must fail the signed B03 bridge.
    changed = json.loads(json.dumps(a))
    changed["reviewed_h1_2026_vnd"]["CFO"] = str(reviewed["CFO"] + 1)
    try:
        source_numbers(changed)
    except AssertionError:
        pass
    else:
        raise AssertionError("Tampered reviewed H1 CFO accepted")
    changed = json.loads(json.dumps(a))
    changed["signed_reviewed_note37_2026_year_open_vnd"]["reclass_from_cash_to_other_current_assets"] = "-11422218904"
    try:
        source_numbers(changed)
    except AssertionError:
        pass
    else:
        raise AssertionError("Tampered TT99 note37 year-open cash was accepted")
    print("PASS GEG 2026 H1 74p signed reviewed upload: B03 CFO/CFI/CFF/net/open/FX/end exact VND,")
    print("     original Q2 vs reviewed H1 deltas, signed Note37 TT99 reclassification,")
    print("     TT43 note3.1.2, 2025 comparatives, 2 negative controls;")
    print("     original Q2 production YTD retained; standalone Q2 cashflow BLOCKED residual -11,422,218,903 VND.")


if __name__ == "__main__":
    main()
