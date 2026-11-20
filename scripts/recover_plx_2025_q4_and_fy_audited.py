#!/usr/bin/env python3
"""Read-only source recovery: PLX FY/Q4 2025 consolidated original and audited FY.

Exact URLs came from public Vietstock Finance eDocument catalogue. The 12M
cashflow requires signed source and standalone Q4 requires signed Q3 9M
same financial presentation basis; audited FY may adjust source vintage.
No financial JSON promotion without full original + visual QA. Each download
is independent, bounded, with no partial PDF trust.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib,json,subprocess
import fitz

OUT=Path("plx-2025-q4-fy-originals")
OUT.mkdir(exist_ok=True)
SOURCES={
 "PLX_2025_Q4_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/PLX_Baocaotaichinh_Q4_2025_Hopnhat.pdf",
 "PLX_2025_FY_AUDITED_CONSOLIDATED":"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/NAM/PLX_Baocaotaichinh_2025_Kiemtoan_Hopnhat.pdf",
}
def fetch(item):
 label,url=item
 folder=OUT/label;folder.mkdir(exist_ok=True)
 dest=folder/"signed_original.pdf"
 cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","12","--max-time","98","--max-filesize","42000000","--output",str(dest),
      "--write-out","%{http_code} %{size_download} %{url_effective}",
      "--header","User-Agent: Mozilla/5.0 (IssuerSignedFinancialSourceQA/1.0)",url]
 rec={"label":label,"source_url":url,"status":"source_unavailable_or_incomplete"}
 try:
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=105)
  rec.update({"curl_exit":p.returncode,"http_report":p.stdout[:400],"stderr":p.stderr[:350]})
  if p.returncode!=0:raise ValueError("source HTTP/transfer not complete")
  raw=dest.read_bytes()
  if not (len(raw)>100000 and raw.startswith(b"%PDF")):raise ValueError("source incomplete/invalid signature")
  doc=fitz.open(str(dest))
  if not 12<=len(doc)<=160:raise ValueError("signed original unexpected page count")
  rec.update({"status":"complete_signed_original_pending_visual_source_qa","sha256":hashlib.sha256(raw).hexdigest(),"pages":len(doc),"bytes":len(raw)})
  for i in range(min(len(doc),21)):
   page=doc[i]
   pix=page.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False)
   pix.save(folder/f"page-{i+1:02d}.png")
   text=page.get_text(sort=True)
   print("SOURCE_PAGE",label,i+1,"text_chars",len(text),flush=True)
   if len(text)>80:print(text[:1800],flush=True)
  doc.close()
  print("SIGNED_ORIGINAL_OK",json.dumps(rec,ensure_ascii=False),flush=True)
 except Exception as e:
  rec.update({"exception_type":type(e).__name__,"failure":str(e)[:300]})
  dest.unlink(missing_ok=True)
  print("SOURCE_BLOCKED",json.dumps(rec,ensure_ascii=False),flush=True)
 return rec
with ThreadPoolExecutor(max_workers=2) as ex:
 result=list(ex.map(fetch,SOURCES.items()))
(OUT/"source-audit.json").write_text(json.dumps({"sources":result},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("SOURCE_RECOVERY_SUMMARY",json.dumps({"complete_count":sum(x["status"].startswith("complete") for x in result),"requested_count":len(result)}),flush=True)
if not any(x["status"].startswith("complete") for x in result):raise RuntimeError("No complete issuer original recovered; preserve all previously PASS data")
