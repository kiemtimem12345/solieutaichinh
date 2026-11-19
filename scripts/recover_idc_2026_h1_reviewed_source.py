#!/usr/bin/env python3
"""Read-only HNX-disclosed IDC 2026 reviewed consolidated H1 source recovery.

BSC preserves HNX attached files (7 Sep 2026). The report is NOT merged
into production; pages need visual review before any changed financial figure.
No SSL bypass, no inferred values, strict PDF/mime/size checks.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import hashlib, json, re
import fitz

SOURCES=[
 ("BSC_HNX_attachment_1","https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1"),
 ("BSC_HNX_attachment_3","https://www.bsc.com.vn/News/NewsAttachedFile/1599258-3"),
 ("BSC_HNX_attachment_2","https://www.bsc.com.vn/News/NewsAttachedFile/1599258-2"),
]
HOSTS={"www.bsc.com.vn","bsc.com.vn","files.bsc.com.vn"}
LIMIT=45*1024*1024
out=Path("idc-2026h1-original-audit")
out.mkdir(parents=True, exist_ok=True)
report={"purpose":"IDC H1 2026 consolidated HNX original B03 opening comparison with Q1/FY2025","results":[],"findings":[]}
for label,url in SOURCES:
 try:
  req=Request(url,headers={"User-Agent":"Mozilla/5.0 (BCTC SourceReview/1.0)","Accept":"application/pdf,application/octet-stream,*/*","Accept-Encoding":"identity","Referer":"https://www.bsc.com.vn/"})
  with urlopen(req,timeout=65) as resp:
   u=urlparse(resp.geturl())
   if u.scheme!="https" or u.hostname not in HOSTS:raise ValueError("Unexpected host redirect "+str(u.hostname))
   payload=resp.read(LIMIT+1)
  if not payload.startswith(b"%PDF") or not 40000<len(payload)<LIMIT:raise ValueError("Not a bounded PDF attachment")
  pdf=fitz.open(stream=payload,filetype="pdf")
  if not 12<=len(pdf)<=210:raise ValueError("Unexpected PDF page count "+str(len(pdf)))
  meta={"label":label,"url":url,"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"pages":len(pdf),"page_text":[]}
  print("SOURCE_OK",json.dumps({k:v for k,v in meta.items() if k!="page_text"},ensure_ascii=False),flush=True)
  for i in range(min(27,len(pdf))):
   p=pdf[i]
   t=p.get_text(sort=True)
   if i<22 or any(w in t.lower() for w in ("lưu chuyển tiền","cash flows","553.943","553,943")):
    if 5<=i<22:
     im=p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
     im.save(out/f"{label}-page-{i+1:02d}.png")
    print(f"PAGE_BEGIN {label} {i+1} text_length={len(t)}",flush=True)
    print(t[:5500] if len(t)>40 else "SCANNED_IMAGE_REVIEW_REQUIRED",flush=True)
    print("PAGE_END",flush=True)
   meta["page_text"].append({"page":i+1,"chars":len(t),"cash_tokens":re.findall(r"(?:553[., ](?:943|052)[., ]\d{3}[., ]\d{3})",t)[:10]})
  report["results"].append(meta)
 except Exception as exc:
  print(f"SOURCE_UNAVAILABLE {label} {type(exc).__name__}: {str(exc)[:200]}",flush=True)
  report["results"].append({"label":label,"url":url,"error":type(exc).__name__,"message":str(exc)[:300]})
(out/"audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
if not any(x.get("pages",0)>12 for x in report["results"]):
 raise RuntimeError("No HNX original PDF recovered; no source-vintage conclusion authorized")
print("AUDIT_SOURCE_RECOVERED_NOT_PRODUCTION_PASS: check original consolidated issuer/scope and B03 source page images",flush=True)
