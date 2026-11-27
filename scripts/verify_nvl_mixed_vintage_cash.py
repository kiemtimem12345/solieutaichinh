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

# Q4 source credit must not be silently turned into a deduction.
credit = rows["2025-Q4"]
assert v(credit,"cost_of_goods_sold") == 1015177327509
assert v(credit,"revenue") + v(credit,"cost_of_goods_sold") == v(credit,"gross_profit")
assert credit["source_validation"]["q4_source_review"]["positive_cogs_note"]
assert "preserveSourceCredit" in js and "!preserveSourceCredit" in js
print("NVL verified positive COGS data and UI guard source anchors passed")

# All in-scope summaries: exact VND identities, explicit quarterly ratio basis.
assert list(sorted(rows)) == ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"]
for period,row in rows.items():
    assert v(row,"total_assets") == v(row,"total_liabilities") + v(row,"equity"), period
    assert v(row,"current_assets") + v(row,"non_current_assets") == v(row,"total_assets"), period
    assert v(row,"revenue") + v(row,"cost_of_goods_sold") == v(row,"gross_profit"), period
    assert sum(v(row,k) for k in ("operating_cash_flow","investing_cash_flow","financing_cash_flow")) == v(row,"net_cash_change"), period
    adj = v(row,"cash_opening_basis_adjustment") if row.get("cash_opening_basis_adjustment") is not None else 0
    assert v(row,"cash_beginning") + v(row,"net_cash_change") + v(row,"exchange_rate_effect_on_cash") + adj == v(row,"cash_ending"), period
    assert v(row,"cash_and_equivalents") == v(row,"cash_ending"), period
    if period != "2025-Q1":
        assert row["source_validation"]["source_bytes_sha256_pending"] is False
        assert len(row["source_validation"]["original_quarter_sha256"]) == 64
        for metric,average in (("roa","average_total_assets"),("roe","average_equity")):
            assert abs(row[metric] - row["net_profit"]*400/row[average]) < Decimal("0.000000001"), (period,metric)
print("NVL seven-period summary identities and derived ratio checks passed")
