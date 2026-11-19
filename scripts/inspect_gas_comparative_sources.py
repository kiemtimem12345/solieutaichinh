#!/usr/bin/env python3
"""Read-only audit source comparison of GAS 2025 audited and 2026 H1 reviewed.

Outputs bounded original issuer source page images and/or original text on a
short-lived GitHub Actions runner. Does not modify JSON, website or backups.
"""
import hashlib, os, re, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import fitz

DOCS={
 "2025-AUDITED": "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14454&documentid=3253&moduleid=648&portalid=0",
 "2026-H1-REVIEWED": "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14606&documentid=3375&moduleid=648&portalid=0",
}
CAP=25*1024*1024

def read_original(url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; GASSourceQA/1.0)","Referer":"https://www.pvgas.com.vn/","Accept":"application/pdf,application/octet-stream,*/*"})
    with urlopen(req,timeout=55) as res:
        redirect=urlparse(res.url)
        if redirect.scheme!="https" or redirect.hostname not in ("www.pvgas.com.vn","pvgas.com.vn"):
            raise ValueError("Untrusted redirect")
        if int(res.headers.get("Content-Length") or "0")>CAP:raise ValueError("File too large")
        body=bytearray()
        while True:
            c=res.read(1024*1024)
            if not c:break
            body.extend(c)
            if len(body)>CAP:raise ValueError("File too large")
    if not body.startswith(b"%PDF"):raise ValueError("No PDF signature")
    print(f"SOURCE_OK bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}",flush=True)
    return fitz.open(stream=body,filetype="pdf")

def main():
    label=os.environ.get("GAS_SOURCE","")
    if label not in DOCS:raise ValueError("Unknown source")
    doc=read_original(DOCS[label])
    print(f"PDF_OK label={label} pages={len(doc)}",flush=True)
    out=Path("source-pages");out.mkdir(exist_ok=True)
    # Financial statements near beginning; preserve report page images for visual QA.
    for i in range(2,min(len(doc),14)):
        p=doc[i]
        txt=p.get_text(sort=True)
        img=p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
        dest=out/f"gas-{label.lower()}-page-{i+1:02d}.png";img.save(dest)
        if len(txt.strip())<300 or len(re.findall(r"\d",txt))<20:
            x=subprocess.run(["tesseract",str(dest),"stdout","-l","eng","--psm","6"],capture_output=True,text=True,timeout=45,check=True)
            method="ocr_unverified";txt=x.stdout
        else:method="source_text"
        print(f"REPORT_PAGE_BEGIN source={label} page={i+1} method={method}",flush=True)
        print(txt[:9000],flush=True)
        print(f"REPORT_PAGE_END source={label} page={i+1}",flush=True)
    print("DONE original source read-only. Review scanned image before asserting values",flush=True)

if __name__=="__main__":sys.exit(main() or 0)
