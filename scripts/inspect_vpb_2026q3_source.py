#!/usr/bin/env python3
"""VPB 2026Q3 signed original consolidated issuer ZIP source-only inspector."""
from pathlib import Path
import zipfile,hashlib,subprocess,tempfile,re
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VPB_Baocaotaichinh_Q3_2026_Hopnhat.zip"
OUT=Path("vpb-2026q3-source")
def cmd(args,timeout=130):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(f"{args[0]} {p.stderr[:250]}")
 return p.stdout
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/"original.zip"
  res=cmd(["curl","-L","--silent","--show-error","--connect-timeout","18",
    "--max-time","135","--speed-time","26","--speed-limit","1800","--max-filesize",str(75*1024*1024),
    "--user-agent","Mozilla/5.0","--output",str(f),
    "--write-out","%{http_code}|%{content_type}|%{size_download}",URL],150)
  assert res.startswith("200|") and f.stat().st_size>50000 and zipfile.is_zipfile(f),res
  print(f"VPB_Q3_2026_ZIP bytes={f.stat().st_size} sha256={hashlib.sha256(f.read_bytes()).hexdigest()} URL={URL}",flush=True)
  with zipfile.ZipFile(f) as z:
   print("VPB_Q3_2026_MEMBERS "+repr([(q.filename,q.file_size) for q in z.infolist()]),flush=True)
   for idx,m in enumerate([x for x in z.infolist() if x.filename.lower().endswith(".pdf") and x.file_size>50000][:3]):
    path=Path(td)/f"original-{idx}.pdf";path.write_bytes(z.read(m))
    assert path.read_bytes()[:5]==b"%PDF-"
    meta=cmd(["pdfinfo",str(path)])
    mm=re.search(r"^Pages:\s*(\d+)",meta,re.M);assert mm
    n=int(mm.group(1))
    print(f"VPB_Q3_2026_PDF member={m.filename} pages={n} bytes={path.stat().st_size} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}",flush=True)
    first,last=4,min(n,18)
    raw=cmd(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(path),"-"],100)
    (OUT/f"pdf-{idx}-text.txt").write_text(raw[:105000],"utf8")
    print(f"VPB_Q3_2026_TEXT_START member={m.filename}",flush=True)
    print(raw[:53000],flush=True)
    print(f"VPB_Q3_2026_TEXT_END member={m.filename}",flush=True)
 print("PASS VPB Q3 2026 original source inspection, production unchanged",flush=True)
if __name__=="__main__":main()
