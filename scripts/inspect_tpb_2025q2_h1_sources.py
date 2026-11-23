#!/usr/bin/env python3
"""Source-only TPB signed 2025 Q2 consolidated and reviewed 2025 H1 bank PDF.

The original Q1/2025 54-page consolidated source is already verified and
must be reused, not reprocessed. The reviewed 2025 H1 PDF is the HOSE
disclosure dated 18 Aug 2025, separate from first-issued Q2. Reject HTML,
corrupted, blocked or truncated PDF before any financial promotion.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

SOURCES={
 "TPB_2025Q2_ORIGINAL_HN":[
   "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/TPB_Baocaotaichinh_Q2_2025_Hopnhat.pdf",
 ],
 "TPB_2025H1_REVIEWED_HN":[
   "https://staticfile.hsx.vn/Uploads/UploadDocuments/2398174/20250818%20-%20TPB%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%20soat%20xet%20ban%20nien%202025%20kem%20giai%20trinh%20chenh%20lech%20LNST_signed.pdf",
   "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/TPB_Baocaotaichinh_6T_2025_Soatxet_Hopnhat.pdf",
 ]
}
OUT=Path("tpb-2025q2-h1-source-preview")
def run(args,timeout):
 p=subprocess.run(args,capture_output=True,text=True,check=False,timeout=timeout)
 if p.returncode:raise RuntimeError(f"{args[0]} exit={p.returncode}: {p.stderr[:200]}")
 return p.stdout

def inspect(label,urls,directory):
 pdf=directory/(label+".pdf")
 good=None
 for url in urls:
  try:
   result=run(["curl","--location","--silent","--show-error",
      "--connect-timeout","13","--max-time","75","--speed-time","15",
      "--speed-limit","4096","--max-filesize",str(52*1024*1024),
      "--user-agent","Mozilla/5.0 (original-financial-review)",
      "--output",str(pdf),"--write-out","%{http_code}|%{content_type}|%{size_download}",
      url],88)
  except (RuntimeError,subprocess.TimeoutExpired) as exc:
   print(f"SOURCE_ALTERNATE label={label} host={url.split('/')[2]} error={str(exc)[:180]}",flush=True)
   continue
  size=pdf.stat().st_size if pdf.exists() else 0
  magic=pdf.open("rb").read(5) if size else b""
  valid=size>60000 and magic==b"%PDF-" and result.startswith("200")
  print(f"SOURCE_ATTEMPT {label} host={url.split('/')[2]} bytes={size} valid={valid} response={result[:110]}",flush=True)
  if valid:
   good=url
   break
 if good is None:raise RuntimeError(f"NO_COMPLETE_SIGNED_{label}; financial publication must remain gated")
 info=run(["pdfinfo",str(pdf)],40)
 m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
 assert m, "Missing source PDF page count"
 count=int(m.group(1))
 assert 15<=count<=160,(label,count)
 sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
 print(f"TPB_ORIGINAL_SOURCE {label} sha256={sha} bytes={pdf.stat().st_size} pages={count} url={good}",flush=True)
 first,last=(4,min(count,14)) if "Q2_ORIGINAL" in label else (7,min(count,20))
 body=run(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(pdf),"-"],80)
 print(f"TEXT_LAYER label={label} chars={len(body)}",flush=True)
 if body.strip():(OUT/(label+"-excerpt.txt")).write_text(body[:60000],"utf-8")
 run(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1550",
      "-jpeg","-jpegopt","quality=68",str(pdf),str(OUT/label)],180)
 got=len(list(OUT.glob(label+"-*.jpg")))
 assert got==last-first+1,(label,got)
 print(f"PASS TPB_SOURCE_PROVENANCE {label} original_pages_rendered={got}; data unmodified",flush=True)

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as d:
  for label,urls in SOURCES.items():inspect(label,urls,Path(d))
 print("PASS TPB 2025Q2 signed original and independently reviewed 2025H1 provenance; source-only, no data changes.",flush=True)
if __name__=="__main__":main()
