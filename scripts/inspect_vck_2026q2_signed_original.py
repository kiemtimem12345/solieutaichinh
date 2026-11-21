#!/usr/bin/env python3
"""VPS VCK 2026Q2 issuer signed PDF evidence, no unsupported financial writes."""
import hashlib,subprocess,tempfile
from pathlib import Path
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCK_Baocaotaichinh_Q2_2026.pdf"
OUT=Path("vck-2026q2-source-previews");OUT.mkdir(exist_ok=True)
def main():
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/"vck-q2-original.pdf"
  cmd=["curl","--location","--silent","--show-error","--fail","--max-time","100",
    "--connect-timeout","12","--speed-limit","8192","--speed-time","20",
    "--max-filesize",str(50*1024*1024),"--user-agent","Mozilla/5.0",
    "--output",str(p),URL]
  r=subprocess.run(cmd,text=True,capture_output=True,timeout=112)
  if r.returncode:raise SystemExit("PDF_SOURCE_UNAVAILABLE curl exit=%d %s"%(r.returncode,r.stderr[:150]))
  if p.open("rb").read(5)!=b"%PDF-":raise SystemExit("Not PDF")
  digest=hashlib.sha256(p.read_bytes()).hexdigest()
  meta=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=24,check=True).stdout
  pages=int(next(x.split(":",1)[1].strip() for x in meta.splitlines() if x.startswith("Pages:")))
  if not 12<=pages<=180:raise SystemExit("Invalid PDF pages="+str(pages))
  print("SOURCE_PDF",URL,"sha256",digest,"bytes",p.stat().st_size,"pages",pages,flush=True)
  txt=subprocess.run(["pdftotext","-layout",str(p),"-"],capture_output=True,timeout=80)
  print("TEXT_CHARACTERS",len(txt.stdout),flush=True)
  n=min(pages,26)
  cmd=["pdftoppm","-f","1","-l",str(n),"-scale-to","1500","-jpeg",
    "-jpegopt","quality=65",str(p),str(OUT/"VCK_Q2_2026")]
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=160)
  if r.returncode:raise SystemExit("Page render failed "+r.stderr[:130])
  imgs=list(OUT.glob("VCK_Q2_2026-*.jpg"))
  print("VISUAL_PAGES",len(imgs),flush=True)
  if len(imgs)!=n:raise SystemExit("Incomplete source images")
  print("PASS source identity; accounting B01/B02/B03 needs original-page verification",flush=True)
if __name__=="__main__":main()
