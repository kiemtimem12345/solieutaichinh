#!/usr/bin/env python3
"""Read-only original-source inspection of GAS 2025-Q4 consolidated statements.

Downloads a public issuer/HOSE financial report to an ephemeral GitHub Actions runner.
Exports only bounded first report pages for human visual QA and prints page text/OCR.
Does not edit financial JSON, disclose secrets, or deploy anything.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import fitz

SOURCES = [
    ("issuer", "https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14435&documentid=3245&moduleid=648&portalid=0"),
    ("hose", "https://staticfile.hsx.vn/Uploads/UploadDocuments/2436855/20260202%20-%20GAS%20-%20Bao%20cao%20tai%20chinh%20Quy%204.%202025%20HN.pdf"),
    ("vietstock", "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/GAS_Baocaotaichinh_Q4_2025_Hopnhat.pdf"),
]
HOSTS = {"www.pvgas.com.vn", "pvgas.com.vn", "staticfile.hsx.vn", "static2.vietstock.vn"}
MAX_BYTES = 25 * 1024 * 1024


def retrieve(name: str, url: str) -> bytes:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; FinancialStatementQA/1.0)",
        "Referer": "https://www.pvgas.com.vn/",
        "Accept": "application/pdf,application/octet-stream,*/*",
    })
    with urlopen(req, timeout=45) as resp:
        resolved = urlparse(resp.url)
        if resolved.hostname not in HOSTS or resolved.scheme != "https":
            raise ValueError("Unexpected redirect host or protocol")
        content_length = int(resp.headers.get("Content-Length") or "0")
        if content_length > MAX_BYTES:
            raise ValueError("Document exceeds size cap")
        body = bytearray()
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            body.extend(chunk)
            if len(body) > MAX_BYTES:
                raise ValueError("Document exceeds size cap")
    if not body.startswith(b"%PDF"):
        raise ValueError("Response is not a PDF")
    print(f"SOURCE_OK name={name} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()}", flush=True)
    return bytes(body)


def inspect(body: bytes, source: str) -> None:
    doc = fitz.open(stream=body, filetype="pdf")
    print(f"PDF_OK source={source} pages={len(doc)}", flush=True)
    output = Path("gas-q4-renders")
    output.mkdir(exist_ok=True)
    for i in range(2, min(11, len(doc))):
        page = doc[i]
        extracted = page.get_text(sort=True)
        pix = page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
        path = output / f"gas-2025-q4-page-{i+1:02d}.png"
        pix.save(path)
        if len(extracted.strip()) > 400 and len(re.findall(r"\d", extracted)) >= 30:
            text = extracted
            mode = "pdf_text"
        else:
            result = subprocess.run(
                ["tesseract", str(path), "stdout", "-l", "eng", "--psm", "6",
                 "-c", "preserve_interword_spaces=1"],
                capture_output=True, text=True, timeout=50, check=True,
            )
            text = result.stdout
            mode = "ocr_needs_visual_crosscheck"
        print(f"REPORT_PAGE_BEGIN pdf_page={i+1} mode={mode} chars={len(text)}", flush=True)
        print(text[:11500], flush=True)
        print(f"REPORT_PAGE_END pdf_page={i+1}", flush=True)
    print("DONE: source pages rendered; OCR text must not be treated as verified financial figures", flush=True)


def main() -> int:
    for name, url in SOURCES:
        try:
            body = retrieve(name, url)
            inspect(body, name)
            return 0
        except Exception as e:
            print(f"SOURCE_UNAVAILABLE name={name} error={type(e).__name__} message={str(e)[:180]}", flush=True)
    print("::error::All published GAS Q4 consolidated source endpoints unavailable", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
