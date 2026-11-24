#!/usr/bin/env python3
"""Source-hash CTG Q4/2025 issuer original and independently PwC audited FY2025 consolidated PDF."""
import hashlib,subprocess,re
from pathlib import Path
from tempfile import TemporaryDirectory
SRC=[("ISSUER_Q4","https://investor.vietinbank.vn/documents/20126/0/BCTC%2Bhop%2Bnhat%2BQuy%2BIV.2025.pdf/5fdb5ab3-7e02-e17d-93b8-b71382cc4426?t=1769777524946",2,10),
 ("PWC_AUDITED_FY","https://investor.vietinbank.vn/documents/20126/0/BCTC%2Bhop%2Bnhat%2Bkiem%2Btoan%2Bnam%2B2025_VN.pdf/4c8eda02-b420-612d-24ac-c12f2bbd3451?t=1774948852539",5,15)]
OUT=Path("ctg-2025q4-fy-pwc-sources")
def run(cmd,t=310):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:330])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for name,url,first,last in SRC:
   f=Path(td)/(name+".pdf")
   response=run(["curl","-L","--silent","--show-error","--connect-timeout","35","--max-time","280",
      "--max-filesize",str(80*1024*1024),"--user-agent","Mozilla/5.0",
      "--output",str(f),"--write-out","%{http_code}|%{size_download}",url],290)
   assert response.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>90000,response
   pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
   print(f"CTG_2025Q4_SOURCE name={name} url={url} pages={pages} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
   txt=run(["pdftotext","-layout","-f","1","-l",str(min(18,pages)),str(f),"-"],100)
   (OUT/(name+"-text.txt")).write_text(txt[:115000],"utf8")
   print(f"CTG_2025Q4_SOURCE_TEXT_START name={name}",flush=True)
   print(txt[:72000],flush=True)
   print(f"CTG_2025Q4_SOURCE_TEXT_END name={name}",flush=True)
   if len(txt.strip())<3000:
    print(f"CTG_2025Q4_SCANNED name={name} pages_{first}_{last}",flush=True)
    run(["pdftoppm","-f",str(first),"-l",str(min(pages,last)),"-scale-to","1700","-gray","-png",str(f),str(OUT/name)],270)
    for img in sorted(OUT.glob(name+"*.png")):
     line=run(["tesseract",str(img),"stdout","-l","vie+eng","--psm","6"],100)
     (OUT/(img.stem+".txt")).write_text(line[:22000],"utf8")
     print(f"CTG_2025Q4_PAGE_OCR name={name} page={img.stem}",flush=True)
     print(line[:14000],flush=True)
 print("PASS CTG Q4 2025 issuer source and independently PwC audited FY original bank source recovery; production unchanged",flush=True)
if __name__=="__main__":main()
