#!/usr/bin/env python3
"""GAS audited FY2025 vs Q4 original and H1-reviewed 2026 vs Q2 original.

Guard source-version comparisons, preserve historic quarter values, and
require independent exact-VND identities in both reviewed and original forms.
"""
import json
from decimal import Decimal
from pathlib import Path

p=Path(__file__).resolve().parents[1]/"data"/"financials-GAS.json"
items={r["period"]:r for r in json.loads(p.read_text("utf-8"))["items"]}
q4,q1,q2=items["2025-Q4"],items["2026-Q1"],items["2026-Q2"]
def v(r,k):return int((Decimal(str(r[k]))*Decimal(1000000)).to_integral_exact())
audit=q4["source_validation"]["audit_version_comparison"]
assert v(q4,"total_assets")==93531511866676
assert int(audit["audited_total_assets_vnd"])==93568198109790
assert int(audit["total_assets_delta_vnd"])==36686243114
assert int(audit["liabilities_delta_vnd"])==36686243113
assert int(audit["cash_delta_vnd"])==0
review=q2["source_validation"]["reviewed_h1_version_comparison"]
src={k:int(x) for k,x in review["reviewed_h1_values_vnd"].items()}
diffs={k:int(x) for k,x in review["reviewed_minus_original_q2_report_vnd"].items()}
assert len(src)==len(diffs)==11
assert all(src[k]-v(q2,k)==diffs[k] for k in src)
assert src["total_assets"]-src["total_liabilities"]-src["equity"]==0
assert sum(src[k] for k in ("operating_cash_flow_ytd","investing_cash_flow_ytd","financing_cash_flow_ytd"))==src["net_cash_change_ytd"]
assert src["cash_beginning_reported_ytd"]+src["net_cash_change_ytd"]+src["foreign_exchange_effect_ytd"]==src["cash_ending"]
assert src["cash_ending"]==v(q2,"cash_ending")==11055638145352
assert diffs["total_assets"]==-15937434327
assert diffs["operating_cash_flow_ytd"]==-583226264264
assert diffs["investing_cash_flow_ytd"]==594377512732
assert diffs["financing_cash_flow_ytd"]==194684448
assert diffs["net_cash_change_ytd"]==11345932916
assert diffs["foreign_exchange_effect_ytd"]==-11361467163
assert diffs["cash_beginning_reported_ytd"]==15534247
assert diffs["cf_pretax"]==-11034262367
assert v(q2,"operating_cash_flow_ytd")==7038604357979
assert v(q1,"pretax_profit")==3754683655851
assert v(q2,"pretax_profit")==7443056154493
assert 11207899960622-v(q1,"pretax_profit")-v(q2,"pretax_profit")==10160150278
assert review["reviewed_h1_b03_pretax_matches_b02"] is True
assert review["evidence_status"].endswith("quarterly_reallocation_unresolved")
print("PASS: GAS audit 2025 + 2026 reviewed H1 source-version differences; audited 36.686bn, review cashflow reclassification and original quarter histories protected")
