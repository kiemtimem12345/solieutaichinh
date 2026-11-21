#!/usr/bin/env python3
"""Source-only GEG Q1 2026 B09 notes 31 Mar restricted deposits; no data writes.

Use already established primary PDF URL + exact original SHA. Capture
the signed original note pages missing from previous 14-page artifact,
then inspect for collateral/bank deposit information at 31 Mar 2026.
"""
from pathlib import Path
import hashlib, io, json
import fitz
from inspect_geg_q1_2026_pdf import read_pdf, SOURCES
SOURCE_SHA="d8dade2f270452432a190bedddb46736523cc3a74b783ae1a2f82b76a5e74d5b"
out=Path("geg-q1-2026-b09-pledged-deposit-notes")
out.mkdir(exist_ok=True)
raw=None
for name,url in SOURCES:
 try:
  raw=read_pdf(name,url)
  if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
   print("HASH_MISMATCH",name,hashlib.sha256(raw).hexdigest(),flush=True)
   raw=None
   continue
  break
 except Exception as e:
  print("SOURCE_UNAVAILABLE",name,repr(e)[:300],flush=True)
if raw is None:raise RuntimeError("GEG Q1 official 82 page signed PDF SHA not recovered")
d=fitz.open(stream=raw,filetype="pdf")
assert len(d)==82,(len(d),"unexpected original format")
pages=[]
for p in range(15,43):
 page=d[p-1]
 txt=page.get_text(sort=True)
 pix=page.get_pixmap(matrix=fitz.Matrix(1.42,1.42),alpha=False)
 target=out/f"geg-q1-2026-original-p{p:02d}.jpg"
 pix.save(str(target),jpg_quality=87)
 pages.append({"page_number_1based":p,"text_chars":len(txt),"file":target.name,
               "matched_text_terms":[s for s in ("bảo lãnh","Tiền gửi","TÀI SẢN NGẮN HẠN KHÁC","Tài sản ngắn hạn khác","tiền và các khoản tương đương") if s.lower() in txt.lower()]})
 print("B09_PAGE",p,"chars",len(txt),"preview",repr(" ".join(txt.split()[:16]))[:100],flush=True)
(out/"audit.json").write_text(json.dumps({"source_sha256":SOURCE_SHA,"pages":pages},ensure_ascii=False,indent=2)+"\n")
print("GEG_Q1_SIGNED_NOTES_RECOVERED",len(pages),flush=True)
