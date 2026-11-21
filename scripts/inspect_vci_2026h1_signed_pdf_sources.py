#!/usr/bin/env python3
"""Evidence-only VCI original Q2 and reviewed H1 2026 PDF recovery.

Run in disposable GitHub Ubuntu runner. Does not distribute or commit
copyrighted PDFs, write financial JSON, use OCR, or assert verified data
if a source could not be obtained.
"""
import hashlib
import re
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

SOURCES = [
    ("VCI_2026Q2_HOSE_original", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2480835/20260720%20-%20VCI%20-%20BCTC%20Q2.2026-CBTT.pdf"),
    ("VCI_2026H1_HOSE_reviewed", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2488911/20260813%20-%20VCI%20-%20BCTC%206T%20nam%202026%20-%20CBTT.pdf"),
    ("VCI_2026Q2_Vietstock_mirror", "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf"),
]
MAX_BYTES=45*1024*1024
NEEDLES=[
    "lưu chuyển tiền thuần từ hoạt động kinh doanh",
    "lưu chuyển tiền thuần từ hoạt động đầu tư",
    "lưu chuyển tiền thuần từ hoạt động tài chính",
    "tiền và các khoản tương đương tiền đầu kỳ",
    "tiền và các khoản tương đương tiền cuối kỳ",
    "tăng/giảm tiền thuần trong kỳ",
    "không có công ty con",
]
def get(url,path):
    error=""
    for i in range(2):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (VCI financial source review)","Accept":"application/pdf,application/octet-stream,*/*"})
            with urllib.request.urlopen(req,timeout=22) as response:
                total=0
                with path.open("wb") as o:
                    while True:
                        chunk=response.read(1024*1024)
                        if not chunk:break
                        total+=len(chunk)
                        if total>MAX_BYTES:raise ValueError("size cap")
                        o.write(chunk)
            if path.open("rb").read(5)!=b"%PDF-":raise ValueError("not PDF magic")
            return total
        except Exception as exc:
            error=f"{type(exc).__name__}: {str(exc)[:170]}"
            print("ATTEMPT_FAILED",i+1,error,flush=True)
            time.sleep(1)
    raise RuntimeError(error)

def inspect(name,url,path):
    print("\n=== ORIGINAL_SOURCE",name,"===",flush=True)
    try:
        size=get(url,path)
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        print("SOURCE_PDF",name,"bytes",size,"SHA256",sha,flush=True)
        info=subprocess.run(["pdfinfo",str(path)],capture_output=True,text=True,timeout=20)
        pages=next((int(v.partition(":")[2].strip()) for v in info.stdout.splitlines() if v.startswith("Pages:")),0)
        print("PAGES",pages,flush=True)
        if not pages or pages>160:raise ValueError("invalid pages")
        proc=subprocess.run(["pdftotext","-layout",str(path),"-"],capture_output=True,text=True,timeout=65,errors="replace")
        if proc.returncode:
            print("TEXT_EXTRACTION_UNAVAILABLE",proc.stderr[:200],flush=True)
            return
        pages_text=proc.stdout.split("\f")
        print("SEARCHABLE_CHARS",len(proc.stdout),flush=True)
        printed=0
        for pageno,text in enumerate(pages_text[:pages],1):
            lines=text.splitlines()
            for line in lines:
                clean=re.sub(r"\s+"," ",line).strip().lower()
                if any(term in clean for term in NEEDLES):
                    print("SOURCE_ROW_PAGE",pageno,re.sub(r"\s+"," ",line.strip())[:210],flush=True)
                    printed+=1
                    if printed>=22:break
            if printed>=22:break
        if not printed:print("NO_RELEVANT_SEARCHABLE_ROWS; scanned pages require targeted manual images",flush=True)
    except Exception as exc:
        print("SOURCE_NOT_RETRIEVED",name,type(exc).__name__,str(exc)[:250],flush=True)

def main():
    with tempfile.TemporaryDirectory() as temp:
        for i,(name,url) in enumerate(SOURCES):
            inspect(name,url,Path(temp)/f"vci_{i}.pdf")
    print("FINISHED evidence only, no production site changes",flush=True)
if __name__=="__main__":main()
