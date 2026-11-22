#!/usr/bin/env python3
"""Read-only source identity and limited B01/B02/B03 page previews for VCB 2025Q1.

Consolidated banking financial statements, not issuer standalone. No guesswork,
no overwriting previously stored provisional figures or original source PDFs.
"""
from pathlib import Path
import tempfile,subprocess,hashlib
URLS=[
 "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/VCB_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
]
OUT=Path("vcb-2025q1-consolidated-previews");OUT.mkdir(exist_ok=True)
def run(a,t):
  p=subprocess.run(a,capture_output=True,text=True,timeout=t)
  if p.returncode:raise RuntimeError(f"{a[0]} exit {p.returncode}: {p.stderr[:180]}")
  return p.stdout
def main():
  with tempfile.TemporaryDirectory() as dirname:
    pdf=Path(dirname)/"vcb_q1_signed_original.pdf"
    run(["curl","--fail","--location","--silent","--show-error",
      "--connect-timeout","12","--max-time","100","--speed-limit","8192","--speed-time","17",
      "--max-filesize",str(48*1024*1024),"--user-agent","Mozilla/5.0",
      "--output",str(pdf),URLS[0]],115)
    assert pdf.open("rb").read(5)==b"%PDF-","not signed source PDF"
    pages=int(next(x.split(":",1)[1].strip() for x in run(["pdfinfo",str(pdf)],24).splitlines() if x.startswith("Pages:")))
    assert 10<=pages<=160,pages
    print("ORIGINAL_CONSOLIDATED_SOURCE",URLS[0],"sha256",hashlib.sha256(pdf.read_bytes()).hexdigest(),"bytes",pdf.stat().st_size,"pages",pages,flush=True)
    t=run(["pdftotext","-layout",str(pdf),"-"],75)
    print("TEXT_CHARS",len(t),flush=True)
    n=min(pages,32)
    run(["pdftoppm","-f","1","-l",str(n),"-scale-to","1350","-jpeg","-jpegopt","quality=65",str(pdf),str(OUT/"VCB_2025Q1")],135)
    print("B01_B02_B03_ORIGINAL_PREVIEWS",len(list(OUT.glob("VCB_2025Q1-*.jpg"))),flush=True)
    assert len(list(OUT.glob("VCB_2025Q1-*.jpg")))==n
    print("PASS_SOURCE_ONLY_NO_PRODUCTION_NUMBERS_CHANGED",flush=True)
if __name__=="__main__":main()
