#!/usr/bin/env python3
"""Targeted reinspection of KPMG reviewed 2025 H1 bank Q2 STB cash pages 9-13 only.
Requires pinned SHA of 104-page KPMG signed scanned source.
"""
from pathlib import Path
import hashlib,subprocess,tempfile
URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/STB_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf"
SHA="244de4c8a97ada2e086b27ac78484265b825d4cde9cbfcaebbda62ec3e4b3833"
OUT=Path("stb-2025h1-kpmg-focused")
def run(cmd,timeout=170):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:250])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/"stb-2025-h1.pdf"
  run(["curl","-L","--silent","--show-error","--connect-timeout","20","--max-time","165",
    "--max-filesize",str(65*1024*1024),"--user-agent","Mozilla/5.0","--output",str(f),URL],175)
  assert hashlib.sha256(f.read_bytes()).hexdigest()==SHA
  print(f"STB_2025H1_KPMG_SHA_CONFIRMED {SHA} bytes={f.stat().st_size}",flush=True)
  run(["pdftoppm","-f","9","-l","13","-scale-to","2100","-gray","-png",str(f),str(OUT/"page")],240)
  for img in sorted(OUT.glob("page-*.png")):
   raw=run(["tesseract",str(img),"stdout","-l","vie+eng","--psm","6"],100)
   (OUT/(img.stem+".txt")).write_text(raw[:20000],"utf8")
   print("STB_2025H1_KPMG_PAGE_START "+img.stem,flush=True)
   print(raw[:20000],flush=True)
   print("STB_2025H1_KPMG_PAGE_END "+img.stem,flush=True)
  assert len(list(OUT.glob("page-*.txt")))==5
 print("PASS STB 2025H1 KPMG independently reviewed scanned bank B03/B04 focused pages",flush=True)
if __name__=="__main__":main()
