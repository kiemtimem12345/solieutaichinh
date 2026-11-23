#!/usr/bin/env python3
"""VPB Q2 2025 original consolidated + independently reviewed H1 source QA.

First-issued Q2 B02a/B03a signed current quarter; H1 B04a cash is year-to-
date. Standalone Q2 cash must equal reviewed H1 6M minus signed Q1 2025
B04a. Never infer financing cash from net cash movement or use OCR wrong
cash opening 443,002,784. Source-only download/visual evidence.
"""
from pathlib import Path
import hashlib,re,subprocess,tempfile
OUT=Path("vpb-2025q2-h1-source")
SOURCES={
 "VPB_Q2_FIRST":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VPB_Baocaotaichinh_Q2_2025_Hopnhat.pdf",
 "VPB_H1_REVIEWED":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VPB_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf",
}
def go(args,timeout=110):
 r=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
 if r.returncode:raise RuntimeError(f"{args[0]} exit={r.returncode}: {r.stderr[:250]}")
 return r.stdout
def source(name,url,td,required):
 dest=Path(td)/(name+".pdf")
 try:
  resp=go(["curl","--location","--silent","--show-error","--connect-timeout","19",
   "--max-time","135","--speed-time","25","--speed-limit","2000",
   "--max-filesize",str(65*1024*1024),"--user-agent","Mozilla/5.0",
   "--output",str(dest),"--write-out","%{http_code}|%{content_type}|%{size_download}",url],155)
  size=dest.stat().st_size if dest.exists() else 0
  with dest.open("rb") as f: magic=f.read(5) if size else b""
  assert resp.startswith("200") and size>60000 and magic==b"%PDF-",resp
  info=go(["pdfinfo",str(dest)],45)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"Missing page count"
  pages=int(m.group(1))
  assert 15<=pages<=240,pages
  digest=hashlib.sha256(dest.read_bytes()).hexdigest()
  print(f"VPB_SOURCE_VERIFIED name={name} sha256={digest} bytes={size} pages={pages} URL={url}",flush=True)
  first,last=(4,min(19,pages)) if name=="VPB_Q2_FIRST" else (6,min(24,pages))
  text=go(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(dest),"-"],100)
  if text.strip():(OUT/(name+"-text.txt")).write_text(text[:75000],"utf-8")
  go(["pdftoppm","-f",str(first),"-l",str(last),
      "-scale-to","1650","-jpeg","-jpegopt","quality=68",str(dest),str(OUT/name)],210)
  count=len(list(OUT.glob(name+"-*.jpg")))
  assert count==last-first+1,count
  print(f"PASS VPB_SOURCE_PAGES name={name} pages_rendered={count}",flush=True)
 except (RuntimeError,AssertionError,subprocess.TimeoutExpired) as e:
  if required:raise
  print(f"VPB_H1_REVIEWED_SOURCE_UNCONFIRMED name={name} reason={str(e)[:250]}",flush=True)
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  for name,url in SOURCES.items():source(name,url,td,required=(name=="VPB_Q2_FIRST"))
 print("PASS VPB 2025 Q2 signed source-only inspection; no production figures promoted",flush=True)
if __name__=="__main__":main()
