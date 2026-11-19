#!/usr/bin/env python3
"""Inspect publicly filed GEG consolidated Q1/2026 original PDF without writing data.

Run only on ephemeral GitHub Actions runner: guard file size/redirect, preserve
only statement-page PNG previews for human visual review, print bounded original
text. OCR is unverified supporting text, never a source of canonical financials.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import fitz

SOURCES=[
 ("HOSE", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2458785/20260429%20-%20GEG%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%20Q1.2026%20%2B%20giai%20trinh%20%28song%20ngu%29.pdf"),
 ("VIETSTOCK", "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/GEG_Baocaotaichinh_Q1_2026_Hopnhat.pdf"),
]
HOSTS={"staticfile.hsx.vn","static2.vietstock.vn"}
MAX_BYTES=45*1024*1024


def read_pdf(name,url):
    request=Request(url,headers={
       "User-Agent":"Mozilla/5.0 (compatible; OriginalFinancialStatementQA/1.0)",
       "Accept":"application/pdf,application/octet-stream,*/*",
       "Referer":"https://www.hsx.vn/",
    })
    with urlopen(request,timeout=35) as resp:
        final=urlparse(resp.url)
        if final.scheme!="https" or final.hostname not in HOSTS:
            raise ValueError("Disallowed redirect")
        if int(resp.headers.get("Content-Length") or "0")>MAX_BYTES:
            raise ValueError("PDF exceeds cap")
        parts=[];size=0
        while True:
            b=resp.read(1024*1024)
            if not b:break
            size+=len(b)
            if size>MAX_BYTES:raise ValueError("PDF exceeds cap")
            parts.append(b)
    body=b"".join(parts)
    if not body.startswith(b"%PDF"):raise ValueError("Not a PDF")
    print(f"SOURCE_OK name={name} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}",flush=True)
    return body


def inspect(blob,name):
    doc=fitz.open(stream=blob,filetype="pdf")
    print(f"PDF_OK source={name} total_pages={len(doc)}",flush=True)
    out=Path("geg-q1-renders");out.mkdir(exist_ok=True)
    for ix in range(0,min(len(doc),24)):
        page=doc[ix]
        txt=page.get_text(sort=True)
        pix=page.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False)
        target=out/f"geg-2026-q1-page-{ix+1:02d}.png"
        pix.save(target)
        if len(txt.strip())>350 and len(re.findall(r"\d",txt))>=25:
            method="pdf_text"
        else:
            got=subprocess.run(
              ["tesseract",str(target),"stdout","-l","eng","--psm","6","-c","preserve_interword_spaces=1"],
              capture_output=True,text=True,check=True,timeout=55)
            txt=got.stdout
            method="ocr_unverified"
        print(f"REPORT_PAGE_BEGIN page={ix+1} method={method} chars={len(txt)}",flush=True)
        print(txt[:12500],flush=True)
        print(f"REPORT_PAGE_END page={ix+1}",flush=True)
    print("SOURCE_RENDER_PASS: images are authoritative, OCR text remains unverified",flush=True)


def main():
    for name,url in SOURCES:
        try:
            inspect(read_pdf(name,url),name)
            return 0
        except Exception as error:
            print(f"SOURCE_UNAVAILABLE name={name} error={type(error).__name__} message={str(error)[:180]}",flush=True)
    print("::error::GEG consolidated 2026-Q1 official PDF unavailable from published endpoints",flush=True)
    return 1


if __name__=="__main__":
    sys.exit(main())
