#!/usr/bin/env python3
"""Read-only issuer original financial evidence for BID 2025Q1 consolidated.

Do not accept existing auto-extracted dashboard numbers before signed
original B01/B03/B04 visual QA and exact million-VND accounting identities.
Archive source SHA and a small, short-lived subset of statement images.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

URL = "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/BID_Baocaotaichinh_Q1_2025_Hopnhat.pdf"
OUT = Path("bid-2025q1-original-evidence")

def execute(cmd: list[str], timeout: int) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    if p.returncode:
        raise RuntimeError(f"{cmd[0]}: exit={p.returncode}; stderr={p.stderr[:350]}")
    return p.stdout

def main() -> None:
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        pdf = Path(td) / "BID-2025Q1-original-consolidated.pdf"
        diag = execute([
            "curl", "--location", "--fail", "--silent", "--show-error",
            "--retry", "1", "--retry-delay", "2",
            "--connect-timeout", "15", "--max-time", "110",
            "--speed-time", "20", "--speed-limit", "4096",
            "--max-filesize", str(40 * 1024 * 1024),
            "--user-agent", "Mozilla/5.0 (financial-source-audit)",
            "--output", str(pdf), "--write-out",
            "%{http_code}|%{content_type}|%{size_download}", URL
        ], 140)
        assert pdf.exists() and pdf.stat().st_size > 60000, ("truncated original", diag)
        with pdf.open("rb") as f:
            assert f.read(5) == b"%PDF-", "original PDF signature missing"
        pdf_info = execute(["pdfinfo", str(pdf)], 35)
        m = re.search(r"^Pages:\s*(\d+)\s*$", pdf_info, re.M)
        assert m, "PDF page count absent"
        page_count = int(m.group(1))
        assert 15 <= page_count <= 150
        sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
        print("SOURCE_ORIGINAL BID_2025Q1_HN URL", URL, "SHA256", sha, "BYTES",
              pdf.stat().st_size, "PAGES", page_count, "HTTP", diag, flush=True)
        txt = execute(["pdftotext", "-f", "1", "-l", str(min(13, page_count)),
                       "-layout", str(pdf), "-"], 65)
        print("TEXT_LAYER_QA BID_2025Q1_HN", len(txt), "characters", flush=True)
        if txt.strip():
            (OUT / "bid-2025q1-original-pages-text.txt").write_text(txt[:60000], "utf-8")
        execute(["pdftoppm", "-f", "1", "-l", str(min(10, page_count)),
                 "-scale-to", "1550", "-jpeg", "-jpegopt", "quality=69",
                 str(pdf), str(OUT / "BID-2025Q1-HN")], 160)
        number = len(list(OUT.glob("BID-2025Q1-HN-*.jpg")))
        assert number == min(10, page_count), (number, page_count)
        print("PASS SOURCE_PROVENANCE_ONLY BID_2025Q1", number,
              "statement images; no financial data promoted", flush=True)

if __name__ == "__main__":
    main()
