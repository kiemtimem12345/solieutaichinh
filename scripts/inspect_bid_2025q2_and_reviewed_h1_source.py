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
    "BID_2025Q2_ORIGINAL_HN": [
        "https://static2.vietstock.vn/vietstock/2025/8/4/2_bid122005_2025_8_4_ba6b664_vi_baocaotaichinhhopnhat_q2_2025.pdf",
        "https://staticfile.hsx.vn/Uploads/UploadDocuments/2394054/20250730%20-%20BID%20-%20CBTT%20BCTC%20hop%20nhat%20giua%20nien%20do%20QII%20nam%202025.pdf",
        "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/BID_Baocaotaichinh_Q2_2025_Hopnhat.pdf",
    ],
    "BID_2025H1_REVIEWED_HN": [
        "https://cafef1.mediacdn.vn/Images/Uploaded/DuLieuDownload/BCTC/BID_Baocaotaichinh_6T_2025_Soatxet_Hopnhat_03102025143111.pdf",
        "https://staticfile.hsx.vn/Uploads/UploadDocuments/2397669/20250815%20-%20BID%20-%20BCTC%20HN%20ban%20nien%202025%20da%20duoc%20soat%20xet.pdf",
    ],
}

OUT = Path("bid-2025q2-h1-evidence")

def run(cmd: list[str], seconds: int) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=seconds, check=False)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]} exit {p.returncode}: {p.stderr[:320]}")
    return p.stdout

def inspect(label: str, urls: list[str], tmp: Path) -> None:
    pdf = tmp / (label + ".pdf")
    used_url = None
    for url in urls:
        try:
            out = run([
                "curl", "--location", "--silent", "--show-error",
                "--connect-timeout", "12", "--max-time", "58",
                "--speed-time", "12", "--speed-limit", "5000",
                "--max-filesize", str(45 * 1024 * 1024),
                "--user-agent", "Mozilla/5.0",
                "--output", str(pdf), "--write-out",
                "%{http_code}|%{content_type}|%{size_download}", url
            ], 65)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"SOURCE_FALLBACK label={label} host={url.split('/')[2]} error={str(e)[:220]}", flush=True)
            continue
        size = pdf.stat().st_size if pdf.exists() else 0
        magic = pdf.open("rb").read(5) if size else b""
        valid = size > 60000 and magic == b"%PDF-" and out[:3] == "200"
        print(f"SOURCE_ATTEMPT label={label} host={url.split('/')[2]} bytes={size} result={out[:110]} valid={valid}", flush=True)
        if valid:
            used_url = url
            break
    if used_url is None:
        raise RuntimeError(f"NO_COMPLETE_ORIGINAL {label}, source blocked, no financial data publication")
    url = used_url
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
        for label, urls in SOURCES.items():
            inspect(label, urls, Path(td))
    print("PASS BID 2025Q2 and H1 reviewed source recovery only; numeric data unchanged", flush=True)

if __name__ == "__main__":
    main()
