#!/usr/bin/env python3
"""Source-only retrieve signed MBB 2026-Q2/H1 and Q3/9M consolidated PDFs.

Validate actual PDF bytes and page renders, including Q3 standalone B03a
bank income and direct-method B04a cashflow. Do not write financial data.
"""
import hashlib,json
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import fitz
R=Path("mbb-2026-q2-q3-signed-source")
R.mkdir(exist_ok=True)
sources={
 "2026-Q2":{"url":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/MBB_Baocaotaichinh_Q2_2026_Hopnhat.pdf?ver=8b5fd9ba","page_numbers":[3,4,6,7,8]},
 "2026-Q3":{"url":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/MBB_Baocaotaichinh_Q3_2026_Hopnhat.pdf","page_numbers":[3,4,6,7,8]},
}
result=[]
for name,s in sources.items():
 try:
  req=Request(s["url"],headers={"User-Agent":"Mozilla/5.0 (MBB signed exact-bank-statement-audit)","Accept-Encoding":"identity","Referer":"https://finance.vietstock.vn/"})
  with urlopen(req,timeout=75) as resp:
   host=urlparse(resp.geturl()).hostname
   assert host=="static2.vietstock.vn",host
   data=resp.read(60*1024*1024)
  assert data.startswith(b"%PDF") and 100000<len(data)<60*1024*1024
  pdf=fitz.open(stream=data,filetype="pdf")
  assert len(pdf)==61,(len(pdf),"expected 61 original signed pages")
  report={"period":name,"source_url":s["url"],"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":len(pdf),"renders":[],"status":"complete"}
  for pn in s["page_numbers"]:
   p=pdf[pn-1];txt=p.get_text(sort=True)
   image=p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
   filename=f"MBB-{name}-signed-p{pn:02d}.jpg"
   image.save(R/filename,jpg_quality=88)
   report["renders"].append({"page":pn,"jpg":filename,"source_text_chars":len(txt)})
  result.append(report)
  print("MBB_PDF_PASS",json.dumps({k:v for k,v in report.items() if k!="renders"}),flush=True)
 except Exception as e:
  result.append({"period":name,"source_url":s["url"],"status":"FAIL","error":repr(e)[:450]})
  print("MBB_PDF_FAIL",repr(e)[:450],flush=True)
(R/"audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
if not all(r.get("status")=="complete" for r in result):raise RuntimeError("Cannot accept B03 derived Q3 without two complete signed original PDFs")
