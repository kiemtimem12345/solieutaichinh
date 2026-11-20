#!/usr/bin/env python3
"""Recover *complete* PLX original Q3 consolidated and reviewed H1 PDFs from
Vietstock public eDocuments, with original sources linked by signed HOSE filing.

Candidate URLs were returned 20 Nov 2026 by the public PLX eDocuments API,
not guessed from filenames. Every download is time-bounded; reject partial PDF
even if it begins %PDF. This source-recovery job does NOT publish data or mark
B01/B02/B03 PASS; exact VND and scope need subsequent visual source checks.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse
import hashlib, json, subprocess
import fitz

OUT=Path("plx-2026-original-mirrors")
OUT.mkdir(exist_ok=True)
SOURCES={
 "PLX_Q3_2026_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2026_Hopnhat.pdf",
 "PLX_H1_2026_REVIEWED_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/PLX_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf?ver=39c44c02",
 "PLX_H1_2026_REVIEWED_PARENT":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/PLX_Baocaotaichinh_6T_2026_Soatxet_Congtyme.pdf?ver=412f8829",
}
CAP=35*1024*1024
def one(entry):
 label,url=entry
 assert urlparse(url).hostname=="static2.vietstock.vn"
 folder=OUT/label;folder.mkdir(exist_ok=True)
 payload_file=folder/"mirrored_issuer_original.pdf"
 cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","12",
   "--max-time","75","--max-filesize",str(CAP),"--output",str(payload_file),
   "--write-out","%{http_code} %{size_download} %{url_effective}",
   "--header","Accept: application/pdf,application/octet-stream,*/*",
   "--header","User-Agent: Mozilla/5.0 (compatible; OriginalFinancialReportQA/1.0)",url]
 entry={"label":label,"original_vietstock_document_api_url":url}
 try:
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=82)
  entry.update({"curl_exit_code":p.returncode,"http_transfer":p.stdout[:500],"curl_stderr":p.stderr[:450]})
  if p.returncode!=0:
   payload_file.unlink(missing_ok=True)
   entry["status"]="unavailable_or_partial_pdf_discarded"
   print("SOURCE_INCOMPLETE",label,json.dumps(entry,ensure_ascii=False),flush=True)
   return entry
  raw=payload_file.read_bytes()
  if not 70000<len(raw)<CAP or not raw.startswith(b"%PDF"):
   raise ValueError("bad length or signature of downloaded full file")
  pdf=fitz.open(str(payload_file))
  if not 12<=len(pdf)<=260:raise ValueError("unexpected original PDF page count "+str(len(pdf)))
  entry.update({"status":"complete_pdf_recovered_pending_source_visual_QA","sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"pages":len(pdf)})
  for i in range(min(20,len(pdf))):
   page=pdf[i]
   # use low/moderate size to keep artifact bounded
   pimage=page.get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
   pimage.save(folder/f"page-{i+1:02d}.png")
   text=page.get_text(sort=True)
   if i<18:
    print(f"PAGE {label} {i+1} textchars={len(text)}",flush=True)
    if len(text)>20:print(text[:1100],flush=True)
  pdf.close()
  print("SOURCE_OK",json.dumps(entry,ensure_ascii=False),flush=True)
  return entry
 except Exception as exc:
  entry.update({"status":"unavailable_or_invalid","error_type":type(exc).__name__,"error":str(exc)[:300]})
  payload_file.unlink(missing_ok=True)
  print("SOURCE_UNAVAILABLE",json.dumps(entry,ensure_ascii=False),flush=True)
  return entry
with ThreadPoolExecutor(max_workers=3) as ex:
 data=list(ex.map(one,SOURCES.items()))
(OUT/"source-audit.json").write_text(json.dumps({"workflow":"issuer original Vietstock eDocument direct","results":data},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
n=sum(x.get("status")=="complete_pdf_recovered_pending_source_visual_QA" for x in data)
print(f"RECOVERY_SUMMARY {n}/{len(data)} complete issuer-original mirror PDFs retrieved; needs visual B01/B02/B03 same-scope verification",flush=True)
if not n:raise RuntimeError("All three exact Vietstock issuer PDF retrievals failed; keep production block")
