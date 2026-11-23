#!/usr/bin/env python3
"""Read-only STB Q4/2025 original issuer vs KPMG-audited FY2025 consolidated signed source.
Use PDF text extraction whenever available; narrowly rendered OCR only for scanned source."""
import hashlib,re,subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
OUT=Path("stb-2025q4-source-evidence")
SOURCES=[
("Q4_ORIGINAL","https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/STB_Baocaotaichinh_Q4_2025_Hopnhat.pdf",True),
("FY_AUDITED","https://www.sacombank.com.vn/content/dam/sacombank/files/nhadautu/baocaotaichinh/2025/Consolidated-Financial-Statements-2025.pdf",True)]
def run(args,timeout=175):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(str(args[:2])+" err "+p.stderr[:350])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for label,url,required in SOURCES:
   try:
    f=Path(td)/(label+".pdf")
    response=run(["curl","--location","--silent","--show-error",
     "--connect-timeout","25","--max-time","210","--speed-time","45","--speed-limit","1000",
     "--max-filesize",str(75*1024*1024),"--user-agent","Mozilla/5.0",
     "--output",str(f),"--write-out","%{http_code}|%{content_type}|%{size_download}",url],225)
    assert response.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>80000,response
    pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
    sha=hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"STB_2025Q4_SIGNED_SOURCE {label} bytes={f.stat().st_size} sha256={sha} pages={pages} url={url}",flush=True)
    raw=run(["pdftotext","-layout","-f","1","-l",str(min(15,pages)),str(f),"-"],110)
    (OUT/(label+".txt")).write_text(raw[:125000],"utf8")
    print(f"STB_2025Q4_SOURCE_TEXT_START name={label}",flush=True)
    print(raw[:90000],flush=True)
    print(f"STB_2025Q4_SOURCE_TEXT_END name={label}",flush=True)
    if len(raw.strip())<1500:
     print(f"STB_2025Q4_SCANNED name={label} target_source_pages_2_to_9",flush=True)
     run(["pdftoppm","-f","2","-l",str(min(9,pages)),"-scale-to","1750",
      "-gray","-png",str(f),str(OUT/label)],190)
     for pic in sorted(OUT.glob(label+"*.png")):
      t=run(["tesseract",str(pic),"stdout","-l","vie+eng","--psm","6"],95)
      (OUT/(pic.stem+".txt")).write_text(t[:18000],"utf8")
      print(f"STB_2025Q4_PAGE_OCR name={label} page={pic.stem}",flush=True)
      print(t[:14500],flush=True)
   except Exception as exc:
    if required:raise
    print("STB_2025Q4_OPTIONAL_SOURCE_UNAVAILABLE "+label+" "+str(exc)[:350],flush=True)
 print("PASS STB 2025 Q4 issuer original and KPMG audited FY source retrieval, finance production unchanged",flush=True)
if __name__=="__main__":main()
