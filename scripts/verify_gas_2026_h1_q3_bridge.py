#!/usr/bin/env python3
"""Trace GAS 2026 first-half earnings ambiguity using Q3's 9M B02 original.

This does not amend any individual quarters. It verifies the later Q3 PDF
corroborates H1 YTD and isolates the 10,160,150,278 VND contradiction between
published standalone Q1+Q2 and reported H1 cost of goods sold/profit.
"""
import json
from decimal import Decimal
from pathlib import Path

data=json.loads((Path(__file__).resolve().parents[1]/"data/financials-GAS.json").read_text("utf-8"))
def report(period):
    rows=[r for r in data["items"] if r["period"]==period and "hợp nhất" in r.get("report_type","").lower()]
    assert len(rows)==1, (period,len(rows))
    return rows[0]
q1,q2,q3=(report(x) for x in ("2026-Q1","2026-Q2","2026-Q3"))
def V(obj,key):
    return int((Decimal(str(obj[key]))*Decimal(1000000)).to_integral_exact())

evidence=q2["source_validation"]["reviewed_h1_version_comparison"]["q3_source_nine_month_consistency"]
assert evidence["report_scope"].startswith("GAS BCTC hợp nhất Q3/2026")
assert "vietstock.vn" in evidence["mirror_url"]
assert evidence["profit_allocation_to_one_quarter_unresolved"] is True
assert evidence["q2_implied_numbers_are_hypothetical"] is True
assert evidence["nine_month_minus_q3_matches_published_h1_for_total_profit"] is True
assert q3["verification_status"]=="verified_manual_visual_reconciliation"
assert q1["verification_status"].startswith("issuer_original_pdf_visual_verified")
assert q2["verification_status"].startswith("issuer_original_pdf_visual_verified")

NINE={
    "revenue":120977138230990,
    "cost_of_goods_sold":102456747387133,
    "gross_profit":18520390843857,
    "pretax_profit":16980511052183,
    "net_profit":13594648848851,
    "net_profit_attributable":13381162041937,
    "non_controlling_interest_profit":213486806914,
    "income_tax_current":3391122703113,
    "income_tax_deferred":-5260499781,
}
H1={
    "revenue":81268744982957,
    "cost_of_goods_sold":68967158848778,
    "gross_profit":12301586134179,
    "pretax_profit":11207899960622,
    "net_profit":9025674760340,
    "net_profit_attributable":8804699596334,
    "non_controlling_interest_profit":220975164006,
    "income_tax_current":2189801309370,
    "income_tax_deferred":-7576109088,
}
EXPECTED_H1_MINUS_Q1_Q2={
    "revenue":0,
    "cost_of_goods_sold":-10160150278,
    "gross_profit":10160150278,
    "pretax_profit":10160150278,
    "net_profit":10160150278,
    "net_profit_attributable":10160150278,
    "non_controlling_interest_profit":0,
    "income_tax_current":0,
    "income_tax_deferred":0,
}
EXPECTED_9M_MINUS_Q3_MINUS_H1={
    "revenue":0,"cost_of_goods_sold":0,"gross_profit":0,
    "pretax_profit":0,"net_profit":0,
    "net_profit_attributable":-1,
    "non_controlling_interest_profit":1,
    "income_tax_current":0,"income_tax_deferred":0,
}
assert set(NINE)==set(H1)==set(evidence["b02_vnd_by_metric"])
for k in NINE:
    z=evidence["b02_vnd_by_metric"][k]
    current_q3=V(q3,"net_profit_non_controlling_interests" if k=="non_controlling_interest_profit" else k)
    assert int(z["nine_month_ytd_vnd"])==NINE[k], k
    assert int(z["originally_published_h1_vnd"])==H1[k], k
    assert int(z["q3_standalone_vnd"])==current_q3, k
    assert int(z["implied_h1_from_nine_minus_q3_vnd"])==NINE[k]-current_q3, k
    assert int(z["original_q1_plus_q2_vnd"])==V(q1,k)+V(q2,k), k
    assert int(z["nine_month_implied_h1_minus_published_h1_vnd"])==EXPECTED_9M_MINUS_Q3_MINUS_H1[k], k
    assert int(z["published_h1_minus_original_quarters_vnd"])==EXPECTED_H1_MINUS_Q1_Q2[k], k
    assert int(z["q2_if_q1_unchanged_vnd"])==H1[k]-V(q1,k), k
    assert int(z["q2_if_q1_unchanged_minus_original_q2_vnd"])==EXPECTED_H1_MINUS_Q1_Q2[k], k
assert H1["revenue"]-H1["cost_of_goods_sold"]==H1["gross_profit"]
assert NINE["revenue"]-NINE["cost_of_goods_sold"]==NINE["gross_profit"]
assert H1["net_profit_attributable"]+H1["non_controlling_interest_profit"]==H1["net_profit"]
assert NINE["net_profit_attributable"]+NINE["non_controlling_interest_profit"]==NINE["net_profit"]
assert H1["pretax_profit"]-H1["income_tax_current"]-H1["income_tax_deferred"]==H1["net_profit"]
assert NINE["pretax_profit"]-NINE["income_tax_current"]-NINE["income_tax_deferred"]==NINE["net_profit"]
assert V(q2,"cost_of_goods_sold")==35465901292563
assert V(q1,"cost_of_goods_sold")==33511417706493
assert V(q2,"pretax_profit")==7443056154493
assert V(q1,"pretax_profit")==3754683655851
print("PASS: GAS 2026 B02 Q3 9M minus Q3 agrees with published H1 for 9 fields (only +/-1 VND NCI split); standalone Q1+Q2 disagree with H1 by exact 10,160,150,278 VND in COGS/profit, original quarters unchanged")
