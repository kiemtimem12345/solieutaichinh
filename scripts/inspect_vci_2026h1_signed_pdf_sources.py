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
from pathlib import Path

SOURCES = [
    ("VCI_2026H1_Vietstock_republished", "https://static2.vietstock.vn/vietstock/2026/8/14/20260813___vci___bctc_6t_nam_2026___cbtt_2.pdf"),
    ("VCI_2026H1_HOSE_reviewed", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2488911/20260813%20-%20VCI%20-%20BCTC%206T%20nam%202026%20-%20CBTT.pdf"),
    ("VCI_2026Q2_Vietstock_mirror", "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCI_Baocaotaichinh_Q2_2026_1.pdf"),
    ("VCI_2026Q2_HOSE_original", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2480835/20260720%20-%20VCI%20-%20BCTC%20Q2.2026-CBTT.pdf"),
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
    """Hard wall-clock per source. Avoid urllib socket timeouts on trickling 17MB PDFs."""
    command = [
        "curl", "--location", "--silent", "--show-error", "--fail",
        "--max-time", "80", "--connect-timeout", "12",
        "--speed-limit", "8192", "--speed-time", "16",
        "--max-filesize", str(MAX_BYTES),
        "--user-agent", "Mozilla/5.0 (financial-source-evidence-only)",
        "--header", "Accept: application/pdf,application/octet-stream",
        "--output", str(path), url,
    ]
    result = subprocess.run(command, text=True, capture_output=True, timeout=92)
    if result.returncode:
        raise RuntimeError(f"curl_exit={result.returncode} {result.stderr.strip()[:180]}")
    size = path.stat().st_size
    if not 0 < size <= MAX_BYTES or path.open("rb").read(5) != b"%PDF-":
        raise ValueError(f"Invalid PDF or source response; bytes={size}")
    return size

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
            return False
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
        if not printed:
            print("NO_RELEVANT_SEARCHABLE_ROWS; scanned pages require targeted manual images",flush=True)
            return False
        return True
    except Exception as exc:
        print("SOURCE_NOT_RETRIEVED",name,type(exc).__name__,str(exc)[:250],flush=True)
        return False

def main():
    evidence = {}
    with tempfile.TemporaryDirectory() as temp:
        for i, (name, url) in enumerate(SOURCES):
            if "2026H1" in name and any(v for k, v in evidence.items() if "2026H1" in k):
                print("SKIP_DUPLICATE_H1_SOURCE", name, flush=True)
                continue
            if "2026Q2" in name and any(v for k, v in evidence.items() if "2026Q2" in k):
                print("SKIP_DUPLICATE_Q2_SOURCE", name, flush=True)
                continue
            evidence[name] = inspect(name, url, Path(temp)/f"vci_{i}.pdf")
    h1 = any(v for k, v in evidence.items() if "2026H1" in k)
    q2 = any(v for k, v in evidence.items() if "2026Q2" in k)
    print("EVIDENCE_STATUS", "H1", h1, "Q2", q2, flush=True)
    print("FINISHED evidence only; no financial JSON or production changes", flush=True)
    if not (h1 and q2):
        raise SystemExit("INCOMPLETE_SOURCE_EVIDENCE: H1 plus Q2 original required; fail closed")
if __name__ == "__main__": main()
