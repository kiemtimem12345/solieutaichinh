#!/usr/bin/env python3
"""Visual QA of IDC consolidated original 2026Q2 6M report from archived HNX PDF.

Read-only source inspection; print JPEGs for human comparison (not OCR-only).
Allows exactly the VietstockFinance-linked original issuer HNX archive.
Never write data/financials-IDC.json or publish provisional numbers.
"""
import base64, hashlib, io, sys, zipfile
from urllib.parse import urlparse
from urllib.request import Request,urlopen
import fitz
from PIL import Image
SOURCE="https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%202/IDC_Baocaotaichinh_Q2_2026_Hopnhat.zip?ver=fec9e0e5"
MAX=60*1024*1024
request=Request(SOURCE,headers={"User-Agent":"Mozilla/5.0 (issuer original BCTC source QA)","Accept-Encoding":"identity","Referer":"https://finance.vietstock.vn/"})
with urlopen(request,timeout=65) as response:
    redirect=urlparse(response.url)
    assert redirect.scheme=="https" and redirect.hostname=="static2.vietstock.vn"
    data=response.read(MAX+1)
assert 100000<len(data)<=MAX and data[:4]==b"PK\x03\x04"
print(f"IDC_Q2_ZIP_OK bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}",flush=True)
scans=[]
with zipfile.ZipFile(io.BytesIO(data)) as z:
    for i,info in enumerate(z.infolist()):
        if info.is_dir() or not info.filename.lower().endswith(".pdf") or not 100000<info.file_size<MAX:
            continue
        if info.compress_size>MAX or info.file_size>MAX:continue
        blob=z.read(info)
        if not blob.startswith(b"%PDF"):continue
        pdf=fitz.open(stream=blob,filetype="pdf")
        print(f"IDC_Q2_PDF_CANDIDATE idx={i} name={info.filename!r} pages={len(pdf)} bytes={len(blob)} sha256={hashlib.sha256(blob).hexdigest()}",flush=True)
        if len(pdf)>=20:scans.append((info.filename,blob))
assert scans, "No full consolidated original PDF source in HNX ZIP"
scans.sort(key=lambda x: (0 if "VI_" in x[0].upper() or "_VI" in x[0].upper() else 1, x[0]))
name,blob=scans[0]
doc=fitz.open(stream=blob,filetype="pdf")
print(f"IDC_Q2_SOURCE_SELECTED name={name!r} sha256={hashlib.sha256(blob).hexdigest()} pages={len(doc)}",flush=True)
for page_number in range(7,min(len(doc),18)+1):
    page=doc[page_number-1]
    pix=page.get_pixmap(matrix=fitz.Matrix(1.48,1.48),alpha=False)
    img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    dst=io.BytesIO()
    img.save(dst,format="JPEG",quality=69,optimize=True)
    encoded=base64.b64encode(dst.getvalue()).decode("ascii")
    print(f"IDC_Q2_JPEG_BEGIN page={page_number} bytes={len(dst.getvalue())} width={pix.width} height={pix.height}",flush=True)
    print(encoded,flush=True)
    print(f"IDC_Q2_JPEG_END page={page_number}",flush=True)
print("IDC_Q2_SOURCE_IMAGES_READY original numeric rows require independent visual review",flush=True)
