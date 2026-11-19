#!/usr/bin/env python3
"""IDC 2026 H1 original reviewed Note 41 TT99 non-cash comparative reclassification.

Hard source evidence: signed 72p HNX-disclosed reviewed consolidated IDC H1
BSC attachment 1599258-1, SHA256 f1366a... (PDF 10 B01, 17 B03, 21
accounting policy, 34 note 4 cash, 71 note 41 comparative presentation).
Never silently allocate source-vintage cash to CFO/CFI/CFF or change Q1 original.
Q2 standalone remains deferred until same-current-period reporting basis cleared.
"""
import json
from decimal import Decimal
from pathlib import Path

rows={r["period"]:r for r in json.loads((Path(__file__).resolve().parents[1]/"data/financials-IDC.json").read_text("utf8"))["items"]}
fy,q1,h1,q3=[rows[p] for p in ("2025-Q4","2026-Q1","2026-Q2","2026-Q3")]
def V(r,k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
e=h1["source_validation"]["h1_2026_reviewed_opening_reclassification_note41"]
sv=h1["source_validation"]
assert e["issuer_signed_original_pdf_sha256"]=="f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944"
assert e["original_pdf_pages"]==72 and e["original_pdf_bytes"]==10086230
assert e["visually_verified_pdf_pages"]==[10,17,21,34,71]
assert "1599258-1" in e["bsc_original_pdf_url"]
assert "Note 41" not in e["issuer_reclassification_note"] or "99/2025" in e["issuer_reclassification_note"]
assert e["disclosed_cash_equivalents_opening_reclassification_vnd"]=="890796892"
original=int(e["original_2025_fy_ending_cash_and_q1_2026_beginning_vnd"])
revised=int(e["reviewed_h1_2026_comparative_cash_and_b03_opening_vnd"])
noncash=int(e["disclosed_cash_equivalents_opening_reclassification_vnd"])
assert original==V(fy,"cash_ending")==V(q1,"cash_beginning")
assert revised==V(h1,"cash_beginning_reported_ytd")==V(q3,"cash_beginning_reported_ytd")
assert revised-original==noncash==890796892
assert int(e["original_cash_equivalents_2025fy_vnd"])+noncash==int(e["reviewed_h1_opening_cash_equivalents_vnd"])
m={k:int(v) for k,v in e["reclassification_balancing_other_accounts_vnd"].items()}
assert (m["cash_equivalents"]+m["short_term_held_to_maturity"]+m["other_short_term_receivables"])==0
assert (m["inventory"]+m["long_term_construction_in_progress"]+m["investment_property"])==0
assert m["cash_equivalents"]==noncash
p={k:int(v) for k,v in sv["q2_arithmetic_only_cash_flow_provisional_vnd"].items()}
assert p["operating_cash_flow"]+p["investing_cash_flow"]+p["financing_cash_flow"]==p["net_cash_change"]
assert V(q1,"cash_ending")==p["cash_beginning"]
unadjusted=p["cash_beginning"]+p["net_cash_change"]+p["foreign_exchange_effect"]-V(h1,"cash_ending")
assert unadjusted==-890796892
assert unadjusted+noncash==0
checks=e["identity_checks_vnd"]
assert int(checks["cash_opening_after_reclassification"])==0
assert int(checks["q2_unadjusted_quarter_cash_bridge"])==-890796892
assert all(int(v)==0 for k,v in checks.items() if k!="q2_unadjusted_quarter_cash_bridge")
assert sv["q2_cashflow_bridge_adjusted_by_disclosed_reclassification_vnd"]=="0"
assert sv["q2_cashflow_non_cash_opening_adjustment_vnd"]=="890796892"
assert "explanation_confirmed_note41" in sv["audited_fy2025_cash_cross_vintage"]
assert q1["source_validation"]["h1_2026_opening_cash_comparison"]["issuer_note_41_reclassification_proven"] is True
assert q1["source_validation"]["h1_2026_opening_cash_comparison"]["issuer_note_confirmation_pending"] is False
assert all(h1.get(k) is None for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","foreign_exchange_effect","capital_expenditure","dividends_paid"))
assert "comparability_pending" in sv["q2_cashflow_quarter_status"]
assert h1["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_6m_ytd_q2_cash_deferred"
assert q3["verification_status"]=="issuer_original_visual_verified_b01_b02_b03_9m_and_q3_standalone_cash"
print("PASS IDC reviewed H1 2026 original signed Note41: 890,796,892 VND opening cash reclassification exactly explained, 0 VND adjusted bridge; Q2 standalone remains deferred pending current-period accounting-basis comparator")
