#!/usr/bin/env python3
"""Read-only signed issuer VCB Q3 2026 original consolidated provenance.

Use currently disclosed original HOSE URL and Vietstock archive path. Do NOT
write numerical dashboard values until original B02/B03/B04 accounting QA.
"""
import hashlib,subprocess,tempfile
from pathlib import Path
SOURCES=[
"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VCB_Baocaotaichinh_Q3_2026_Hopnhat.pdf",
"https://staticfile.hsx.vn/Uploads/UploadDocuments/2510515/20261030%20-%20VCB%20-%20BCTC%20Hop%20nhat%20Q3%202026.pdf"
]
OUT=Path("vcb-2026q3-consolidated-preview");OUT.mkdir(exist_ok=True)
def run(cmd,timeout):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
 if p.returncode:raise RuntimeError(cmd[0]+" exit "+str(p.returncode)+" "+p.stderr[:200])
 return p.stdout
def main():
 with tempfile.TemporaryDirectory() as td:
  pdf=Path(td)/"original.pdf";url=None
  for candidate in SOURCES:
   try:
    run(["curl","--location","--fail","--show-error","--silent","--connect-timeout","12",
         "--max-time","65","--speed-time","16","--speed-limit","8192",
         "--max-filesize",str(55*1024*1024),"--user-agent","Mozilla/5.0",
         "--output",str(pdf),candidate],80)
    if pdf.open("rb").read(5)!=b"%PDF-":raise RuntimeError("not PDF")
    if pdf.stat().st_size<1000000:raise RuntimeError("Unexpected small PDF")
    url=candidate;break
   except (RuntimeError,subprocess.TimeoutExpired) as exc:
    print("ATTEMPTED_SOURCE",candidate,"RETRY_ALTERNATE",str(exc)[:220],flush=True)
  if url is None:raise SystemExit("NO_ORIGINAL_PDF_RETRIEVED no financial rows changed")
  info=run(["pdfinfo",str(pdf)],25)
  pages=int(next(x.split(":",1)[1].strip() for x in info.splitlines() if x.startswith("Pages:")))
  if pages<20 or pages>180:raise SystemExit("BAD_PAGE_COUNT "+str(pages))
  hash=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print("SOURCE_PDF",url,"SHA256",hash,"PAGES",pages,"BYTES",pdf.stat().st_size,flush=True)
  print("TEXT_CHARS",len(run(["pdftotext","-layout",str(pdf),"-"],65)),flush=True)
  n=min(pages,33)
  run(["pdftoppm","-f","1","-l",str(n),"-jpeg","-scale-to","1450","-jpegopt","quality=67",str(pdf),str(OUT/"VCB_2026Q3")],145)
  assert len(list(OUT.glob("VCB_2026Q3-*.jpg")))==n
  print("VISUAL_PAGES",n,"PASS_SOURCE_ONLY_NOT_FINANCIAL_VALIDATION",flush=True)
if __name__=="__main__":main()
