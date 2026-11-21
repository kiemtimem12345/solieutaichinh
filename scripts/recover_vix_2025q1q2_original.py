#!/usr/bin/env python3
"""Recover original VIX Q1/Q2 2025 separate-financial PDFs, READ ONLY.

No financial values are changed. Source scope and source image evidence must
be inspected before accepting any existing OCR/crawler numeric field.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib, json, subprocess
import fitz

DOCS = {
    "VIX-2025Q1-Vietstock": "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/VIX_Baocaotaichinh_Q1_2025.pdf",
    "VIX-2025Q2-Vietstock": "https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/VIX_Baocaotaichinh_Q2_2025.pdf",
    "VIX-2025Q1-issuer": "https://vixs.vn/wp-content/uploads/2025/04/20250418-VIX-Bao-cao-tai-chinh-Quy-I.2025.pdf",
    "VIX-2025Q2-issuer": "https://vixs.vn/wp-content/uploads/2025/07/20250718-VIX-Baoaotaichinh-Quy-2.2025-VIE.pdf",
}
OUT=Path("vix-2025-q1q2-source-audit")
OUT.mkdir(exist_ok=True)

def recover(item):
    name,url=item
    pdf=OUT/f"{name}.pdf"
    cmd=["curl","--fail","--location","--silent","--show-error",
         "--connect-timeout","10","--max-time","65","--max-filesize","30000000",
         "--retry","0","--output",str(pdf),"--write-out","%{http_code} %{size_download}",
         "--header","User-Agent: Mozilla/5.0 (SignedReportSourceReview/1.0)",url]
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=72)
        result={"name":name,"source_url":url,"curl_returncode":p.returncode,
                "curl_status":p.stdout[:100],"error":p.stderr[:200]}
        if p.returncode==0 and pdf.exists() and pdf.stat().st_size>100000:
            raw=pdf.read_bytes()
            if raw[:4]==b"%PDF":
                doc=fitz.open(pdf)
                result.update({"status":"recovered_original_pdf",
                   "size":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"pages":len(doc)})
                lines=[]
                for n,page in enumerate(doc):
                    s=page.get_text(sort=True)
                    lines.append(f"PAGE {n+1} chars={len(s)} TEXT {s[:2200]!r}")
                    # Save first 12 pages of signed reports for B01/B02/B03 (asset cap).
                    if n<12:
                        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(OUT/f"{name}-p{n+1:02d}.png")
                (OUT/f"{name}-pages.txt").write_text("\n".join(lines)+"\n")
                result["text_pages_with_100_chars"]=sum("chars=" in z and int(z.split("chars=")[1].split()[0])>100 for z in lines)
                doc.close()
                # Keep PDFs in artifact for visual QA, do not commit copyrighted bytes to Git.
                return result
        pdf.unlink(missing_ok=True)
        result["status"]="unavailable_or_partial"
        return result
    except Exception as e:
        pdf.unlink(missing_ok=True)
        return {"name":name,"status":"fetch_error","source_url":url,"error":repr(e)[:250]}

with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(recover,DOCS.items()))
for r in results:
    print("SOURCE_RESULT",json.dumps(r,ensure_ascii=False),flush=True)
(OUT/"audit.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
count=sum(r["status"]=="recovered_original_pdf" for r in results)
print("RECOVERED",count,"of",len(DOCS),"signed source PDF copies (source provenance, NO financial values were changed)",flush=True)
if count==0:raise RuntimeError("Neither original PDF source recovered")
