import concurrent.futures, hashlib, json, pathlib, subprocess, tempfile, urllib.request
from urllib.parse import urlparse
SOURCES = json.loads("{\"2025-Q2\":[\"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/NVL_Baocaotaichinh_Q2_2025_Hopnhat.pdf\",\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2025/20250728%20-%20BCTC/250728_VI_BCTC_HN_Q2.2025.pdf\"],\"2025-H1-reviewed\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2025/20250826/250826_VN_BCTC_HN_6T2025_sx.pdf\"],\"2025-Q3\":[\"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/NVL_Baocaotaichinh_Q3_2025_Hopnhat.pdf\"],\"2025-Q4\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260130/260130_NVLG_Consolidated_FS_Q4.2025_Vn_w.pdf\"],\"2025-FY-audited\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260325/NVLG_BCKT%20Hop%20nhat_31.12.2025_VN_rs%20x.pdf\"],\"2026-Q1\":[\"https://static2.vietstock.vn/vietstock/2026/5/4/20260429___nvl___bctc_hop_nhat_1q2026___giai_trinh_lnst.pdf\",\"https://cafef1.mediacdn.vn/download/060526/nvl122001-bao-cao-tai-chinh-hop-nhat-q1-2026-va-giai-trinh-lnst-0-613710.pdf\"],\"2026-Q2\":[\"https://staticfile.hsx.vn/Uploads/UploadDocuments/2485616/20260730%20-%20NVL%20-%20BCTC%20Hop%20nhat%20Q2%202026%20va%20giai%20trinh%20LNST.pdf\"],\"2026-H1-reviewed\":[\"https://owa.hnx.vn/ftp/cims/2026/8_W5/000000016821977_VI_BaoCaoTaiChinhHopNhatSoatXet_6T2026.pdf\",\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260828/20260828_NVLG_BCTC_HN_6T2026_SX.pdf\"],\"2026-Q3\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20261030/20261030_NVLG_BCTC_HN_2026Q3.pdf\"]}")
SOURCES["2026-Q2"].insert(0, "https://static2.vietstock.vn/data/HOSE/2026/BCTC/VN/QUY%202/NVL_Baocaotaichinh_Q2_2026_Hopnhat.pdf")
ALLOWED = {"static2.vietstock.vn","www.novaland.com.vn","cafef1.mediacdn.vn","staticfile.hsx.vn","owa.hnx.vn"}
EXPECTED = {"2025-Q2":"4c0c28fe3a42b55d90b56855e8f1918785cf8dce349179d8d987c4b3ad5d08f8","2025-H1-reviewed":"618d514b355387ade90d2266f8f8c4c7098d94339592dc696d900482c96b4e6c","2025-Q3":"9fddbc42c2cc38b1b5d485e7e37cff19a15c3948ef3f285941920790190759e8","2025-Q4":"061fe7287652d908c515a9d2456b603f270d9d23a5eac680a94c8d83742adf07","2025-FY-audited":"8a1cb94cbe9ef5d98550ef6ab734f54f99ecb9376f43c8aa4a3662cd6d5d0353","2026-Q1":"7402852212422f2c639968c39e95cd72b24c563a859ce84095bc98d22637ed14","2026-Q2":"4c62126cc62d6221cbdd7c4c5bfd54a709ae5c39a40c000314e3d1334ae77f64","2026-H1-reviewed":"20aa7254735542d470f12ada8d02786dfa5e673035274e42d3404352e266a007","2026-Q3":"bda9bbefd267912493ac3c08d7e4bfe099b7dcba007cbf121852ec7d45ee82c0"}
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
            if digest != EXPECTED[period]:
                raise ValueError("source changed or mirror bytes differ; review required: " + digest)
            with tempfile.TemporaryDirectory() as tmp:
                p=pathlib.Path(tmp)/"source.pdf"
                p.write_bytes(data)
                info=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=30,check=True).stdout
                pages=int(next(line.split(":")[1] for line in info.splitlines() if line.startswith("Pages:")))
                extract=subprocess.run(["pdftotext","-f","1","-l",str(min(pages,18)),str(p),"-"],capture_output=True,timeout=60,check=True).stdout
                evidence = pathlib.Path("nvl-page-evidence") / period
                evidence.mkdir(parents=True, exist_ok=True)
                # Only selected initial statement pages, not the full report.
                if len(extract.strip()) < 1000:
                    subprocess.run(["pdftoppm","-f","1","-l",str(min(pages,15)),"-r","180","-png",str(p),str(evidence/"page")],capture_output=True,timeout=120,check=True)
                else:
                    subprocess.run(["pdftotext","-layout","-f","1","-l",str(min(pages,15)),str(p),str(evidence/"statements.txt")],capture_output=True,timeout=60,check=True)
            return {"period":period,"url":url,"final_url":final_url,"status":"pdf_bytes_verified","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":pages,"first_pages_text_bytes":len(extract.strip()),"attempts":attempts}
        except Exception as exc:
            attempts.append({"url":url,"error":str(exc)[:300]})
    return {"period":period,"status":"unavailable","attempts":attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results=list(executor.map(verify,SOURCES.items()))
pathlib.Path("nvl-source-verification.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(x["status"]=="pdf_bytes_verified" for x in results) else 1)
