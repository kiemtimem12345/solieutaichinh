#!/usr/bin/env python3
"""Read-only issuer original VPB 2025 Q1 consolidated bank source inspection.

Retrieve exact signed B02a/B03a/B04a source before promoting OCR-provisional
figures. Recover original PDF SHA/pages and visual original statement crops,
do not change site rows until signed source identities and FX cash pass.
"""
from pathlib import Path
import hashlib,re,subprocess,tempfile

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/VPB_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
OUT=Path("vpb-2025q1-original-evidence")
def go(args,seconds=90):
 p=subprocess.run(args,capture_output=True,text=True,timeout=seconds,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} error {p.returncode}: {p.stderr[:260]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as d:
  pdf=Path(d)/"VPB-2025Q1-original.pdf"
  args=["curl","--location","--silent","--show-error","--connect-timeout","20",
   "--max-time","155","--speed-time","27","--speed-limit","2500",
   "--max-filesize",str(65*1024*1024),"--user-agent","Mozilla/5.0",
   "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL]
  resp=go(args,175)
  assert resp.startswith("200"),resp
  assert pdf.exists() and pdf.stat().st_size>60000,"Original bank PDF unavailable or truncated"
  with pdf.open("rb") as f:assert f.read(5)==b"%PDF-","Source is not actual PDF"
  info=go(["pdfinfo",str(pdf)],40)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"PDF pages unavailable"
  pages=int(m.group(1))
  assert 15<=pages<=210,pages
  digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"VPB_2025Q1_SIGNED_SOURCE sha256={digest} bytes={pdf.stat().st_size} pages={pages} URL={URL}",flush=True)
  first,last=4,min(20,pages)
  layer=go(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],95)
  print(f"VPB_2025Q1_TEXT_LAYER chars={len(layer)}",flush=True)
  if layer.strip():(OUT/"VPB-2025Q1-source-text.txt").write_text(layer[:80000],"utf-8")
  go(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1650",
      "-jpeg","-jpegopt","quality=68",str(pdf),str(OUT/"VPB-2025Q1-HN")],200)
  n=len(list(OUT.glob("VPB-2025Q1-HN-*.jpg")))
  assert n==last-first+1,(n,last-first+1)
  print(f"PASS VPB_Q1_2025_SOURCE_PROVENANCE original_visual_pages={n}, data unchanged",flush=True)
if __name__=="__main__":main()
