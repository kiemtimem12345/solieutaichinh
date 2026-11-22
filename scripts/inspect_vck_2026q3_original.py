#!/usr/bin/env python3
"""Read-only VCK 2026Q3 source identity; render first 18 pages of signed issuer PDF."""
from pathlib import Path
import hashlib, subprocess, tempfile
URLS=[
 "https://staticfile.hsx.vn/Uploads/UploadDocuments/2505926/20261020%20-%20VCK%20-%20Bao%20cao%20tai%20chinh%20Quy%203.2026%20-%20signed.pdf",
 "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VCK_Baocaotaichinh_Q3_2026.pdf"
]
OUT=Path("vck-2026q3-source-previews");OUT.mkdir(exist_ok=True)
def run(cmd,timeout):
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
  if p.returncode:raise RuntimeError(f"{cmd[0]} exit {p.returncode}: {p.stderr[:150]}")
  return p.stdout
def main():
 with tempfile.TemporaryDirectory() as root:
  file=Path(root)/"issuer.pdf";source=None
  for url in URLS:
   try:
    run(["curl","--fail","--location","--silent","--show-error",
         "--connect-timeout","9","--max-time","45","--speed-limit","8192",
         "--speed-time","12","--max-filesize",str(38*1024*1024),
         "--user-agent","Mozilla/5.0","--output",str(file),url],54)
    if file.open("rb").read(5)!=b"%PDF-":raise ValueError("non PDF response")
    source=url;break
   except (ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
    print("SOURCE_ACCESS_ALTERNATE_NEEDED",url,repr(exc)[:170],flush=True)
  if source is None:raise SystemExit("SIGNED_SOURCE_NOT_RECOVERED (no data changed)")
  pages=int(next(l.split(":",1)[1] for l in run(["pdfinfo",str(file)],20).splitlines() if l.startswith("Pages:")))
  if pages<35 or pages>130:raise SystemExit("Unexpected pages "+str(pages))
  digest=hashlib.sha256(file.read_bytes()).hexdigest()
  print("SIGNED_ORIGINAL",source,"sha256",digest,"bytes",file.stat().st_size,"pages",pages,flush=True)
  print("PDF_TEXT_CHARS",len(run(["pdftotext","-layout",str(file),"-"],55)),flush=True)
  n=min(pages,18)
  run(["pdftoppm","-f","1","-l",str(n),"-scale-to","1250","-jpeg","-jpegopt","quality=62",str(file),str(OUT/"vck2026q3")],100)
  assert len(list(OUT.glob("vck2026q3-*.jpg")))==n
  print("PASS_SIGNED_ORIGINAL_B01_B02_B03_PREVIEWS",n,flush=True)
if __name__=="__main__":main()
