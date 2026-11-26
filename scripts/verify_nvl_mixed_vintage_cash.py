"""Regression gate for explicit mixed-vintage cash presentation (million VND storage)."""
import json
from decimal import Decimal
from pathlib import Path

def v(row, key):
    return int((Decimal(str(row[key])) * 1000000).to_integral_exact())

def validate(q, p):
    assert q["cashflow_period_basis"] == "quarter_derived_mixed_vintage_explicit_adjustment"
    assert q["cashflow_comparability"] == "mixed_vintage_not_like_for_like"
    assert q["source_validation"]["standalone_cash_status"] == "user_approved_mixed_vintage_derived_presentation"
    for key in ("operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "net_cash_change", "exchange_rate_effect_on_cash"):
        assert v(q,key) == v(q,key+"_ytd") - v(p,key), key
    assert v(q,"cash_opening_basis_adjustment") == v(q,"cash_beginning_reported_ytd") - v(p,"cash_beginning")
    assert v(q,"cash_beginning") == v(p,"cash_ending")
    assert sum(v(q,k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow")) == v(q,"net_cash_change")
    assert sum(v(q,k) for k in ("cash_beginning","net_cash_change","exchange_rate_effect_on_cash","cash_opening_basis_adjustment")) == v(q,"cash_ending")
    assert v(q,"cash_ending") == v(q,"cash_ending_ytd") == v(q,"cash_and_equivalents")

rows={x["period"]:x for x in json.loads(Path("data/financials-NVL.json").read_text(),parse_float=Decimal)["items"]}
q,p=rows["2026-Q2"],rows["2026-Q1"]
validate(q,p)
for key in ("cash_opening_basis_adjustment","operating_cash_flow","investing_cash_flow","financing_cash_flow","net_cash_change","exchange_rate_effect_on_cash","cash_beginning","cash_ending","cash_and_equivalents"):
    bad=dict(q)
    bad[key]=Decimal(str(q[key]))+Decimal("0.000001")
    try:
        validate(bad,p)
    except AssertionError:
        continue
    raise AssertionError("tamper accepted: "+key)
js=Path("assets/app.js").read_text()
assert "Điều chỉnh cơ sở trình bày (không phải dòng tiền)" in js
assert "exchange_rate_effect_on_cash_ytd" in js
assert "không hoàn toàn cùng cơ sở so sánh" in js
print("NVL mixed-vintage exact cash identities and nine one-VND tamper guards passed; UI source anchors present")
