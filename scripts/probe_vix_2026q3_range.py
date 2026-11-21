#!/usr/bin/env python3
"""Probe official VIX Q3 PDF HTTP Range; never claim complete PDF with a partial response."""
import subprocess, pathlib, json
url="https://vixs.vn/wp-content/uploads/2026/10/20261019-VIX-Baocaotaichinh-Quy-3-nam-2026.pdf"
dst=pathlib.Path("vix-q3-range-probe");dst.mkdir(exist_ok=True)
out=dst/"first64KB.bin";hdr=dst/"headers.txt"
cmd=["curl","-L","-s","-S","--connect-timeout","12","--max-time","35","--retry","0",
     "--range","0-65535","--dump-header",str(hdr),"-o",str(out),
     "-w","HTTP=%{http_code} BYTES=%{size_download} TIME=%{time_total} CONTENT=%{content_type}",
     "-H","User-Agent: Mozilla/5.0",url]
p=subprocess.run(cmd,capture_output=True,text=True,timeout=42)
headers=hdr.read_text(errors="replace") if hdr.is_file() else ""
print("Q3_RANGE_PROBE",json.dumps({"returncode":p.returncode,"response":p.stdout,"error":p.stderr,
"response_headers":headers[-2000:],"payload_bytes":out.stat().st_size if out.exists() else 0,
"pdf_magic":out.read_bytes()[:8].decode('latin1') if out.exists() else None}),flush=True)
