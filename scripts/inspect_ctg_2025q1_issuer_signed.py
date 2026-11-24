#!/usr/bin/env python3
"""CTG consolidated signed Q1 2025 original source: record SHA256 and inspect bank B02/B03/B04."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,hashlib,re
URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/CTG_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
OUT=Path("ctg-2025q1-issuer-source")
def run(cmd,timeout=270):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:380])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  f=Path(td)/"original.pdf"
  res=run(["curl","-L","--silent","--show-error","--connect-timeout","25","--max-time","260",
   "--speed-time","35","--speed-limit","1000","--max-filesize",str(80*1024*1024),
   "--user-agent","Mozilla/5.0","--output",str(f),"--write-out","%{http_code}|%{size_download}",URL],270)
  assert res.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>100000,res
  pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
  print(f"CTG_2025Q1_SIGNED_SOURCE url={URL} pages={pages} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
  raw=run(["pdftotext","-f","3","-l","12","-layout",str(f),"-"],100)
  (OUT/"source-B02-B03-B04.txt").write_text(raw[:115000],"utf8")
  print("CTG_2025Q1_PDF_TEXT_START",flush=True);print(raw[:60000],flush=True);print("CTG_2025Q1_PDF_TEXT_END",flush=True)
  if len(raw.strip())<1000:
   print("CTG_2025Q1_SIGNED_SCAN_OCR_PAGES_4_to_11",flush=True)
   run(["pdftoppm","-f","4","-l","11","-scale-to","1850","-gray",
    "-png",str(f),str(OUT/"page")],235)
   for image in sorted(OUT.glob("page-*.png")):
    t=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],100)
    (OUT/(image.stem+".txt")).write_text(t[:24000],"utf8")
    print("CTG_2025Q1_SOURCE_PAGE_START "+image.stem,flush=True)
    print(t[:18500],flush=True)
    print("CTG_2025Q1_SOURCE_PAGE_END "+image.stem,flush=True)
 print("PASS CTG Q1 2025 issuer consolidated original PDF retrieval and signed source hash; production unchanged",flush=True)
if __name__=="__main__":main()
