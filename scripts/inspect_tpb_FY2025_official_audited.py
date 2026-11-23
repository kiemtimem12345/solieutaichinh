#!/usr/bin/env python3
"""Download TPBank official FY2025 audited consolidated PDF: evidence only.

Issuer website direct link is from public TPBank disclosure dated 2026-03-31.
Inspect beginning pages and locate bank signed B02a/B03a/B04a via thumbnails.
Never confuse original Q4 2025 current-quarter column with audited FY data.
"""
import hashlib
import re
import subprocess
import tempfile
from pathlib import Path

OFFICIAL_URL="https://tpb.vn/wps/wcm/connect/f59a40f2-f438-482b-aa7d-a53d3b5f5877/20260331%2B-%2BTPB%2B-%2B2025%2Baudited%2Bconsolidated%2Bfinancial%2Bstatements%2Bwith%2Bdifference%2Bin%2BPAT.pdf?CACHEID=ROOTWORKSPACE-f59a40f2-f438-482b-aa7d-a53d3b5f5877-pR3TNED&CONVERT_TO=url&MOD=AJPERES"
OUT=Path("tpb-2025FY-official-audited")

def run(cmd,seconds):
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=seconds,check=False)
 if p.returncode:raise RuntimeError(f"{cmd[0]} exit {p.returncode}: {p.stderr[:240]}")
 return p.stdout

def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as tmp:
  f=Path(tmp)/"TPB-FY2025-audited-original.pdf"
  resp=run(["curl","--location","--silent","--show-error","--connect-timeout","14","--max-time","145",
    "--speed-time","20","--speed-limit","4096","--max-filesize",str(80*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(f),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",OFFICIAL_URL],160)
  assert resp.startswith("200"),("Official TPB URL failed",resp)
  assert f.exists() and f.stat().st_size>60000,"Official PDF incomplete"
  with f.open("rb") as h:assert h.read(5)==b"%PDF-",("Official site did not return PDF",resp)
  info=run(["pdfinfo",str(f)],50)
  m=re.search(r"^Pages:\s*(\d+)\s*$",info,re.M)
  assert m,"Official original PDF page count missing"
  pages=int(m.group(1))
  assert 20<=pages<=270,pages
  digest=hashlib.sha256(f.read_bytes()).hexdigest()
  print(f"TPB_2025FY_AUDITED_OFFICIAL sha256={digest} bytes={f.stat().st_size} pages={pages} source={OFFICIAL_URL}",flush=True)
  text=run(["pdftotext","-f","1","-l",str(min(30,pages)),"-layout",str(f),"-"],100)
  print("OFFICIAL_AUDITED_TEXT_CHARS",len(text),flush=True)
  if text.strip():(OUT/"tpb-2025FY-first30-pages.txt").write_text(text[:100000],"utf-8")
  first,last=4,min(25,pages)
  run(["pdftoppm","-f",str(first),"-l",str(last),
      "-scale-to","1500","-jpeg","-jpegopt","quality=68",str(f),str(OUT/"TPB-2025FY-AUDITED")],240)
  n=len(list(OUT.glob("TPB-2025FY-AUDITED-*.jpg")))
  assert n==last-first+1,n
  print(f"PASS TPB 2025FY audited official source pages={pages}, original visual pages={n}; production unchanged",flush=True)

if __name__=="__main__":main()
