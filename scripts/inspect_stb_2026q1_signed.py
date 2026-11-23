#!/usr/bin/env python3
"""STB signed original issuer consolidated 2026Q1 PDF, SHA and visual statement evidence."""
from pathlib import Path
from tempfile import TemporaryDirectory
import re,hashlib,subprocess
SRC="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/STB_Baocaotaichinh_Q1_2026_Hopnhat.pdf"
OUT=Path("stb-2026q1-original")
def run(args,timeout=190):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(str(args[0])+" "+p.stderr[:280])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  f=Path(td)/"original.pdf"
  r=run(["curl","-L","--silent","--show-error","--connect-timeout","25","--max-time","230",
   "--max-filesize",str(70*1024*1024),"--user-agent","Mozilla/5.0",
   "--output",str(f),"--write-out","%{http_code}|%{size_download}",SRC],245)
  assert r.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>20000,r
  n=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
  print(f"STB_2026Q1_SIGNED_SOURCE url={SRC} pages={n} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
  txt=run(["pdftotext","-f","1","-l",str(min(n,10)),"-layout",str(f),"-"],110)
  (OUT/"source-original.txt").write_text(txt[:85000],"utf8")
  print("STB_Q1_2026_PDF_TEXT_START",flush=True);print(txt[:45000],flush=True);print("STB_Q1_2026_PDF_TEXT_END",flush=True)
  if len(txt.strip())<1100:
   print("STB_Q1_2026_SIGNED_SCAN_OCR_2_TO_8",flush=True)
   run(["pdftoppm","-f","2","-l",str(min(n,8)),"-scale-to","1800","-gray","-png",str(f),str(OUT/"page")],210)
   for image in sorted(OUT.glob("page-*.png")):
    t=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],85)
    (OUT/(image.stem+".txt")).write_text(t[:16000],"utf8")
    print("STB_2026Q1_OCR_START "+image.stem,flush=True);print(t[:14500],flush=True);print("STB_2026Q1_OCR_END "+image.stem,flush=True)
 print("PASS STB signed Q1 2026 original-source retrieval only, production not mutated",flush=True)
if __name__=="__main__":main()
