#!/usr/bin/env python3
"""Read-only IDC 2026-Q3 consolidated source recovery from HNX and BSC/HNX copies.

Original issuer B01/B02/B03 is a prerequisite to recording figures.
Never publish OCR-only values or mix consolidated and parent PDF scopes.
"""
import hashlib,io,re,subprocess,sys,zipfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,urlopen
import fitz

URLS=[
("bsc1","https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1"),
("bsc2","https://www.bsc.com.vn/News/NewsAttachedFile/1632697-2"),
("bsc3","https://www.bsc.com.vn/News/NewsAttachedFile/1632697-3"),
("bsc4","https://www.bsc.com.vn/News/NewsAttachedFile/1632697-4"),
("hnx_vi_consolidated","https://owa.hnx.vn/ftp///cims/2026/10_W5/000000016989520_VI_BaoCaoTaiChinhHN_Q3_2026_signed.pdf"),
("vietstock_zip","https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2026_Hopnhat.zip"),
("vietstock_pdf","https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2026_Hopnhat.pdf"),
]
HOSTS={"www.bsc.com.vn","bsc.com.vn","owa.hnx.vn","static2.vietstock.vn"}
MAXSIZE=55*1024*1024
out=Path("idc-q3-report-images");out.mkdir(exist_ok=True)

def download(label,url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (finance source QA)",
        "Accept":"application/pdf,application/zip,application/octet-stream,*/*",
        "Accept-Encoding":"identity","Referer":"https://www.bsc.com.vn/"})
    with urlopen(req,timeout=25) as response:
        dest=urlparse(response.url)
        if dest.scheme!="https" or dest.hostname not in HOSTS:raise ValueError("Disallowed redirect")
        if int(response.headers.get("Content-Length") or "0")>MAXSIZE:raise ValueError("Oversize")
        chunks=[];size=0
        while True:
            buf=response.read(1024*1024)
            if not buf:break
            size+=len(buf)
            if size>MAXSIZE:raise ValueError("Oversize")
            chunks.append(buf)
    buf=b"".join(chunks)
    print(f"SOURCE_OK label={label} bytes={len(buf)} sha256={hashlib.sha256(buf).hexdigest()} magic={buf[:8].hex()}",flush=True)
    return buf

def inspect(label,blob):
    doc=fitz.open(stream=blob,filetype="pdf")
    print(f"PDF_OK label={label} pages={len(doc)} SHA256={hashlib.sha256(blob).hexdigest()}",flush=True)
    for i in range(min(len(doc),18)):
        page=doc[i]
        text=page.get_text(sort=True)
        pix=page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
        f=out/f"{label}-p{i+1:02d}.png";pix.save(f)
        if len(text.strip())<300 or len(re.findall(r"\d",text))<15:
            try:
                t=subprocess.run(["tesseract",str(f),"stdout","-l","eng","--psm","6",
                    "-c","preserve_interword_spaces=1"],capture_output=True,text=True,check=True,timeout=55)
                text=t.stdout;method="OCR_UNVERIFIED"
            except Exception as exc:text=str(exc);method="OCR_FAILED"
        else:method="PDF_TEXT"
        print(f"REPORT_PAGE_BEGIN source={label} page={i+1} method={method}",flush=True)
        print(text[:10000],flush=True)
        print(f"REPORT_PAGE_END source={label} page={i+1}",flush=True)
    print(f"RENDER_PASS source={label}; financial values require human source image QA",flush=True)

def main():
    count=0
    for label,url in URLS:
        try:
            b=download(label,url)
            if b.startswith(b"%PDF"):
                inspect(label,b);count+=1
            elif b.startswith(b"PK\x03\x04"):
                with zipfile.ZipFile(io.BytesIO(b)) as z:
                    files=[x for x in z.infolist() if x.filename.lower().endswith(".pdf") and 1000<x.file_size<MAXSIZE]
                    print(f"ZIP_OK label={label} pdf_count={len(files)}",flush=True)
                    for ix,x in enumerate(files[:5]):
                        member=z.read(x)
                        if member.startswith(b"%PDF"):inspect(label+f"_pdf{ix}",member);count+=1
            else:raise ValueError("Neither PDF nor ZIP")
        except Exception as exc:
            print(f"SOURCE_UNAVAILABLE label={label} {type(exc).__name__}: {str(exc)[:180]}",flush=True)
    if count==0:print("::error::IDC consolidated source inaccessible; no figures published",flush=True);return 1
    print(f"SOURCE_RECOVERY_PASS pdf_documents={count}; images require independent original visual review",flush=True)
    return 0

if __name__=="__main__":sys.exit(main())
