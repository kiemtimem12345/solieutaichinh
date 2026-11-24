#!/usr/bin/env python3
"""Inspect issuer-original CTG 2025Q3 consolidated signed 9M bank source and optional Vietstock ZIP.
Read-only: SHA256, file sizes, exact source B02/B03/B04 line text.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,subprocess,re,zipfile
SRC="https://investor.vietinbank.vn/documents/20126/168545/BCTC%20hop%20nhat%203Q2025..pdf.pdf/7cebff86-0a61-f4d6-ca68-b41a07a7b556?download=true"
OUT=Path("ctg-2025q3-issuer-evidence")
def run(cmd,timeout=220):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:400])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  f=Path(td)/"original.pdf"
  z=run(["curl","-L","--silent","--show-error","--connect-timeout","30","--max-time","250",
    "--max-filesize",str(75*1024*1024),"--user-agent","Mozilla/5.0",
    "--output",str(f),"--write-out","%{http_code}|%{size_download}",SRC],265)
  assert z.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>100000,z
  pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
  sha=hashlib.sha256(f.read_bytes()).hexdigest()
  print(f"CTG_2025Q3_ORIGINAL_SOURCE pages={pages} bytes={f.stat().st_size} sha256={sha} url={SRC}",flush=True)
  raw=run(["pdftotext","-layout","-f","2","-l",str(min(13,pages)),str(f),"-"],140)
  (OUT/"original-issuer-B02-B03-B04.txt").write_text(raw[:155000],"utf8")
  print("CTG_2025Q3_SOURCE_START",flush=True)
  print(raw[:100000],flush=True)
  print("CTG_2025Q3_SOURCE_END",flush=True)
  if len(raw.strip())<1100:
   print("CTG_2025Q3_SCANNED_SOURCE_PAGES_3_TO_11",flush=True)
   run(["pdftoppm","-f","3","-l",str(min(11,pages)),"-scale-to","1750","-gray","-png",str(f),str(OUT/"page")],230)
   for image in sorted(OUT.glob("page-*.png")):
    txt=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],100)
    (OUT/(image.stem+".txt")).write_text(txt[:16500],"utf8")
    print(f"CTG_2025Q3_PAGE_OCR page={image.stem}",flush=True)
    print(txt[:13000],flush=True)
  assert pages>=55,"issuer signed original too short"
 print("PASS CTG 2025Q3 signed 9M issuer consolidated PDF source retrieval, hash and page inspection; production unchanged",flush=True)
if __name__=="__main__":main()
