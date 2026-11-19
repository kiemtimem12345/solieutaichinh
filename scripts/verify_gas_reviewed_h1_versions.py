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
# Enforce exact issuer-audited FY2025 B03 source figures and protect original Q4 vintage.
audited = audit["audited_b03_values_vnd"]
original = audit["original_q4_report_b03_values_vnd"]
delta = audit["audited_minus_original_b03_delta_vnd"]
keys = ["operating_cash_flow_ytd", "investing_cash_flow_ytd", "financing_cash_flow_ytd",
        "net_cash_change_ytd", "foreign_exchange_effect_ytd", "cash_beginning_reported_ytd",
        "cash_ending", "capital_expenditure_ytd", "dividends_paid_ytd"]
assert set(keys) == set(audited) == set(original) == set(delta)
assert int(audited["operating_cash_flow_ytd"]) == 13040237870138
assert int(audited["investing_cash_flow_ytd"]) == -6468619501015
assert int(audited["financing_cash_flow_ytd"]) == -5264541765224
assert int(audited["net_cash_change_ytd"]) == 1307076603899
assert int(audited["foreign_exchange_effect_ytd"]) == 1408246718
for key in keys:
    assert int(original[key]) == v(q4, key), ("original-vintage-protection", key)
    assert int(audited[key]) - int(original[key]) == int(delta[key]), ("audit-delta", key)
assert len(audit["audited_b03_exact_identity_residuals_vnd"]) == 6
assert all(x == "0" for x in audit["audited_b03_exact_identity_residuals_vnd"].values())
assert (int(audited["operating_cash_flow_ytd"])+int(audited["investing_cash_flow_ytd"])
        +int(audited["financing_cash_flow_ytd"]) == int(audited["net_cash_change_ytd"]))
assert (int(audited["cash_beginning_reported_ytd"])+int(audited["net_cash_change_ytd"])
        +int(audited["foreign_exchange_effect_ytd"]) == int(audited["cash_ending"]))
assert int(delta["net_cash_change_ytd"])+int(delta["foreign_exchange_effect_ytd"]) == 0
assert int(delta["operating_cash_flow_ytd"]) == -338136507224
assert int(delta["investing_cash_flow_ytd"]) == 249924365177
assert int(delta["financing_cash_flow_ytd"]) == 87620645762

# Reviewed H1 source B01 should reconcile at each asset/debt class and not overwrite Q2.
classes = review["reviewed_b01_classes_vnd"]
assert len(classes) == 9
assert int(classes["current_assets"]) + int(classes["non_current_assets"]) == src["total_assets"]
assert int(classes["current_liabilities"]) + int(classes["long_term_liabilities"]) == src["total_liabilities"]
assert sum(int(classes[k]) for k in ("cash_and_equivalents", "short_term_investments",
                                      "short_term_receivables", "inventory",
                                      "other_current_assets")) == int(classes["current_assets"])
assert all(x == "0" for x in review["reviewed_b01_exact_check_residuals_vnd"].values())
assert int(classes["cash_and_equivalents"]) == v(q2, "cash_and_equivalents")
assert int(audit["audited_b01_component_deltas_vnd"]["equity"]) == 1
assert sum(int(audit["audited_b01_component_deltas_vnd"][k]) for k in
           ("short_term_receivables", "inventory", "other_current_assets")) == 41048624111

print("PASS: GAS audited FY2025 B03 6 exact source/delta checks; reviewed H1 B01 3 class checks; original quarter observations retained")
print("PASS: GAS audit 2025 + 2026 reviewed H1 source-version differences; audited 36.686bn, review cashflow reclassification and original quarter histories protected")
