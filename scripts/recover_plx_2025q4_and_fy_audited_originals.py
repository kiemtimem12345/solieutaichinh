#!/usr/bin/env python3
"""Recover complete PLX consolidated Q4 2025 and audited FY2025 signed originals.

Use exact public Vietstock eDocuments original issuer PDF URLs. This script is
READ-ONLY; does not modify production financial JSON, never infers quarterly
cash before signed 12M and 9M source-vintage comparison. Strict curl success,
PDF footer/structure and SHA256; reject %PDF prefix partial downloads.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse
import hashlib,json,subprocess
import fitz

DIR=Path("plx-2025q4-annual-original")
DIR.mkdir(exist_ok=True)
sources={
"Q4_2025_CONSOLIDATED_SOURCE":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/PLX_Baocaotaichinh_Q4_2025_Hopnhat.pdf",
"FY2025_AUDITED_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/NAM/PLX_Baocaotaichinh_2025_Kiemtoan_Hopnhat.pdf",
}
def recover(pair):
 label,url=pair
 assert urlparse(url).hostname=="static2.vietstock.vn"
 dst=DIR/label;dst.mkdir(exist_ok=True)
 pdf=dst/"full_signed_original.pdf"
 args=["curl","--fail","--location","--silent","--show-error",
       "--connect-timeout","12","--max-time","115","--max-filesize","90000000",
       "--output",str(pdf),"--write-out","%{http_code} %{size_download} %{url_effective}",
       "--header","User-Agent: Mozilla/5.0 (OriginalFinancialSourceQA/1.0)",url]
 info={"label":label,"url":url,"status":"download_unverified"}
 try:
  p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=121)
  info.update({"curl_rc":p.returncode,"transfer":p.stdout[:320],"stderr":p.stderr[:250]})
  if p.returncode!=0:raise ValueError("incomplete or HTTP source failed")
  raw=pdf.read_bytes()
  if not 100000<len(raw)<90000000 or not raw.startswith(b"%PDF"):raise ValueError("invalid complete PDF signature/bytes")
  doc=fitz.open(str(pdf))
  if not 8<=len(doc)<=260:raise ValueError("invalid page count")
  info.update({"status":"full_pdf_recovered_pending_visual_source_qa","sha256":hashlib.sha256(raw).hexdigest(),
               "bytes":len(raw),"pages":len(doc),"page_text_lengths":[]})
  # Save legible full-size source scans for manual visual comparison; Q4 p2-9
  # and audited FY starts with KPMG opinion / statements later in first 25p.
  for i in range(min(len(doc),26)):
   page=doc[i]
   scan=page.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
   scan.save(dst/f"page-{i+1:02d}.png")
   txt=page.get_text(sort=True)
   info["page_text_lengths"].append(len(txt))
   print("SOURCE_PAGE",label,i+1,"text_chars",len(txt),flush=True)
   if txt and i<17:print("TEXT_SAMPLE",label,i+1,txt[:1800].replace("\n"," | "),flush=True)
  doc.close()
  print("ORIGINAL_SOURCE_COMPLETE",json.dumps({k:v for k,v in info.items() if k!="page_text_lengths"},ensure_ascii=False),flush=True)
 except Exception as e:
  info.update({"status":"source_blocked_or_partial_discarded","error":repr(e)[:300]})
  pdf.unlink(missing_ok=True)
  print("SOURCE_BLOCKED",json.dumps(info,ensure_ascii=False),flush=True)
 return info

with ThreadPoolExecutor(max_workers=2) as pool:
 result=list(pool.map(recover,sources.items()))
(DIR/"source_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SOURCE_STATUS",sum(x["status"].startswith("full_pdf") for x in result),"/",len(result),flush=True)
if not any(x["status"].startswith("full_pdf") for x in result):
 raise RuntimeError("No signed PLX FY2025 or Q4 original available, retain existing unverified JSON.")
