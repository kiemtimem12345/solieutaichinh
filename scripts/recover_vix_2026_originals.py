#!/usr/bin/env python3
"""Retrieve three VIX issuer-signed original reports for financial statement validation.

Read-only source recovery. No data mutation or OCR: source PDF + page render
will be inspected before any field is marked verified.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, hashlib, json
import fitz

ROOT=Path("vix-2026-original-sources")
ROOT.mkdir(exist_ok=True)
URLS={
 "2026-Q1":"https://vixs.vn/wp-content/uploads/2026/04/20260417-VIX-BAO-CAO-TAI-CHINH-QUY-I-2026.pdf",
 "2026-Q2":"https://vixs.vn/wp-content/uploads/2026/07/20260717-VIX-Bao-cao-tai-chinh-Quy-2-nam-2026.pdf",
 "2026-Q3":"https://vixs.vn/wp-content/uploads/2026/10/20261019-VIX-Baocaotaichinh-Quy-3-nam-2026.pdf",
}
def fetch(entry):
 period,url=entry
 dest=ROOT/f"VIX-{period}-issuer-original.pdf"
 args=["curl","-L","-f","-s","-S","--connect-timeout","12","--max-time","115",
       "--retry","1","--retry-delay","2","--max-filesize","80000000",
       "-H","User-Agent: Mozilla/5.0 (source-validation/1.0)",
       "-w","HTTP=%{http_code} SIZE=%{size_download}","-o",str(dest),url]
 try:
  p=subprocess.run(args,text=True,capture_output=True,timeout=132)
  info={"period":period,"url":url,"curl_rc":p.returncode,"transport":p.stdout,"stderr":p.stderr[:360]}
  if p.returncode==0 and dest.is_file() and dest.stat().st_size>150000 and dest.read_bytes()[:4]==b"%PDF":
   doc=fitz.open(dest)
   info.update({"status":"complete","sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
                "bytes":dest.stat().st_size,"pages":len(doc),
                "first_20_pages_text_chars":[len(doc[i].get_text()) for i in range(min(20,len(doc)))],
                "page_first_lines":[(i+1," ".join(doc[i].get_text().split()[:18])) for i in range(min(20,len(doc))) if doc[i].get_text().strip()]})
   doc.close()
  else:
   info["status"]="blocked"
   dest.unlink(missing_ok=True)
  return info
 except Exception as e:
  dest.unlink(missing_ok=True)
  return {"period":period,"url":url,"status":"exception","error":str(e)[:350]}
with ThreadPoolExecutor(max_workers=3) as ex:
 reports=list(ex.map(fetch,URLS.items()))
for item in reports:print("ISSUER_SOURCE",json.dumps(item,ensure_ascii=False),flush=True)
(ROOT/"audit.json").write_text(json.dumps(reports,indent=2,ensure_ascii=False)+"\n")
if not all(i["status"]=="complete" for i in reports):
 raise RuntimeError("One or more signed originals inaccessible; no financial PASS allowed")
print("ALL_THREE_ORIGINALS_VERIFIED",flush=True)
