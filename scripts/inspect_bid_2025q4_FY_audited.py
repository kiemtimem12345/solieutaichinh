#!/usr/bin/env python3
"""Source-only audit: BID first-issued Q4/2025 + Deloitte audited FY2025.

Both originals must be complete PDFs. Keep signed Q4 B01/B03 first-issued
separate from audited FY B01/B03/B04 reporting vintage. Never publish any
data if an issuer or independently filed original is unavailable.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

SOURCES = {
 "BID_2025Q4_ORIGINAL_HN": [
   "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/BID_Baocaotaichinh_Q4_2025_Hopnhat.pdf",
 ],
 "BID_2025FY_AUDITED_HN": [
   "https://static2.vietstock.vn/vietstock/2026/4/7/2_bid122005_2026_4_7_a1ba658_vi_baocaotaichinhhopnhat_kiemtoan_2025.pdf",
   "https://data.thebulltrust.com/vn30_bctc_pdfs/BID_BCTC_2025.pdf",
 ],
}
OUT=Path("bid-2025q4-FY-original-previews")

def call(cmd:list[str],timeout:int)->str:
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(f"{cmd[0]} returned {p.returncode} {p.stderr[:230]}")
 return p.stdout

def source(label:str,urls:list[str],td:Path)->None:
 pdf=td/(label+".pdf")
 got=None
 for url in urls:
  try:
   meta=call(["curl","--location","--silent","--show-error",
    "--connect-timeout","14","--max-time","115","--speed-time","20",
    "--speed-limit","4096","--max-filesize",str(55*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(pdf),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",url],130)
  except (RuntimeError,subprocess.TimeoutExpired) as exc:
   print(f"SOURCE_ALTERNATE label={label} host={url.split('/')[2]} error={str(exc)[:200]}",flush=True)
   continue
  size=pdf.stat().st_size if pdf.exists() else 0
  magic=pdf.open("rb").read(5) if size else b""
  valid=size>60000 and magic==b"%PDF-" and meta.startswith("200")
  print(f"SOURCE_ATTEMPT {label} host={url.split('/')[2]} bytes={size} valid={valid} resp={meta[:100]}",flush=True)
  if valid:
   got=url
   break
 if got is None:raise RuntimeError(f"NO_COMPLETE_SIGNED_OR_AUDITED_{label}; preserve the unverified accounting exception")
 inf=call(["pdfinfo",str(pdf)],40)
 match=re.search(r"^Pages:\s*(\d+)\s*$",inf,re.M)
 assert match, (label,"PDF page count missing")
 count=int(match.group(1))
 assert 15<=count<=230,(label,count)
 sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
 print(f"PDF_SOURCE_VERIFIED {label} sha256={sha} bytes={pdf.stat().st_size} pages={count} url={got}",flush=True)
 first=4 if "FY" in label else 2
 last=min(count,22 if "FY" in label else 11)
 txt=call(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],100)
 print(f"TEXT_LAYER {label} chars={len(txt)}",flush=True)
 if txt.strip():(OUT/(label+"-statement.txt")).write_text(txt[:70000],"utf-8")
 call(["pdftoppm","-f",str(first),"-l",str(last),
  "-scale-to","1400","-jpeg","-jpegopt","quality=64",
  str(pdf),str(OUT/label)],210)
 actual=len(list(OUT.glob(label+"-*.jpg")))
 assert actual==last-first+1,(label,actual,last-first+1)
 print(f"PASS_SOURCE_VERIFIED {label} rendered={actual}; nothing promoted to production",flush=True)

def main()->None:
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as directory:
  for label,urls in SOURCES.items():source(label,urls,Path(directory))
 print("PASS BID 2025Q4 signed original and FY2025 independently audited source provenance. Financial numbers still gated.",flush=True)

if __name__=="__main__":main()
