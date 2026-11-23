#!/usr/bin/env python3
"""STB 2025 Q3 signed original source, source-only. Scan 2–8 for B02a B03a 9M B04a."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,re,hashlib
URL="https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/STB_Baocaotaichinh_Q3_2025_Hopnhat.pdf"
OUTPUT=Path("stb-2025q3-original")
def run(argv,timeout=180):
 p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout,check=False)
 if p.returncode:raise RuntimeError(str(argv[0])+" exit "+str(p.returncode)+": "+p.stderr[:350])
 return p.stdout
def main():
 OUTPUT.mkdir(exist_ok=True)
 with TemporaryDirectory() as td:
  p=Path(td)/"signed-stb-q3.pdf"
  res=run(["curl","--location","--silent","--show-error","--connect-timeout","22",
    "--max-time","170","--speed-time","30","--speed-limit","1100",
    "--max-filesize",str(90*1024*1024),"--user-agent","Mozilla/5.0",
    "--output",str(p),"--write-out","%{http_code}|%{content_type}|%{size_download}",URL],195)
  assert res.startswith("200|") and p.read_bytes()[:5]==b"%PDF-" and p.stat().st_size>50000,res
  meta=run(["pdfinfo",str(p)]);pages=int(re.search(r"^Pages:\s*(\d+)",meta,re.M).group(1))
  sha=hashlib.sha256(p.read_bytes()).hexdigest()
  print(f"STB_2025Q3_ORIGINAL url={URL} bytes={p.stat().st_size} pages={pages} sha256={sha}",flush=True)
  raw=run(["pdftotext","-layout","-f","1","-l",str(min(12,pages)),str(p),"-"],70)
  (OUTPUT/"original-first-pages.txt").write_text(raw[:65000],"utf8")
  print("STB_Q3_ORIGINAL_TEXT_BEGIN",flush=True);print(raw[:38000],flush=True);print("STB_Q3_ORIGINAL_TEXT_END",flush=True)
  if len(raw.strip())<1100:
   print("STB_2025Q3_SCANNED_ORIGINAL; run targeted pages 2-9 Vietnamese OCR",flush=True)
   run(["pdftoppm","-f","2","-l",str(min(9,pages)),"-scale-to","1850",
     "-gray","-png",str(p),str(OUTPUT/"page")],230)
   for img in sorted(OUTPUT.glob("page-*.png")):
    txt=run(["tesseract",str(img),"stdout","-l","vie+eng","--psm","6"],85)
    (OUTPUT/(img.stem+".txt")).write_text(txt[:15000],"utf8")
    print("STB_2025Q3_OCR_START "+img.stem,flush=True)
    print(txt[:13800],flush=True)
    print("STB_2025Q3_OCR_END "+img.stem,flush=True)
   assert len(list(OUTPUT.glob("page-*.txt")))>5
 print("PASS STB 2025 Q3 original source recovered; no production figures changed",flush=True)
if __name__=="__main__":main()
