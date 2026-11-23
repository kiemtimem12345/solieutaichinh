#!/usr/bin/env python3
"""Read-only VPB Q1/2026 original consolidated ZIP source inspection, bank B02a/B03a/B04a.
Recover source archive and exact source member hashes; do not promote provisional OCR.
"""
from pathlib import Path
import hashlib, subprocess, tempfile, zipfile, re
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/VPB_Baocaotaichinh_Q1_2026_Hopnhat.zip"
OUT=Path("vpb-2026q1-first-issuer-source")
def run(args,t=125):
 p=subprocess.run(args,capture_output=True,text=True,timeout=t,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} code={p.returncode}: {p.stderr[:280]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  t=Path(td);zfn=t/"vpb-q1.zip"
  response=run(["curl","--location","--silent","--show-error","--connect-timeout","20","--max-time","145",
    "--speed-time","27","--speed-limit","1800","--max-filesize",str(65*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(zfn),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],160)
  assert response.startswith("200|") and zfn.stat().st_size>50000 and zipfile.is_zipfile(zfn),response
  print("VPB_Q1_2026_ARCHIVE verified HTTP="+response+
    " bytes="+str(zfn.stat().st_size)+" sha256="+hashlib.sha256(zfn.read_bytes()).hexdigest()+
    " source="+URL,flush=True)
  with zipfile.ZipFile(zfn) as z:
   members=z.infolist()
   print("VPB_Q1_2026_MEMBERS "+repr([(m.filename,m.file_size) for m in members]),flush=True)
   picks=[m for m in members if m.filename.lower().endswith(".pdf") and m.file_size>60000 and m.file_size<80*1024*1024]
   assert picks,"No source PDF members"
   for i,m in enumerate(picks[:4]):
    f=t/("source"+str(i)+".pdf");f.write_bytes(z.read(m))
    assert f.read_bytes()[:5]==b"%PDF-",m.filename
    meta=run(["pdfinfo",str(f)])
    pp=re.search(r"^Pages:\s*(\d+)",meta,re.M);assert pp,m.filename
    count=int(pp.group(1));assert 15<=count<=240,count
    print(f"VPB_Q1_2026_PDF member={m.filename} pages={count} bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()}",flush=True)
    start,stop=4,min(count,16)
    txt=run(["pdftotext","-layout","-f",str(start),"-l",str(stop),str(f),"-"],125)
    (OUT/(f"member-{i}-text.txt")).write_text(txt[:80000],"utf-8")
    print(f"VPB_Q1_2026_STATEMENTS_BEGIN member={m.filename} pages={start}-{stop} chars={len(txt)}",flush=True)
    print(txt[:34000],flush=True)
    print(f"VPB_Q1_2026_STATEMENTS_END member={m.filename}",flush=True)
  print("PASS VPB 2026 Q1 original ZIP source recovery; no production figures changed",flush=True)
if __name__=="__main__":main()
