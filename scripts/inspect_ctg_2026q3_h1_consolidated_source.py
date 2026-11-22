#!/usr/bin/env python3
"""Read-only source identity for VietinBank CTG 2026 Q3 & H1 consolidated.

Bank B02a/B03a/B04a exact original issuer PDFs, preserve prior audited
vintages. No dashboard numeric write without visual source validation.
"""
import hashlib,subprocess,tempfile
from pathlib import Path
SOURCES={
 "CTG_2026Q3_9M":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/CTG_Baocaotaichinh_Q3_2026_Hopnhat.pdf",
 "CTG_2026Q2_H1":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/CTG_Baocaotaichinh_Q2_2026_Hopnhat.pdf"
}
OUT=Path("ctg-2026q3-h1-consolidated-previews");OUT.mkdir(exist_ok=True)
def run(cmd,t):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(f"{cmd[0]} exit {p.returncode}: {p.stderr[:300]}")
 return p.stdout
def main():
 with tempfile.TemporaryDirectory() as td:
  for label,url in SOURCES.items():
   p=Path(td)/(label+".pdf")
   run(["curl","--fail","--location","--silent","--show-error","--connect-timeout","14",
     "--max-time","110","--speed-time","16","--speed-limit","8192","--max-filesize",str(65*1024*1024),
     "--user-agent","Mozilla/5.0","--output",str(p),url],135)
   if p.open("rb").read(5)!=b"%PDF-":raise SystemExit("SOURCE_NOT_PDF "+label)
   info=run(["pdfinfo",str(p)],25)
   pages=int(next(line.split(":",1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
   if not 30<=pages<=180:raise SystemExit("INVALID_PAGES "+label)
   sha=hashlib.sha256(p.read_bytes()).hexdigest()
   chars=len(run(["pdftotext","-layout",str(p),"-"],70))
   print("SIGNED_CONSOLIDATED_SOURCE",label,"URL",url,"SHA256",sha,"PAGES",pages,"BYTES",p.stat().st_size,"TEXT_CHARS",chars,flush=True)
   count=min(34,pages)
   run(["pdftoppm","-f","1","-l",str(count),"-scale-to","1500","-jpeg",
      "-jpegopt","quality=68",str(p),str(OUT/label)],160)
   assert len(list(OUT.glob(label+"-*.jpg")))==count
   print("SOURCE_PREVIEW",label,count,"PASS_PROVENANCE_ONLY",flush=True)
if __name__=="__main__":main()
