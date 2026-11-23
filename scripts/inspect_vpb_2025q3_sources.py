#!/usr/bin/env python3
"""Read-only recover VPB Q3 2025 first-issued ZIP and issuer lookup PDF, log SHA and render bank pages.
No production number is promoted by this source-only inspection.
"""
import hashlib, zipfile, subprocess, tempfile, re
from pathlib import Path
OUT=Path("vpb-2025q3-source")
URL_ZIP="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/VPB_Baocaotaichinh_Q3_2025_Hopnhat.zip"
URL_ISSUER="https://www.vpbank.com.vn/-/media/vpbank-latest/5nha-dau-tu/bao-cao-tai-chinh/vas/nam-2025/q3/3-bctc-hop-nhat-ban-tra-cuu.pdf"
def sh(args,seconds=100):
    p=subprocess.run(args,capture_output=True,text=True,timeout=seconds,check=False)
    if p.returncode: raise RuntimeError(f"{args[0]} exit {p.returncode}: {p.stderr[:350]}")
    return p.stdout
def fetch(url,dest):
    out=sh(["curl","--location","--silent","--show-error","--connect-timeout","18",
      "--max-time","125","--speed-time","24","--speed-limit","1500","--max-filesize",str(60*1024*1024),
      "--user-agent","Mozilla/5.0","--output",str(dest),"--write-out","%{http_code}|%{content_type}|%{size_download}",url],145)
    assert out.startswith("200|") and dest.stat().st_size>60000,(out,dest)
    print(f"VPB_2025Q3_SOURCE_DOWNLOAD type={dest.suffix} HTTP={out} SHA256={hashlib.sha256(dest.read_bytes()).hexdigest()} URL={url}",flush=True)
def pdf(name,path):
    assert path.read_bytes()[:5]==b"%PDF-",name
    info=sh(["pdfinfo",str(path)])
    m=re.search(r"^Pages:\s*(\d+)",info,re.M); assert m,info[:400]
    n=int(m.group(1));print(f"VPB_2025Q3_PDF name={name} bytes={path.stat().st_size} SHA256={hashlib.sha256(path.read_bytes()).hexdigest()} pages={n}",flush=True)
    first,last=4,min(15,n)
    txt=sh(["pdftotext","-f",str(first),"-l",str(last),"-layout",str(path),"-"],95)
    (OUT/(name+"-extracted.txt")).write_text(txt[:65000],"utf-8")
    sh(["pdftoppm","-f",str(first),"-l",str(last),"-scale-to","1500",
        "-jpeg","-jpegopt","quality=62",str(path),str(OUT/name)],150)
    print(f"PASS VPB_2025Q3_RENDER name={name} pages={last-first+1}",flush=True)
def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)
        z=t/"vietstock.zip";fetch(URL_ZIP,z)
        assert zipfile.is_zipfile(z),"Original is not valid ZIP"
        with zipfile.ZipFile(z) as f:
            names=f.namelist()
            print("VPB_2025Q3_ZIP_MEMBERS="+repr([(x.filename,x.file_size) for x in f.infolist()])[:2500],flush=True)
            pdfs=[x for x in f.infolist() if x.filename.lower().endswith(".pdf") and 60000<x.file_size<60*1024*1024]
            assert pdfs,"Original ZIP has no safe PDF"
            for i,m in enumerate(pdfs[:3]):
                p=t/f"orig-{i}.pdf";p.write_bytes(f.read(m));pdf(f"original-{i}",p)
        p=t/"issuer.pdf";fetch(URL_ISSUER,p);pdf("vpbank-issuer-lookup",p)
    print("PASS VPB 2025 Q3 original ZIP and issuer PDF source-only inspection, no production figures promoted",flush=True)
if __name__=="__main__":main()
