#!/usr/bin/env python3
"""Read-only retrieval of IDC Q1 2025 HNX-signed consolidated statements.

Uses issuer/HNX disclosure mirror in preference to secondary quarterly numbers.
Produces page images and a bounded, auditable exact-source log for manual visual QA.
No data/financials-IDC.json mutation. No numeric PASS without image inspection.
"""
from __future__ import annotations

import hashlib
import io
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import fitz

SOURCES = [
    ("HNX_Vietstock_signed_original_pdf", "https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2025_Hopnhat.pdf"),
]
HOSTS = {"static2.vietstock.vn"}
DOWNLOAD_CAP = 42 * 1024 * 1024
PDF_CAP = 28 * 1024 * 1024
OUTPUT = Path("idc-q1-2025-source-pages")
OUTPUT.mkdir(parents=True, exist_ok=True)
pdf_raw = None
source = None

for label, url in SOURCES:
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (BCTC-original-archive-visual-qa)",
            "Accept": "application/pdf,application/zip,*/*",
            "Accept-Encoding": "identity",
            "Referer": "https://finance.vietstock.vn/" if "vietstock.vn" in url else "https://cafef.vn/",
        })
        with urlopen(req, timeout=55) as resp:
            dest = urlparse(resp.geturl())
            if dest.scheme != "https" or dest.hostname not in HOSTS:
                raise ValueError("Unexpected host redirect")
            contents = resp.read(DOWNLOAD_CAP + 1)
        if not 20000 < len(contents) <= DOWNLOAD_CAP:
            raise ValueError("Bad download size")
        print(f"DOWNLOAD_OK {label} bytes={len(contents)} sha256={hashlib.sha256(contents).hexdigest()}", flush=True)
        if contents.startswith(b"%PDF"):
            pdf_raw = contents
            source = f"{label}:{url}"
        elif contents.startswith(b"PK"):
            with zipfile.ZipFile(io.BytesIO(contents)) as archive:
                members = [m for m in archive.infolist()
                           if m.filename.lower().endswith(".pdf")
                           and not m.is_dir() and 20000 < m.file_size < PDF_CAP]
                if not members:
                    raise ValueError("ZIP has no bounded PDF")
                print("ZIP_PDF_MEMBERS", [(m.filename, m.file_size) for m in members], flush=True)
                choices = [m for m in members
                           if ("hn" in m.filename.lower() or "hopnhat" in m.filename.lower() or "hợp nhất" in m.filename.lower())
                           and not any(b in m.filename.lower() for b in ("giaitrinh", "giai_trinh", "explanation", "congtyme", "cong_ty_me", "riengle"))]
                if not choices:
                    raise ValueError("Cannot select unambiguous consolidated original")
                choices.sort(key=lambda m:("vi" not in m.filename.lower(), "en" in m.filename.lower(), m.file_size))
                with archive.open(choices[0]) as f:
                    pdf_raw = f.read(PDF_CAP + 1)
                source = f"{label}:{choices[0].filename}"
        else:
            raise ValueError("Source neither PDF nor ZIP")
        if not pdf_raw or not pdf_raw.startswith(b"%PDF") or len(pdf_raw) > PDF_CAP:
            raise ValueError("No bounded PDF")
        break
    except Exception as exc:
        pdf_raw = None
        source = None
        print(f"SOURCE_UNAVAILABLE {label} {type(exc).__name__}: {str(exc)[:280]}", flush=True)

if pdf_raw is None:
    raise RuntimeError("Could not recover the exact IDC Q1 2025 HNX consolidated original; do not mark QA PASS")

print("IDC_Q1_2025_PDF", {
    "source": source, "bytes": len(pdf_raw),
    "sha256": hashlib.sha256(pdf_raw).hexdigest()
}, flush=True)

doc = fitz.open(stream=pdf_raw, filetype="pdf")
if len(doc) < 15 or len(doc) > 160:
    raise ValueError(f"Unexpected PDF page count: {len(doc)}")
print(f"IDC_Q1_2025_PAGES {len(doc)}", flush=True)
joined_text = " ".join(page.get_text(sort=True) for page in list(doc)[:18])
if len(joined_text) > 1500:
    folded = re.sub(r"\s+", " ", joined_text).lower()
    if not any(k in folded for k in ("idico", "tổng công ty idico", "tong cong ty idico")):
        raise ValueError("Issuer name IDICO not found in searchable original")
    if not any(k in folded for k in ("31 tháng 3 năm 2025", "31 thang 3 nam 2025", "31/03/2025", "31 march 2025", "march 31, 2025")):
        print("DATE_NOT_MACHINE_READABLE: visual confirmation required", flush=True)
else:
    print("SCANNED_PDF_TEXT_EMPTY: visual issuer/scope confirmation required", flush=True)

for i in range(6, min(20,len(doc))):
    page = doc[i]
    text = page.get_text(sort=True)
    p = OUTPUT / f"IDC-2025-Q1-HNX-original-page-{i+1:02d}.png"
    page.get_pixmap(matrix=fitz.Matrix(1.3,1.3), alpha=False).save(p)
    print(f"PAGE_BEGIN pdf_page={i+1} textchars={len(text)} image={p}", flush=True)
    print(text[:7000] if len(text)>100 else "SCANNED_IMAGE_REQUIRED", flush=True)
    print(f"PAGE_END pdf_page={i+1}", flush=True)
print("SOURCE_READY for independent B01/B02/B03 original visual QA. NO PRODUCTION CHANGES.", flush=True)
