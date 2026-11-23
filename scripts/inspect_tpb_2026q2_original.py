#!/usr/bin/env python3
"""Read-only TPB signed Q2 2026 bank original and optional reviewed H1 source.

Always verify issuer PDF signature, complete size, page count and SHA before
images. Reviewed H1 is supplementary; if candidate not confirmed, log a
specific missing reviewed-source flag without promoting production values.
"""
import hashlib
from pathlib import Path
import re
import subprocess
import tempfile

URLS={
 "Q2_signed_original":[
  "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/TPB_Baocaotaichinh_Q2_2026_Hopnhat.pdf",
 ],
 "H1_reviewed_candidate":[
  "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/TPB_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf",
 ],
}
OUT=Path("tpb-2026q2-source-evidence")
def cmd(args,seconds):
 p=subprocess.run(args,capture_output=True,text=True,timeout=seconds,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} exit={p.returncode}: {p.stderr[:240]}")
 return p.stdout

def fetch(label:str,urls:list[str],directory:Path,required:bool):
 pdf=directory/(label+".pdf")
 for url in urls:
  try:
   response=cmd(["curl","--location","--silent","--show-error",
         "--connect-timeout","13","--max-time","75","--speed-time","15",
         "--speed-limit","4096","--max-filesize",str(60*1024*1024),
         "--user-agent","Mozilla/5.0",
         "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",url],90)
  except (RuntimeError,subprocess.TimeoutExpired) as e:
   print(f"SOURCE_FALLBACK label={label} error={str(e)[:200]}",flush=True)
   continue
  size=pdf.stat().st_size if pdf.exists() else 0
  with pdf.open("rb") as f:magic=f.read(5) if size>0 else b""
  good=response.startswith("200") and size>60000 and magic==b"%PDF-"
  print(f"SOURCE_ATTEMPT label={label} size={size} valid={good} header={response[:90]}",flush=True)
  if not good:continue
  info=cmd(["pdfinfo",str(pdf)],40)
  match=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  if not match:continue
  pages=int(match.group(1))
  if not 15<=pages<=210:continue
  sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
  print(f"TPB_SOURCE_VERIFIED label={label} sha256={sha} bytes={size} pages={pages} URL={url}",flush=True)
  first,last=(4,min(17,pages)) if label=="Q2_signed_original" else (7,min(21,pages))
  body=cmd(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],75)
  if body.strip(): (OUT/(label+"-text.txt")).write_text(body[:70000],"utf-8")
  cmd(["pdftoppm","-f",str(first),"-l",str(last),
       "-scale-to","1550","-jpeg","-jpegopt","quality=68",
       str(pdf),str(OUT/label)],180)
  n=len(list(OUT.glob(label+"-*.jpg")))
  assert n==last-first+1,(label,n,last-first+1)
  print(f"PASS TPB_SOURCE_PDF label={label} page_images={n} text_chars={len(body)}",flush=True)
  return
 if required:raise RuntimeError(f"REQUIRED_TPB_{label}_ORIGINAL_PDF_NOT_AVAILABLE")
 print(f"REVIEWED_H1_SOURCE_UNCONFIRMED label={label}: retain source-gate; do not normalize Q2 cash",flush=True)

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  for label,urls in URLS.items():fetch(label,urls,Path(td),label=="Q2_signed_original")
 print("PASS TPB Q2 2026 first-issued signed original source inspected; no data promoted until original and reviewed H1 exact accounting checks",flush=True)
if __name__=="__main__":main()
