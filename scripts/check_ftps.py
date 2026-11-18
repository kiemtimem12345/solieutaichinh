#!/usr/bin/env python3
"""Read-only explicit FTPS diagnostic. Does not mutate remote files."""
import io
import subprocess
import tempfile
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

def inspect_public_certificate(host, port):
    """Read only the public server certificate. Never send credentials."""
    try:
        # Unverified TLS is allowed ONLY to inspect the public certificate;
        # the production login still requires verified TLS.
        with FTP_TLS(context=ssl._create_unverified_context(), timeout=15) as ftp:
            ftp.connect(host, port)
            ftp.auth()
            cert_der = ftp.sock.getpeercert(binary_form=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pem") as cert:
            cert.write(ssl.DER_cert_to_PEM_cert(cert_der))
            cert.flush()
            result = subprocess.run(
                ["openssl", "x509", "-in", cert.name, "-noout", "-subject", "-ext", "subjectAltName"],
                capture_output=True, text=True, timeout=10, check=False
            )
        if result.returncode == 0:
            # Certificate subject names are public; do not print FTP_SERVER or credentials.
            print("Server public certificate identity:\\n" + result.stdout.strip())
        else:
            print("Could not parse server certificate identity")
    except Exception:
        print("Could not inspect server public certificate")

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
        print("BLOCKED: TLS certificate does not match FTP_SERVER")
        try:
            inspect_public_certificate(required("FTP_SERVER"), int(os.getenv("FTP_PORT", "21")))
        except Exception:
            pass
        sys.exit(1)
    except (socket.timeout, TimeoutError, ConnectionError, OSError):
        sys.exit("BLOCKED: network or TLS connectivity error; check FTP host, port and server")
    except error_perm:
        sys.exit("BLOCKED: FTPS permission/login issue; confirm username, password and parent path")
    except ValueError as exc:
        sys.exit(f"BLOCKED: {exc}")
