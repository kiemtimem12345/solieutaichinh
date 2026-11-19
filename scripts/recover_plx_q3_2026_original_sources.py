#!/usr/bin/env python3
"""Read-only recovery of exact PLX Q3/2026 parent signed B03 original only.

Exact issuer/HOSE financial reports ONLY. No numeric production changes.
The B03 printed CFF differs from sum of its component rows by VND 87,654,015,000;
images of original pages distinguish signed-printing inconsistencies from OCR.
Never use a subsidiary's report or silently correct original values.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import fitz

SOURCES=[
 ("PLX_Q3_2026_PARENT_ISSUER","https://files.petrolimex.com.vn/files/6783dc1271ff449e95b74a9520964169/application%3Dpdf/5011693c3c5240a0833bfaea0e7983a5/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20m%E1%BA%B9%20Q3%20nam%202026.pdf"),
]
HOSTS={"files.petrolimex.com.vn","staticfile.hsx.vn"}
CAP=38*1024*1024
OUT=Path("plx-q3-2026-original-source-qa")
OUT.mkdir(parents=True,exist_ok=True)
report={"task":"PLX Q3/2026 parent printed B03 financing subtotal mismatch 87654015000 VND","sources":[]}
for label,url in SOURCES:
 item={"label":label,"original_url":url,"source_status":"unavailable"}
 try:
  req=Request(url,headers={
   "User-Agent":"Mozilla/5.0 (compatible; OriginalIssuerFinancialQA/1.0)",
   "Accept":"application/pdf,application/octet-stream,*/*",
   "Accept-Encoding":"identity",
   "Referer":"https://www.petrolimex.com.vn/" if "petrolimex" in url else "https://www.hsx.vn/",
  })
  with urlopen(req,timeout=65) as resp:
   final=urlparse(resp.geturl())
   if final.scheme!="https" or final.hostname not in HOSTS:
    raise ValueError("redirect outside official issuer/exchange hosts: "+str(final.hostname))
   payload=resp.read(CAP+1)
  if len(payload)>CAP or len(payload)<30000 or not payload.startswith(b"%PDF"):
   raise ValueError("download not bounded original PDF")
  pdf=fitz.open(stream=payload,filetype="pdf")
  if not 5<=len(pdf)<=250:raise ValueError("Implausible original PDF page count")
  item.update({"source_status":"retrieved_pdf_pending_visual_identity_check","final_url":final.geturl(),
   "size_bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"pdf_pages":len(pdf)})
  target=OUT/label
  target.mkdir(exist_ok=True)
  # Source hash + image pages are ephemeral CI artifact, not persisted in Git.
  # Preserve exact PDF for original-image review if transport allowed.
  (target/"signed-source.pdf").write_bytes(payload)
  for i in range(min(len(pdf),19)):
   page=pdf[i]
   pic=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
   path=target/f"pdf-page-{i+1:02d}.png"
   pic.save(path)
   raw=page.get_text(sort=True)
   print(f"PAGE {label} {i+1} textchars={len(raw)} image={path}",flush=True)
   if raw.strip():print(raw[:4000],flush=True)
  print("SOURCE_OK",json.dumps({k:v for k,v in item.items() if k!="original_url"},ensure_ascii=False),flush=True)
 except Exception as exc:
  item.update({"error_type":type(exc).__name__,"error_message":str(exc)[:350]})
  print(f"SOURCE_UNAVAILABLE {label} cause={type(exc).__name__} {str(exc)[:250]}",flush=True)
 report["sources"].append(item)
(OUT/"source-audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("RESULT",json.dumps({i["label"]:i["source_status"] for i in report["sources"]},ensure_ascii=False),flush=True)
if not any(i["source_status"]=="retrieved_pdf_pending_visual_identity_check" for i in report["sources"]):
 raise RuntimeError("All exact official PLX PDFs unavailable through runner. Original B03 remains blocked; no guessed figures.")
