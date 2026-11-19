#!/usr/bin/env python3
"""Retrieve GAS original public consolidated Q3/2025 PDF, inspect B01/B02/B03 read-only.

Runs on a GitHub Actions ephemeral runner. Never commits PDF, writes to Hostinger
or touches stored financial figures; prints source page text for accounting
cross-checks and caps transfer volume and printed output.
"""
import io, re, sys, unicodedata
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import fitz

SOURCES=[
 ("issuer", "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14381&documentid=3214&moduleid=648&portalid=0"),
 ("vietstock", "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/GAS_Baocaotaichinh_Q3_2025_Hopnhat.pdf"),
]
ALLOWED_HOSTS={"www.pvgas.com.vn","pvgas.com.vn","static2.vietstock.vn"}
MAX_BYTES=22*1024*1024

def norm(text):
    text=unicodedata.normalize("NFD",text).lower()
    return "".join(c for c in text if not unicodedata.combining(c))

def load_url(name,url):
    req=Request(url,headers={
      "User-Agent":"Mozilla/5.0 (compatible; FinancialStatementSourceQA/1.0)",
      "Accept":"application/pdf,*/*",
      "Referer":"https://www.pvgas.com.vn/",
    })
    with urlopen(req,timeout=35) as resp:
        host=urlparse(resp.url).hostname
        typ=resp.headers.get("Content-Type","").split(";")[0]
        if host not in ALLOWED_HOSTS:
            raise ValueError(f"Redirected to unexpected host {host}")
        chunks=[];size=0
        while True:
            b=resp.read(1024*1024)
            if not b:break
            size+=len(b)
            if size>MAX_BYTES:
                raise ValueError("PDF exceeds guarded download cap")
            chunks.append(b)
    body=b"".join(chunks)
    print(f"SOURCE_CHECK: {name}, bytes={len(body)}, MIME={typ}, pdf_signature={body.startswith(b'%PDF')}",flush=True)
    if not body.startswith(b"%PDF"):
        raise ValueError("PDF not accessible from this endpoint")
    return body

def inspect(body,source):
    doc=fitz.open(stream=body,filetype="pdf")
    print(f"PASS: public GAS Q3 2025 PDF opened, pages={len(doc)}, source={source}",flush=True)
    heads=[]
    for i in range(min(16,len(doc))):
        t=doc[i].get_text(sort=True)
        n=norm(t)
        if "bang can doi ke toan" in n or "bao cao ket qua" in n or "bao cao luu chuyen tien te" in n:
            kind="B01" if "bang can doi ke toan" in n else "B02" if "bao cao ket qua" in n else "B03"
            heads.append((i,kind))
    if not heads:
        print("::warning::No extractable B01/B02/B03 text headers in first 16 pages (possible scanned PDF)",flush=True)
        for i in range(min(10,len(doc))):
            print(f"TEXT_SUMMARY: pdf_page={i+1}, text_chars={len(doc[i].get_text())}",flush=True)
        return 1
    seen=set()
    for i,kind in heads:
        if (i,kind) in seen:continue
        seen.add((i,kind))
        # Entire matching report pages up to 10,500 characters each.
        t=doc[i].get_text(sort=True)
        print(f"REPORT_PAGE_BEGIN page={i+1} kind={kind} text_chars={len(t)}",flush=True)
        print(t[:10500],flush=True)
        print(f"REPORT_PAGE_END page={i+1}",flush=True)
    return 0

def main():
    for name,url in SOURCES:
        try:
            data=load_url(name,url)
            return inspect(data,name)
        except Exception as exc:
            print(f"SOURCE_UNAVAILABLE: {name}; error={type(exc).__name__}; msg={str(exc)[:140]}",flush=True)
    print("::error::Unable to retrieve original GAS Q3/2025 consolidated PDF through either known official/indexed URL",flush=True)
    return 1

if __name__=="__main__":sys.exit(main())
