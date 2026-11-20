#!/usr/bin/env python3
"""Rebuild official HOSE PLX Q3/2026 parent PDF using verified HTTP 206 ranges.

Source is EXACT official HOSE URL discovered from issuer announcement. A bounded
4KiB 206-range probe already succeeded (Actions 44675803871). This script
strictly requires HTTP 206, correct Content-Range and byte count for EVERY
segment, and a valid complete PDF. No certificate bypass, partial-file trust,
issuer accounting rewrites, or public Git storage of PDF bytes.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib,json,math,re,subprocess,time
import fitz

URL="https://staticfile.hsx.vn/Uploads/UploadDocuments/2510747/20261030%20-%20PLX%20-%20Bao%20cao%20tai%20chinh%20Cong%20ty%20me%20Q3%20nam%202026.pdf"
SIZE=14241486
CHUNK=262144
OUT=Path("plx-hose-q3-parent-official-range-source")
OUT.mkdir(exist_ok=True)
PARTS=OUT/"parts"
PARTS.mkdir(exist_ok=True)
EXPECTED_PETROLIMEX_SIGNED_SOURCE_BYTES=14198075
EXPECTED_PETROLIMEX_SIGNED_SOURCE_SHA256="a8073e73803664a01601be8b4e416cb33ec90bfd3eca05560bbed454edcbefef"
def task(i):
 start=i*CHUNK
 end=min(SIZE-1,start+CHUNK-1)
 length=end-start+1
 outfile=PARTS/f"segment-{i:03d}.bin"
 headers=PARTS/f"segment-{i:03d}.headers"
 last=""
 for attempt in range(2):
  cmd=["curl","--fail","--location","--silent","--show-error","--connect-timeout","9","--max-time","44",
    "--range",f"{start}-{end}","--dump-header",str(headers),"--output",str(outfile),
    "--write-out","%{http_code} %{size_download} %{url_effective}",
    "--header","Accept-Encoding: identity",
    "--header","User-Agent: Mozilla/5.0 (ExchangeSignedSourceQA/1.0)",URL]
  try:
   p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=49)
   received=outfile.read_bytes() if outfile.exists() else b""
   h=headers.read_text("utf-8",errors="replace") if headers.exists() else ""
   statuses=re.findall(r"(?mi)^HTTP/\S+\s+(\d{3})",h)
   content_ranges=re.findall(r"(?mi)^content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)",h)
   code=statuses[-1] if statuses else p.stdout[:3]
   valid=(p.returncode==0 and code=="206" and len(received)==length and
    content_ranges and content_ranges[-1]==(str(start),str(end),str(SIZE)))
   if valid:return {"index":i,"start":start,"end":end,"bytes":length,"sha256":hashlib.sha256(received).hexdigest(),"attempt":attempt+1}
   last=f"curl={p.returncode} code={code} received={len(received)}/{length} cr={content_ranges[-1:]}, stderr={p.stderr[:120]}"
  except Exception as e:last=type(e).__name__+": "+str(e)[:140]
  outfile.unlink(missing_ok=True)
  headers.unlink(missing_ok=True)
 raise RuntimeError(f"segment {i} range {start}-{end} failed after 2 attempts: {last}")
results=[]
failures=[]
count=math.ceil(SIZE/CHUNK)
with ThreadPoolExecutor(max_workers=10) as pool:
 futures={pool.submit(task,i):i for i in range(count)}
 for future in as_completed(futures):
  try:
   result=future.result()
   results.append(result)
   print(f"RANGE_OK {result['index']+1}/{count} len={result['bytes']} retry={result['attempt']-1}",flush=True)
  except Exception as e:
   failures.append({"segment":futures[future],"error":str(e)[:280]})
   print("RANGE_FAILED",str(e)[:280],flush=True)
a={"official_exchange":"HOSE","url":URL,"expected_original_bytes":SIZE,
   "segment_size":CHUNK,"segment_count":count,"success_segments":len(results),
   "failures":failures,"previous_petrolimex_signed_original_pdf_sha256":EXPECTED_PETROLIMEX_SIGNED_SOURCE_SHA256,
   "previous_petrolimex_signed_original_bytes":EXPECTED_PETROLIMEX_SIGNED_SOURCE_BYTES}
if failures:
 (OUT/"audit.json").write_text(json.dumps(a,indent=2)+"\n")
 raise RuntimeError("Range assembly incomplete. No full official source or financial conclusion permitted.")
dest=OUT/"PLX-Q3-2026-parent-HOSE-original.pdf"
with dest.open("wb") as out:
 for i in range(count):
  path=PARTS/f"segment-{i:03d}.bin"
  out.write(path.read_bytes())
  path.unlink(missing_ok=True)
  (PARTS/f"segment-{i:03d}.headers").unlink(missing_ok=True)
raw=dest.read_bytes()
if len(raw)!=SIZE or not raw.startswith(b"%PDF"):raise ValueError("Assembled byte length/PDF signature mismatch")
pdf=fitz.open(str(dest))
if not 20<=len(pdf)<=75:raise ValueError("Unexpected HOSE PDF structure page count "+str(len(pdf)))
a.update({"verified_complete_pdf":True,"assembled_sha256":hashlib.sha256(raw).hexdigest(),"assembled_pages":len(pdf),"same_sha256_as_petrolimex_original":hashlib.sha256(raw).hexdigest()==EXPECTED_PETROLIMEX_SIGNED_SOURCE_SHA256})
for i in range(min(16,len(pdf))):
 page=pdf[i]
 pic=page.get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False)
 pic.save(OUT/f"PLX-HOSE-page-{i+1:02d}.png")
 text=page.get_text(sort=True)
 print(f"PDF_PAGE {i+1}: readable_text_chars={len(text)}",flush=True)
 if len(text)>40:print(text[:3000],flush=True)
a["status"]="signed_issuer_original_HOSE_complete_requires_independent_visual_B03_subtotal_comparison"
(OUT/"audit.json").write_text(json.dumps(a,indent=2)+"\n")
print("HOSE_COMPLETE_PDF",json.dumps(a,ensure_ascii=False),flush=True)
