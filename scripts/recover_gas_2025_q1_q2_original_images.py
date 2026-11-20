#!/usr/bin/env python3
"""Read-only issuer-signed GAS consolidated Q1/Q2 2025 source visual recovery.

Preserve existing validated figures and archival source edition. No financial
JSON changes here. Fetch exact URLs referenced in data/financials-GAS.json,
verify full PDF, SHA256, render source pages, never treat partial %PDF as valid.
"""
import hashlib,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import fitz

out=Path("gas-q1-q2-2025-original-sources")
out.mkdir(exist_ok=True)
items={
 "GAS_2025_Q1_CONSOLIDATED":"https://static2.vietstock.vn/vietstock/2025/4/29/20250429_20240429___gas___cbtt_bctc_q1_2025_hop_nhat.pdf",
 "GAS_2025_Q2_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/GAS_Baocaotaichinh_Q2_2025_Hopnhat.pdf",
}
def fetch(item):
 label,url=item
 assert urlparse(url).hostname=="static2.vietstock.vn"
 folder=out/label;folder.mkdir(exist_ok=True)
 dst=folder/"issuer_source.pdf"
 cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","12","--max-time","72","--max-filesize","35000000","--output",str(dst),"--write-out","%{http_code} %{size_download} %{url_effective}","--header","User-Agent: Mozilla/5.0 (source-visual-reconciliation/1.0)",url]
 a={"label":label,"url":url}
 try:
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=78)
  a.update({"curl_rc":p.returncode,"transfer":p.stdout[:300],"error":p.stderr[:300]})
  if p.returncode!=0:raise ValueError("download incomplete / HTTP error")
  raw=dst.read_bytes()
  if not 50000<len(raw)<35000000 or not raw.startswith(b"%PDF"):raise ValueError("invalid complete PDF")
  pdf=fitz.open(str(dst))
  if not 8<=len(pdf)<=160:raise ValueError("unexpected page count")
  a.update({"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"pages":len(pdf),"source_status":"recovered_pending_visual"})
  for i in range(min(23,len(pdf))):
   page=pdf[i];pic=page.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False)
   pic.save(folder/f"page-{i+1:02d}.png")
   txt=page.get_text(sort=True)
   print("PAGE",label,i+1,"text_length",len(txt),flush=True)
   if 20<len(txt)<22000:print(txt[:3000],flush=True)
  pdf.close()
  print("SOURCE_OK",json.dumps(a),flush=True)
 except Exception as e:
  dst.unlink(missing_ok=True)
  a.update({"source_status":"blocked_or_invalid","failure":str(e)[:300]})
  print("SOURCE_FAILED",json.dumps(a),flush=True)
 return a
with ThreadPoolExecutor(max_workers=2) as ex:
 results=list(ex.map(fetch,items.items()))
(out/"audit.json").write_text(json.dumps({"results":results},indent=2)+"\n")
print("RESULT complete",sum(x["source_status"]=="recovered_pending_visual" for x in results),"/",len(results),flush=True)
if not any(x["source_status"]=="recovered_pending_visual" for x in results):
 raise RuntimeError("Neither original GAS BCTC PDF was fully retrievable")
