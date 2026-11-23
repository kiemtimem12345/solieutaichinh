#!/usr/bin/env python3
"""TPB Q3/2026 signed issuer B02a/B03a/B04a 9M original provenance only.

This ticker currently has SIX 2025Q1-2026Q2 rows. Q3 2026 must be a new
seventh period, not an overwritten Q2, and cannot be marked verified before
source 9M B04a minus KPMG-reviewed H1 bank cash including FX checks.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/TPB_Baocaotaichinh_Q3_2026_Hopnhat.pdf"
OUT=Path("tpb-2026q3-original-source")
def run(args,timeout):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} exit {p.returncode}: {p.stderr[:250]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  pdf=Path(td)/"TPB-Q3-2026-original.pdf"
  resp=run(["curl","--location","--silent","--show-error",
    "--connect-timeout","14","--max-time","115","--speed-time","18",
    "--speed-limit","4096","--max-filesize",str(60*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(pdf),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],130)
  assert resp.startswith("200"),resp
  assert pdf.exists() and pdf.stat().st_size>60000,"TPB Q3 original source unavailable or truncated"
  with pdf.open("rb") as f:assert f.read(5)==b"%PDF-","Not original PDF"
  info=run(["pdfinfo",str(pdf)],50)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"No signed PDF page count"
  pages=int(m.group(1))
  assert 15<=pages<=180,pages
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"TPB_2026Q3_SIGNED_SOURCE sha256={sha} bytes={pdf.stat().st_size} pages={pages} URL={URL}",flush=True)
  first,last=4,min(18,pages)
  layer=run(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],90)
  print(f"TPB_Q3_ORIGINAL_TEXT_LAYER chars={len(layer)}",flush=True)
  if layer.strip():(OUT/"TPB-Q3-2026-plaintext.txt").write_text(layer[:75000],"utf-8")
  run(["pdftoppm","-f",str(first),"-l",str(last),
       "-scale-to","1650","-jpeg","-jpegopt","quality=68",
       str(pdf),str(OUT/"TPB-Q3-HN")],190)
  n=len(list(OUT.glob("TPB-Q3-HN-*.jpg")))
  assert n==last-first+1,(n,last-first+1)
  print(f"PASS TPB 2026Q3 original consolidated signed B02a B03a B04a source provenance pages={n}; no production record yet",flush=True)
if __name__=="__main__":main()
