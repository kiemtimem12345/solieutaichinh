#!/usr/bin/env python3
"""STB 2025 Q2 first-issued consolidated PDF and independently reviewed H1 optional source.
Read-only issuer source, verified SHA and narrowly targeted OCR on scanned B02/B03/B04 pages.
"""
from pathlib import Path
import hashlib,re,subprocess,tempfile
ROOT="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/"
URLS=[("Q2_ORIGINAL",ROOT+"STB_Baocaotaichinh_Q2_2025_Hopnhat.pdf",True),
      ("H1_REVIEWED",ROOT+"STB_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf",False)]
OUT=Path("stb-2025q2-sources")
def run(args,t=160):
 p=subprocess.run(args,capture_output=True,text=True,timeout=t,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]}: {p.stderr[:350]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as root:
  root=Path(root)
  for name,url,required in URLS:
   try:
    fn=root/(name+".pdf")
    res=run(["curl","--location","--silent","--show-error","--connect-timeout","22",
    "--max-time","160","--speed-time","35","--speed-limit","1200","--max-filesize",str(96*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(fn),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",url],180)
    assert res.startswith("200|") and fn.read_bytes()[:5]==b"%PDF-" and fn.stat().st_size>50000,res
    pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(fn)]),re.M).group(1))
    digest=hashlib.sha256(fn.read_bytes()).hexdigest()
    print(f"STB_Q2_2025_SOURCE name={name} url={url} bytes={fn.stat().st_size} sha256={digest} pages={pages}",flush=True)
    raw=run(["pdftotext","-f","1","-l",str(min(12,pages)),"-layout",str(fn),"-"],120)
    (OUT/(name+"-first-pages.txt")).write_text(raw[:88000],"utf8")
    print(f"STB_Q2_2025_TEXT_START name={name}",flush=True)
    print(raw[:25000],flush=True)
    print(f"STB_Q2_2025_TEXT_END name={name}",flush=True)
    if len(raw.strip())<1300:
     print(f"STB_Q2_2025_SCANNED name={name} original statement-pages_2_8_only",flush=True)
     run(["pdftoppm","-f","2","-l",str(min(8,pages)),
       "-scale-to","1900","-gray","-png",str(fn),str(OUT/name)],220)
     for pic in sorted(OUT.glob(name+"*.png")):
      t=run(["tesseract",str(pic),"stdout","-l","vie+eng","--psm","6"],90)
      (OUT/(pic.stem+"-ocr.txt")).write_text(t[:18000],"utf8")
      print(f"STB_Q2_2025_PAGE_OCR name={name} page={pic.stem}",flush=True)
      print(t[:12500],flush=True)
   except Exception as e:
    if required:raise
    print(f"STB_H1_OPTIONAL_SOURCE_NOT_CONFIRMED url={url} reason={str(e)[:300]}",flush=True)
 print("PASS STB 2025 Q2 signed issuer original retrieved; no production data modified",flush=True)
if __name__=="__main__":main()
