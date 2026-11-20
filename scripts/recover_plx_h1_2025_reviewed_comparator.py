#!/usr/bin/env python3
"""Recover PLX 2025 H1 *reviewed* consolidated original as same-vintage comparator.

Do not reinterpret signed Q3 2025 standalone quarter amounts from 9M less the
earlier unsigned/signed pre-review H1 without explicit issuer restatement.
Official mirror URL was returned in 2025 Vietstock Finance eDocuments API.
"""
from pathlib import Path
import hashlib, json, subprocess
import fitz

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/PLX_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf"
OUT=Path("plx-2025-h1-reviewed-original")
OUT.mkdir(exist_ok=True)
DEST=OUT/"H1-reviewed-original.pdf"
p=subprocess.run(["curl","--fail","--location","--silent","--show-error","--connect-timeout","12","--max-time","110",
   "--max-filesize","36000000","--output",str(DEST),"--write-out","%{http_code} %{size_download} %{url_effective}",
   "--header","User-Agent: Mozilla/5.0 (IssuerFinancialSourceQA/1.0)",URL],
   capture_output=True,text=True,timeout=117)
rec={"url":URL,"curl_code":p.returncode,"http_bytes":p.stdout[:400],"stderr":p.stderr[:300],"status":"incomplete_or_unavailable"}
if p.returncode==0 and DEST.exists():
 raw=DEST.read_bytes()
 if len(raw)>100000 and raw.startswith(b"%PDF"):
  try:
   doc=fitz.open(str(DEST))
   if not 12<=len(doc)<=130:raise ValueError("Unexpected PDF pages")
   rec.update({"status":"complete_original_pending_manual_visual","sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"pages":len(doc)})
   for idx in range(min(22,len(doc))):
    pg=doc[idx]
    pg.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(OUT/f"page-{idx+1:02d}.png")
    txt=pg.get_text(sort=True)
    print(f"REVIEWED_SOURCE_PAGE {idx+1} text_chars={len(txt)}",flush=True)
    if len(txt)>100:print(txt[:2400],flush=True)
   doc.close()
  except Exception as exc:
   rec["error"]=repr(exc)
if rec["status"]!="complete_original_pending_manual_visual":
 DEST.unlink(missing_ok=True)
 print("REVIEWED_SOURCE_UNAVAILABLE",json.dumps(rec),flush=True)
(OUT/"audit.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
if rec["status"]=="complete_original_pending_manual_visual":
 print("REVIEWED_SOURCE_OK",json.dumps(rec,ensure_ascii=False),flush=True)
else:raise RuntimeError("No full H1 2025 consolidated reviewed original recovered")
