#!/usr/bin/env python3
"""Read-only VPB original Q4 issuer ZIP and independently audited EY FY2025 source reconciliation.
Print source statement text with page provenance. NEVER promote source numbers directly.
"""
from pathlib import Path
import hashlib, zipfile, tempfile, subprocess, re
Q4_URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VPB_Baocaotaichinh_Q4_2025_Hopnhat.zip"
EY_URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/NAM/VPB_Baocaotaichinh_2025_Kiemtoan_Hopnhat.pdf"
OUT=Path("vpb-2025q4-ey-audit-source")
def run(args,t=120):
 r=subprocess.run(args,capture_output=True,text=True,timeout=t,check=False)
 if r.returncode:raise RuntimeError(f"{args[0]} exit {r.returncode}: {r.stderr[:300]}")
 return r.stdout
def fetch(url,fn):
 s=run(["curl","--location","--silent","--show-error","--connect-timeout","20",
  "--max-time","150","--speed-time","30","--speed-limit","1500","--max-filesize",str(65*1024*1024),
  "--user-agent","Mozilla/5.0","--output",str(fn),
  "--write-out","%{http_code}|%{content_type}|%{size_download}",url],165)
 assert s.startswith("200|") and fn.stat().st_size>80000,s
 print(f"VPB_SOURCE_VALID_HTTP {url} {s} SHA256={hashlib.sha256(fn.read_bytes()).hexdigest()}",flush=True)
def pdf(name,file,pgfrom,pglast):
 assert file.read_bytes()[:5]==b"%PDF-",name
 inf=run(["pdfinfo",str(file)])
 m=re.search(r"^Pages:\s*(\d+)",inf,re.M); assert m,name
 pages=int(m.group(1))
 print(f"VPB_PDF name={name} pages={pages} bytes={file.stat().st_size} sha256={hashlib.sha256(file.read_bytes()).hexdigest()}",flush=True)
 n=min(pglast,pages)
 txt=run(["pdftotext","-layout","-f",str(pgfrom),"-l",str(n),str(file),"-"],90)
 (OUT/(name+"-pages.txt")).write_text(txt[:150000],"utf-8")
 print(f"VPB_STATEMENT_TEXT_BEGIN name={name} pdf_pages={pgfrom}-{n}",flush=True)
 print(txt[:28500],flush=True)
 print(f"VPB_STATEMENT_TEXT_END name={name}",flush=True)
 # Q4 issuer original and lookup pages already rendered and verified by source run 45248057271.
 # EY FY pages 6-11 were visually examined against original PDF, so retain only text here.
 print(f"PASS VPB_TEXT_ONLY name={name} pdf_pages={pgfrom}-{n}",flush=True)

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  folder=Path(td);q4=folder/"q4.zip";ey=folder/"ey2025.pdf"
  fetch(Q4_URL,q4)
  assert zipfile.is_zipfile(q4)
  with zipfile.ZipFile(q4) as z:
   print("VPB_Q4_MEMBERS="+repr([(x.filename,x.file_size) for x in z.infolist()]),flush=True)
   names=["bctc-hop-nhat-ban-tra-cuu.pdf","Bctc-hop-nhat-1901.pdf"]
   for k,n in enumerate(names):
    file=folder/f"q4-{k}.pdf";file.write_bytes(z.read(n))
    pdf(["Q4_LOOKUP","Q4_SIGNED"][k],file,5,15)
  fetch(EY_URL,ey);pdf("EY_FY_AUDITED",ey,9,14)
 print("PASS VPB Q4 2025 original ZIP and EY FY audited source inspection; signed-vintage audit only, production Q4 not modified",flush=True)
if __name__=="__main__":main()
