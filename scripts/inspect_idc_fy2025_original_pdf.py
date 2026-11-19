#!/usr/bin/env python3
"""Read-only independent IDC 2025 consolidated 2025Q4 and FY audited visual source QA.

Do not edit JSON, website or GitHub. The 2025 audited 31-Dec cash comparator
is compared to IDC Q1/2026 and H1/2026 originally reported beginning cash.
Audit-style full-VND assertions are kept in the separate CI regression gate.
"""
import hashlib
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import fitz

PDFS = {
  "q4_issuer": "https://admin.idico.com.vn/uploads/VIE_BCTC_HOP_NHAT_Q4_2025_170f9f2fa3.pdf",
  "fy_audited": "https://admin.idico.com.vn/uploads/VI_Annual_Report_2025_942f6f68b7.pdf",
}
CAP = 29 * 1024 * 1024
SIGNALS = ("553.052.678.239","553052678239","BẢNG CÂN ĐỐI KẾ TOÁN HỢP NHẤT",
           "BÁO CÁO LƯU CHUYỂN TIỀN TỆ HỢP NHẤT", "BÁO CÁO KẾT QUẢ HOẠT ĐỘNG",
           "LƯU CHUYỂN TIỀN TỆ","Tiền và tương đương tiền cuối kỳ")
name = os.environ.get("IDC_2025_DOCUMENT", "q4_issuer")
if name not in PDFS:
    raise ValueError("Unsupported original report")
url = PDFS[name]
req = Request(url, headers={"User-Agent":"Mozilla/5.0 (original issuer financial source QA)",
                            "Accept":"application/pdf,*/*","Accept-Encoding":"identity"})
with urlopen(req,timeout=65) as res:
    dest = urlparse(res.url)
    if dest.scheme != "https" or dest.hostname != "admin.idico.com.vn":
        raise ValueError("Unexpected redirect host")
    body = res.read(CAP+1)
if not body.startswith(b"%PDF") or len(body)>CAP or len(body)<50_000:
    raise ValueError("Missing or oversized issuer PDF")
print(f"SOURCE_OK source={name} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}",flush=True)
pdf = fitz.open(stream=body,filetype="pdf")
print(f"PDF_OK source={name} pages={len(pdf)}",flush=True)
directory = Path("idc-fy2025-report-pages")
directory.mkdir(exist_ok=True)
selected = []
matches = []
for idx in range(len(pdf)):
    page=pdf[idx]
    txt=page.get_text(sort=True)
    if any(s.lower() in txt.lower() for s in SIGNALS):
        matches.append(idx)
        if len(matches)<=24:
            print(f"MATCH source={name} pdf_page={idx+1} signals={','.join(k for k in SIGNALS if k.lower() in txt.lower())[:140]}",flush=True)
# First report starts at page 1 for standalone Q4; annual audit near the end.
if name=="q4_issuer":
    selected = sorted(set(range(min(len(pdf),17))) | set(matches[:8]))[:24]
else:
    selected = sorted(set(matches[:16]))
    if not selected:
        selected = list(range(max(0,len(pdf)-85),min(len(pdf),max(0,len(pdf)-85)+15)))
print(f"SELECTED source={name} pdf_pages={[idx+1 for idx in selected]}",flush=True)
for idx in selected:
    page=pdf[idx]
    pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    filename=directory / f"idc-{name}-page-{idx+1:03d}.png"
    pix.save(filename)
    txt=page.get_text(sort=True)
    if len(re.findall(r"\d",txt))<15:
        print(f"PAGE_IMAGE_ONLY source={name} pdf_page={idx+1} path={filename}",flush=True)
    else:
        print(f"SOURCE_PAGE_BEGIN source={name} pdf_page={idx+1} chars={len(txt)}",flush=True)
        print(txt[:10000],flush=True)
        print(f"SOURCE_PAGE_END source={name} pdf_page={idx+1}",flush=True)
print(f"DONE source={name} selected_pages={len(selected)} cash_audit_hint=553052678239",flush=True)
