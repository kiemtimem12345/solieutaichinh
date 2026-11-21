#!/usr/bin/env python3
"""Recover VCK Q3/2025 original VPS/VPSS issuer ZIP, inspect PDF identities.

Evidence-only. Exact issuer filing scope first. Never write numeric dashboard
data without source and accounting reconciliation.
"""
import hashlib,shutil,subprocess,tempfile,zipfile
from pathlib import Path

URL="https://static2.vietstock.vn/data/OTC/2025/BCTC/VN/QUY%203/VPSS_Baocaotaichinh_Q3_2025.zip"
OUT=Path("vck-2025q3-original-previews")
OUT.mkdir(exist_ok=True)
def execute(argv,timeout):
    p=subprocess.run(argv,text=True,capture_output=True,timeout=timeout)
    if p.returncode:raise RuntimeError(f"{argv[0]} exit={p.returncode}: {p.stderr[:190]}")
    return p.stdout
def main():
    with tempfile.TemporaryDirectory() as folder:
        base=Path(folder);archive=base/"vck-q3-original.zip"
        execute(["curl","--location","--silent","--show-error","--fail",
                 "--connect-timeout","12","--max-time","100","--speed-limit","8192",
                 "--speed-time","20","--max-filesize",str(50*1024*1024),
                 "--user-agent","Mozilla/5.0","--output",str(archive),URL],115)
        assert archive.read_bytes()[:2]==b"PK","Not ZIP"
        sha=hashlib.sha256(archive.read_bytes()).hexdigest()
        print("ARCHIVE_SOURCE",URL,"sha256",sha,"bytes",archive.stat().st_size,flush=True)
        with zipfile.ZipFile(archive) as z:
            matches=[x for x in z.infolist() if x.filename.lower().endswith(".pdf") and not x.is_dir() and x.file_size<=50*1024*1024]
            print("PDF_MEMBERS",[(x.filename[:100],x.file_size) for x in matches[:8]],flush=True)
            if not matches:raise SystemExit("NO_PDF_MEMBER")
            statements=[x for x in matches if "baocaotaichinh" in x.filename.lower().replace("_","").replace(" ","") or "financialstatement" in x.filename.lower().replace("_","").replace(" ","")]
            if not statements:raise SystemExit("STATEMENT_PDF_NOT_FOUND; never extract explanation instead")
            member=sorted(statements,key=lambda item:item.file_size,reverse=True)[0]
            print("SELECTED_SIGNED_STATEMENT_MEMBER",member.filename,"bytes",member.file_size,flush=True)
            pdf=base/"issuer.pdf"
            with z.open(member) as inp,pdf.open("wb") as out:shutil.copyfileobj(inp,out)
        assert pdf.open("rb").read(5)==b"%PDF-","Not PDF"
        lines=execute(["pdfinfo",str(pdf)],25).splitlines()
        pages=int(next(x.split(":",1)[1].strip() for x in lines if x.startswith("Pages:")))
        assert 20<=pages<=180
        print("ORIGINAL_PDF","pdf_sha256",hashlib.sha256(pdf.read_bytes()).hexdigest(),"bytes",pdf.stat().st_size,"pages",pages,flush=True)
        extracted=subprocess.run(["pdftotext","-layout",str(pdf),"-"],text=True,capture_output=True,timeout=90)
        print("SOURCE_TEXT_CHARS",len(extracted.stdout),"returncode",extracted.returncode,flush=True)
        # These pages cover cover, signed issuer B01, B02, B03 and scope notes.
        cap=min(pages,24)
        execute(["pdftoppm","-f","1","-l",str(cap),"-scale-to","1500","-jpeg",
                 "-jpegopt","quality=66",str(pdf),str(OUT/"VCK_Q3_2025")],155)
        imgs=list(OUT.glob("VCK_Q3_2025-*.jpg"))
        assert len(imgs)==cap
        print("SIGNED_SOURCE_PREVIEWS",len(imgs),flush=True)
        print("PASS Q3 original evidence only; financial line items require visual/source verification",flush=True)
if __name__=="__main__":main()
