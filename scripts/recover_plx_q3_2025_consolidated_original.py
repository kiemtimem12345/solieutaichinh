#!/usr/bin/env python3
"""Recover PLX Q3/2025 consolidated issuer B01/B02/B03 for exact source QA.

Source URL is confirmed by 2025 official Vietstock Finance public
/data/getdocument listing. Existing PLX Q3 data are partially verified only from archived OCR; original 9M signed source B01/B02/B03 not yet fully visually checked:
never publish original OCR-derived fields as signed-visual-verified before
full signed PDF and manual page-image checks. Preserve already PASS periods.
"""
from pathlib import Path
import hashlib,json,subprocess
import fitz

URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/PLX_Baocaotaichinh_Q3_2025_Hopnhat.pdf"
OUT=Path("plx-2025-q3-consolidated-original")
OUT.mkdir(exist_ok=True)
PDF=OUT/"issuer_original.pdf"
cmd=["curl","--fail","--location","--silent","--show-error",
     "--connect-timeout","12","--max-time","85","--max-filesize","32000000",
     "--output",str(PDF),"--write-out","%{http_code} %{size_download} %{url_effective}",
     "--header","User-Agent: Mozilla/5.0 (SignedSourceQA/1.0)",URL]
p=subprocess.run(cmd,capture_output=True,text=True,timeout=92)
meta={"source_url":URL,"curl_return_code":p.returncode,"download_report":p.stdout[:350],"stderr":p.stderr[:350],
      "status":"missing_or_partial_original"}
if p.returncode==0 and PDF.exists():
    raw=PDF.read_bytes()
    if len(raw)>100000 and raw.startswith(b"%PDF"):
        try:
            doc=fitz.open(str(PDF))
            if not 7<=len(doc)<=130:raise ValueError("unexpected pdf pages")
            meta.update({"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"pages":len(doc),"status":"complete_original_pdf_pending_visual_source_qa"})
            for i in range(min(len(doc),19)):
                page=doc[i]
                page.get_pixmap(matrix=fitz.Matrix(1.65,1.65),alpha=False).save(OUT/f"page-{i+1:02d}.png")
                txt=page.get_text(sort=True)
                print("SOURCE_PAGE",i+1,"extracted_chars",len(txt),flush=True)
                if len(txt)>50:print(txt[:3400],flush=True)
            doc.close()
            print("ORIGINAL_SOURCE_COMPLETE",json.dumps(meta,ensure_ascii=False),flush=True)
        except Exception as exc:
            meta["error"]=repr(exc)
if meta["status"]!="complete_original_pdf_pending_visual_source_qa":
    PDF.unlink(missing_ok=True)
    print("SOURCE_UNAVAILABLE_OR_PARTIAL",json.dumps(meta,ensure_ascii=False),flush=True)
(OUT/"audit.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if meta["status"]!="complete_original_pdf_pending_visual_source_qa":
    raise RuntimeError("PLX Q3 full signed original is not available; no data changes permitted")
