#!/usr/bin/env python3
"""Read-only explicit FTPS diagnostic. Does not mutate remote files."""
import io
import os
import socket
import ssl
import sys
from ftplib import FTP_TLS, error_perm

def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"{name} is missing")
    return value

def check():
    host = required("FTP_SERVER")
    user = required("FTP_USERNAME")
    password = required("FTP_PASSWORD")
    port = int(os.getenv("FTP_PORT", "21"))
    path = required("FTP_DATA_DIR").replace("\\", "/")
    if path not in ("/data/", "/public_html/data/"):
        raise ValueError("FTP_DATA_DIR must be /data/ or /public_html/data/")
    parent = "/" if path == "/data/" else "/public_html"
    print("FTPS: trying TLS-verified connection; no remote writes")
    with FTP_TLS(context=ssl.create_default_context(), timeout=20) as ftp:
        ftp.connect(host, port)
        ftp.login(user, password)
        ftp.prot_p()
        print("PASS: explicit FTPS login and protected data channel")
        ftp.cwd(parent)
        print("PASS: configured parent directory accessible")
        marker = io.BytesIO()
        try:
            ftp.retrbinary("RETR CNAME", marker.write)
        except error_perm:
            print("BLOCKED: CNAME file unavailable at configured parent")
            return 2
        if b"solieutaichinh.online" not in marker.getvalue():
            print("BLOCKED: CNAME marker does not match requested domain")
            return 3
        print("PASS: CNAME marker verified at deployment parent")
        try:
            ftp.cwd("data")
            print("PASS: data directory exists and is accessible")
        except error_perm:
            print("NOTICE: data directory not yet present (will need creation at deployment)")
        ftp.quit()
    return 0

if __name__ == "__main__":
    try:
        sys.exit(check())
    except ssl.SSLCertVerificationError:
        sys.exit("BLOCKED: FTPS server TLS certificate is not valid for FTP_SERVER; use Hostinger-certified hostname")
    except (socket.timeout, TimeoutError, ConnectionError, OSError):
        sys.exit("BLOCKED: network or TLS connectivity error; check FTP host, port and server")
    except error_perm:
        sys.exit("BLOCKED: FTPS permission/login issue; confirm username, password and parent path")
    except ValueError as exc:
        sys.exit(f"BLOCKED: {exc}")
