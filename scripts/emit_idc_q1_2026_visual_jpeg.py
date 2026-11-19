#!/usr/bin/env python3
"""Read-only visual validation of IDC 2026Q1 consolidated issuer signed PDF.

Download exact original PDF from Vietstock's HNX filing mirror, render pages
of the B01/B02/B03. Do not parse financial values or write production data.
"""
import base64,hashlib,io
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import fitz
from PIL import Image
URL="https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2026_Hopnhat.pdf"
MAX=28*1024*1024
req=Request(URL,headers={"User-Agent":"Mozilla/5.0 (signed financial report visual QA)","Referer":"https://finance.vietstock.vn/","Accept-Encoding":"identity"})
with urlopen(req,timeout=70) as response:
  parsed=urlparse(response.url)
  assert parsed.scheme=="https" and parsed.hostname=="static2.vietstock.vn",parsed
  data=response.read(MAX+1)
assert data.startswith(b"%PDF") and 100000<len(data)<MAX,"Bad or oversized PDF"
pdf=fitz.open(stream=data,filetype="pdf")
print(f"IDC_Q1_SOURCE_OK bytes={len(data)} SHA256={hashlib.sha256(data).hexdigest()} PDF_PAGES={len(pdf)}",flush=True)
for n in range(8,min(len(pdf),15)+1):
  pix=pdf[n-1].get_pixmap(matrix=fitz.Matrix(1.45,1.45),alpha=False)
  im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  f=io.BytesIO()
  im.save(f,format="JPEG",quality=68,optimize=True)
  coded=base64.b64encode(f.getvalue()).decode()
  print(f"IDC_Q1_JPEG_BEGIN page={n} bytes={len(f.getvalue())}",flush=True)
  print(coded,flush=True)
  print(f"IDC_Q1_JPEG_END page={n}",flush=True)
print("IDC_Q1_PAGES_READY: independently review images, do not treat text/OCR as verified",flush=True)
