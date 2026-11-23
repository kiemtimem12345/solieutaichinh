#!/usr/bin/env python3
"""Read-only provenance of TPB signed Q4/2025 consolidated B02a/B03a/B04a.

Keep Q1-Q3 signed checkpoints immutable. Test audited FY source candidates
separately: failure to find audited original must NOT permit provisional
Q4 values to publish or overwrite direct first-issued Q4 B03a.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/TPB_Baocaotaichinh_Q4_2025_Hopnhat.pdf"
OUT=Path("tpb-2025q4-original-source")

def run(args,timeout):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} return={p.returncode} stderr={p.stderr[:230]}")
 return p.stdout

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  pdf=Path(td)/"TPB-2025-Q4-original.pdf"
  response=run(["curl","--location","--silent","--show-error","--connect-timeout","14",
   "--max-time","115","--speed-time","17","--speed-limit","4096",
   "--max-filesize",str(60*1024*1024),"--user-agent","Mozilla/5.0",
   "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL],130)
  assert response.startswith("200"),response
  assert pdf.exists() and pdf.stat().st_size>60000,"Missing/truncated original PDF"
  with pdf.open("rb") as f:assert f.read(5)==b"%PDF-","Invalid PDF"
  info=run(["pdfinfo",str(pdf)],40)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"Original PDF page count unknown"
  pages=int(m.group(1))
  assert 15<=pages<=200,pages
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"TPB_2025Q4_ORIGINAL sha256={sha} bytes={pdf.stat().st_size} pages={pages} source={URL}",flush=True)
  first,last=4,min(17,pages)
  txt=run(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],90)
  print(f"SOURCE_TEXT_LAYER chars={len(txt)}",flush=True)
  if txt.strip():(OUT/"TPB-2025Q4-excerpt.txt").write_text(txt[:75000],"utf-8")
  run(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1550",
       "-jpeg","-jpegopt","quality=70",str(pdf),str(OUT/"TPB-2025Q4-HN")],190)
  n=len(list(OUT.glob("TPB-2025Q4-HN-*.jpg")))
  assert n==last-first+1,n
  print(f"PASS TPB 2025Q4 original bank consolidated provenance images={n}, unverified data unchanged",flush=True)

if __name__=="__main__":main()
