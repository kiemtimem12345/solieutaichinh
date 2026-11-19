#!/usr/bin/env python3
"""PLX Q3 issuer-signed limited-data check (do not infer absent B01/B02/B03)."""
import json
from decimal import Decimal
from pathlib import Path
obj=json.loads((Path(__file__).resolve().parents[1]/"data/financials-PLX.json").read_text(encoding="utf-8"))
q=[r for r in obj["items"] if r["period"]=="2026-Q3"]
assert len(q)==2, "Missing or duplicate PLX Q3 report scope"
expected={"consolidated":Decimal("1363096.640781"),"parent_company":Decimal("1315029.909162")}
signed_source={"consolidated":1363096640781,"parent_company":1315029909162}
for r in q:
 scope=r["source_validation"]["scope"]
 assert scope in expected and Decimal(str(r["net_profit"]))==expected[scope]
 assert r["source_validation"]["reported_vnd"]==signed_source[scope]
 assert int(expected[scope]*Decimal(1000000))==signed_source[scope], "VND to million conversion"
 assert r["financial_line_items_extracted_fields"]==["net_profit"]
 assert not r["source_validation"]["full_b01_b02_b03_visual_reviewed"]
 assert not any(isinstance(r.get(x),(int,float)) for x in
                ("revenue","gross_profit","total_assets","cash_ending",
                 "operating_cash_flow","pretax_profit","net_profit_attributable"))
assert {r["source_validation"]["scope"] for r in q}==set(expected)
previous=next(r for r in obj["items"] if r["period"]=="2025-Q3" and "hợp nhất" in r["report_type"].lower())
prev_issuer=Decimal("705970.238434")
assert abs(Decimal(str(previous["net_profit"]))-prev_issuer)/prev_issuer*100<=Decimal("0.01")
print("PASS: PLX 2026-Q3 parent/consolidated precise LNST from official issuer statement; no unsupported numeric fields")
