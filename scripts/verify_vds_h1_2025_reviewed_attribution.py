#!/usr/bin/env python3
"""VDS H1/2025 reviewed B02 parent/NCI source-vintage QA, exact VND.

Prevents any auto-correction of issuer originally published Q1/Q2 B02 columns
using an unallocated H1 YTD parent/NCI difference.
"""
import json
from decimal import Decimal
from pathlib import Path
d=json.loads((Path(__file__).resolve().parents[1]/"data/financials-VDS.json").read_text("utf-8"))
records={r["period"]:r for r in d["items"]}
a,h=records["2025-Q1"],records["2025-Q2"]
def V(row,k):return int((Decimal(str(row[k]))*Decimal(1000000)).to_integral_exact())
s=h["source_validation"]["reviewed_h1_2025_consolidated_vintage"]
assert s["original_pdf_sha256"]=="75de6381cdb92812422c264f9d4729e69e5bf7c31c852b77d60c0052140ac57f"
assert s["original_pdf_bytes"]==9476053 and s["original_pdf_pages_total"]==84
assert s["visually_reviewed_original_pdf_pages"]==[20,21,22]
assert s["no_quarterly_adjustment_without_issuer_evidence"] is True
assert s["verification_status"]=="confirmed_source_originals_not_resolved_per_quarter_allocation"
review=s["b02_H1_reviewed_source_vnd"]
expected={
"revenue":349950141337,
"operating_expense":273327926577,
"operating_profit":5189063536,
"pretax_profit":5201163732,
"income_tax":-2617272857,
"net_profit":7818436589,
"parent_attributable_profit":8071151977,
"non_controlling_profit":-252715388}
assert set(review)==set(expected)
for k,n in expected.items():assert int(review[k])==n,k
checks={
 "h1_income_profit":int(review["net_profit"])-int(review["pretax_profit"])+int(review["income_tax"]),
 "h1_parent_nci":int(review["net_profit"])-int(review["parent_attributable_profit"])-int(review["non_controlling_profit"]),
 "quarter_sum_net":V(a,"net_profit")+V(h,"net_profit")-int(review["net_profit"]),
 "quarter_parent_variance":V(a,"net_profit_attributable")+V(h,"net_profit_attributable")-int(review["parent_attributable_profit"]),
 "quarter_nci_variance":V(a,"non_controlling_interest_profit")+V(h,"non_controlling_interest_profit")-int(review["non_controlling_profit"]),
 "prior_H1_same_parent":V(h,"net_profit_attributable_ytd")-int(review["parent_attributable_profit"]),
 "prior_H1_same_nci":V(h,"non_controlling_interest_profit_ytd")-int(review["non_controlling_profit"]),
 "prior_H1_same_revenue":V(h,"revenue_ytd")-int(review["revenue"]),
 "prior_H1_same_pretax":V(h,"pretax_profit_ytd")-int(review["pretax_profit"]),
 "prior_H1_same_net":V(h,"net_profit_ytd")-int(review["net_profit"]),
}
assert len(checks)==10
assert checks["quarter_parent_variance"]==1117693283
assert checks["quarter_nci_variance"]==-1117693283
assert sum((checks["quarter_parent_variance"],checks["quarter_nci_variance"]))==0
assert all(x==0 for k,x in checks.items() if k not in ("quarter_parent_variance","quarter_nci_variance"))
assert {k:str(n) for k,n in checks.items()}==s["reviewed_H1_exact_identity_checks_vnd"]
assert V(a,"net_profit_attributable")==19089097924
assert V(h,"net_profit_attributable")==-9900252664
assert V(a,"non_controlling_interest_profit")==-76755668
assert V(h,"non_controlling_interest_profit")==-1293653003
assert a["source_validation"]["manually_visual_reviewed"] is True
assert h["source_validation"]["manually_visual_reviewed"] is True
print("PASS: VDS original signed Q1/Q2 standalone plus reviewed H1 issuer B02; parent/NCI 1,117,693,283 VND offset exactly, consolidated net stable; quarter originals untouched")
