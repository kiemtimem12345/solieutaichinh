#!/usr/bin/env python3
"""VPB 2026 Q2 original issuer ZIP and independently reviewed H1 B04 source-only retrieval."""
from pathlib import Path
import zipfile,hashlib,subprocess,tempfile,re
BASE="https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/"
SOURCES=[("Q2_ISSUER_ORIGINAL",BASE+"VPB_Baocaotaichinh_Q2_2026_Hopnhat.zip",True),
 ("H1_2026_REVIEWED",BASE+"VPB_Baocaotaichinh_6T_2026_Soatxet_Hopnhat.pdf",False)]
OUT=Path("vpb-2026q2-original-source")
def run(args,t=150):
 p=subprocess.run(args,capture_output=True,text=True,timeout=t,check=False)
 if p.returncode:raise RuntimeError(str(args[0])+" "+p.stderr[:250])
 return p.stdout
def pdf(name,p):
 assert p.read_bytes()[:5]==b"%PDF-",name
 inf=run(["pdfinfo",str(p)],50)
 m=re.search(r"^Pages:\s*(\d+)",inf,re.M);assert m
 n=int(m.group(1));print(f"VPB_Q2_2026_PDF name={name} pages={n} bytes={p.stat().st_size} SHA256={hashlib.sha256(p.read_bytes()).hexdigest()}",flush=True)
 first,last=4,min(n,20)
 raw=run(["pdftotext","-layout","-f",str(first),"-l",str(last),str(p),"-"],110)
 (OUT/(name+"-text.txt")).write_text(raw[:115000],"utf8")
 print(f"VPB_Q2_2026_TEXT_BEGIN name={name}",flush=True)
 print(raw[:48000],flush=True)
 print(f"VPB_Q2_2026_TEXT_END name={name}",flush=True)
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  root=Path(td)
  for name,url,required in SOURCES:
   f=root/(name+(".zip" if url.endswith(".zip") else ".pdf"))
   try:
    http=run(["curl","--location","--silent","--show-error","--connect-timeout","19",
     "--max-time","150","--speed-time","25","--speed-limit","1600",
     "--max-filesize",str(72*1024*1024),"--user-agent","Mozilla/5.0",
     "--output",str(f),"--write-out","%{http_code}|%{content_type}|%{size_download}",url],170)
    assert http.startswith("200|") and f.stat().st_size>60000,http
    print(f"VPB_Q2_2026_FETCH name={name} sha256={hashlib.sha256(f.read_bytes()).hexdigest()} bytes={f.stat().st_size} URL={url}",flush=True)
    if f.suffix==".pdf":pdf(name,f);continue
    assert zipfile.is_zipfile(f)
    with zipfile.ZipFile(f) as z:
     print("VPB_Q2_2026_MEMBERS "+repr([(i.filename,i.file_size) for i in z.infolist()]),flush=True)
     for j,i in enumerate([x for x in z.infolist() if x.filename.lower().endswith(".pdf") and x.file_size>60000][:3]):
      dest=root/("m"+str(j)+".pdf");dest.write_bytes(z.read(i));pdf(name+"_"+str(j),dest)
   except Exception as e:
    if required:raise
    print(f"VPB_Q2_2026_H1_OPTIONAL_UNCONFIRMED {str(e)[:250]}",flush=True)
 print("PASS VPB Q2 original issuer ZIP source inspection; all production data unchanged",flush=True)
if __name__=="__main__":main()
