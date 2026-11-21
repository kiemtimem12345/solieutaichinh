#!/usr/bin/env python3
"""VIX signed original Q3/2025 separate PDF read-only recovery for B01/B02/B03."""
from pathlib import Path
import subprocess,hashlib,json,fitz
URLS={
 "issuer":"https://vixs.vn/wp-content/uploads/2025/10/VIX-BCTC-QuyIII-2025.pdf",
 "vietstock":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/VIX_Baocaotaichinh_Q3_2025.pdf"
}
OUT=Path("vix-2025q3-original-audit"); OUT.mkdir(exist_ok=True)
reports={}
for name,url in URLS.items():
 dst=OUT/(name+".pdf")
 cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","12","--max-time","75",
      "--max-filesize","30000000","--output",str(dst),"--write-out","%{http_code} %{size_download}",
      "--header","User-Agent: Mozilla/5.0 (VIXIssuerOriginalQA/1.0)",url]
 try:
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=82)
  row={"url":url,"curl_rc":p.returncode,"http_size":p.stdout[:110],"error":p.stderr[:200]}
  if p.returncode==0 and dst.exists() and dst.stat().st_size>100000 and dst.read_bytes()[:4]==b"%PDF":
   doc=fitz.open(dst)
   row.update({"status":"complete","sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),
              "bytes":dst.stat().st_size,"pages":len(doc)})
   for i in range(min(24,len(doc))):
    doc[i].get_pixmap(matrix=fitz.Matrix(1.75,1.75),alpha=False).save(OUT/f"{name}-p{i+1:02d}.png")
   row["pages_native_text_chars"]=[len(doc[i].get_text()) for i in range(min(20,len(doc)))]
   doc.close()
  else:
   row["status"]="unavailable_or_partial";dst.unlink(missing_ok=True)
  reports[name]=row
 except Exception as exc:
  reports[name]={"url":url,"status":"error","message":repr(exc)[:300]};dst.unlink(missing_ok=True)
 print("ORIGINAL_RESULT",name,json.dumps(reports[name],ensure_ascii=False),flush=True)
(OUT/"audit.json").write_text(json.dumps(reports,indent=2,ensure_ascii=False)+"\n")
assert reports["issuer"]["status"]=="complete","Never accept unverified Q3 PDF"
print("PRIMARY_ORIGINAL_COMPLETE",json.dumps(reports["issuer"],ensure_ascii=False),flush=True)
