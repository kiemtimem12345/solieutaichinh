#!/usr/bin/env python3
"""Evidence-only retrieval for signed GEG/IDC H1 reviewed reports.

Print document identity, SHA256 and short focused PDF text excerpts.
Do not save PDF binaries in git, infer missing numeric values or update production JSON.
"""
from __future__ import annotations
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

SOURCES = [
 ("GEG_H1_2026_reviewed_consolidated_HOSE",
  "https://staticfile.hsx.vn/Uploads/UploadDocuments/2491976/20260825%20-%20GEG%20-%20Bao%20cao%20tai%20chinh%20hop%20nhat%20ban%20nien%20soat%20xet%202026%20%2B%20giai%20trinh.pdf", None),
 ("IDC_H1_2026_reviewed_consolidated_HNX",
  "https://owa.hnx.vn/ftp///cims/2026/9_W1/000000016828159_VI_BaoCaoTaiChinh_KiemToan_HN_T6.2026_s.pdf", None),
 ("IDC_H1_2026_reviewed_consolidated_BSC_archived",
  "https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1",
  "f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944"),
]
WORD_MATCHES = [
 "trình bày lại", "phân loại lại", "chuyển đổi", "tiền gửi", "bảo lãnh",
 "31/03/2026", "31.03.2026", "quý i/2026", "quý 1/2026", "thông tư 43",
 "thông tư số 43", "thuyết minh số 41", "thuyết minh 41",
]
ALLOWED_MAX_BYTES = 55 * 1024 * 1024

def download(url: str, target: Path):
    err = ""
    for attempt in range(2):
        try:
            request = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; so-lieu-filing-source-check/1.0)",
                "Accept": "application/pdf,application/octet-stream,*/*",
            })
            with urllib.request.urlopen(request, timeout=25) as resp:
                headers = resp.headers
                length = headers.get("Content-Length", "")
                if length.isdigit() and int(length) > ALLOWED_MAX_BYTES:
                    raise ValueError("content-length exceeds cap")
                total = 0
                with target.open("wb") as output:
                    while True:
                        chunk = resp.read(1024 * 1024)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > ALLOWED_MAX_BYTES:
                            raise ValueError("stream exceeds size cap")
                        output.write(chunk)
                if target.open("rb").read(5) != b"%PDF-":
                    raise ValueError("bad PDF magic bytes; response content type: " + str(headers.get("Content-Type")))
                return {"size": total, "content_type": headers.get("Content-Type"),
                        "last_modified": headers.get("Last-Modified"), "accept_ranges":headers.get("Accept-Ranges")}
        except Exception as e:
            err = str(e)[:220]
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(err)

def page_text(path: Path, number: int) -> str:
    result = subprocess.run(["pdftotext","-f",str(number),"-l",str(number),"-layout",str(path),"-"],
                            capture_output=True, text=True, timeout=18, errors="replace")
    if result.returncode:
        return ""
    return result.stdout

def inspect(name: str, url: str, expected_sha: str|None, target:Path):
    print("\n=== SOURCE", name, "===",flush=True)
    try:
        header = download(url, target)
    except Exception as e:
        print("RETRIEVAL_BLOCKED", str(e)[:260],flush=True)
        return
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    print("PDF_BYTES", header["size"], "SHA256", sha, "CONTENT_TYPE", header["content_type"], flush=True)
    print("EXPECTED_SHA_MATCH", bool(expected_sha and sha==expected_sha) if expected_sha else "not_previously_known",flush=True)
    r=subprocess.run(["pdfinfo",str(target)],capture_output=True,text=True,timeout=20)
    pages=0
    for line in r.stdout.splitlines():
        if line.startswith("Pages:"):
            pages=int(line.split(":",1)[1].strip())
    print("PDF_PAGES", pages,flush=True)
    if not pages or pages>200: return
    # One whole-file PDF text extraction avoids O(N^2) per-page reopens.
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(target), "-"],
            capture_output=True, text=True, timeout=90, errors="replace"
        )
    except Exception as exc:
        print("TEXT_EXTRACTION_BLOCKED", str(exc)[:140], flush=True)
        return
    if result.returncode:
        print("PDFTOTEXT_ERROR", result.stderr[:200], flush=True)
        return
    noteworthy = []
    for i, txt in enumerate(result.stdout.split("\\f")[:pages], start=1):
        canonical = re.sub(r"\\s+", " ", txt).lower()
        hits = [word for word in WORD_MATCHES if word in canonical]
        if hits:
            noteworthy.append((i, hits, canonical))
    print("SEARCHABLE_HIT_PAGES",[(p,words) for p,words,_ in noteworthy[:30]],flush=True)
    for p,words,canonical in noteworthy[:10]:
        print("PAGE",p,"MATCHES",",".join(words),flush=True)
        # short excerpts only to respect publishers' rights; never log full source.
        for word in words[:3]:
            idx=canonical.index(word)
            print("CONTEXT",repr(canonical[max(0,idx-90):idx+190]),flush=True)
    if not noteworthy:
        print("NO_SEARCHABLE_MATCH; may be image-scanned: requires targeted visual review",flush=True)

def main():
    assert shutil.which("pdfinfo") and shutil.which("pdftotext"), "poppler-utils missing"
    with tempfile.TemporaryDirectory() as tmp:
        for idx,(name,url,expected) in enumerate(SOURCES):
            try: inspect(name,url,expected,Path(tmp)/f"source-{idx}.pdf")
            except Exception as e: print("INSPECTION_ERROR",name,type(e).__name__,str(e)[:260],flush=True)
    print("END: evidence-only retrieval, no site/data modifications.",flush=True)

if __name__=="__main__": main()
