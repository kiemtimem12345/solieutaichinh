#!/usr/bin/env python3
"""Stage ORIGINAL static frontend from Hostinger private staging and 41 audited JSON
as *tracked Git files* to survive Hostinger's automatic Git checkout resets.

No direct remote Hostinger writes; no private PHP, archive, or secrets committed.
"""
import base64
import hashlib
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import sys
import paramiko

HOST, PORT, USER = "195.35.62.53", 65002, "u154814653"
DOMAIN = "/home/u154814653/domains/solieutaichinh.online"
STAGING = DOMAIN + "/restore-stage-ui-20261119/domains/solieutaichinh.online/public_html"
FINGERPRINT = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
EXPECTED = {
    "index.html": ("5e0573a9345a353f31415f446979fb849b29d4c836cdcd6c3f6bc1df64209437", 80661),
    "assets/app.js": ("92df346c7b98de31ef5ad58739084417bb6e38b00a4fd983312a9a037f9c2755", 206075),
    "assets/styles.css": ("cd963abc744fb0f6981e6c90464111884f8d8c41d918a1dc2a1d980604cdd4a8", 63298),
}
HIDDEN_CREDENTIAL_MARKERS = (b"-----BEGIN PRIVATE KEY", b"ghp_", b"github_pat_", b"AKIA", b"sk-proj-")


def fp(key):
    return "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")


def get_file(sftp, name, target):
    source = STAGING + "/" + name
    info = sftp.lstat(source)
    expected_hash, expected_size = EXPECTED[name]
    if not stat.S_ISREG(info.st_mode) or info.st_size != expected_size:
        raise ValueError("Original asset size/type mismatch: " + name)
    digest = hashlib.sha256()
    data = bytearray()
    with sftp.open(source, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            digest.update(chunk)
            data.extend(chunk)
            if len(data) > expected_size:
                raise ValueError("Unexpected oversized asset: " + name)
    if digest.hexdigest() != expected_hash:
        raise ValueError("Original archive SHA256 mismatch: " + name)
    if any(marker in data for marker in HIDDEN_CREDENTIAL_MARKERS):
        raise ValueError("Potential private credential detected; do not publish: " + name)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise ValueError("Already tracked asset at destination; refuse overwrite: " + name)
    target.write_bytes(data)
    print(f"READY: original {name}: bytes={len(data)} sha256={expected_hash}")


def main():
    if os.getenv("SFTP_USERNAME") != USER or not os.getenv("SFTP_PASSWORD"):
        print("::error::Missing Hostinger SSH secrets")
        return 2
    destination = Path(".").resolve()
    source_data = destination / "deploy" / "data"
    if len(list(source_data.glob("*.json"))) != 41:
        print("::error::Validated deploy/data must contain exactly 41 JSON")
        return 2
    if (destination / "data").exists():
        print("::error::Repo root data/ already exists; refuse unexpected replacement")
        return 2

    transport = sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        transport = paramiko.Transport(sock)
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.banner_timeout = 15
        transport.auth_timeout = 15
        transport.start_client(timeout=15)
        key = transport.get_remote_server_key()
        if key.get_name() != "ssh-ed25519" or fp(key) != FINGERPRINT:
            print("::error::Hostinger SSH fingerprint mismatch")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::SSH password rejected")
            return 2
        sftp = paramiko.SFTPClient.from_transport(transport)
        for name in EXPECTED:
            get_file(sftp, name, destination / name)
    except Exception as exc:
        print("::error::Original static assets retrieval failed:", type(exc).__name__, str(exc)[:140])
        return 1
    finally:
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()

    html = (destination / "index.html").read_text(encoding="utf-8", errors="replace").lower()
    if "<html" not in html or "</html>" not in html:
        print("::error::Original index.html did not pass basic structural check")
        return 2
    print("INDEX_REFERENCES_APP_JS:", "app.js" in html)
    print("INDEX_REFERENCES_STYLES_CSS:", "styles.css" in html)
    (destination / "data").mkdir()
    for path in source_data.glob("*.json"):
        shutil.copyfile(path, destination / "data" / path.name)
    copied = sorted((destination / "data").glob("*.json"))
    financial = [p for p in copied if p.name.startswith("financials-")]
    if len(copied) != 41 or len(financial) != 32:
        print("::error::Unexpected copied JSON count")
        return 2
    print("PASS: 3 original frontend assets + 41 validated JSON prepared as Git-tracked static files")
    print("GUARD: no PHP, backup archive, secrets or private staging files are included")
    return 0


if __name__ == "__main__":
    sys.exit(main())
