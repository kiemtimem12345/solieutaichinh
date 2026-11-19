#!/usr/bin/env python3
"""Read-only capture of VDS reviewed H1/2025 consolidated issuer original.

Purpose: decide if the 1,117,693,283 VND parent/NCI attribution discrepancy
in 2025 Q1+Q2 original B02 versus original H1 YTD is retrospective
reclassification. Never writes canonical numbers from unverified OCR.
"""
import hashlib,re,subprocess,sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,urlopen
import fitz
URL="https://www.vdsc.com.vn/data/api/app/file-storage/6d34c594-a07c-4fc9-88a1-08ddd9f82764/VDSC_Cong%20bo%20BCTC%20hop%20nhat%20ban%20nien%202025%20da%20soat%20xet.pdf?downloadFrom=ManagementDocument-921"
CAP=45*1024*1024
req=Request(URL,headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.vdsc.com.vn/","Accept":"application/pdf,*/*"})
with urlopen(req,timeout=70) as resp:
  final=urlparse(resp.url)
  if final.scheme!="https" or final.hostname not in ("www.vdsc.com.vn","vdsc.com.vn"):
    raise ValueError("Issuer redirect not allowed")
  data=bytearray()
  while True:
    c=resp.read(1024*1024)
    if not c:break
    data.extend(c)
    if len(data)>CAP: raise ValueError("PDF exceeds download cap")
if not data.startswith(b"%PDF"):raise ValueError("Issuer response is not PDF")
doc=fitz.open(stream=data,filetype="pdf")
print("ISSUER_REVIEWED_SOURCE_OK bytes=%d pages=%d sha256=%s"%(len(data),len(doc),hashlib.sha256(data).hexdigest()),flush=True)
out=Path("vds-2025-h1-reviewed-pages");out.mkdir(exist_ok=True)
for ix in range(3,min(len(doc),43)):
   p=doc[ix]
   raw=p.get_text(sort=True)
   pix=p.get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
   dest=out/("vds-reviewed-h1-pdfpage-%02d.png"%(ix+1))
   pix.save(dest)
   if len(raw.strip())>400 and len(re.findall(r"\d",raw))>=25:
     text,method=raw,"pdf_text"
   else:
     r=subprocess.run(["tesseract",str(dest),"stdout","-l","eng","--psm","6"],capture_output=True,text=True,timeout=50,check=True)
     text,method=r.stdout,"ocr_unverified"
   matches=("KET QUA" in text.upper() or "KET QUA" in text.upper().replace("Ế","E") or "DOANH THU" in text.upper() or "RECLASS" in text.upper())
   print("PDF_PAGE page=%d extraction=%s chars=%d candidate=%s"%(ix+1,method,len(text),matches),flush=True)
   if matches:print("PAGE_TEXT_UNVERIFIED_BEGIN %d\n%s\nPAGE_TEXT_UNVERIFIED_END %d"%(ix+1,text[:11500],ix+1),flush=True)
print("REVIEWED_H1_RENDER_COMPLETE; source image validation required before publication",flush=True)
