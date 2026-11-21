#!/usr/bin/env python3
"""Recover original signed issuer Q4/2025 VIX separate PDF; no data modification."""
import hashlib,json,subprocess
from pathlib import Path
import fitz
OUT=Path("vix-2025q4-original-source")
OUT.mkdir(exist_ok=True)
URLS={
 "issuer_Q4":"https://vixs.vn/wp-content/uploads/2026/01/20260112-VIX-Baocaotaichinh-Quy-4-2025.pdf",
 "issuer_self_2025_erratum":"https://vixs.vn/wp-content/uploads/2026/02/20260210-VIX-Dinh-chinh-BCTC-NAM-2025-tu-lap-Phat-hanh-lai.pdf"
}
all={}
for name,url in URLS.items():
    dest=OUT/f"{name}.pdf"
    cmd=["curl","-f","-L","-s","-S","--connect-timeout","10","--max-time","110",
         "--max-filesize","35000000","-H","User-Agent: Mozilla/5.0 (SignedSourceQA/1.0)",
         "--output",str(dest),"--write-out","%{http_code} %{size_download}",url]
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
        x={"url":url,"curl_rc":p.returncode,"http_bytes":p.stdout,"err":p.stderr[:240]}
        if p.returncode==0 and dest.is_file() and dest.stat().st_size>100000 and dest.read_bytes()[:4]==b"%PDF":
            blob=dest.read_bytes()
            pdf=fitz.open(dest)
            x.update({"status":"original_complete","bytes":len(blob),"sha256":hashlib.sha256(blob).hexdigest(),"pages":len(pdf)})
            if name=="issuer_Q4":
                for i in range(min(18,len(pdf))):
                    page=pdf[i]
                    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(OUT/f"Q4-page-{i+1:02d}.png")
            pdf.close()
        else:
            x["status"]="source_inaccessible_or_partial"
            dest.unlink(missing_ok=True)
        all[name]=x
    except Exception as e:
        all[name]={"url":url,"status":"error","error":repr(e)[:250]};dest.unlink(missing_ok=True)
    print("SOURCE_RESULT",name,json.dumps(all[name],ensure_ascii=False),flush=True)
(OUT/"audit.json").write_text(json.dumps(all,indent=2,ensure_ascii=False)+"\n")
assert all["issuer_Q4"]["status"]=="original_complete","Q4 original not fully downloaded and verified"
print("ISSUER_Q4_COMPLETE",json.dumps(all["issuer_Q4"]),flush=True)
