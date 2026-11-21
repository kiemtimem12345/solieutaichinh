#!/usr/bin/env python3
"""Regulatory-vintage gate for GEG and IDC Q2/2026 consolidated B03.

This is NOT a conclusion about issuer legal compliance. It distinguishes
fiscal-year applicability, the effective date, the issuer's signed basis,
and a quarter cash bridge. It never creates Q2 standalone cash-flow amounts.
"""
from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "config/reporting-regime-rules-2025-2026.json"
GEG_AUDIT = ROOT / "reports/source-audits/GEG-2026Q2-note11-pledged-cash-opening-reclassification-vnd.json"
IDC_AUDIT = ROOT / "reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json"
NULL_Q2 = ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
           "net_cash_change", "cash_beginning", "capital_expenditure",
           "foreign_exchange_effect", "dividends_paid")
MILLION = Decimal("1000000")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def exact_vnd(row: dict, field: str) -> int:
    val = row.get(field)
    if type(val) not in (int, float):
        raise AssertionError((row.get("period"), field, val))
    n = Decimal(str(val)) * MILLION
    assert n == n.to_integral_value(), (field, val)
    return int(n)


def accounting_basis(policy: dict, fiscal_start: str, *, consolidated: bool,
                     industry: str = "general") -> dict:
    assert industry in ("general", "banking", "securities")
    date.fromisoformat(fiscal_start)
    if industry != "general":
        return {"status": "requires_sector_specific_validation",
                "reason": policy["specialized_exclusions"][industry]}
    if fiscal_start < policy["fiscal_year_crossover"]:
        rules = policy["rules"]["before_2026"]
    else:
        rules = policy["rules"]["from_2026"]
    return {"status": "regime_applicability_identified_not_issuer_compliance",
            "general": rules["general_accounting"],
            "consolidated": rules["consolidated_accounting"] if consolidated else None,
            "fiscal_start": fiscal_start}


def consolidated_rows(ticker: str) -> tuple[dict, dict]:
    fin = load(ROOT / ("data/financials-" + ticker + ".json"))
    assert fin["symbol"] == ticker
    pairs = []
    for period in ("2026-Q1", "2026-Q2"):
        matching = [r for r in fin["items"] if r["period"] == period
                    and "hợp nhất" in (r.get("report_type") or "").lower()]
        assert len(matching) == 1, (ticker, period, len(matching))
        assert matching[0]["unit"] == "triệu VND"
        assert matching[0]["cashflow_period_basis"] == "year_to_date"
        pairs.append(matching[0])
    return pairs[0], pairs[1]


def ensure_quarter_null(row: dict) -> None:
    for field in NULL_Q2:
        assert row.get(field) is None, ("unverified standalone cash value", field, row.get(field))


def cash_bridge(q1: dict, h1: dict) -> dict:
    assert q1["period"] == "2026-Q1" and h1["period"] == "2026-Q2"
    q1_end, h1_end = exact_vnd(q1, "cash_ending"), exact_vnd(h1, "cash_ending")
    net_q2 = exact_vnd(h1, "net_cash_change_ytd") - exact_vnd(q1, "net_cash_change_ytd")
    fx_q2 = exact_vnd(h1, "foreign_exchange_effect_ytd") - exact_vnd(q1, "foreign_exchange_effect_ytd")
    residual = h1_end - q1_end - net_q2 - fx_q2
    return {"signed_q1_end_vnd": q1_end, "signed_h1_end_vnd": h1_end,
            "provisional_net_flow_vnd": net_q2, "provisional_fx_vnd": fx_q2,
            "quarter_cash_bridge_residual_vnd": residual}


def evidence_gate(case: str, evidence: dict, q1: dict, h1: dict) -> dict:
    """Fail closed: no source bridge => no Q2 standalone data regardless of tolerance."""
    ensure_quarter_null(h1)
    bridge = cash_bridge(q1, h1)
    v = q1["source_validation"]
    hv = h1["source_validation"]
    if case == "GEG":
        assert evidence["symbol"] == case and evidence["period"] == "2026-Q2"
        note = evidence["signed_note11"]
        pledged = int(note["at_2026_year_open_vnd"])
        begin = evidence["version_facts"]["q1_signed_original"]["year_open_cash_equivalents_vnd"]
        later = evidence["version_facts"]["q2_signed_original"]["year_open_cash_equivalents_vnd"]
        assert pledge_or_difference(begin, later) == pledged == 11422218903
        assert bridge["quarter_cash_bridge_residual_vnd"] == -pledged
        assert evidence["caution"]["same_amount_remained_restricted_at_Mar31_NOT_proven"] is True
        assert v["march_31_2026_restricted_deposits_balance_verified"] is False
        assert hv["q2_quarter_cashflow_still_blocked_for_unverified_mar31_reclassification"] is True
        source_paths = [evidence["version_facts"]["q1_signed_original"]["url"],
                        evidence["version_facts"]["q2_signed_original"]["url"]]
        reason = "March 31 pledged bank deposit balance and same-basis Q1 B03 not signed/confirmed"
    elif case == "IDC":
        assert evidence["ticker"] == case and evidence["period"] == "2026-Q2"
        assert evidence["decision"]["same_consolidated_scope"] is True
        assert evidence["decision"]["Q1_signed_TT99_2025"] is True
        assert evidence["decision"]["H1_signed_TT99_and_TT43"] is True
        assert evidence["decision"]["signed_same_vintage_Q1_2026_current_period_TT43_comparator_found"] is False
        assert evidence["decision"]["prior_B03_reclass_cannot_be_transferred_into_2026_flow"] is True
        prior = evidence["signed_note41"]["prior_2025_B03_comparative_reclassification_items_vnd"]
        assert sum(int(v) for v in prior.values()) == 0
        assert int(evidence["signed_note41"]["opening_cash_equivalents_2025_prior_reclass_vnd"]) == 890796892
        assert bridge["quarter_cash_bridge_residual_vnd"] == 890796892
        assert v["Q1_2026_TT43_same_current_period_original_comparator_unverified"] is True
        assert hv["IDC_Q2_2026_standalone_cashflow_promotion_blocked_current_basis"] is True
        source_paths = [evidence["Q1_original"]["url"], evidence["H1_reviewed"]["url"]]
        reason = "H1 Note41 adjusts 2025 comparative only; no signed 2026 Q1 TT43 current-period line bridge"
    else:
        raise AssertionError("Unexpected issuer")
    assert q1["source_url"] == source_paths[0]
    assert q1["verification_status"].startswith("issuer_original_visual_verified")
    assert h1["verification_status"].startswith("issuer_original_visual_verified")
    assert len(source_paths) == 2 and all(path.startswith("https://") for path in source_paths)
    # Different statement versions can be individually true without creating a quarter.
    return {"symbol": case, "quarter": "2026-Q2", "scope": "consolidated",
            "original_source_B01_B02_B03_ytd": "retained_verified",
            "standalone_B03": "blocked_missing_signed_same_basis_bridge",
            "missing_signed_evidence": reason, **bridge}


def pledge_or_difference(a: dict, b: dict) -> int:
    e = int(a["cash_equivalents"]) - int(b["cash_equivalents"])
    assert e == int(b["other_current_assets"]) - int(a["other_current_assets"])
    assert int(a["current_assets_total"]) == int(b["current_assets_total"])
    assert int(a["cash_total"]) - int(b["cash_total"]) == e
    return e


def verify_policy(rules: dict) -> None:
    assert rules["fiscal_year_crossover"] == "2026-01-01"
    assert rules["rules"]["from_2026"]["general_effective_on"] == "2026-01-01"
    assert rules["rules"]["from_2026"]["consolidation_amendment_effective_on"] == "2026-04-20"
    assert rules["rules"]["from_2026"]["consolidation_fiscal_start_on_or_after"] == "2026-01-01"
    assert "TT99/2025" in accounting_basis(rules,"2026-01-01",consolidated=True)["general"]
    assert "TT43/2026" in accounting_basis(rules,"2026-01-01",consolidated=True)["consolidated"]
    assert "TT43/2026" not in accounting_basis(rules,"2025-01-01",consolidated=True)["consolidated"]
    assert accounting_basis(rules,"2026-01-01",consolidated=False)["consolidated"] is None
    assert accounting_basis(rules,"2026-01-01",consolidated=True,industry="banking")["status"] == "requires_sector_specific_validation"
    assert accounting_basis(rules,"2026-01-01",consolidated=True,industry="securities")["status"] == "requires_sector_specific_validation"
    d = rules["disclosure"]
    assert d["independent_from_accounting_method"] is True
    assert d["never_infer_original_is_invalid_only_from_new_amendment"] is True
    assert d["must_determine_applicable_version_at_publication"] is True
    g = rules["cashflow_derivation"]
    assert all(g[k] is True for k in ("require_same_scope", "require_same_2026_current_period_policy",
      "require_signed_same_vintage_or_source_supported_bridge", "require_exact_cash_bridge",
      "do_not_apply_subtotal_tolerance_to_cash_bridge", "no_transfer_of_2025_prior_period_comparatives_to_2026_cashflow"))


def main() -> None:
    policy = load(POLICY)
    verify_policy(policy)
    assert policy["schema_version"] == 1
    cases = {"GEG": load(GEG_AUDIT), "IDC": load(IDC_AUDIT)}
    results = []
    for ticker, doc in cases.items():
        q1, h1 = consolidated_rows(ticker)
        assert accounting_basis(policy, "2026-01-01", consolidated=True)["status"] == "regime_applicability_identified_not_issuer_compliance"
        result = evidence_gate(ticker, doc, q1, h1)
        # Negative control: a fabricated zero (or estimated number) must never be accepted as actual quarter value.
        tampered = dict(h1)
        tampered["operating_cash_flow"] = 0
        try:
            ensure_quarter_null(tampered)
        except AssertionError:
            pass
        else:
            raise AssertionError("Allowed invented standalone Q2 CFO")
        results.append(result)
        print(ticker, "PASS verified originals / B03-Q2 BLOCKED",
              result["quarter_cash_bridge_residual_vnd"], "VND")
    assert sorted(r["symbol"] for r in results) == ["GEG", "IDC"]
    print("PASS accounting regime cutover, sector exclusions, disclosure separation,"
          " GEG/IDC Q2 2026 original-vintage guards, exact-VND bridges, tamper tests")


if __name__ == "__main__":
    main()
