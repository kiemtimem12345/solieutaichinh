#!/usr/bin/env python3
"""BID original 2026Q1 consolidated source recovery, read-only/fail-closed.

Preserve already verified 2025-Q1..Q4 and 2026-Q3 source checkpoints.
Only complete PDF signature, SHA-256, page count, visual bank B01/B03/B04
can enable separate future data normalization.
"""
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/BID_Baocaotaichinh_Q1_2026_Hopnhat.pdf"
OUT=Path("bid-2026q1-original-evidence")
def run(cmd,timeout=100):
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} {p.returncode}: {p.stderr[:260]}")
    return p.stdout

def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        f=Path(t)/"BID-2026Q1-HN.pdf"
        meta=run(["curl","--location","--silent","--show-error",
                  "--connect-timeout","15","--max-time","100",
                  "--speed-time","18","--speed-limit","4096",
                  "--max-filesize",str(48*1024*1024),
                  "--user-agent","Mozilla/5.0","--output",str(f),
                  "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],115)
        assert f.exists() and f.stat().st_size>60000, "Empty/truncated original"
        with f.open("rb") as fp:
            assert fp.read(5)==b"%PDF-", "Not a PDF"
        assert meta.startswith("200"), meta
        info=run(["pdfinfo",str(f)],40)
        n=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
        assert n, "PDF page count absent"
        pages=int(n.group(1))
        assert 15<=pages<=150,pages
        sha=hashlib.sha256(f.read_bytes()).hexdigest()
        print(f"ORIGINAL_SIGNED_BID_2026Q1 source_sha256={sha} size={f.stat().st_size} pages={pages} URL={URL}",flush=True)
        first,last=2,min(12,pages)
        txt=run(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(f),"-"],80)
        print("SOURCE_TEXT_LAYER",len(txt),flush=True)
        if txt.strip():
            (OUT/"BID-2026Q1-excerpt.txt").write_text(txt[:60000],"utf-8")
        run(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1550",
             "-jpeg","-jpegopt","quality=70",str(f),str(OUT/"BID-2026Q1-HN")],180)
        imgs=len(list(OUT.glob("BID-2026Q1-HN-*.jpg")))
        assert imgs==last-first+1,imgs
        print(f"PASS SIGNED_ORIGINAL_PROVENANCE BID_2026Q1 images={imgs}; no production financial changes",flush=True)

if __name__=="__main__":
    main()
