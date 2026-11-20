#!/usr/bin/env python3
"""Read-only financial-report source health and original document catalogue audit.

The sources were approved in the user's project: issuer official IR, HOSE/HNX,
SSC disclosure portal, Vietstock eDocuments, WiData as secondary cross-check.
A reachable page or indexed URL is NOT the same as a complete issuer PDF, and
a secondary aggregated statistic NEVER upgrades a primary-source PASS flag.
"""
from concurrent.futures import ThreadPoolExecutor
from http.cookiejar import CookieJar
from html import unescape
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError
import datetime, json, re, subprocess
OUT=Path("financial-source-audit-20261120")
OUT.mkdir(exist_ok=True)
BASE="https://finance.vietstock.vn"
CODES=["PLX","GAS","VDS","GEG","IDC"]
YEARS=[2025,2026]
SITES={
 "HOSE_root":"https://www.hsx.vn/",
 "HOSE_PDF_PLX_parent_Q3":"https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%20Q3%20nam%202026.pdf",
 "HNX_IDC_disclosures":"https://www.hnx.vn/vi-vn/cophieu-etfs/chi-tiet-chung-khoan-ny-IDC.html?_des_tab=1",
 "SSC_public_portal":"https://congbothongtin.ssc.gov.vn/",
 "PLX_issuer_official_IR":"https://plx.petrolimex.com.vn/quan-he-nha-dau-tu.html",
 "PLX_issuer_other_IR":"https://www.petrolimex.com.vn/nha-dau-tu.html",
 "PVGAS_issuer_reports":"https://www.pvgas.com.vn/sanpham-dich-vu/category/bao-cao-tai-chinh",
 "PVGAS_Q2_2026_full_issuer_pdf":"https://www.pvgas.com.vn/DesktopModules/EasyDNNNews/DocumentDownload.ashx?articleid=14585&documentid=3358&moduleid=648&portalid=0",
 "PVGAS_issuer_shareholder":"https://www.pvgas.com.vn/quan-he-co-%C4%91ong/tai-lieu-co-%C4%91ong",
 "IDC_HNX_original_BSC_attachment":"https://www.bsc.com.vn/News/NewsAttachedFile/1632697-1",
 "VDS_issuer_IR":"https://www.vdsc.com.vn/",
 "IDICO_issuer_site":"https://idico.com.vn/",
 "WiData_PLX_documents":"https://widata.vn/PLX?tab=documents",
 "WiData_GAS_documents":"https://widata.vn/GAS?tab=documents",
 "WiData_VDS_documents":"https://widata.vn/VDS?tab=documents",
 "WiData_GEG_documents":"https://widata.vn/GEG?tab=documents",
 "WiData_IDC_documents":"https://widata.vn/IDC?tab=documents",
 "Vietstock_PLX_catalog":"https://finance.vietstock.vn/PLX/tai-tai-lieu.htm?doctype=1",
 "Vietstock_GAS_catalog":"https://finance.vietstock.vn/GAS/tai-tai-lieu.htm?doctype=1",
 "Vietstock_VDS_catalog":"https://finance.vietstock.vn/VDS/tai-tai-lieu.htm?doctype=1",
 "Vietstock_GEG_catalog":"https://finance.vietstock.vn/GEG/tai-tai-lieu.htm?doctype=1",
 "Vietstock_IDC_catalog":"https://finance.vietstock.vn/IDC/tai-tai-lieu.htm?doctype=1"
}
def probe_site(pair):
 label,url=pair
 # --head keeps large/slow official PDF payloads off the runner entirely.
 p=subprocess.run(["curl","--location","--head","--silent","--show-error","--connect-timeout","8","--max-time","14","--user-agent","Mozilla/5.0 (SourceEvidenceAudit/1.0)","--write-out","\nRESULT_HTTP:%{http_code} FINAL_URL:%{url_effective} DOWNLOADED:%{size_download}",url],
     capture_output=True,text=True,timeout=18)
 statuses=re.findall(r"^HTTP/\S+\s+(\d{3})",p.stdout,re.M)
 size=re.findall(r"(?im)^content-length:\s*(\d+)",p.stdout)
 result={"label":label,"url":url,"curl_exit":p.returncode,
   "http_status":statuses[-1] if statuses else None,
   "content_length_header":size[-1] if size else None,
   "error":p.stderr.strip()[:210],
   "category":("secondary_aggregated_statistics_only" if label.startswith("WiData_") else
       "issuer_original_mirror_index_links_only" if label.startswith("Vietstock_") else
       "signed_original_pdf_locator_needs_identity_check" if label.startswith(("HOSE_PDF","PVGAS_Q2","IDC_HNX_original")) else
       "original_issuer_or_exchange_disclosure_site")}
 # Some known financial listings implement GET but return 404/405 to HEAD.
 # Recheck safe HTML listings, never use bypass for invalid TLS or DNS.
 if result["http_status"] in ("404","405") and not label.startswith("HOSE_PDF"):
  x=subprocess.run(["curl","--location","--silent","--show-error",
     "--connect-timeout","8","--max-time","14","--max-filesize","500000",
     "--range","0-131071","--output","/dev/null",
     "--write-out","%{http_code}",url],capture_output=True,text=True,timeout=18)
  result["head_http_status"]=result["http_status"]
  result["get_probe_status"]=x.stdout[-3:] if len(x.stdout)>=3 else None
  result["get_probe_curl_exit"]=x.returncode
  if x.returncode==0 and result["get_probe_status"] in ("200","206"):
   result["http_status"]=result["get_probe_status"]
   result["verified_method"]="GET fallback after HEAD method rejected"
 if result["http_status"] in ("200","206"):
  result["status"]="reachable_listing_or_url_not_pdf_visual_PASS"
 elif p.returncode!=0:
  result["status"]="timeout_or_unavailable_not_proof_of_missing_report"
 else:result["status"]="http_status_not_verified"
 print("WEB_SOURCE",json.dumps(result,ensure_ascii=False),flush=True)
 return result
def catalog(code):
 from urllib.parse import urljoin
 opener=build_opener(HTTPCookieProcessor(CookieJar()))
 doc_url=f"{BASE}/{code}/tai-tai-lieu.htm?doctype=1"
 data={"code":code,"results":[]}
 try:
  req=Request(doc_url,headers={"User-Agent":"Mozilla/5.0 (PublicFinancialDocs/1.0)","Accept":"text/html,*/*"})
  with opener.open(req,timeout=20) as r:raw=r.read(600000).decode("utf-8","replace")
  m=re.search(r'<form[^>]*id=__CHART_AjaxAntiForgeryForm[^>]*>\s*<input[^>]*name=__RequestVerificationToken[^>]*value=([^\s>]+)',raw,re.I)
  if not m:m=re.search(r'__RequestVerificationToken\s+type=hidden\s+value=([^\s>]+)',raw,re.I)
  if not m:raise ValueError("fresh public anti-forgery token unavailable")
  token=unescape(m.group(1).strip('"').strip("'"))
  for year in YEARS:
   payload=urlencode({"code":code,"page":1,"year":year,"type":1,"__RequestVerificationToken":token}).encode()
   req=Request(BASE+"/data/getdocument",data=payload,
      headers={"User-Agent":"Mozilla/5.0 (PublicFinancialDocs/1.0)","Referer":doc_url,
      "Accept":"application/json, */*","X-Requested-With":"XMLHttpRequest"})
   with opener.open(req,timeout=18) as r:reply=json.loads(r.read(700000).decode("utf-8","replace"))
   rows=reply if isinstance(reply,list) else reply.get("data",[]) if isinstance(reply,dict) else []
   if not isinstance(rows,list):raise ValueError("invalid API rows")
   docs=[{"label":unescape(str(x.get("FullName") or x.get("Title") or "")),
          "url":str(x.get("Url") or ""),"file_info_id":x.get("FileInfoID"),
          "type":str(x.get("FileExt") or "").strip()} for x in rows if isinstance(x,dict)]
   ok=[x for x in docs if x["url"].startswith(("https://static2.vietstock.vn/","https://www.pvgas.com.vn/","https://files.petrolimex.com.vn/"))]
   data["results"].append({"year":year,"records":len(docs),"valid_original_report_link_candidates":len(ok),"documents":ok})
  data["status"]="public_document_catalogue_retrieved_links_only"
 except Exception as e:
  data["status"]="catalogue_not_retrieved";data["error"]=type(e).__name__+": "+str(e)[:220]
 print("CATALOG",code,data["status"],"years",[(x["year"],x["records"]) for x in data["results"]],flush=True)
 return data
def probe_hose_ranges():
 # Real content-range support determines whether 14MB original can be recovered
 # safely in bounded pieces without SSL bypass or unbounded PDF download.
 url=SITES["HOSE_PDF_PLX_parent_Q3"]
 target=OUT/"hose_q3_parent_range_first_4kb.bin"
 p=subprocess.run(["curl","--fail","--location","--silent","--show-error",
   "--connect-timeout","8","--max-time","17","--max-filesize","131072",
   "--range","0-4095","--output",str(target),
   "--write-out","%{http_code} %{size_download}",url],
   capture_output=True,text=True,timeout=21)
 raw=target.read_bytes() if target.exists() else b""
 supports=p.returncode==0 and p.stdout.strip().startswith("206") and len(raw)==4096 and raw.startswith(b"%PDF")
 answer={"url":url,"range":"bytes=0-4095","curl_exit":p.returncode,
   "http_and_downloaded":p.stdout.strip(),"bytes_saved":len(raw),
   "is_pdf_header":raw.startswith(b"%PDF"),"supports_exact_206_byte_ranges":supports,
   "error":p.stderr.strip()[:220],"original_complete_pdf_validated":False}
 target.unlink(missing_ok=True)
 print("HOSE_RANGE_PROBE",json.dumps(answer,ensure_ascii=False),flush=True)
 return answer

with ThreadPoolExecutor(max_workers=9) as pool:
 sites=list(pool.map(probe_site,SITES.items()))
with ThreadPoolExecutor(max_workers=5) as pool:
 catalogs=list(pool.map(catalog,CODES))
report={"generated_at_utc":"2026-11-20","purpose":"recheck previously added financial-report data sources, no production financial changes",
 "sources":sites,"document_catalogues":catalogs,"hose_parent_original_range_probe":probe_hose_ranges(),
 "rules":["issuer/exchange signed PDF and source version is primary","Vietstock document URL is original-PDF mirror/index only, needs byte/full visual gate","WiData is secondary statistic cross-check only","SSC ADF dynamic table without verified file is existence only","PLC is not PLX; no subsidiary cross-scope substitution","HEAD HTTP 200 is NOT visual financial PASS"]}
(OUT/"sources-and-catalogues.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("AUDIT_SUMMARY",json.dumps({"site_200":sum(s["http_status"]=="200" for s in sites),
 "site_count":len(sites),"catalog_success":sum(c["status"].startswith("public") for c in catalogs),
 "catalog_count":len(catalogs),"total_document_urls":sum(y["valid_original_report_link_candidates"] for c in catalogs for y in c["results"])},ensure_ascii=False),flush=True)
