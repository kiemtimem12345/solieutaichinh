#!/usr/bin/env python3
"""STB signed original 2026Q3 consolidated, Oct 27; hash source and inspect B02 B03 B04 9M."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,hashlib,re
SOURCES=[("VI_ORIGINAL","https://static2.vietstock.vn/vietstock/2026/10/27/20261027___stb___bctc_hop_nhat_q3_2026.pdf",True),
("EN_ISSUER","https://www.sacombank.com.vn/content/dam/sacombank/files/nhadautu/baocaotaichinh/2026/Consolidated-Financial-Statements-Q3.2026.pdf",True)]
OUT=Path("stb-2026q3-signed-source")
def run(cmd,t=250):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:350])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for name,url,required in SOURCES:
   try:
    f=Path(td)/(name+".pdf")
    res=run(["curl","-L","--silent","--show-error","--connect-timeout","28",
     "--max-time","270","--speed-time","45","--speed-limit","1000",
     "--max-filesize",str(65*1024*1024),"--user-agent","Mozilla/5.0",
     "--output",str(f),"--write-out","%{http_code}|%{size_download}",url],280)
    assert res.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>50000,res
    pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
    print(f"STB_2026Q3_ISSUER_SOURCE name={name} url={url} pages={pages} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
    txt=run(["pdftotext","-f","1","-l",str(min(13,pages)),"-layout",str(f),"-"],110)
    (OUT/(name+".txt")).write_text(txt[:115000],"utf8")
    print(f"STB_2026Q3_TEXT_START name={name}",flush=True);print(txt[:53000],flush=True);print(f"STB_2026Q3_TEXT_END name={name}",flush=True)
    if len(txt.strip())<1100:
     print(f"STB_2026Q3_SCANNED name={name} targeted_2_8",flush=True)
     run(["pdftoppm","-f","2","-l",str(min(8,pages)),"-scale-to","1850",
        "-gray","-png",str(f),str(OUT/name)],225)
     for image in sorted(OUT.glob(name+"*.png")):
      s=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],95)
      (OUT/(image.stem+".txt")).write_text(s[:15000],"utf8")
      print("STB_2026Q3_OCR_START "+image.stem,flush=True);print(s[:13500],flush=True);print("STB_2026Q3_OCR_END "+image.stem,flush=True)
   except Exception as exc:
    if required:raise
    print("STB_2026Q3_OPTIONAL_SOURCE_ERROR "+name+" "+str(exc)[:240],flush=True)
 print("PASS STB 2026 Q3 original signed issuer sources retrieved and examined; production not modified",flush=True)
if __name__=="__main__":main()
