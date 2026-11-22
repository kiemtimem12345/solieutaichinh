#!/usr/bin/env python3
"""Read-only original SHS Q3/2026 issuer and independently reviewed H1/2026.

Capture page images for accounting B01/B02/B03, verify original source hashes,
keep full source PDFs temporary, never write unverified numbers to dashboard.
"""
from pathlib import Path
import hashlib,subprocess,tempfile
FILES={
  "Q3_signed_issuer":("https://s3-storage.shs.com.vn/shs-website/VI_SHS_Bao_Cao_Tai_Chinh_Q3_2026_UB_94d6052636.pdf",1,23),
  "H1_independently_reviewed":("https://s3-storage.shs.com.vn/shs-website/VI_SHS_Bannien_BCTC_2026_f1d999d678.pdf",1,27)
}
OUT=Path("shs-2026q3-h1-signed-source-preview")
OUT.mkdir(exist_ok=True)
def cmd(argv,timeout):
  p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
  if p.returncode: raise RuntimeError(f"{argv[0]} exit {p.returncode}: {p.stderr[:220]}")
  return p.stdout
def main():
  with tempfile.TemporaryDirectory() as directory:
    for key,(url,start,stop) in FILES.items():
      pdf=Path(directory)/(key+".pdf")
      cmd(["curl","--fail","--location","--silent","--show-error","--connect-timeout","12","--max-time","125",
          "--speed-time","15","--speed-limit","8192","--user-agent","Mozilla/5.0",
          "--max-filesize",str(60*1024*1024),"--output",str(pdf),url],145)
      assert pdf.open("rb").read(5)==b"%PDF-",(key,"not PDF")
      info=cmd(["pdfinfo",str(pdf)],30)
      pages=int(next(line.split(":",1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
      assert 30<=pages<=150,(key,pages)
      bytes_=pdf.stat().st_size
      sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
      chars=len(cmd(["pdftotext","-layout",str(pdf),"-"],70))
      print("SIGNED_SOURCE",key,"URL",url,"SHA256",sha,"BYTES",bytes_,"PAGES",pages,"TEXT_CHARS",chars,flush=True)
      last=min(pages,stop)
      cmd(["pdftoppm","-f",str(start),"-l",str(last),"-scale-to","1750",
           "-jpeg","-jpegopt","quality=72",str(pdf),str(OUT/key)],150)
      images=list(OUT.glob(key+"-*.jpg"))
      assert len(images)==last-start+1,(key,len(images),last)
      print("SOURCE_PAGES_RENDERED",key,len(images),"PASS_ONLY_PROVENANCE_NOT_FINANCIAL_RELEASE",flush=True)
if __name__=="__main__":main()
