#!/usr/bin/env python3
"""One-time recovery: create absent Hostinger /data and upload only validated JSON.

Designed to be safely rerunnable after partial failure: never replace, rename or delete a
remote file. If an existing file differs from local SHA256, stop with error.
No other remote directory/file is written.
"""
import base64, hashlib, json, os, re, socket, stat, sys
from pathlib import Path
import paramiko

HOST = "195.35.62.53"
PORT = 65002
USER = "u154814653"
ROOT = "/home/u154814653/domains/solieutaichinh.online/public_html"
TARGET = ROOT + "/data"
FINGERPRINT = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
SOURCE = Path("deploy/data")
NAME = re.compile(r"^[A-Za-z0-9_-]+\.json$")

def local_files():
    if not SOURCE.is_dir():
        raise ValueError("Staged JSON directory missing; run scripts/prepare_deploy.py")
    items = sorted(SOURCE.glob("*.json"))
    financial = [p for p in items if p.name.startswith("financials-")]
    if len(items) != 41 or len(financial) != 32:
        raise ValueError("Incorrect stage file count; expected 41 total, 32 financials")
    for f in items:
        if not NAME.fullmatch(f.name) or f.is_symlink() or f.parent != SOURCE:
            raise ValueError("Unexpected staged file path")
        json.loads(f.read_text(encoding="utf-8"))
    return items

def fingerprint(key):
    return "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")

def remote_digest(sftp, remote):
    hasher = hashlib.sha256()
    with sftp.open(remote, "rb") as stream:
        while True:
            chunk = stream.read(65536)
            if not chunk: break
            hasher.update(chunk)
    return hasher.hexdigest()

def run():
    files = local_files()
    if os.getenv("SFTP_USERNAME") != USER or not os.getenv("SFTP_PASSWORD"):
        print("::error::Hostinger SFTP credentials missing or unexpected user")
        return 2
    if os.getenv("SFTP_DATA_DIR", "").rstrip("/") != TARGET:
        print("::error::Destination path differs from pinned website data root")
        return 2
    transport = None
    sftp = None
    created = 0
    verified = 0
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        transport = paramiko.Transport(sock)
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.banner_timeout = 15
        transport.auth_timeout = 15
        transport.start_client(timeout=15)
        key = transport.get_remote_server_key()
        if key.get_name() != "ssh-ed25519" or fingerprint(key) != FINGERPRINT:
            print("::error::SSH identity mismatch. No recovery writes permitted.")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::SSH password authentication failed")
            return 2
        sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp is None:
            print("::error::SFTP subsystem unavailable")
            return 2
        root = sftp.lstat(ROOT)
        if not stat.S_ISDIR(root.st_mode):
            print("::error::Expected site public_html is not a regular directory")
            return 2
        print("PASS: verified Hostinger identity and SFTP authentication")
        try:
            target_stat = sftp.lstat(TARGET)
        except FileNotFoundError:
            sftp.mkdir(TARGET, mode=0o755)
            print("CREATED: missing public_html/data directory (other site files unchanged)")
            target_stat = sftp.lstat(TARGET)
        if not stat.S_ISDIR(target_stat.st_mode):
            print("::error::data target is not a regular directory (or is a symlink)")
            return 2
        # No remote file deletion, replacement, chmod, move, PHP/HTML/CSS/JS.
        for path in files:
            remote = TARGET + "/" + path.name
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            try:
                attr = sftp.lstat(remote)
            except FileNotFoundError:
                attr = None
            if attr is not None:
                if not stat.S_ISREG(attr.st_mode):
                    print(f"::error::Target exists but is not regular file: {path.name}")
                    return 2
                if remote_digest(sftp, remote) != digest:
                    print(f"::error::Existing file differs; refusing to overwrite: {path.name}")
                    return 2
                verified += 1
                continue
            # Paramiko 'x' -> EXCL: prevents creating over a file added since lstat.
            with sftp.open(remote, "xb") as dst:
                with path.open("rb") as src:
                    while True:
                        data = src.read(65536)
                        if not data: break
                        dst.write(data)
            if remote_digest(sftp, remote) != digest:
                print(f"::error::Upload content mismatch: {path.name}; refusing to proceed")
                return 1
            created += 1
            verified += 1
        print(f"PASS: {verified}/41 JSON files verified by remote SHA256; new files={created}")
        print("PASS: No existing files overwritten or deleted; no UI/CSS/PHP/JS files touched")
        return 0
    except Exception as exc:
        print(f"::error::Data recovery stopped ({type(exc).__name__}). "
              f"Uploaded {created} files; safe to rerun, no remote overwrites.")
        return 1
    finally:
        if sftp is not None: sftp.close()
        if transport is not None: transport.close()

if __name__ == "__main__":
    sys.exit(run())
