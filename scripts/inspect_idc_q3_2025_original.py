#!/usr/bin/env python3
"""Read-only issuer original IDC 2025Q3 signed consolidated PDF page capture.

B01/B02 standalone Q3 and B03 9M YTD must be visually checked before FY2025
minus 9M can produce 2025Q4 standalone CFO/CFI/CFF. No production writes.
"""
import hashlib,re
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import fitz
URL="https://admin.idico.com.vn/uploads/VIE_BCTC_HOP_NHAT_Q3_2025_506ed62acb.pdf"
CAP=29*1024*1024
request=Request(URL,headers={"User-Agent":"Mozilla/5.0 (IssuerFinancialSourceQA/1.0)","Accept":"application/pdf,*/*","Accept-Encoding":"identity"})
with urlopen(request,timeout=65) as resp:
    parsed=urlparse(resp.url)
    if parsed.scheme!="https" or parsed.hostname!="admin.idico.com.vn":raise ValueError("Unexpected source redirect")
    content=resp.read(CAP+1)
if not content.startswith(b"%PDF") or not(50000<len(content)<CAP):raise ValueError("Original PDF unavailable or oversized")
print(f"IDC_2025Q3_SOURCE_OK sha256={hashlib.sha256(content).hexdigest()} bytes={len(content)}",flush=True)
pdf=fitz.open(stream=content,filetype="pdf")
print(f"IDC_2025Q3_PDF_OK pages={len(pdf)}",flush=True)
out=Path("idc-q3-original-pages");out.mkdir(exist_ok=True)
for n in range(7,min(len(pdf),19)+1):
    page=pdf[n-1]
    pic=page.get_pixmap(matrix=fitz.Matrix(1.65,1.65),alpha=False)
    fp=out/f"idc-q3-2025-original-page-{n:02d}.png";pic.save(fp)
    txt=page.get_text(sort=True)
    print(f"IDC_2025Q3_PAGE_BEGIN page={n} textchars={len(txt)} image={fp}",flush=True)
    if len(re.findall(r"\d",txt))>30:print(txt[:8000],flush=True)
    else:print("IMAGE_REQUIRED original signed scan; do not treat empty text as zero",flush=True)
    print(f"IDC_2025Q3_PAGE_END page={n}",flush=True)
print("IDC_2025Q3_ORIGINAL_READY: verify images against original issuer signed B01/B02/B03",flush=True)
