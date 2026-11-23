#!/usr/bin/env python3
"""STB 2025Q1 consolidated issuer PDF source-only recovery, no production mutation."""
from pathlib import Path
import subprocess,hashlib,tempfile,re
URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/STB_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
OUT=Path("stb-2025q1-original")
def cmd(args,t=110):
 p=subprocess.run(args,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(args[0])+" "+p.stderr[:220])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/"source.pdf"
  res=cmd(["curl","-L","--silent","--show-error","--connect-timeout","19",
   "--max-time","150","--speed-time","28","--speed-limit","1600",
   "--max-filesize",str(55*1024*1024),"--user-agent","Mozilla/5.0",
   "--output",str(f),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL],165)
  assert res.startswith("200|") and f.read_bytes()[:5]==b"%PDF-"
  meta=cmd(["pdfinfo",str(f)]);m=re.search(r"^Pages:\s*(\d+)",meta,re.M);assert m
  pages=int(m.group(1));start=1;end=min(18,pages)
  print(f"STB_SOURCE_VERIFIED url={URL} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()} pages={pages}",flush=True)
  raw=cmd(["pdftotext","-f",str(start),"-l",str(end),"-layout",str(f),"-"],90)
  (OUT/"original-extracted.txt").write_text(raw[:95000],"utf8")
  print("STB_ORIGINAL_START",flush=True)
  print(raw[:52000],flush=True)
  print("STB_ORIGINAL_END",flush=True)
  if len(raw.strip())<=1000:
   print("STB_Q1_SCAN_DETECTED targeted_Vietnamese_OCR_pages_2_to_10",flush=True)
   cmd(["pdftoppm","-f","2","-l",str(min(10,pages)),"-r","160","-gray","-png",
    str(f),str(OUT/"page")],220)
   for picture in sorted(OUT.glob("page-*.png")):
    txt=cmd(["tesseract",str(picture),"stdout","-l","vie+eng","--psm","6"],90)
    (OUT/(picture.stem+"-ocr.txt")).write_text(txt[:10000],"utf8")
    print("STB_Q1_PAGE_OCR "+picture.stem,flush=True)
    print(txt[:11000],flush=True)
   assert len(list(OUT.glob("page-*-ocr.txt")))>=5

 print("PASS STB 2025 Q1 signed original source recovery; finance production unchanged",flush=True)
if __name__=="__main__":main()
