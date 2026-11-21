#!/usr/bin/env python3
"""Fail-closed source guard: GEG Q1/2026 note5/16a leaves pledged cash 31 Mar unquantified.

Original Q1 signed 82 page source: B01 p6, B09 note5 p22, note16a p27.
Q2 B09 note11 p24 Jan1 pledged deposits 11,422,218,903 VND and Jun30
54,079,653,068 VND cannot prove the restricted balance as at March31.
"""
import json
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
LEDGER=R/"reports/source-audits/GEG-2026Q1-B09-note5-and-16a-no-March31-pledged-balance.json"
DATA=R/"data/financials-GEG.json"
a=json.loads(LEDGER.read_text("utf-8"))
d=json.loads(DATA.read_text("utf-8"))
q=next(x for x in d["items"] if x["period"]=="2026-Q1" and "hợp nhất" in x["report_type"].lower())
h=next(x for x in d["items"] if x["period"]=="2026-Q2" and "hợp nhất" in x["report_type"].lower())
v=lambda row,key:int(Decimal(str(row[key]))*Decimal(1000000))
assert a["original_sha256"]=="d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b"
assert a["original_pages"]==82 and a["github_actions_artifact_run_id"]==44869922268
assert a["signed_B09_note_5_page_22"]["explicit_pledge_restricted_cash_balance_at_2026_03_31"] is False
assert a["signed_B09_note_16a_page_27"]["assets_code_165_pledged_bank_deposit_separately_reported"] is False
assert a["conclusion"]["q1_actual_pledged_deposits_at_Mar31_unknown"] is True
assert a["conclusion"]["absence_of_code165_does_not_prove_restricted_deposits_zero"] is True
assert a["signed_B09_Q2_note11_page24_crosscheck"]["balance_at_Mar31_vnd"] is None
assert a["signed_B09_Q2_note11_page24_crosscheck"]["restricted_deposits_Jan1_vnd"]=="11422218903"
assert a["signed_B09_Q2_note11_page24_crosscheck"]["restricted_deposits_Jun30_vnd"]=="54079653068"
assert int(a["original_B01_page_6"]["code_110_cash_and_equivalents_2026_03_31_vnd"])==v(q,"cash_and_equivalents")
assert int(a["original_B01_page_6"]["code_112_cash_equivalents_2026_03_31_vnd"])==v(q,"cash_equivalents_only")
assert int(a["signed_B09_note_5_page_22"]["cash_2026_03_31_vnd"])+int(a["signed_B09_note_5_page_22"]["cash_equivalents_2026_03_31_vnd"])==v(q,"cash_and_equivalents")
assert int(a["signed_B09_note_16a_page_27"]["short_term_prepaids_2026_03_31_vnd"])==v(q,"short_term_prepaid_expenses")
for row in (q,h):
 s=row["source_validation"]
 assert s["q1_2026_signed_b09_collateral_note_inspection"]==str(LEDGER.relative_to(R))
 assert s["q1_2026_signed_b09_note5_cash_equivalents_20260331_vnd"]=="59231282740"
 assert s["q1_2026_march31_restricted_deposit_explicit_figure_available"] is False
 assert s["q1_2026_march31_collateral_exclusion_unknown"] is True
 assert s["q2_standalone_cashflow_awaits_march31_restricted_cash_amount"] is True
 assert s["q1_2026_signed_b09_note5_pdf_page"]==22 and s["q1_2026_signed_b09_note16a_pdf_page"]==27
assert all(h[k] is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","cash_beginning","net_cash_change"))
assert h["cashflow_period_basis"]=="year_to_date"
print("PASS: GEG Q1 original PDF 82p p22 note5 and p27 note16a source SHA; signed 31 Mar cash exact, pledged funds 31 Mar not separately disclosed. GEG Q2 stand-alone B03 remains safely NULL.")
