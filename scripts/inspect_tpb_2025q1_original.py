#!/usr/bin/env python3
"""TPB Q1/2025 consolidated original source inspection (read-only).

The dashboard's provisional OCR bank cash flow is not evidence; check
original signed B01/B03/B04 at million VND and exact statement pages first.
Do not modify production data in this source retrieval.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/TPB_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
OUT=Path("tpb-2025q1-original-pages")
def execute(cmd,seconds=100):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=seconds,check=False)
 if p.returncode:raise RuntimeError(f"{cmd[0]} exit={p.returncode} {p.stderr[:260]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  pdf=Path(td)/"TPB-Q1-2025-HN-original.pdf"
  meta=execute(["curl","--location","--silent","--show-error","--connect-timeout","14","--max-time","110",
                "--speed-time","18","--speed-limit","4096","--max-filesize",str(55*1024*1024),
                "--user-agent","Mozilla/5.0","--output",str(pdf),
                "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],125)
  assert meta.startswith("200"),meta
  assert pdf.exists() and pdf.stat().st_size>60000,"Original PDF truncated"
  with pdf.open("rb") as f:assert f.read(5)==b"%PDF-","Not a signed PDF source"
  info=execute(["pdfinfo",str(pdf)],40)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"Page count unavailable"
  pages=int(m.group(1))
  assert 15<=pages<=160,pages
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"TPB_2025Q1_ORIGINAL sha256={sha} bytes={pdf.stat().st_size} pages={pages} url={URL}",flush=True)
  first,last=5,min(18,pages)
  text=execute(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],90)
  print(f"TPB_2025Q1_TEXT_LAYER chars={len(text)}",flush=True)
  if text.strip():(OUT/"TPB-Q1-2025-statement-text.txt").write_text(text[:60000],"utf-8")
  execute(["pdftoppm","-f",str(first),"-l",str(last),
           "-scale-to","1600","-jpeg","-jpegopt","quality=67",
           str(pdf),str(OUT/"TPB-2025Q1-HN")],180)
  n=len(list(OUT.glob("TPB-2025Q1-HN-*.jpg")))
  assert n==last-first+1,(n,last-first+1)
  print(f"PASS TPB_2025Q1_ORIGINAL_SOURCE_PROVENANCE visual_pages={n}; production untouched",flush=True)
if __name__=="__main__":main()
