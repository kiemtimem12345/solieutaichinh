#!/usr/bin/env python3
"""Explicit FTPS upload of JSON only. Never delete remote files.

Requires a CNAME marker containing solieutaichinh.online in the
target parent directory, to reduce the risk of uploading outside public_html.
"""
import io
import os
import pathlib
import ssl
import sys
from ftplib import FTP_TLS

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "deploy" / "data"

def need(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing environment variable {name}")
    return value

def main():
    server = need("FTP_SERVER")
    username = need("FTP_USERNAME")
    password = need("FTP_PASSWORD")
    directory = need("FTP_DATA_DIR").replace("\\", "/")
    path = "/" + directory.strip("/") + "/"
    if path not in ("/", "/data/", "/public_html/data/"):
        raise ValueError("Unsupported FTP_DATA_DIR")
    restricted_root = path == "/"
    if restricted_root and username != "u154814653.githubdeploy":
        raise ValueError("Root upload only allowed for dedicated restricted githubdeploy account")
    parent = "/" if path == "/data/" else "/public_html"
    files = sorted(DATA.glob("*.json"))
    if len(files) != 41 or any(not f.is_file() for f in files):
        raise ValueError(f"Expected 41 staged JSON files, found {len(files)}")
    port = int(os.getenv("FTP_PORT", "21"))
    if not 1 <= port <= 65535:
        raise ValueError("Invalid FTP_PORT")
    # Certificate verification is enabled. Use an FTPS hostname whose TLS
    # certificate matches; never silently downgrade to plaintext FTP.
    with FTP_TLS(context=ssl.create_default_context(), timeout=45) as ftp:
        ftp.connect(server, port)
        ftp.login(username, password)
        ftp.prot_p()
        if restricted_root:
            ftp.cwd("/")
            if ftp.pwd() != "/":
                raise ValueError("FTP root verification failed")
        else:
            ftp.cwd(parent)
            marker = io.BytesIO()
        if not restricted_root:
            try:
                ftp.retrbinary("RETR CNAME", marker.write)
            except Exception as exc:
                raise ValueError("No readable CNAME in deployment parent; verify FTP_DATA_DIR") from exc
            if b"solieutaichinh.online" not in marker.getvalue():
                raise ValueError("CNAME does not match website; aborting upload")
            try:
                ftp.cwd("data")
            except Exception:
                ftp.mkd("data")
                ftp.cwd("data")
        for i, f in enumerate(files, 1):
            with f.open("rb") as handle:
                ftp.storbinary(f"STOR {f.name}", handle)
            print(f"Uploaded {i}/{len(files)}: {f.name}")
        ftp.quit()
    print("PASS: 41 JSON uploaded with FTPS. No remote files deleted.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"FTPS deploy aborted: {exc}")
