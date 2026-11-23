#!/usr/bin/env python3
"""Targeted OCR fallback for 2026 VPB reviewed H1 bank B04a pages only; scanned PDF."""
import hashlib,subprocess,tempfile
from pathlib import Path
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VPB_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf"
SHA="901f91a3b6e05c3342d9b77972c58627df06a8b8a4483cbc9d63eef1e01b6782"
def run(args,t=150):
 p=subprocess.run(args,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(args[0])+" "+p.stderr[:300])
 return p.stdout
def main():
 with tempfile.TemporaryDirectory() as td:
  folder=Path(td);pdf=folder/"reviewed.pdf"
  run(["curl","-L","--fail","--silent","--show-error","--max-time","140","--output",str(pdf),URL],160)
  assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
  # Selected scanned report pages near the bank B02/B03/B04 section
  run(["pdftoppm","-f","8","-l","15","-r","165","-gray","-png",str(pdf),str(folder/"pg")],220)
  for p in sorted(folder.glob("pg-*.png")):
   text=run(["tesseract",str(p),"stdout","-l","vie+eng","--psm","6"],90)
   print("VPB_H1_REVIEWED_OCR_PAGE "+p.stem,flush=True)
   print(text[:8500],flush=True)
 print("PASS VPB reviewed H1 scanned PDF hash and targeted visual-page OCR",flush=True)
if __name__=="__main__":main()
