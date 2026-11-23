#!/usr/bin/env python3
"""BID 2026Q3 signed consolidated original and reviewed H1 read-only verification.

No production data modifications. Download issuer-public PDFs with bounded
time and size; refuse HTML/truncated files; preserve SHA and page provenance.
Print only an excerpt of relevant statement rows, NOT the full source PDF.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

SOURCES = {
  "BID_2026Q3_HN": "https://bidv.com.vn/wps/wcm/connect/69a3b6bf-9fb3-4ef3-bb61-156cd541bc7d/20261030%2B-%2BBID%2B-%2BCBTT%2BBCTC%2BHN%2Bgiua%2Bnien%2Bdo%2BQ3.pdf?MOD=AJPERES",
  "BID_2026H1_REVIEWED_HN": "https://bidv.com.vn/wps/wcm/connect/6e490bbf-6629-4667-9ae4-c6134af2fcd8/20260818%2B-%2BBID%2B-%2BCBTT%2BBCTC%2BHN%2Bban%2Bnien%2Bda%2Bduoc%2Bsoat%2Bxet.pdf?MOD=AJPERES",
}
OUTPUT = Path("bid-2026q3-h1-signed-evidence")
KEYWORDS = re.compile(
    r"tổng tài sản|tổng nợ|vốn chủ sở hữu|tổng thu nhập|thu nhập lãi|chi phí lãi|"
    r"lãi/lỗ thuần|lãi thuần|lợi nhuận|thuế thu nhập|chi phí dự phòng|"
    r"tiền gửi của khách|tiền mặt|cho vay khách|tiền và tương đương|"
    r"lưu chuyển tiền|lưu chuyển thuần|tiền đầu kỳ|tiền cuối kỳ|"
    r"tăng giảm tiền|chênh lệch tỷ giá|giấy tờ có giá|"
    r"trước dự phòng|kinh doanh ngoại hối",
    re.I,
)

def exec_bound(argv: list[str], timeout: int) -> str:
    result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    if result.returncode:
        raise RuntimeError(f"{argv[0]} exited {result.returncode}: {result.stderr[:500]}")
    return result.stdout

def inspect(label: str, url: str, directory: Path) -> None:
    pdf = directory / (label + ".pdf")
    exec_bound([
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--retry", "1", "--retry-delay", "2",
        "--connect-timeout", "15", "--max-time", "115",
        "--speed-time", "18", "--speed-limit", "4096",
        "--max-filesize", str(40 * 1024 * 1024),
        "--user-agent", "Mozilla/5.0", "--output", str(pdf), url,
    ], 140)
    if not pdf.exists() or pdf.stat().st_size < 60000:
        raise RuntimeError(f"Truncated or empty issuer report {label}")
    with pdf.open("rb") as f:
        assert f.read(5) == b"%PDF-", f"Not a PDF: {label}"
    metadata = exec_bound(["pdfinfo", str(pdf)], 30)
    match = re.search(r"^Pages:\s*(\d+)\s*$", metadata, re.M)
    assert match, f"PDF page count missing: {label}"
    count = int(match.group(1))
    assert 10 <= count <= 150, (label, count)
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    print(f"ORIGINAL_SOURCE label={label} sha256={sha} size={pdf.stat().st_size} pages={count} URL={url}", flush=True)
    text_pages = min(13, count)
    all_text = exec_bound([
        "pdftotext", "-f", "1", "-l", str(text_pages),
        "-layout", "-nopgbrk", str(pdf), "-"
    ], 90)
    (OUTPUT / (label + "-statement-excerpt.txt")).write_text(
        all_text[:130000], encoding="utf-8"
    )
    print(f"EXTRACTED_TEXT label={label} chars={len(all_text)} first_pdf_pages={text_pages}", flush=True)
    rows = [re.sub(r"\s+", " ", line).strip() for line in all_text.splitlines()]
    relevant = [line for line in rows if len(line) >= 12 and KEYWORDS.search(line) and re.search(r"\d", line)]
    for line in relevant[:115]:
        print(f"BANK_STATEMENT_ROW {label} {line[:250]}", flush=True)
    print(f"RELEVANT_LINES label={label} count={len(relevant)} shown={min(115, len(relevant))}", flush=True)
    # Keep only a few source statement previews for manual image QA; expire quickly.
    exec_bound([
        "pdftoppm", "-f", "3", "-l", str(min(10, count)), "-scale-to", "1150",
        "-jpeg", "-jpegopt", "quality=60",
        str(pdf), str(OUTPUT / label),
    ], 160)
    print(f"VISUAL_PREVIEW label={label} images={len(list(OUTPUT.glob(label+'-*.jpg')))}", flush=True)

def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for label, url in SOURCES.items():
            inspect(label, url, Path(tmp))
    print("PASS provenance-only BID 2026Q3 plus 2026 reviewed H1; production remains UNVERIFIED until numeric reconciliation", flush=True)

if __name__ == "__main__":
    main()
