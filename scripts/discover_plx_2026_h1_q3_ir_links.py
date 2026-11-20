#!/usr/bin/env python3
"""Bounded, read-only PLX H1/2026 parent reviewed and Q3 consolidated source discovery.

Issuer's IR page lists both disclosures. Discover original attachment URL rather
than inventing a PDF filename. Per-URL curl subprocess has an enforced total
deadline (unlike urllib read socket timeouts), and all origins are issuer-owned.
No production data changes; discovered links are unverified until PDF inspection.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import html, json, re, subprocess, unicodedata

OUT=Path("plx-2026-ir-discovery")
OUT.mkdir(parents=True, exist_ok=True)
PAGES=[
 ("official_IR","https://www.petrolimex.com.vn/quan-he-nha-dau-tu.html"),
 ("plx_IR","https://plx.petrolimex.com.vn/quan-he-nha-dau-tu.html"),
 ("w_IR","https://w.petrolimex.com.vn/quan-he-nha-dau-tu.html"),
 ("issuer_shareholder","https://www.petrolimex.com.vn/ndi/thong_tin_co_dong/"),
 ("issuer_nha_dau_tu","https://www.petrolimex.com.vn/nha-dau-tu.html"),
 ("vietstock_PLX_catalog","https://finance.vietstock.vn/PLX/tai-tai-lieu.htm?doctype=1"),
 ("HOSE_Q3_consolidated_listing","https://nmquan.vn/data/ma/PLX/cong-bo/245179924-bao-cao-tai-chinh-hop-nhat-q3-nam-2026"),
 ("HOSE_H1_parent_listing","https://nmquan.vn/data/ma/PLX/cong-bo/50884368-bao-cao-tai-chinh-cong-ty-me-6-thang-nam-2026-sau-soat-xet"),
 ("HOSE_H1_consolidated_listing","https://nmquan.vn/data/ma/PLX/cong-bo/52619791-bao-cao-tai-chinh-hop-nhat-6-thang-nam-2026-sau-soat-xet"),
 ("issuer_parent_H1_pdf_HOSE_candidate","https://staticfile.hsx.vn/Uploads/UploadDocuments/2493840/20260828%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%206%20thang%20nam%202026%20sau%20soat%20xet.pdf"),
]
ALLOWED={"www.petrolimex.com.vn","plx.petrolimex.com.vn","w.petrolimex.com.vn","files.petrolimex.com.vn","staticfile.hsx.vn","finance.vietstock.vn","nmquan.vn"}
def ascii_text(t):
 t=unicodedata.normalize("NFKD",html.unescape(unquote(t or ""))).lower()
 return "".join(c for c in t if not unicodedata.combining(c))
def relevant(t):
 t=ascii_text(t)
 return any(x in t for x in ("2026", "bao cao tai chinh", "bao cao", "soat xet", "q3"))
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.link=None
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=="a":self.link={"href":d.get("href",""),"title":d.get("title",""),"data":d,"text":""}
 def handle_data(self,t):
  if self.link is not None:self.link["text"]+=t
 def handle_endtag(self,tag):
  if tag=="a" and self.link is not None:self.links.append(self.link);self.link=None

def probe(pair):
 label,url=pair
 path=OUT/(label+".bin")
 cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","10","--max-time","28","--max-filesize","26000000","--compressed","--output",str(path),"--write-out","%{http_code} %{url_effective}","--header","User-Agent: Mozilla/5.0 (compatible; FinancialSourceVerification/1.0)",url]
 try:
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=32)
  status=p.stdout[:400]
  entry={"label":label,"source_url":url,"curl_return_code":p.returncode,"status_final":status,"stderr":p.stderr[:240]}
  if not path.exists():
   return entry
  raw=path.read_bytes()
  entry.update({"bytes":len(raw),"signature":raw[:12].hex()})
  if raw.startswith(b"%PDF"):
   import hashlib
   entry.update({"pdf_sha256":hashlib.sha256(raw).hexdigest(),"is_pdf":True})
   # PDF source only: keep as short-lived Actions artifact, not in Git.
   (OUT/(label+".pdf")).write_bytes(raw)
   return entry
  if b"<" not in raw[:1000] or len(raw)>3000000:
   return entry
  body=raw.decode("utf-8","replace")
  parsed=Page();parsed.feed(body)
  entry["anchor_count"]=len(parsed.links)
  matches=[]
  for a in parsed.links:
   text=ascii_text(a["text"]+" "+a["title"]+" "+a["href"])
   if "2026" not in text or not any(x in text for x in ("6 thang","ban nien","quy 3","quy iii","q3","soat xet","hop nhat","cong ty me","bctc")):continue
   target=urljoin(url,a["href"])
   host=urlparse(target).hostname
   if host and not (host.endswith("petrolimex.com.vn") or host in ("staticfile.hsx.vn",)):
    continue
   matches.append({"label":(a["text"]+" "+a["title"]).strip()[:280],"target_url":target,"attributes":{k:v for k,v in a["data"].items() if k in ("href","onclick","download","target","title")}})
  entry["matched_anchors"]=matches[:70]
  entry["candidate_attachment_url_spans"]=list(dict.fromkeys(re.findall(r"(?:https?:)?//[^\s\"\'<>]{0,360}(?:2026|pdf)[^\s\"\'<>]{0,160}",body,re.I)))[:40]
  corpus=ascii_text(body)
  snippets=[]
  for needle in ("bao cao tai chinh cong ty me 6 thang nam 2026","bao cao tai chinh hop nhat quy 3 nam 2026","bao cao tai chinh cong ty me quy 3 nam 2026"):
   i=corpus.find(needle)
   if i>=0:snippets.append({"search_phrase":needle,"index":i,"html_context":body[max(0,i-500):i+900]})
  entry["text_snippets"]=snippets
  print("SOURCE_IR",label,"status",p.returncode,"anchors",len(parsed.links),"targets",len(matches),flush=True)
  for m in matches[:40]:print("SOURCE_LINK",label,json.dumps(m,ensure_ascii=False),flush=True)
  return entry
 except Exception as exc:
  return {"label":label,"source_url":url,"error":type(exc).__name__,"detail":str(exc)[:240]}
with ThreadPoolExecutor(max_workers=5) as pool:
 entries=list(pool.map(probe,PAGES))
(OUT/"discovery.json").write_text(json.dumps({"sources":entries},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for e in entries:print("SOURCE_RESULT",json.dumps({k:v for k,v in e.items() if k not in ("matched_anchors","text_snippets","candidate_attachment_url_spans")},ensure_ascii=False),flush=True)
print("DONE: discovered URLs are candidates only; verify original signed PDF and report scope before any JSON update",flush=True)
