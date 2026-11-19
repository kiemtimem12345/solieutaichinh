#!/usr/bin/env python3
"""Read-only IDC Q3/2025 signed consolidated original, issuer then HNX/Vietstock.

Try issuer first (currently may return HTTP404), archived official disclosure
ZIP next and its signed Vietnamese consolidated PDF, then published English
consolidated PDF. Never accept the parent-only report as a substitute.
Download caps and bounded ZIP decompression prevent unsafe archives.
"""
import hashlib,io,re,zipfile
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import fitz

SOURCES=[
 ("issuer","https://admin.idico.com.vn/uploads/VIE_BCTC_HOP_NHAT_Q3_2025_506ed62acb.pdf"),
 ("hnx_vietstock_zip","https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2025_Hopnhat.zip"),
 ("hnx_vietstock_en_pdf","https://static2.vietstock.vn/data/HNX/2025/BCTC/VN/QUY%203/IDC_Baocaotaichinh_Q3_2025_Hopnhat/4_idc_2025_10_30_de24c2b_en_financialstatementshn_q3_2025hn_s.pdf"),
]
HOSTS={"admin.idico.com.vn","static2.vietstock.vn"}
CAP=43*1024*1024
DEC_CAP=35*1024*1024
raw=None
source_label=None
for label,url in SOURCES:
    try:
        request=Request(url,headers={"User-Agent":"Mozilla/5.0 (IssuerFinancialSourceQA/1.0)",
                  "Referer":"https://finance.vietstock.vn/" if "vietstock.vn" in url else "https://www.idico.com.vn/",
                  "Accept":"application/pdf,application/zip,*/*","Accept-Encoding":"identity"})
        with urlopen(request,timeout=50) as response:
            final=urlparse(response.url)
            if final.scheme!="https" or final.hostname not in HOSTS:raise ValueError("Unexpected source redirect")
            blob=response.read(CAP+1)
        if len(blob)>CAP or len(blob)<30000:raise ValueError("Archive too large or empty")
        print(f"DOWNLOAD_OK label={label} bytes={len(blob)} sha256={hashlib.sha256(blob).hexdigest()}",flush=True)
        if blob.startswith(b"%PDF"):
            raw=blob
            source_label=label
        elif blob.startswith(b"PK"):
            pack=zipfile.ZipFile(io.BytesIO(blob))
            members=[p for p in pack.infolist() if p.filename.lower().endswith(".pdf") and p.file_size<DEC_CAP and not p.is_dir()]
            print("ZIP_MEMBERS "+str([(m.filename,m.file_size) for m in members])[:4000],flush=True)
            choices=[m for m in members if "hn" in m.filename.lower() and not any(x in m.filename.lower() for x in ("_r_", "congtyme","cong_ty_me","giai_trinh","giaitrinh"))]
            choices.sort(key=lambda m:("vi" not in m.filename.lower(),"en" in m.filename.lower(),m.file_size))
            if not choices:raise ValueError("No unambiguous signed consolidated PDF in ZIP")
            with pack.open(choices[0]) as r:
                raw=r.read(DEC_CAP+1)
            if len(raw)>DEC_CAP or not raw.startswith(b"%PDF"):raise ValueError("Bad PDF member")
            source_label=label+":"+choices[0].filename
        else:raise ValueError("Not signed original PDF/ZIP")
        break
    except Exception as exc:
        print(f"SOURCE_UNAVAILABLE label={label} cause={type(exc).__name__} text={str(exc)[:150]}",flush=True)
if not raw:
    raise RuntimeError("Official consolidated IDC 2025-Q3 source cannot be recovered")
print(f"IDC_2025Q3_SOURCE_OK kind={source_label} sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",flush=True)
pdf=fitz.open(stream=raw,filetype="pdf")
print(f"IDC_2025Q3_PDF_OK pages={len(pdf)}",flush=True)
out=Path("idc-q3-original-pages");out.mkdir(exist_ok=True)
for n in range(7,min(len(pdf),20)+1):
    page=pdf[n-1]
    pic=page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
    fp=out/f"idc-q3-2025-original-page-{n:02d}.png";pic.save(fp)
    txt=page.get_text(sort=True)
    print(f"IDC_2025Q3_PAGE_BEGIN page={n} textchars={len(txt)} image={fp}",flush=True)
    if len(re.findall(r"\d",txt))>30:print(txt[:6500],flush=True)
    else:print("IMAGE_REQUIRED signed scan; do not treat empty text as zero",flush=True)
    print(f"IDC_2025Q3_PAGE_END page={n}",flush=True)
print("IDC_2025Q3_ORIGINAL_READY: verify consolidated label and original B01/B02/B03 images",flush=True)
