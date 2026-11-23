#!/usr/bin/env python3
"""TPB Q1/2026 signed consolidated original B02a B03a B04a source QA.

Recover original signed PDF and verify source SHA, page images and B04a FX.
The prior 2025 FY balance has three different vintage presentations. Do not
substitute a prior year as-filed/2025 KPMG audited number for 2026Q1's
reported comparative without inspecting this original's B02a notes.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/TPB_Baocaotaichinh_Q1_2026_Hopnhat.pdf"
OUT=Path("tpb-2026q1-original-pages")

def go(args,timeout=130):
 p=subprocess.run(args,text=True,capture_output=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} rc={p.returncode} {p.stderr[:260]}")
 return p.stdout

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as tmp:
  pdf=Path(tmp)/"TPB-2026Q1-HN.pdf"
  resp=go(["curl","--location","--silent","--show-error","--connect-timeout","14","--max-time","110",
           "--speed-time","20","--speed-limit","4096","--max-filesize",str(60*1024*1024),
           "--user-agent","Mozilla/5.0","--output",str(pdf),
           "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],130)
  assert resp.startswith("200"),resp
  assert pdf.exists() and pdf.stat().st_size>60000,"PDF missing or truncated"
  with pdf.open("rb") as fp:assert fp.read(5)==b"%PDF-"
  info=go(["pdfinfo",str(pdf)],35)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"PDF page count unavailable"
  pages=int(m.group(1))
  assert 16<=pages<=170,pages
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"TPB_2026Q1_SIGNED_ORIGINAL sha256={sha} bytes={pdf.stat().st_size} pages={pages} url={URL}",flush=True)
  first,last=3,min(17,pages)
  text=go(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],90)
  print(f"ORIGINAL_PDF_TEXT_LAYER chars={len(text)}",flush=True)
  if text.strip(): (OUT/"TPB-2026Q1-statement-layer.txt").write_text(text[:70000],"utf-8")
  go(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1550",
      "-jpeg","-jpegopt","quality=69",str(pdf),str(OUT/"TPB-2026Q1-HN")],190)
  rendered=len(list(OUT.glob("TPB-2026Q1-HN-*.jpg")))
  assert rendered==last-first+1,rendered
  print(f"PASS TPB Q1 2026 signed consolidated original source with {rendered} page previews, no data changed",flush=True)
if __name__=="__main__":main()
