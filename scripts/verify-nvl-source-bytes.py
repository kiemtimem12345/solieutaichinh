import concurrent.futures, hashlib, json, pathlib, subprocess, tempfile, urllib.request
from urllib.parse import urlparse
SOURCES = json.loads("{\"2025-Q2\":[\"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%202/NVL_Baocaotaichinh_Q2_2025_Hopnhat.pdf\",\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2025/20250728%20-%20BCTC/250728_VI_BCTC_HN_Q2.2025.pdf\"],\"2025-H1-reviewed\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2025/20250826/250826_VN_BCTC_HN_6T2025_sx.pdf\"],\"2025-Q3\":[\"https://static2.vietstock.vn/data/HOSE/2025/BCTC/VN/QUY%203/NVL_Baocaotaichinh_Q3_2025_Hopnhat.pdf\"],\"2025-Q4\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260130/260130_NVLG_Consolidated_FS_Q4.2025_Vn_w.pdf\"],\"2025-FY-audited\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260325/NVLG_BCKT%20Hop%20nhat_31.12.2025_VN_rs%20x.pdf\"],\"2026-Q1\":[\"https://static2.vietstock.vn/vietstock/2026/5/4/20260429___nvl___bctc_hop_nhat_1q2026___giai_trinh_lnst.pdf\",\"https://cafef1.mediacdn.vn/download/060526/nvl122001-bao-cao-tai-chinh-hop-nhat-q1-2026-va-giai-trinh-lnst-0-613710.pdf\"],\"2026-Q2\":[\"https://staticfile.hsx.vn/Uploads/UploadDocuments/2485616/20260730%20-%20NVL%20-%20BCTC%20Hop%20nhat%20Q2%202026%20va%20giai%20trinh%20LNST.pdf\"],\"2026-H1-reviewed\":[\"https://owa.hnx.vn/ftp/cims/2026/8_W5/000000016821977_VI_BaoCaoTaiChinhHopNhatSoatXet_6T2026.pdf\",\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20260828/20260828_NVLG_BCTC_HN_6T2026_SX.pdf\"],\"2026-Q3\":[\"https://www.novaland.com.vn/Data/Sites/1/media/quan-h%E1%BB%87-%C4%91%E1%BA%A7u-t%C6%B0/2026/20261030/20261030_NVLG_BCTC_HN_2026Q3.pdf\"]}")
ALLOWED = {"static2.vietstock.vn","www.novaland.com.vn","cafef1.mediacdn.vn","staticfile.hsx.vn","owa.hnx.vn"}
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
            with opener.open(urllib.request.Request(url, headers={"User-Agent":"Financial report verification/1.0"}), timeout=40) as response:
                data = response.read(64*1024*1024+1)
                final_url = response.geturl()
            if len(data)>64*1024*1024 or not data.startswith(b"%PDF-"):
                raise ValueError("not a supported PDF")
            with tempfile.TemporaryDirectory() as tmp:
                p=pathlib.Path(tmp)/"source.pdf"
                p.write_bytes(data)
                info=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,timeout=30,check=True).stdout
                pages=int(next(line.split(":")[1] for line in info.splitlines() if line.startswith("Pages:")))
                extract=subprocess.run(["pdftotext","-f","1","-l",str(min(pages,18)),str(p),"-"],capture_output=True,timeout=60,check=True).stdout
            return {"period":period,"url":url,"final_url":final_url,"status":"pdf_bytes_verified","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"pages":pages,"first_pages_text_bytes":len(extract.strip()),"attempts":attempts}
        except Exception as exc:
            attempts.append({"url":url,"error":str(exc)[:300]})
    return {"period":period,"status":"unavailable","attempts":attempts}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results=list(executor.map(verify,SOURCES.items()))
pathlib.Path("nvl-source-verification.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(x["status"]=="pdf_bytes_verified" for x in results) else 1)
