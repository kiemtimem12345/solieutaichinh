#!/usr/bin/env python3
"""VPB 2025 Q4 issuer original ZIP source-only QA: recover member hashes and source pages.
FY 2025 audited comparator must be separately verified before normalizing Q4 standalone B04a.
"""
import hashlib, re, subprocess, tempfile, zipfile
from pathlib import Path
OUT=Path("vpb-2025q4-original-source")
URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VPB_Baocaotaichinh_Q4_2025_Hopnhat.zip"
def cmd(args,timeout=140):
    x=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
    if x.returncode: raise RuntimeError(f"{args[0]} exit {x.returncode}: {x.stderr[:300]}")
    return x.stdout
def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);zf=root/"vpbank-q4-original.zip"
        res=cmd(["curl","--location","--silent","--show-error","--connect-timeout","19",
          "--max-time","140","--speed-time","25","--speed-limit","1600",
          "--max-filesize",str(70*1024*1024),"--user-agent","Mozilla/5.0",
          "--output",str(zf),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL],155)
        assert res.startswith("200|") and zf.stat().st_size>60000 and zipfile.is_zipfile(zf),res
        print(f"VPB_Q4_ZIP_VERIFIED bytes={zf.stat().st_size} sha256={hashlib.sha256(zf.read_bytes()).hexdigest()} URL={URL}",flush=True)
        with zipfile.ZipFile(zf) as z:
            print("VPB_Q4_ZIP_MEMBERS="+repr([(q.filename,q.file_size) for q in z.infolist()])[:2500],flush=True)
            members=[m for m in z.infolist() if m.filename.lower().endswith(".pdf") and 60000<m.file_size<70*1024*1024]
            assert members,"No readable source PDF in original archive"
            for i,m in enumerate(members[:3]):
                p=root/f"original-{i}.pdf";p.write_bytes(z.read(m))
                assert p.read_bytes()[:5]==b"%PDF-",m.filename
                meta=cmd(["pdfinfo",str(p)],50)
                mm=re.search(r"^Pages:\s*(\d+)",meta,re.M)
                assert mm,(m.filename,meta[:300])
                pages=int(mm.group(1));assert 16<=pages<=260
                print(f"VPB_Q4_PDF_VERIFIED member={m.filename} bytes={p.stat().st_size} sha256={hashlib.sha256(p.read_bytes()).hexdigest()} pages={pages}",flush=True)
                start,end=4,min(pages,15)
                txt=cmd(["pdftotext","-f",str(start),"-l",str(end),"-layout",str(p),"-"],100)
                (OUT/f"original-{i}-text.txt").write_text(txt[:75000],"utf-8")
                cmd(["pdftoppm","-f",str(start),"-l",str(end),"-scale-to","1500",
                    "-jpeg","-jpegopt","quality=60",str(p),str(OUT/f"original-{i}")],190)
                print(f"PASS VPB_Q4_PDF_RENDER member={m.filename} rendered={end-start+1}",flush=True)
        print("PASS VPB 2025 Q4 ZIP issuer source-only original metadata and visual pages; production figures remain provisional",flush=True)
if __name__=="__main__":main()
