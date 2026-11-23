#!/usr/bin/env python3
"""Read issuer signed Q2 2026 and independently reviewed H1 consolidated STB bank financials."""
import hashlib,re,subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
SRC=[("Q2_ORIGINAL","https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/STB_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=5b3df9bf",2,8),
 ("H1_REVIEWED","https://www.sacombank.com.vn/content/dam/sacombank/files/nhadautu/baocaotaichinh/2026/Interim-Consolidated-Financial-Statements-2026.pdf",7,14)]
OUT=Path("stb-2026q2-review-source")
def run(cmd,t=240):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:300])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for name,url,first,last in SRC:
   f=Path(td)/(name+".pdf")
   res=run(["curl","-L","--silent","--show-error","--connect-timeout","25","--max-time","290",
    "--speed-time","42","--speed-limit","1000",
    "--max-filesize",str(65*1024*1024),"--user-agent","Mozilla/5.0",
    "--output",str(f),"--write-out","%{http_code}|%{size_download}",url],300)
   assert res.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>100000,res
   n=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
   sha=hashlib.sha256(f.read_bytes()).hexdigest()
   print(f"STB_2026Q2_SOURCE name={name} url={url} pages={n} bytes={f.stat().st_size} sha256={sha}",flush=True)
   raw=run(["pdftotext","-f","1","-l",str(min(n,17)),"-layout",str(f),"-"],120)
   (OUT/(name+"-source.txt")).write_text(raw[:125000],"utf8")
   print("STB_2026Q2_TEXT_START "+name,flush=True);print(raw[:68000],flush=True);print("STB_2026Q2_TEXT_END "+name,flush=True)
   if len(raw.strip())<1300:
    print(f"STB_2026Q2_SCANNED name={name} pages_{first}_{last}",flush=True)
    run(["pdftoppm","-f",str(first),"-l",str(min(n,last)),"-scale-to","1950","-gray","-png",
     str(f),str(OUT/name)],260)
    for img in sorted(OUT.glob(name+"*.png")):
     s=run(["tesseract",str(img),"stdout","-l","vie+eng","--psm","6"],95)
     (OUT/(img.stem+".txt")).write_text(s[:18000],"utf8")
     print(f"STB_2026Q2_OCR_START name={name} page={img.stem}",flush=True)
     print(s[:15800],flush=True)
     print(f"STB_2026Q2_OCR_END name={name}",flush=True)
 print("PASS STB 2026 Q2 original and H1 reviewed issuer PDFs independently source-recovered; production unchanged",flush=True)
if __name__=="__main__":main()
