#!/usr/bin/env python3
"""Recover TPB Q3/2025 issuer-signed original B02a/B03a/B04a (source-only).

Consolidated signed Q3 cash is nine-month YTD. Standalone Q3 CFO/CFI/CFF
will be derived from this original 9M and already-verified KPMG H1 source.
All earlier TPB 2025Q1 and 2025Q2 checkpoint values remain immutable.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/TPB_Baocaotaichinh_Q3_2025_Hopnhat.pdf"
OUT=Path("tpb-2025q3-original-evidence")

def cmd(args,timeout):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
    if p.returncode:
        raise RuntimeError(f"{args[0]} exit={p.returncode} stderr={p.stderr[:230]}")
    return p.stdout

def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        pdf=Path(td)/"TPB-2025Q3-original.pdf"
        response=cmd(["curl","--location","--silent","--show-error",
            "--connect-timeout","15","--max-time","110",
            "--speed-time","18","--speed-limit","4096",
            "--max-filesize",str(55*1024*1024),"--user-agent","Mozilla/5.0",
            "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL],125)
        assert response.startswith("200"),response
        assert pdf.exists() and pdf.stat().st_size>60000, "PDF truncated or missing"
        with pdf.open("rb") as f:
            assert f.read(5)==b"%PDF-", "HTML or invalid file rather than original"
        info=cmd(["pdfinfo",str(pdf)],40)
        found=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
        assert found, "Original page count missing"
        pages=int(found.group(1))
        assert 15<=pages<=160,pages
        sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
        print(f"TPB_Q3_SIGNED_SOURCE sha256={sha} bytes={pdf.stat().st_size} pages={pages} url={URL}",flush=True)
        first,last=4,min(17,pages)
        txt=cmd(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],95)
        print(f"TPB_Q3_TEXT_LAYER chars={len(txt)}",flush=True)
        if txt.strip():
            (OUT/"TPB-2025Q3-statement-layer.txt").write_text(txt[:75000],"utf-8")
        cmd(["pdftoppm","-f",str(first),"-l",str(last),
             "-scale-to","1550","-jpeg","-jpegopt","quality=70",
             str(pdf),str(OUT/"TPB-2025Q3-HN")],190)
        n=len(list(OUT.glob("TPB-2025Q3-HN-*.jpg")))
        assert n==last-first+1,(n,last-first+1)
        print(f"PASS TPB_Q3_ORIGINAL_PDF_REVIEW_SOURCE rendered={n}, no financial data yet changed",flush=True)

if __name__=="__main__":
    main()
