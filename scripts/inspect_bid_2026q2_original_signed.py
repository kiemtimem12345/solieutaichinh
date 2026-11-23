#!/usr/bin/env python3
"""Read-only source provenance for BID Q2/2026 original consolidated PDF.

Reviewed consolidated 2026 H1 bank statements were already source-verified
in BID Q3/2026 PR #146, SHA 3c3f6c39..., 57 pages. Only recover original
Q2 here; do not repeat old completed source extraction or substitute
reviewed H1 B01/B03 current-quarter figures for first-issued Q2.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/BID_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=1cd27481"
OUT=Path("bid-2026q2-original-evidence")

def exec_bound(cmd,limit=130):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=limit,check=False)
 if p.returncode:raise RuntimeError(f"{cmd[0]} exit={p.returncode}: {p.stderr[:200]}")
 return p.stdout

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as d:
  pdf=Path(d)/"BID-2026Q2-HN.pdf"
  r=exec_bound([
    "curl","--location","--silent","--show-error",
    "--connect-timeout","14","--max-time","105",
    "--speed-time","16","--speed-limit","4096",
    "--max-filesize",str(55*1024*1024),
    "--user-agent","Mozilla/5.0",
    "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL
  ],120)
  assert r.startswith("200"),r
  assert pdf.exists() and pdf.stat().st_size>60000,"Truncated original PDF"
  with pdf.open("rb") as f:assert f.read(5)==b"%PDF-", "Invalid PDF signature"
  meta=exec_bound(["pdfinfo",str(pdf)],45)
  match=re.search(r"^Pages:\s*(\d+)\s*$",meta,re.M)
  assert match,"PDF page count not accessible"
  pages=int(match.group(1))
  assert 15<=pages<=180,pages
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"ORIGINAL_SIGNED_BID_2026Q2 sha256={sha} bytes={pdf.stat().st_size} pages={pages} source={URL}",flush=True)
  first,last=2,min(12,pages)
  txt=exec_bound(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],85)
  print("ORIGINAL_TEXT_LAYER",len(txt),flush=True)
  if txt.strip():(OUT/"BID-2026Q2-first-pages.txt").write_text(txt[:60000],"utf-8")
  exec_bound(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1600","-jpeg","-jpegopt","quality=70",str(pdf),str(OUT/"BID-2026Q2-HN")],180)
  n=len(list(OUT.glob("BID-2026Q2-HN-*.jpg")))
  assert n==last-first+1,n
  print(f"PASS BID_2026Q2_ORIGINAL_PDF_PROVENANCE rendered={n}; no data promoted",flush=True)
if __name__=="__main__":main()
