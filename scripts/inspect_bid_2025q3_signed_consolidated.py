#!/usr/bin/env python3
"""Recover BID 2025Q3 signed consolidated B01/B03/B04, fail closed.

Original PDF may have scanner-only pages. Record original SHA and render pages
for visual confirmation; do not publish OCR-derived or unverified numbers.
The already-verified Deloitte 2025H1 source and its data are retained in the
existing 2025Q2 ledger, not reprocessed.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

SOURCES = [
    "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/BID_Baocaotaichinh_Q3_2025_Hopnhat_1.pdf",
]
OUT = Path("bid-2025q3-original-preview")

def execute(args: list[str], timeout: int = 90) -> str:
    process = subprocess.run(args, text=True, capture_output=True, timeout=timeout, check=False)
    if process.returncode:
        raise RuntimeError(f"{args[0]} code={process.returncode} stderr={process.stderr[:200]}")
    return process.stdout

def main() -> None:
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        pdf = Path(t) / "BID-2025Q3-original-hn.pdf"
        url_used = None
        for url in SOURCES:
            try:
                out = execute([
                    "curl", "--location", "--silent", "--show-error",
                    "--connect-timeout", "12", "--max-time", "60",
                    "--speed-time", "15", "--speed-limit", "4096",
                    "--max-filesize", str(45 * 1024 * 1024),
                    "--user-agent", "Mozilla/5.0",
                    "--output", str(pdf), "--write-out",
                    "%{http_code}|%{content_type}|%{size_download}", url
                ], 70)
            except (RuntimeError, subprocess.TimeoutExpired) as e:
                print("PDF_SOURCE_ATTEMPT_FAILED", url.split("/")[2], str(e)[:170], flush=True)
                continue
            size = pdf.stat().st_size if pdf.exists() else 0
            magic = pdf.open("rb").read(5) if size else b""
            valid = size > 60000 and magic == b"%PDF-" and out.startswith("200")
            print(f"PDF_SOURCE_ATTEMPT {url.split('/')[2]} bytes={size} detail={out} valid={valid}", flush=True)
            if valid:
                url_used = url
                break
        if url_used is None:
            raise RuntimeError("NO_COMPLETE_SIGNED_BID_2025Q3_PDF - keep source quarantine")
        metadata = execute(["pdfinfo", str(pdf)], 35)
        match = re.search(r"^Pages:\s*(\d+)", metadata, re.M)
        assert match, "PDF page count missing"
        count = int(match.group(1))
        assert 15 <= count <= 180, count
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        print(f"SIGNED_Q3_ORIGINAL PDF_SHA256={digest} PAGE_COUNT={count} BYTES={pdf.stat().st_size} URL={url_used}", flush=True)
        first, last = 2, min(count, 12)
        body = execute(["pdftotext", "-f", str(first), "-l", str(last), "-layout", str(pdf), "-"], 90)
        print(f"SIGNED_Q3_TEXT_LAYER chars={len(body)} visible={len(body.strip())}", flush=True)
        if body.strip():
            (OUT / "q3-first-12-pages.txt").write_text(body[:75000], encoding="utf-8")
        execute([
            "pdftoppm", "-f", str(first), "-l", str(last), "-scale-to", "1650",
            "-jpeg", "-jpegopt", "quality=72",
            str(pdf), str(OUT / "BID-2025Q3-HN")
        ], 170)
        n = len(list(OUT.glob("BID-2025Q3-HN-*.jpg")))
        assert n == last - first + 1, n
        print(f"PASS SIGNED_BID_2025Q3_SOURCE_PROVENANCE pages_rendered={n}; data not yet promoted", flush=True)

if __name__ == "__main__":
    main()
