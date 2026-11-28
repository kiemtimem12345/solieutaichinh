import os, concurrent.futures, hashlib, json, pathlib, subprocess, tempfile, urllib.request
from urllib.parse import urlparse
SOURCES={"2025-Q1":["https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/HHV_Baocaotaichinh_Q1_2025_Hopnhat.pdf"]}
ALLOWED={"static2.vietstock.vn","hhv.cdn.vccloud.vn"}
if os.environ.get("HHV_SOURCE_BATCH") == "2025-Q2":
    SOURCES={
      "2025-Q2":["https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/HHV_Baocaotaichinh_Q2_2025_Hopnhat.pdf","https://hhv.cdn.vccloud.vn/wp-content/uploads/2025/07/20250730-HHV-Bao-cao-tai-chinh-hop-nhat-Quy-2-2025.pdf"],
      "2025-H1-reviewed":["https://hhv.cdn.vccloud.vn/wp-content/uploads/2025/08/20250825-HHV-Bao-cao-tai-chinh-hop-nhat-ban-nien-2025-da-soat-xet.pdf"]
    }
EXPECTED={'2025-Q1':'ac52e528cfe30786c3d251c38d6c0b27c0fc5347bd1e9873d692e85b7d461a94','2025-Q2':'cef9348b5d370efa3e4cbfdfb8f2821978da6de1765051f85a6350e1120f6e56','2025-H1-reviewed':'d4b002485c868803f012af5e10ccdea54d77b3c4978d14fd28e5a6a8de9a2abe'}
if os.environ.get("HHV_SOURCE_BATCH") == "2025-Q3":
    SOURCES={"2025-Q3":["https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/HHV_Baocaotaichinh_Q3_2025_Hopnhat.pdf"]}
EXPECTED["2025-Q3"]="de02046176473385304e2cbb535219f695d0625bfeb8ad9599d602a293e66e88"
if os.environ.get("HHV_SOURCE_BATCH") == "2025-Q4":
    SOURCES={"2025-Q4":["https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%204/HHV_Baocaotaichinh_Q4_2025_Hopnhat.pdf"]}
EXPECTED["2025-Q4"]="8a23361f4138cc2c685770b62a66b72baea59b122a7716d2d9cc03971561ec85"
if os.environ.get("HHV_SOURCE_BATCH") == "2025-FY-audited":
    SOURCES={"2025-FY-audited":["https://hhv.cdn.vccloud.vn/wp-content/uploads/2026/03/20260331-HHV-Bao-cao-tai-chinh-hop-nhat-kiem-toan-nam-2025.pdf"]}
EXPECTED["2025-FY-audited"]="11ebfc25d213771c8af0a4b9e9ff95378d5b1af3a097b7ef07d7518d4df7ceee"
if os.environ.get("HHV_SOURCE_BATCH") == "2026-Q1":
    SOURCES={
      "2025-FY-audited":["https://hhv.cdn.vccloud.vn/wp-content/uploads/2026/03/20260331-HHV-Bao-cao-tai-chinh-hop-nhat-kiem-toan-nam-2025.pdf"],
      "2026-Q1":["https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%201/HHV_Baocaotaichinh_Q1_2026_Hopnhat.pdf"]
    }
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).scheme != "https" or urlparse(newurl).hostname not in ALLOWED:
            raise ValueError("redirect outside source allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)
def verify(item):
    period, urls = item
    attempts = []
    limit = (96 if period == '2025-H1-reviewed' else 64)*1024*1024
    for url in urls:
        try:
            assert urlparse(url).scheme == "https" and urlparse(url).hostname in ALLOWED
            opener = urllib.request.build_opener(SafeRedirect())
            with opener.open(urllib.request.Request(url, headers={"User-Agent":"Financial report verification/1.0"}), timeout=120) as response:
                data = response.read(limit+1)
                final_url = response.geturl()
            if len(data)>limit or not data.startswith(b"%PDF-"):
                raise ValueError("not a supported PDF")
            digest = hashlib.sha256(data).hexdigest()
            if period in EXPECTED and digest != EXPECTED[period]:
                raise ValueError("source changed or mirror bytes differ; review required: " + digest)
            with tempfile.TemporaryDirectory() as tmp:
                p=pathlib.Path(tmp)/"source.pdf"
                p.write_bytes(data)
                info=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=30,check=True).stdout
                pages=int(next(line.split(":")[1] for line in info.splitlines() if line.startswith("Pages:")))
                first,last=(19,min(pages,20)) if period=="2025-FY-audited" and os.environ.get("HHV_SOURCE_BATCH")=="2026-Q1" else (1,min(pages,22))
                extract=subprocess.run(["pdftotext","-f",str(first),"-l",str(last),str(p),"-"],capture_output=True,timeout=60,check=True).stdout
                evidence = pathlib.Path("hhv-page-evidence") / period
                evidence.mkdir(parents=True, exist_ok=True)
                # Only selected initial statement pages, not the full report.
                if len(extract.strip()) < 1000:
                    subprocess.run(["pdftoppm","-f",str(first),"-l",str(last),"-r","180","-png",str(p),str(evidence/"page")],capture_output=True,timeout=120,check=True)
                else:
                    subprocess.run(["pdftotext","-layout","-f",str(first),"-l",str(last),str(p),str(evidence/"statements.txt")],capture_output=True,timeout=60,check=True)
            return {"period":period,"url":url,"final_url":final_url,"status":"pdf_bytes_verified","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":pages,"first_pages_text_bytes":len(extract.strip()),"attempts":attempts}
        except Exception as exc:
            attempts.append({"url":url,"error":str(exc)[:300]})
    return {"period":period,"status":"unavailable","attempts":attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results=list(executor.map(verify,SOURCES.items()))
pathlib.Path("hhv-source-verification.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(x["status"]=="pdf_bytes_verified" for x in results) else 1)
