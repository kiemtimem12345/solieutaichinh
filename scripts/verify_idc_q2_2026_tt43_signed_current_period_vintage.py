#!/usr/bin/env python3
"""IDC 2026 Q2 signed Q1 vs reviewed H1 TT99/TT43 presentation-vintage gate.

Issuer original Q1 66p note2.5 pdf page17 first TT99; reviewed H1 72p
B09a note3.1 page21 explicitly applies TT43 consolidated guidance and Note41
page71 changes 2025 comparative B01 and B03 (NOT 2026 Q1 current B03).
Do not add retrospective 2025 comparatives to 2026 quarterly CFO/CFI/CFF.
"""
import json
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
AUDIT=R/"reports/source-audits/IDC-2026Q1-vs-H1-TT43-source-policy-and-Note41-B03-comparatives.json"
FIN=R/"data/financials-IDC.json"
def v(row,k):
 x=row.get(k)
 assert type(x) in (int,float),(k,x)
 return int(Decimal(str(x))*Decimal(1000000))
def source_check(a):
 assert a["ticker"]=="IDC" and a["scope"]=="consolidated" and a["period"]=="2026-Q2"
 assert a["Q1_original"]["sha256"]=="229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b"
 assert a["Q1_original"]["policy_note_page"]==17 and a["Q1_original"]["pdf_pages"]==66
 assert a["H1_reviewed"]["sha256"]=="f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944"
 assert a["H1_reviewed"]["pdf_pages"]==72 and a["H1_reviewed"]["policy_page"]==21
 assert a["H1_reviewed"]["note41_page"]==71
 d=a["signed_note41"]["prior_2025_B03_comparative_reclassification_items_vnd"]
 assert d["depreciation_and_amortization"]=="-141514712612"
 assert d["decrease_inventory"]=="-25335127650"
 assert d["increase_receivables"]=="-331959067818"
 assert d["interest_paid"]=="-27028341934"
 assert d["cash_paid_capex"]=="525837250014"
 assert sum(map(int,d.values()))==0
 assert a["signed_note41"]["prior_2025_B03_comparative_reclassification_total_vnd"]=="0"
 assert a["signed_note41"]["opening_cash_equivalents_2025_prior_reclass_vnd"]=="890796892"
 for k in ("Q1_signed_TT99_2025","H1_signed_TT99_and_TT43","prior_B03_reclass_cannot_be_transferred_into_2026_flow","Q2_standalone_CFO_CFI_CFF_null_required"):
  assert a["decision"][k] is True,k
 assert a["decision"]["signed_same_vintage_Q1_2026_current_period_TT43_comparator_found"] is False
 return d
def main():
 a=json.loads(AUDIT.read_text("utf-8"))
 d=json.loads(FIN.read_text("utf-8"))
 src=source_check(a)
 rows={x["period"]:x for x in d["items"]}
 q,h=rows["2026-Q1"],rows["2026-Q2"]
 for r in (q,h):
  x=r["source_validation"]
  assert x["q1_vs_h1_TT43_source_policy_audit"]==str(AUDIT.relative_to(R))
  assert x["Q1_signed_Q1_2026_TT99_adoption_confirmed"] is True
  assert x["H1_signed_2026_TT43_adoption_confirmed"] is True
  assert x["H1_note41_prior_year_B03_reclassification_net_vnd"]=="0"
  assert x["H1_note41_B03_prior_year_reclass_does_not_restate_Q1_2026_current_period"] is True
  assert x["Q1_2026_TT43_same_current_period_original_comparator_unverified"] is True
  assert x["IDC_Q2_2026_standalone_cashflow_promotion_blocked_current_basis"] is True
  assert x["issuer_Q1_2026_signed_restated_TT43_B03_not_yet_recovered"] is True
 assert h["source_validation"]["q2_cashflow_quarter_status"].endswith("TT43_not_documented")
 for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","cash_beginning","capital_expenditure","foreign_exchange_effect","dividends_paid"):
  assert h[k] is None,(k,h[k])
 assert h["cashflow_period_basis"]=="year_to_date"
 assert v(q,"cash_ending")==800729495703
 assert v(h,"cash_ending")==608684579632
 assert v(q,"cash_beginning_reported_ytd")==553052678239
 assert v(h,"cash_beginning_reported_ytd")==553943475131
 assert v(h,"operating_cash_flow_ytd")==-5019037910
 assert v(q,"operating_cash_flow_ytd")==197524137001
 assert h["source_validation"]["q2_cashflow_bridge_adjusted_by_disclosed_reclassification_vnd"]=="0"
 # Fail closed: 2025 prior B03 reclassification tampering cannot authorize quarter publication.
 bad=json.loads(json.dumps(a));bad["signed_note41"]["prior_2025_B03_comparative_reclassification_items_vnd"]["cash_paid_capex"]="525837250013"
 try:source_check(bad)
 except AssertionError:pass
 else:raise AssertionError("Incorrect Note41 prior-period cashflow reclass was accepted")
 print("PASS IDC 2026 Q1 original TT99 note2.5 vs H1 reviewed TT43 note3.1; "
       "Note41 B03 reclassifies 2025 comparative 5 signed items net 0 VND and "
       "cash opening +890,796,892; NOT evidence of 2026Q1 current-period TT43 "
       "re-statement; Q2 quarterly CFO/CFI/CFF remain source-blocked.")
if __name__=="__main__":main()
