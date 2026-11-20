#!/usr/bin/env python3
"""Retrieve PLX public BCTC document index using Vietstock's published API contract.

Discovered from the site's live JS bundle 2026-11-20:
  POST /data/getdocument {code: PLX, page, year, type, __RequestVerificationToken}.
The public listing is an index only. Never treat its data as a verified issuer PDF.
Use a session cookie and the dynamically generated anti-forgery token, not a
hardcoded token, no login, bounded response/time. No data/financials edits.
"""
import json, re, sys, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,build_opener,HTTPCookieProcessor
from urllib.error import HTTPError
from http.cookiejar import CookieJar
BASE="https://finance.vietstock.vn"
INDEX=BASE+"/PLX/tai-tai-lieu.htm?doctype=1"
OUT=Path("plx-2026-vietstock-documents")
OUT.mkdir(exist_ok=True)
op=build_opener(HTTPCookieProcessor(CookieJar()))
def fetch(path,data=None):
 req=Request(BASE+path if path.startswith("/") else path,data=data,
 headers={"User-Agent":"Mozilla/5.0 (compatible; PublicBCTCIndexDiscovery/1.0)",
          "Accept":"application/json, text/javascript, */*" if data else "text/html, */*",
          "Accept-Encoding":"identity","Referer":INDEX,
          "X-Requested-With":"XMLHttpRequest" if data else ""})
 with op.open(req,timeout=25) as f:
  return f.status,f.read(1600000),f.headers.get("Content-Type","")
status,html,ct=fetch(INDEX)
assert status==200 and len(html)>10000,"Public source listing unavailable"
raw=html.decode("utf-8","replace")
match=re.search(r'<form[^>]*id=__CHART_AjaxAntiForgeryForm[^>]*>\s*<input[^>]*name=__RequestVerificationToken[^>]*value=([^\s>]+)',raw,re.I)
if not match:
 match=re.search(r'__RequestVerificationToken\s+type=hidden\s+value=([^\s>]+)',raw,re.I)
if not match:raise RuntimeError("Missing fresh public anti-forgery token. Do not reuse an older session token.")
token=match.group(1).strip('"').strip("'")
results=[]
for page in (1,2,3):
 payload=urlencode({"code":"PLX","page":page,"year":2026,"type":1,"__RequestVerificationToken":token}).encode()
 try:
  st,body,ct=fetch("/data/getdocument",payload)
 except HTTPError as e:
  print("INDEX_HTTP_BLOCKED",page,e.code,str(e.reason),flush=True)
  results.append({"page":page,"status":e.code})
  break
 text=body.decode("utf-8","replace")
 try: data=json.loads(text)
 except Exception:
  print("INDEX_NONJSON",page,st,ct,len(text),repr(text[:280]),flush=True)
  results.append({"page":page,"status":st,"content_type":ct,"body_prefix":text[:280]})
  break
 rows=data if isinstance(data,list) else data.get("data",data.get("Data",[])) if isinstance(data,dict) else []
 print("INDEX_RESPONSE",page,"status",st,"kind",type(data).__name__,"rows",len(rows) if isinstance(rows,list) else "unknown",flush=True)
 if isinstance(data,dict):print("INDEX_KEYS",list(data)[:24],flush=True)
 matches=[]
 if isinstance(rows,list):
  for v in rows:
   if not isinstance(v,dict):continue
   joined=" ".join(str(x) for x in v.values()).lower()
   if "2026" in joined or any(t in joined for t in ("bctc","financial","quý 3","quy 3","soát xét","soat xet","bán niên")):
    matches.append(v)
    print("DOCUMENT_INDEX_ROW",json.dumps(v,ensure_ascii=False)[:1350],flush=True)
 results.append({"page":page,"status":st,"type":type(data).__name__,"count":len(rows) if isinstance(rows,list) else 0,"matching_rows":matches[:35]})
 if not rows or not isinstance(rows,list) or len(rows)<20:break
(OUT/"public-document-index.json").write_text(json.dumps({"index":INDEX,"discovered_api_endpoint":"/data/getdocument","retrieved_on":"2026-11-20","results":results},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("DOCUMENT_INDEX_DONE source_metadata_only_no_original_pdf_validation",flush=True)
