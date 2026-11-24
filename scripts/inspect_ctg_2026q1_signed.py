#!/usr/bin/env python3
"""CTG Q1 2026 issuer-original signed bank B02 B03 B04 source SHA256 and direct source text."""
from tempfile import TemporaryDirectory
from pathlib import Path
import subprocess,hashlib,re
SRC="https://investor.vietinbank.vn/documents/20126/745243/BCTC%20hop%20nhat%20Quy%20I.2026.pdf.pdf/fe475c57-822f-3c6d-5bf1-53e6612969e9"
OUT=Path("ctg-2026q1-signed-evidence")
def run(cmd,t=250):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(cmd[0])+" "+p.stderr[:330])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  f=Path(td)/"original.pdf"
  response=run(["curl","-L","--silent","--show-error","--connect-timeout","30","--max-time","240",
    "--max-filesize",str(70*1024*1024),"--user-agent","Mozilla/5.0","--output",str(f),
    "--write-out","%{http_code}|%{size_download}",SRC],250)
  assert response.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>80000,response
  pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
  print(f"CTG_2026Q1_SIGNED_SOURCE url={SRC} pages={pages} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
  txt=run(["pdftotext","-layout","-f","1","-l",str(min(12,pages)),str(f),"-"],100)
  (OUT/"source-B02-B03-B04.txt").write_text(txt[:115000],"utf8")
  print("CTG_2026Q1_PDF_TEXT_START",flush=True);print(txt[:74000],flush=True);print("CTG_2026Q1_PDF_TEXT_END",flush=True)
  if len(txt.strip())<1300:
   print("CTG_2026Q1_ORIGINAL_SCANNED_READING_PAGES_3_TO_10",flush=True)
   run(["pdftoppm","-f","3","-l",str(min(10,pages)),"-scale-to","1750","-gray","-png",str(f),str(OUT/"page")],235)
   for image in sorted(OUT.glob("page-*.png")):
    text=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],105)
    (OUT/(image.stem+".txt")).write_text(text[:16000],"utf8")
    print("CTG_2026Q1_ORIGINAL_PAGE "+image.stem,flush=True);print(text[:13500],flush=True)
 print("PASS CTG original signed 2026 Q1 PDF verified and hashed, no production mutation",flush=True)
if __name__=="__main__":main()
