#!/usr/bin/env python3
"""Emit small JPEG previews of issuer IDC Q3/2026 original *consolidated* PDF.

This is solely for visual source validation, never for OCR-only financial entry.
Source hash locked to the successful HNX-distributed copy from BSC/Vietstock.
"""
import base64, hashlib, io, sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import fitz
from PIL import Image

URL="https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1"
SHA256="dde75e3efe8a569a0d264b27f7d7a0d8a4edb4abdf22a56144e0847f2c8dc790"
MAX=22*1024*1024
req=Request(URL,headers={"User-Agent":"Mozilla/5.0 (IDC consolidated source visual QA)","Referer":"https://www.bsc.com.vn/","Accept-Encoding":"identity"})
with urlopen(req,timeout=45) as response:
    dest=urlparse(response.url)
    assert dest.scheme=="https" and dest.hostname=="www.bsc.com.vn",dest
    data=response.read(MAX+1)
assert 100000 < len(data) < MAX and data.startswith(b"%PDF")
assert hashlib.sha256(data).hexdigest()==SHA256
doc=fitz.open(stream=data,filetype="pdf")
assert len(doc)==70
print(f"IDC_CONSOLIDATED_VISUAL_SOURCE_OK SHA256={SHA256} pages={len(doc)}",flush=True)
for page_number in list(range(8,18)):
    p=doc[page_number-1]
    pix=p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False)
    img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    dst=io.BytesIO()
    img.save(dst,format="JPEG",quality=68,optimize=True)
    payload=base64.b64encode(dst.getvalue()).decode("ascii")
    print(f"IDC_JPEG_BEGIN page={page_number} bytes={len(dst.getvalue())} width={pix.width} height={pix.height}",flush=True)
    print(payload,flush=True)
    print(f"IDC_JPEG_END page={page_number}",flush=True)
print("IDC_VISUAL_PAGES_READY_for_independent_image_read",flush=True)
