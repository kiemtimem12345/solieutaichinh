#!/usr/bin/env python3
"""Recover source-signed Q3/2026 VIX archive from Vietstock disclosure catalog.

Only accept when ZIP contains signed source financial PDF with original scope.
Never assume ZIP data are approved before inspecting page renders.
"""
from pathlib import Path
import subprocess,zipfile,json,hashlib
import fitz
d=Path("vix-q3-2026-vietstock-recovery");d.mkdir(exist_ok=True)
sources={
 "Vietstock_listing_zip":"https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%203/VIX_Baocaotaichinh_Q3_2026.zip?ver=8c766727",
 "Issuer_www_alternate":"https://www.vixs.vn/wp-content/uploads/2026/10/20261019-VIX-Baocaotaichinh-Quy-3-nam-2026.pdf",
}
rows=[]
for key,url in sources.items():
 dst=d/("source.zip" if "zip" in key else "issuer_www.pdf")
 cmd=["curl","-L","-f","-s","-S","--connect-timeout","18","--max-time","95",
      "--max-filesize","70000000","-H","User-Agent: Mozilla/5.0",
      "-o",str(dst),"-w","HTTP=%{http_code} BYTES=%{size_download}",url]
 try:
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=105)
  info={"source":key,"url":url,"rc":p.returncode,"result":p.stdout,"error":p.stderr[:200]}
  if p.returncode==0 and dst.exists() and dst.stat().st_size>50000:
   blob=dst.read_bytes()
   info.update({"sha256":hashlib.sha256(blob).hexdigest(),"bytes":len(blob)})
   if blob[:4]==b"%PDF":
    pdf=fitz.open(dst);info.update({"status":"pdf_complete","pages":len(pdf)})
    pdf.close()
   elif zipfile.is_zipfile(dst):
    with zipfile.ZipFile(dst) as archive:
     info["members"]=[{"name":x.filename,"bytes":x.file_size} for x in archive.infolist()]
     for member in archive.infolist():
      if member.filename.lower().endswith(".pdf") and 150000<member.file_size<60000000:
       out=d/Path(member.filename).name;out.write_bytes(archive.read(member))
       p2=fitz.open(out)
       info.setdefault("extracted_pdfs",[]).append({
        "name":out.name,"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
        "pages":len(p2),"bytes":out.stat().st_size,
        "text_chars_first_18":[len(p2[i].get_text()) for i in range(min(18,len(p2)))]})
       p2.close()
    info["status"]="zip_complete"
   else:info["status"]="unexpected_binary";dst.unlink(missing_ok=True)
  else:info["status"]="unavailable";dst.unlink(missing_ok=True)
  rows.append(info)
 except Exception as e:
  rows.append({"source":key,"status":"error","err":repr(e)})
 print("SOURCE_RESULT",json.dumps(rows[-1],ensure_ascii=False),flush=True)
(d/"audit.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False)+"\n")
assert any("complete" in z["status"] for z in rows),"Could not retrieve any Q3 original or mirror"
