#!/usr/bin/env python3
"""VCB 2026Q2 official HOSE issuer consolidated original; transient visual source QA."""
from pathlib import Path
import subprocess,hashlib,tempfile
SOURCES=[
"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCB_Baocaotaichinh_Q2_2026_Hopnhat.pdf"
]
OUT=Path("vcb-2026q2-consolidated-preview");OUT.mkdir(exist_ok=True)
def run(args,seconds):
    p=subprocess.run(args,text=True,capture_output=True,timeout=seconds)
    if p.returncode:raise RuntimeError(args[0]+" exit "+str(p.returncode)+" "+p.stderr[:200])
    return p.stdout
def main():
  with tempfile.TemporaryDirectory() as tmp:
    pdf=Path(tmp)/"source.pdf"
    for url in SOURCES:
      try:
        run(["curl","--location","--fail","--show-error","--silent","--max-time","115",
             "--connect-timeout","15","--speed-limit","8192","--speed-time","16",
             "--max-filesize",str(48*1024*1024),"--user-agent","Mozilla/5.0",
             "--output",str(pdf),url],130)
        if pdf.open("rb").read(5)!=b"%PDF-":raise ValueError("non PDF response")
        break
      except (RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:
        print("SOURCE_RETRY_REQUIRED",url,str(exc)[:250],flush=True)
    else:
      raise SystemExit("ISSUER_ORIGINAL_SOURCE_RETRIEVAL_FAILED; no financial production data changed")
    info=run(["pdfinfo",str(pdf)],30)
    pages=int(next(x.split(":",1)[1].strip() for x in info.splitlines() if x.startswith("Pages:")))
    assert 10<=pages<=150,pages
    print("SIGNED_ORIGINAL_SOURCE",url,"sha256",hashlib.sha256(pdf.read_bytes()).hexdigest(),"pages",pages,"bytes",pdf.stat().st_size,flush=True)
    t=run(["pdftotext","-layout",str(pdf),"-"],55)
    print("SOURCE_TEXT_CHARS",len(t),flush=True)
    n=min(32,pages)
    run(["pdftoppm","-f","1","-l",str(n),"-scale-to","1450","-jpeg","-jpegopt","quality=67",str(pdf),str(OUT/"VCB_2026Q2")],140)
    assert len(list(OUT.glob("VCB_2026Q2-*.jpg")))==n
    print("SOURCE_EVIDENCE_PREVIEWS",n,flush=True)
    print("PASS_SOURCE_ONLY_NO_NUMERIC_RELEASE",flush=True)
if __name__=="__main__":main()
