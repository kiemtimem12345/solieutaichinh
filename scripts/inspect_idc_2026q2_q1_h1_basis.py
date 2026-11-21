#!/usr/bin/env python3
"""Inspect issuer originals IDC 2026Q1 vs H1 2026 TT99/TT43 accounting basis.

Bounded source-only original recovery; no source values changed. Focus on
current-period cashflow note and accounting policy, comparative restatement.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import fitz,hashlib,json
out=Path("idc-2026q2-tt43-quarter-comparison");out.mkdir(exist_ok=True)
sources=[
 ("Q1_original","https://static2.vietstock.vn/data/HNX/2026/BCTC/VN/QUY%201/IDC_Baocaotaichinh_Q1_2026_Hopnhat.pdf",
 "229a1ff9af9d3e1bffd777a0c9b92b4bd5cbee5bc02765f02bee5778c2b2085b",66,[11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]),
 ("H1_2026_reviewed","https://www.bsc.com.vn/News/NewsAttachedFile/1599258-1",
 "f1366ab8629fb1482e30995ae28462d03a7819c72a70aab5311c5b2f9ee28944",72,[10,16,17,18,19,20,21,22,34,70,71])
]
result=[]
for name,url,sha,expected_pages,indices in sources:
 try:
  req=Request(url,headers={"User-Agent":"Mozilla/5.0 (IDC original current-period B03 QA)","Accept-Encoding":"identity","Referer":"https://finance.vietstock.vn/"})
  with urlopen(req,timeout=70) as resp:
   host=urlparse(resp.geturl()).hostname
   assert host in ("static2.vietstock.vn","www.bsc.com.vn","bsc.com.vn","files.bsc.com.vn"),("bad redirect",host)
   raw=resp.read(30*1024*1024)
  assert raw[:4]==b"%PDF"
  assert hashlib.sha256(raw).hexdigest()==sha,("source SHA mismatch",name,hashlib.sha256(raw).hexdigest())
  d=fitz.open(stream=raw,filetype="pdf")
  assert len(d)==expected_pages,(name,len(d))
  pages=[]
  for pn in indices:
   page=d[pn-1]; t=page.get_text(sort=True)
   pix=page.get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False)
   dest=out/f"{name}-signed-p{pn:02d}.jpg"
   pix.save(dest,jpg_quality=87)
   pages.append({"page":pn,"textchars":len(t),"preview":" ".join(t.split()[:18])[:110]})
  result.append({"source":name,"url":url,"sha256":sha,"pages":len(d),"inspection":pages,"status":"PASS"})
  print("SOURCE_PASS",name,"pages",len(d),"renders",len(indices),flush=True)
 except Exception as e:
  result.append({"source":name,"status":"unavailable","error":repr(e)[:400]})
  print("SOURCE_ERROR",name,repr(e)[:400],flush=True)
(out/"audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
assert all(x.get("status")=="PASS" for x in result),"Missing signed primary source evidence"
