#!/usr/bin/env python3
"""Source-hash CTG signed original Q2 2025 and independently PwC-reviewed 2025H1 consolidated.
Preserve cash flow 79,310 million VND classification movement CFO<->CFI, no balancing plug.
"""
import hashlib,re,subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
SOURCE=[
 ("ISSUER_FIRST_Q2","https://investor.vietinbank.vn/documents/20126/169610/BCTC%2Bhop%2Bnhat%2BQuy%2BII.2025.pdf.pdf/35e4e2fa-04ef-fb04-3104-2b6aae0a7d3e"),
 ("PWC_REVIEWED_H1","https://investor.vietinbank.vn/documents/20126/223928/Vietinbank%20FS%20conso%2030.6.2025%20VN.pdf.pdf/46ebb297-6b5f-8e52-d65f-449ef00b3cfa")]
OUT=Path("ctg-2025q2-original-pwc")
def run(cmd,timeout=340):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(cmd[0]+" "+p.stderr[:350])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for name,url in SOURCE:
   f=Path(td)/(name+".pdf")
   res=run(["curl","-L","--silent","--show-error","--connect-timeout","35","--max-time","300",
    "--max-filesize",str(75*1024*1024),"--user-agent","Mozilla/5.0",
    "--output",str(f),"--write-out","%{http_code}|%{size_download}",url],315)
   assert res.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>100000,res
   pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
   print(f"CTG_2025Q2_SOURCE name={name} url={url} pages={pages} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
   text=run(["pdftotext","-f","1","-l",str(min(16,pages)),"-layout",str(f),"-"],120)
   (OUT/(name+".txt")).write_text(text[:165000],"utf8")
   print(f"CTG_2025Q2_TEXT_START name={name}",flush=True)
   print(text[:55000],flush=True)
   print(f"CTG_2025Q2_TEXT_END name={name}",flush=True)
   if len(text.strip())<2000:
    first,last=(2,9) if name=="ISSUER_FIRST_Q2" else (6,13)
    print(f"CTG_2025Q2_ORIGINAL_SCAN_OCR name={name} pages_{first}_{last}",flush=True)
    run(["pdftoppm","-f",str(first),"-l",str(min(pages,last)),
      "-scale-to","1850","-gray","-png",str(f),str(OUT/name)],240)
    for image in sorted(OUT.glob(name+"*.png")):
     transcribed=run(["tesseract",str(image),"stdout","-l","vie+eng","--psm","6"],120)
     (OUT/(image.stem+".txt")).write_text(transcribed[:17000],"utf8")
     print(f"CTG_2025Q2_OCR_START name={name} file={image.stem}",flush=True)
     print(transcribed[:12500],flush=True)
     print(f"CTG_2025Q2_OCR_END name={name} file={image.stem}",flush=True)
 print("PASS CTG Q2 signed original versus independently PwC-reviewed H1 2025 source files retrieved; production unchanged",flush=True)
if __name__=="__main__":main()
