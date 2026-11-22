#!/usr/bin/env python3
"""Read-only identity proof of VCK 2026Q2 VPS original 61-page issuer PDF.

Do not commit original proprietary PDF. Previews expire after 1 day.
"""
from pathlib import Path
import subprocess, tempfile, hashlib
SOURCE="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/VCK_Baocaotaichinh_Q2_2026.pdf"
OUT=Path("vck-2026q2-original-previews");OUT.mkdir(exist_ok=True)
def run(args,timeout):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
    if p.returncode: raise RuntimeError(args[0]+": "+p.stderr[:250])
    return p.stdout
def main():
    with tempfile.TemporaryDirectory() as directory:
        pdf=Path(directory)/"signed-original.pdf"
        run(["curl","--location","--fail","--silent","--show-error","--max-time","115",
             "--connect-timeout","14","--speed-limit","8192","--speed-time","16",
             "--max-filesize",str(40*1024*1024),"--user-agent","Mozilla/5.0",
             "--output",str(pdf),SOURCE],130)
        assert pdf.open("rb").read(5)==b"%PDF-","not a PDF"
        n=pdf.stat().st_size
        assert 800000<n<40*1024*1024,n
        info=run(["pdfinfo",str(pdf)],20)
        pages=int(next(line.split(":",1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
        assert pages>=58 and pages<=75,pages
        print("ORIGINAL_SOURCE",SOURCE,flush=True)
        print("SOURCE_SHA256",hashlib.sha256(pdf.read_bytes()).hexdigest(),"bytes",n,"pages",pages,flush=True)
        txt=run(["pdftotext","-layout",str(pdf),"-"],70)
        print("TEXT_CHARS",len(txt),flush=True)
        npreview=19
        run(["pdftoppm","-f","1","-l",str(npreview),"-jpeg","-scale-to","1500",
             "-jpegopt","quality=65",str(pdf),str(OUT/"VCK_2026Q2")],130)
        images=list(OUT.glob("VCK_2026Q2-*.jpg"))
        assert len(images)==npreview,len(images)
        print("VISUAL_PREVIEW_COUNT",len(images),"B01 B02 B03 customer-separate",flush=True)
        print("PASS_SOURCE_IDENTITY_ONLY",flush=True)
if __name__=="__main__":main()
