import concurrent.futures, hashlib, json, pathlib, subprocess, tempfile, urllib.request
from urllib.parse import urlparse
SOURCES={"2025-Q1":["https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%201/HHV_Baocaotaichinh_Q1_2025_Hopnhat.pdf"]}
ALLOWED={"static2.vietstock.vn"}
EXPECTED={}
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).scheme != "https" or urlparse(newurl).hostname not in ALLOWED:
            raise ValueError("redirect outside source allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)
def verify(item):
    period, urls = item
    attempts = []
    for url in urls:
        try:
            assert urlparse(url).scheme == "https" and urlparse(url).hostname in ALLOWED
            opener = urllib.request.build_opener(SafeRedirect())
            with opener.open(urllib.request.Request(url, headers={"User-Agent":"Financial report verification/1.0"}), timeout=75) as response:
                data = response.read(64*1024*1024+1)
                final_url = response.geturl()
            if len(data)>64*1024*1024 or not data.startswith(b"%PDF-"):
                raise ValueError("not a supported PDF")
            digest = hashlib.sha256(data).hexdigest()
            if period in EXPECTED and digest != EXPECTED[period]:
                raise ValueError("source changed or mirror bytes differ; review required: " + digest)
            with tempfile.TemporaryDirectory() as tmp:
                p=pathlib.Path(tmp)/"source.pdf"
                p.write_bytes(data)
                info=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=30,check=True).stdout
                pages=int(next(line.split(":")[1] for line in info.splitlines() if line.startswith("Pages:")))
                extract=subprocess.run(["pdftotext","-f","1","-l",str(min(pages,18)),str(p),"-"],capture_output=True,timeout=60,check=True).stdout
                evidence = pathlib.Path("hhv-page-evidence") / period
                evidence.mkdir(parents=True, exist_ok=True)
                # Only selected initial statement pages, not the full report.
                if len(extract.strip()) < 1000:
                    subprocess.run(["pdftoppm","-f","1","-l",str(min(pages,18)),"-r","180","-png",str(p),str(evidence/"page")],capture_output=True,timeout=120,check=True)
                else:
                    subprocess.run(["pdftotext","-layout","-f","1","-l",str(min(pages,18)),str(p),str(evidence/"statements.txt")],capture_output=True,timeout=60,check=True)
            return {"period":period,"url":url,"final_url":final_url,"status":"pdf_bytes_verified","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":pages,"first_pages_text_bytes":len(extract.strip()),"attempts":attempts}
        except Exception as exc:
            attempts.append({"url":url,"error":str(exc)[:300]})
    return {"period":period,"status":"unavailable","attempts":attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results=list(executor.map(verify,SOURCES.items()))
pathlib.Path("hhv-source-verification.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(x["status"]=="pdf_bytes_verified" for x in results) else 1)
