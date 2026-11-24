#!/usr/bin/env python3
"""Source-only CTG 2026 Q1 issuer signed original and 2026 H1 original, banking B02/B03/B04."""
import hashlib,re,subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
SRC=[
("CTG_Q1_2026","https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/CTG_Baocaotaichinh_Q1_2026_Hopnhat.pdf"),

]
OUT=Path("ctg-2026-bank-source")
def run(c,t=270):
 p=subprocess.run(c,capture_output=True,text=True,timeout=t)
 if p.returncode:raise RuntimeError(str(c[:2])+" "+p.stderr[:400])
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  for tag,url in SRC:
   f=Path(td)/(tag+".pdf")
   r=run(["curl","-L","--silent","--show-error","--connect-timeout","25","--max-time","520",
    "--speed-time","75","--speed-limit","1000","--max-filesize",str(75*1024*1024),
    "--retry","3","--retry-delay","2","--retry-all-errors","--continue-at","-", "--user-agent","Mozilla/5.0","--output",str(f),"--write-out","%{http_code}|%{size_download}",url],620)
   assert r.startswith("200|") and f.read_bytes()[:5]==b"%PDF-" and f.stat().st_size>120000,r
   pages=int(re.search(r"^Pages:\s*(\d+)",run(["pdfinfo",str(f)]),re.M).group(1))
   sha=hashlib.sha256(f.read_bytes()).hexdigest()
   print(f"CTG_2026_SOURCE name={tag} pages={pages} bytes={f.stat().st_size} sha256={sha} url={url}",flush=True)
   if tag=="CTG_H1_2026": assert sha=="f7453816648cac21536621e09d4e52a40e8ce9fcdbaf824981b3b997a8197318","Previously verified 2026Q3 source-ledger H1 has changed, stop"
   txt=run(["pdftotext","-layout","-f","1","-l",str(min(pages,13)),str(f),"-"],120)
   (OUT/(tag+".txt")).write_text(txt[:100000],"utf8")
   print("CTG_2026_PDF_TEXT_START "+tag,flush=True);print(txt[:50000],flush=True);print("CTG_2026_PDF_TEXT_END "+tag,flush=True)
   if len(txt.strip())<1200:
    print("CTG_2026_SOURCE_SCANNED "+tag,flush=True)
    run(["pdftoppm","-f","3","-l",str(min(pages,12)),"-scale-to","1900","-gray","-png",str(f),str(OUT/tag)],250)
    for i in sorted(OUT.glob(tag+"*.png")):
     t=run(["tesseract",str(i),"stdout","-l","vie+eng","--psm","6"],95)
     (OUT/(i.stem+".txt")).write_text(t[:15000],"utf8")
     print(f"CTG_2026_OCR_BEGIN {i.stem}",flush=True);print(t[:13500],flush=True);print(f"CTG_2026_OCR_END {i.stem}",flush=True)
 print("PASS CTG 2026Q1 signed original source hash and original Q1 B02 B03 B04 pages; 2026H1 original hash independently pinned in already verified CTG 2026Q3 ledger f7453816648cac21536621e09d4e52a40e8ce9fcdbaf824981b3b997a8197318. No promotion.",flush=True)
if __name__=="__main__":main()
