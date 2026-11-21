#!/usr/bin/env python3
"""Read-only signed VCI 2026Q1 source recovery with bounded PDF download and visual-page output.

No financial JSON writes, no OCR assumptions, no original PDF retention in Git.
"""
import hashlib
import subprocess
import tempfile
from pathlib import Path

URLS = [
    ("VCI_2026Q1_Vietstock", "https://www.vietcap.com.vn/api/cms-api/uploads/froala/files/20260420%20-%20VCI%20-%20Bao%20Cao%20Tai%20Chinh%20Q1.2026.pdf"),
]
MAX_BYTES = 45 * 1024 * 1024
PREVIEW = Path("vci-2026q1-previews")
PREVIEW.mkdir(exist_ok=True)

def download(url, dest):
    command = ["curl", "--location", "--fail", "--silent", "--show-error",
               "--max-time", "90", "--connect-timeout", "14",
               "--speed-limit", "8192", "--speed-time", "20",
               "--max-filesize", str(MAX_BYTES),
               "--user-agent", "Mozilla/5.0",
               "--output", str(dest), url]
    p = subprocess.run(command, capture_output=True, text=True, timeout=103)
    if p.returncode:
        raise RuntimeError("SOURCE_HTTP_FAILED curl_exit=%s %s" % (p.returncode,p.stderr.strip()[:170]))
    size = dest.stat().st_size
    if not 0 < size <= MAX_BYTES or dest.open("rb").read(5) != b"%PDF-":
        raise ValueError("SOURCE_NOT_PDF")
    return size

def inspect(name,url,dest):
    size = download(url,dest)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    info = subprocess.run(["pdfinfo",str(dest)],capture_output=True,text=True,timeout=20,check=True)
    pages = next((int(t.split(":",1)[1].strip()) for t in info.stdout.splitlines() if t.startswith("Pages:")),0)
    if not 6 <= pages <= 160:
        raise ValueError("IMPLAUSIBLE_SOURCE_PAGES "+str(pages))
    print("SOURCE_PDF",name,"bytes",size,"sha256",digest,"pages",pages,flush=True)
    txt = subprocess.run(["pdftotext","-layout",str(dest),"-"],capture_output=True,text=True,timeout=70)
    print("TEXT_EXTRACT_CHARS",len(txt.stdout),"returncode",txt.returncode,flush=True)
    stop = min(pages,26)
    command = ["pdftoppm","-f","1","-l",str(stop),"-scale-to","1500",
               "-jpeg","-jpegopt","quality=65",str(dest),str(PREVIEW/"VCI_Q1_2026")]
    subprocess.run(command,capture_output=True,text=True,timeout=145,check=True)
    count = len(list(PREVIEW.glob("VCI_Q1_2026-*.jpg")))
    print("PAGE_PREVIEWS",count,"expected",stop,flush=True)
    if count != stop:
        raise ValueError("VISUAL_EXPORT_MISSING_PAGES")
    return digest

def main():
    with tempfile.TemporaryDirectory() as temp:
        errors=[]
        for name,url in URLS:
            try:
                sha=inspect(name,url,Path(temp)/"vci-q1-2025.pdf")
                print("SOURCE_RECOVERED_NEEDS_VISUAL_ACCOUNTING_REVIEW",name,sha,flush=True)
                return
            except Exception as exc:
                errors.append(str(exc)[:240])
                print("SOURCE_FAILURE",name,str(exc)[:240],flush=True)
        raise SystemExit("NO_SIGNED_SOURCE_RECOVERED: "+"; ".join(errors))
if __name__=="__main__":
    main()
