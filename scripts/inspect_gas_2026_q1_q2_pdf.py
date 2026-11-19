#!/usr/bin/env python3
"""Read-only GAS consolidated 2026 Q1/Q2 PDF source inspection on GitHub Actions.

Ephemeral runner; bounded download and report-page capture. It neither updates
production data nor accepts OCR-only amounts as verified accounting figures.
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import fitz

REPORTS = {
    "2026-Q1": [
        ("issuer", "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14496&documentid=3276&moduleid=648&portalid=0"),
        ("vietstock", "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/GAS_Baocaotaichinh_Q1_2026_Hopnhat.pdf"),
    ],
    "2026-Q2": [
        ("issuer", "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14585&documentid=3358&moduleid=648&portalid=0"),
        ("vietstock", "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/GAS_Baocaotaichinh_Q2_2026_Hopnhat.pdf"),
    ],
}
ALLOWED = {"www.pvgas.com.vn", "pvgas.com.vn", "static2.vietstock.vn"}
CAP = 25 * 1024 * 1024


def fetch_source(label, url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; OriginalFinancialStatementQA/1.0)",
        "Accept": "application/pdf,application/octet-stream,*/*",
        "Referer": "https://www.pvgas.com.vn/",
    })
    with urlopen(req, timeout=50) as resp:
        u = urlparse(resp.url)
        if u.scheme != "https" or u.hostname not in ALLOWED:
            raise ValueError("Unexpected source redirect")
        length = int(resp.headers.get("Content-Length") or "0")
        if length > CAP:
            raise ValueError("Oversized PDF")
        body = bytearray()
        while True:
            b = resp.read(1024 * 1024)
            if not b:
                break
            body.extend(b)
            if len(body) > CAP:
                raise ValueError("Oversized PDF")
    if not body.startswith(b"%PDF"):
        raise ValueError("Not a PDF response")
    print(f"SOURCE_OK label={label} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}", flush=True)
    return body


def inspect(data, period, label):
    doc = fitz.open(stream=data, filetype="pdf")
    print(f"PDF_OK period={period} source={label} pages={len(doc)}", flush=True)
    out = Path("report-pages")
    out.mkdir(exist_ok=True)
    for i in range(2, min(len(doc), 12)):
        page = doc[i]
        raw = page.get_text(sort=True)
        img = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
        dest = out / f"gas-{period.lower()}-pdf-page-{i+1:02d}.png"
        img.save(dest)
        if len(raw.strip()) >= 400 and len(re.findall(r"\d", raw)) >= 30:
            method, txt = "pdf_text", raw
        else:
            result = subprocess.run(
                ["tesseract", str(dest), "stdout", "-l", "eng", "--psm", "6",
                 "-c", "preserve_interword_spaces=1"],
                capture_output=True, text=True, check=True, timeout=60,
            )
            method, txt = "ocr_unverified", result.stdout
        print(f"REPORT_PAGE_BEGIN period={period} page={i+1} mode={method} chars={len(txt)}", flush=True)
        print(txt[:13000], flush=True)
        print(f"REPORT_PAGE_END period={period} page={i+1}", flush=True)
    print(f"RENDER_COMPLETE period={period} review images before storing figures", flush=True)


def main():
    period = os.environ.get("GAS_PERIOD", "")
    if period not in REPORTS:
        raise ValueError("GAS_PERIOD must be 2026-Q1 or 2026-Q2")
    for label, url in REPORTS[period]:
        try:
            return inspect(fetch_source(label, url), period, label) or 0
        except Exception as e:
            print(f"SOURCE_UNAVAILABLE period={period} label={label} error={type(e).__name__} message={str(e)[:150]}", flush=True)
    print(f"::error::No accessible original GAS consolidated report for {period}", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
