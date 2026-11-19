#!/usr/bin/env python3
"""Prove deploy/data contains source-controlled JSON byte-for-byte.

Protect completed VDS/GEG/GAS and other tickers from rollback to the
2026-11-18 restore ZIP when future FTPS deployments are manually triggered.
"""
from hashlib import sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"data"
staged=ROOT/"deploy"/"data"
expected=sorted(source.glob("*.json"))
produced=sorted(staged.glob("*.json"))
assert len(expected)==len(produced)==41
assert len([x for x in expected if x.name.startswith("financials-")])==32
assert [p.name for p in expected]==[p.name for p in produced]
for a,b in zip(expected,produced):
    actual=a.read_bytes()
    uploaded=b.read_bytes()
    assert sha256(actual).digest()==sha256(uploaded).digest(),a.name
    assert actual==uploaded,a.name
    json.loads(uploaded)
geg=json.loads((staged/"financials-GEG.json").read_text(encoding="utf-8"))
vds=json.loads((staged/"financials-VDS.json").read_text(encoding="utf-8"))
g={r["period"]:r for r in geg["items"] if "hợp nhất" in r.get("report_type","").lower()}
v={r["period"]:r for r in vds["items"]}
assert g["2025-Q4"]["verification_status"].startswith("issuer_signed_original_visual_verified_B01_B02_B03_FY")
assert g["2025-Q4"]["source_validation"]["manually_visual_reviewed"] is True
assert g["2025-Q4"]["operating_cash_flow_ytd"] == 932884.327033
assert g["2026-Q1"]["source_validation"]["manually_visual_reviewed"] is True
assert g["2026-Q2"]["source_validation"]["manually_visual_reviewed"] is True
assert all(v[p]["source_validation"]["manually_visual_reviewed"] is True for p in ("2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1","2026-Q2","2026-Q3"))
assert all("data" == p.parent.name for p in produced)
print("PASS: 41 staged JSON byte-identical to Git data; includes latest issuer-verified GEG/VDS; no archive rollback possible")
