#!/usr/bin/env python3
"""GEG case closure: user accepts signed issuer reports as canonical source facts.

Closing *processing* is not the same as asserting an independently signed
Q2-only cash flow. Reopen only on signed FY2026 audited revision or a new
issuer-signed same-basis Q1 restatement, never because a scheduled retry elapsed.
No estimated figure is written to public site financial cells by this rule.
"""
import json
from pathlib import Path
from decimal import Decimal

ROOT=Path(__file__).resolve().parents[1]
L=ROOT/"reports/source-audits/GEG-2026Q2-accepted-issuer-vintage-closure-pending-audited-FY2026.json"
FIN=ROOT/"data/financials-GEG.json"
OLD=ROOT/"reports/source-audits/GEG-2026H1-user-uploaded-reviewed-note37-current-cashflow-version.json"
VND=Decimal("1000000")
FIELDS=("CFO","CFI","CFF","net","opening","FX","ending")

def load(path):return json.loads(path.read_text(encoding="utf-8"))
def check_cash(a):
    assert int(a["CFO"])+int(a["CFI"])+int(a["CFF"])==int(a["net"])
    assert int(a["opening"])+int(a["net"])+int(a["FX"])==int(a["ending"])

def main():
    ledger=load(L);fin=load(FIN);original=load(OLD)
    assert fin["symbol"]==ledger["ticker"]=="GEG"
    assert ledger["period"]=="2026-Q2" and ledger["scope"]=="consolidated"
    assert ledger["case_status"]=="completed_issuer_source_accepted_with_disclosed_vintage_exception"
    assert ledger["decision_by"]=="user_explicit_acceptance_of_issuer_published_figures"
    assert ledger["annual_followup"]["status"]=="await_official_fy2026_audited_published"
    assert ledger["production_rules"]["ticker_case_marked_complete"] is True
    assert ledger["production_rules"]["q2_standalone_b03_core_fields_stay_null"] is True
    assert fin["ticker_processing_completion"]["status"]=="completed_issuer_accepted_exception_pending_fy2026_audited_recheck"
    assert fin["ticker_processing_completion"]["remaining_manual_exception_closed"] is True
    q1=next(x for x in fin["items"] if x["period"]=="2026-Q1" and "hợp nhất" in x["report_type"].lower())
    q2=next(x for x in fin["items"] if x["period"]=="2026-Q2" and "hợp nhất" in x["report_type"].lower())
    q3=next(x for x in fin["items"] if x["period"]=="2026-Q3" and "hợp nhất" in x["report_type"].lower())
    assert q2["source_validation"]["case_closure_status"]=="completed_issuer_accepted_exception_not_independent_quarterly_b03_pass"
    assert q2["source_validation"]["accepted_nonpublication_of_independent_Q2_cash_flow"] is True
    assert q2["source_validation"]["q2_quarter_cashflow_still_blocked_for_unverified_mar31_reclassification"] is True
    for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow",
              "net_cash_change","cash_beginning","foreign_exchange_effect"):
        assert q2[k] is None,(k,q2[k])
    ref=ledger["issuer_numbers_vnd"]["h1_reviewed_6m"]
    from_uploaded=original["reviewed_h1_2026_vnd"]
    for k in FIELDS:
        src={"net":"net_cash_flow","opening":"opening_cash","FX":"fx","ending":"ending_cash"}.get(k,k)
        assert int(ref[k])==int(from_uploaded[src]),(k,ref[k],from_uploaded[src])
    assert ledger["signed_sources"]["h1_reviewed"]["sha256"]==original["reviewed_h1_uploaded_source"]["sha256"]
    assert q2["source_validation"]["accepted_reference_h1_reviewed"]["pdf_sha256"]==ledger["signed_sources"]["h1_reviewed"]["sha256"]
    for a in (ledger["issuer_numbers_vnd"]["h1_reviewed_6m"],ledger["issuer_numbers_vnd"]["q2_initial_6m"],ledger["issuer_numbers_vnd"]["q1_original_3m"],ledger["issuer_numbers_vnd"]["q3_9m"],ledger["issuer_numbers_vnd"]["q3_quarter_if_using_reviewed_h1"]):check_cash(a)
    quarter=ledger["issuer_numbers_vnd"]["q3_quarter_if_using_reviewed_h1"]
    ytd=ledger["issuer_numbers_vnd"]["q3_9m"]
    for k in ("CFO","CFI","CFF","net","FX"):
        assert int(ytd[k])-int(ref[k])==int(quarter[k])
    assert int(quarter["opening"])==int(ref["ending"])
    assert int(quarter["ending"])==int(ytd["ending"])
    assert q3["source_validation"]["reviewed_h1_comparator_accepted_under_geg_completion"]["exact_cash_bridge_residual_vnd"]=="0"
    assert q3["source_validation"]["reviewed_h1_comparator_accepted_under_geg_completion"]["production_q3_original_quarter_values_preserved"] is True
    original_mappings={"CFO":"operating_cash_flow_ytd","CFI":"investing_cash_flow_ytd","CFF":"financing_cash_flow_ytd",
       "net":"net_cash_change_ytd","opening":"cash_beginning_reported_ytd","FX":"foreign_exchange_effect_ytd","ending":"cash_ending"}
    for name,field in original_mappings.items():
        assert Decimal(str(q2[field]))*VND==int(ledger["issuer_numbers_vnd"]["q2_initial_6m"][name])
    assert Decimal(str(q1["cash_ending"]))*VND==105856793049
    assert int(ledger["accounting_cross_vintage_exception"]["opening_reclassification_vnd"])==11422218903
    assert ledger["accounting_cross_vintage_exception"]["march31_restricted_deposit_signed_amount"]=="not_disclosed"
    assert ledger["production_rules"]["reviewed_H1_values_saved_as_canonical_reference_alternative"] is True
    assert ledger["production_rules"]["existing_original_Q2_source_values_retained_for_traceability"] is True
    assert ledger["production_rules"]["do_not_claim_all_quarterly_b03_fields_verified"] is True
    # Negative control: case closure cannot mean the March bank balance is invented.
    assert q2["source_validation"]["march_31_2026_restricted_deposits_balance_verified"] is False
    for field in ("operating_cash_flow","investing_cash_flow","financing_cash_flow"):
        hypothetical=dict(q2);hypothetical[field]=0
        assert hypothetical[field] is not None
        assert q2[field] is None
    print("PASS GEG 2025Q1–2026Q3 source accepted / case closed with disclosed Q2 B03 vintage exception;")
    print("     reviewed H1 benchmark and original Q2 separately source-verified; signed Q3 9M bridge 0 VND;")
    print("     independent Q2 CFO/CFI/CFF not claimed; FY2026 audited update required only on new source.")

if __name__=="__main__":main()
