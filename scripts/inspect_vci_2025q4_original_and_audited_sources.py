#!/usr/bin/env python3
"""Issuer VCI Q4 2025 signed source recovery, no data writes or OCR guesses.

Original as-filed quarter and audited FY are different accounting vintages.
Download only to temporary runner storage; export limited visual-page evidence.
"""
import hashlib
import subprocess
import tempfile
import zipfile
from pathlib import Path

SOURCES = [
    ("VCI_Q4_2025_Vietstock_ZIP","https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/VCI_Baocaotaichinh_Q4_2025.zip"),
    ("VCI_Q4_2025_HOSE_PDF","https://staticfile.hsx.vn/Uploads/UploadDocuments/2431831/20260119%20-%20VCI%20-%20CBTT%20Bao%20cao%20tai%20chinh%20Q4.2025.pdf"),
    ("VCI_FY2025_HOSE_audited","https://staticfile.hsx.vn/Uploads/UploadDocuments/2439372/20260213%20-%20VCI%20-%20BCTC%202025%20-%20CBTT.pdf"),
]
DEST = Path("vci-2025q4-source-previews")
DEST.mkdir(exist_ok=True)
MAX_SIZE = 48*1024*1024
def get(url,path):
    cmd=["curl","--location","--fail","--silent","--show-error","--max-time","83",
         "--connect-timeout","12","--speed-limit","8192","--speed-time","16",
         "--max-filesize",str(MAX_SIZE),"--user-agent","Mozilla/5.0",
         "--output",str(path),url]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=98)
    if p.returncode:raise RuntimeError("curl_exit=%s, %s"%(p.returncode,p.stderr[:170]))
    if not 0<path.stat().st_size<=MAX_SIZE:raise ValueError("invalid file bytes")
    return hashlib.sha256(path.read_bytes()).hexdigest()
def render(label,pdf):
    info=subprocess.run(["pdfinfo",str(pdf)],text=True,capture_output=True,timeout=20,check=True)
    pages=next((int(line.split(":",1)[1].strip()) for line in info.stdout.splitlines() if line.startswith("Pages:")),0)
    if not 8<=pages<=180:raise ValueError("invalid PDF pages "+str(pages))
    preview_count=min(23,pages)
    out=DEST/label
    subprocess.run(["pdftoppm","-f","1","-l",str(preview_count),"-scale-to","1450","-jpeg",
                    "-jpegopt","quality=62",str(pdf),str(out)],text=True,capture_output=True,timeout=110,check=True)
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],capture_output=True,timeout=60)
    print("SOURCE_PDF",label,"sha256",hashlib.sha256(pdf.read_bytes()).hexdigest(),
          "bytes",pdf.stat().st_size,"pages",pages,"text_chars",len(text.stdout),
          "preview_images",len(list(DEST.glob(label+"-*.jpg"))),flush=True)
    return pages
def main():
    got_q4=False
    got_annual=False
    with tempfile.TemporaryDirectory() as temp:
        for index,(label,url) in enumerate(SOURCES):
            if got_q4 and "Q4_" in label:continue
            try:
                file=Path(temp)/("src%d"%index+(".zip" if url.endswith(".zip") else ".pdf"))
                source_sha=get(url,file)
                print("SOURCE_CONTAINER",label,"sha256",source_sha,"bytes",file.stat().st_size,flush=True)
                if file.open("rb").read(4)==b"PK\\x03\\x04":
                    with zipfile.ZipFile(file) as bundle:
                        names=[z for z in bundle.infolist() if z.filename.lower().endswith(".pdf") and not z.is_dir() and z.file_size<=MAX_SIZE]
                        print("ZIP_PDFS",[(z.filename[:90],z.file_size) for z in names[:8]],flush=True)
                        if not names: raise ValueError("Q4 ZIP contains no PDF")
                        first=names[0]
                        pdf=Path(temp)/"q4_selected.pdf"
                        with bundle.open(first) as source,pdf.open("wb") as output:
                            import shutil;shutil.copyfileobj(source,output)
                        if pdf.open("rb").read(5)!=b"%PDF-":raise ValueError("ZIP PDF invalid")
                        render(label,pdf)
                else:
                    if file.open("rb").read(5)!=b"%PDF-":raise ValueError("not PDF")
                    render(label,file)
                if label.startswith("VCI_Q4_"):got_q4=True
                if label.startswith("VCI_FY"):got_annual=True
            except Exception as exc:
                print("SOURCE_NOT_RETRIEVED",label,type(exc).__name__,str(exc)[:190],flush=True)
    print("SOURCES_RESOLVED", "Q4",got_q4,"FY_AUDITED",got_annual,flush=True)
    if not got_q4:raise SystemExit("Q4 ORIGINAL_NOT_RECOVERED; no financial data changed")
    print("PASS_Q4_SOURCE_ONLY; numerical review and signed FY version bridge still mandatory",flush=True)
if __name__=="__main__":main()
