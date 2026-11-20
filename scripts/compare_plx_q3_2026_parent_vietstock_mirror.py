#!/usr/bin/env python3
"""Compare a third-party eDocument archive's exact PLX Q3/2026 parent original
with signed issuer original. No inferred financial fields or changes.
"""
from pathlib import Path
import fitz,hashlib,json,subprocess
URL="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2026_Congtyme.pdf?ver=35b831da"
ORIGINAL_SHA="a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef"
ORIGINAL_BYTES=14198075
out=Path("plx-q3-parent-vietstock-version")
out.mkdir(exist_ok=True)
dest=out/"PLX-Q3-parent-Vietstock-archive.pdf"
cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","11","--max-time","85",
 "--max-filesize","26000000","--output",str(dest),"--write-out","%{http_code} %{size_download}",
 "--header","User-Agent: Mozilla/5.0 (OriginalIssuerPdfMirrorQA/1.0)",URL]
p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=91)
r={"source":URL,"status":"incomplete_or_unavailable","curl_return_code":p.returncode,
  "http_downloaded":p.stdout[:180],"stderr":p.stderr[:350],
  "issuer_signed_pdf_sha256":ORIGINAL_SHA,"issuer_signed_pdf_bytes":ORIGINAL_BYTES}
if p.returncode==0 and dest.exists():
 raw=dest.read_bytes()
 if 40000<len(raw)<26000000 and raw.startswith(b"%PDF"):
  pdf=fitz.open(str(dest))
  if 15<=len(pdf)<=120:
   h=hashlib.sha256(raw).hexdigest()
   r.update({"status":"full_original_mirror_recovered_visual_pending","sha256":h,
    "bytes":len(raw),"pages":len(pdf),"exact_byte_same_as_issuer_original":(h==ORIGINAL_SHA and len(raw)==ORIGINAL_BYTES)})
   for i in range(min(12,len(pdf))):
    pix=pdf[i].get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False)
    pix.save(out/f"PLX-Vietstock-page-{i+1:02d}.png")
    print("PAGE",i+1,"text",len(pdf[i].get_text(sort=True)),flush=True)
   print("SOURCE_OK",json.dumps(r),flush=True)
if r["status"]!="full_original_mirror_recovered_visual_pending":
 dest.unlink(missing_ok=True)
 print("SOURCE_UNAVAILABLE",json.dumps(r),flush=True)
(out/"audit.json").write_text(json.dumps(r,indent=2)+"\n")
if r["status"]!="full_original_mirror_recovered_visual_pending":
 raise RuntimeError("Vietstock parent Q3 full signed archive unavailable")
