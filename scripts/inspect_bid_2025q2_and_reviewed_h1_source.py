#!/usr/bin/env python3
"""Read-only original Q2/2025 BID consolidated and independently reviewed H1 QA.

Recover complete issuer-published source files, inspect page images, record
each exact SHA/page metadata, and do not alter financials-BID.json here.
Original Q1 2025 source is already verified; derive Q2 bank B04 later only
from an independently verified 6M report and same-vintage Q1 source.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

SOURCES = {
    "BID_2025Q2_ORIGINAL_HN": "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/BID_Baocaotaichinh_Q2_2025_Hopnhat.pdf",
    "BID_2025H1_REVIEWED_HN": "https://cafef1.mediacdn.vn/Images/Uploaded/DuLieuDownload/BCTC/BID_Baocaotaichinh_6T_2025_Soatxet_Hopnhat_03102025143111.pdf",
}
OUT = Path("bid-2025q2-h1-evidence")

def run(cmd: list[str], seconds: int) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=seconds, check=False)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} exit {p.returncode}: {p.stderr[:320]}")
    return p.stdout

def inspect(label: str, url: str, tmp: Path) -> None:
    pdf = tmp / (label + ".pdf")
    out = run([
        "curl", "--location", "--fail", "--silent", "--show-error",
        "--retry", "1", "--retry-delay", "2",
        "--connect-timeout", "15", "--max-time", "120",
        "--speed-time", "20", "--speed-limit", "4096",
        "--max-filesize", str(45 * 1024 * 1024),
        "--user-agent", "Mozilla/5.0 (BID original financial proof)",
        "--output", str(pdf), "--write-out",
        "%{http_code}|%{content_type}|%{size_download}", url
    ], 150)
    assert pdf.exists() and pdf.stat().st_size > 60000, ("file truncated", label, out)
    with pdf.open("rb") as f:
        assert f.read(5) == b"%PDF-", ("not pdf", label)
    info = run(["pdfinfo", str(pdf)], 45)
    m = re.search(r"^Pages:\s*(\d+)\s*$", info, re.M)
    assert m, ("page count not detected", label)
    pages = int(m.group(1))
    assert 15 <= pages <= 200
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    print(f"ORIGINAL_SOURCE {label} SHA256={sha} BYTES={pdf.stat().st_size} PAGES={pages} HTTP={out} URL={url}", flush=True)
    # Signed front matter typically precedes B01, B03 and B04.
    first, last = (3, min(11, pages)) if "Q2" in label else (6, min(16, pages))
    text = run(["pdftotext", "-f", str(first), "-l", str(last), "-layout", str(pdf), "-"], 75)
    if text.strip():
        (OUT / (label + "-text.txt")).write_text(text[:75000], "utf-8")
    run(["pdftoppm", "-f", str(first), "-l", str(last),
         "-scale-to", "1400", "-jpeg", "-jpegopt", "quality=66",
         str(pdf), str(OUT / label)], 170)
    image_count = len(list(OUT.glob(label + "-*.jpg")))
    assert image_count == last - first + 1, (label, image_count)
    print(f"PASS_SOURCE_PROVENANCE {label} IMAGE_COUNT={image_count} text_chars={len(text)}", flush=True)

def main() -> None:
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        for label, url in SOURCES.items():
            inspect(label, url, Path(td))
    print("PASS BID 2025Q2 and H1 reviewed source recovery only; numeric data unchanged", flush=True)

if __name__ == "__main__":
    main()
