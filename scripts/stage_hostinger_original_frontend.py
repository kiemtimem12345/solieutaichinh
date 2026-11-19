#!/usr/bin/env python3
"""Extract four allowlisted original frontend files from a private Hostinger
backup into a private staging directory. Never touch public_html or data.
Only metadata/hash of staged files is printed.
"""
import base64
import hashlib
import os
import posixpath
import shlex
import socket
import stat
import sys
import time
import paramiko

HOST, PORT, USER = "195.35.62.53", 65002, "u154814653"
BASE = "/home/u154814653/domains/solieutaichinh.online"
BACKUPS = BASE + "/restore-source"
STAGE = BASE + "/restore-stage-ui-20261119"
WEBROOT = BASE + "/public_html"
DATA = WEBROOT + "/data"
FP = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
FILES = {
    "index.html": (5_000_000, b"<html"),
    "assets/app.js": (8_000_000, None),
    "assets/styles.css": (5_000_000, None),
    "api/analysis-reports.php": (2_000_000, b"<?"),
}
PREFIX = "./domains/solieutaichinh.online/public_html/"
EXTENSIONS = (".tar.gz", ".tgz", ".gz")


def fp(key):
    return "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")


def hash_remote(sftp, path, limit):
    digest = hashlib.sha256()
    count = 0
    first = b""
    with sftp.open(path, "rb") as f:
        while True:
            b = f.read(65536)
            if not b:
                break
            if not first:
                first = b[:400]
            count += len(b)
            if count > limit:
                raise ValueError("Original asset exceeds guarded size limit")
            digest.update(b)
    return count, first, digest.hexdigest()


def run():
    if os.environ.get("SFTP_USERNAME") != USER or not os.environ.get("SFTP_PASSWORD"):
        print("::error::Required SSH credentials unavailable")
        return 2
    transport = sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        transport = paramiko.Transport(sock)
        transport.banner_timeout = 15
        transport.auth_timeout = 15
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.start_client(timeout=15)
        k = transport.get_remote_server_key()
        if k.get_name() != "ssh-ed25519" or fp(k) != FP:
            print("::error::SSH identity mismatch")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::SSH password authentication failed")
            return 2
        sftp = paramiko.SFTPClient.from_transport(transport)
        backups = [
            x for x in sftp.listdir_attr(BACKUPS)
            if x.filename.lower().endswith(EXTENSIONS) and x.st_size > 1024 ** 3
            and stat.S_ISREG(x.st_mode)
        ]
        if len(backups) != 1:
            print(f"::error::Expected one private backup archive >1 GiB, got {len(backups)}")
            return 2
        archive = BACKUPS + "/" + backups[0].filename
        # Stage is private, outside live public_html. Existing stage is never wiped.
        try:
            st = sftp.lstat(STAGE)
            if not stat.S_ISDIR(st.st_mode):
                print("::error::Private staging path is not a directory")
                return 2
            print("CHECK: using private staging directory from previous attempt")
        except FileNotFoundError:
            sftp.mkdir(STAGE, mode=0o700)
            print("CREATED: private staging directory outside public_html")
        # Exact paths only: never expand wildcards, extract unrelated files or
        # use tar's original ownership/permissions.
        members = [PREFIX + path for path in FILES]
        cmd = (
            "timeout 660 tar -xzf " + shlex.quote(archive)
            + " -C " + shlex.quote(STAGE)
            + " --no-same-owner --no-same-permissions -- "
            + " ".join(shlex.quote(x) for x in members)
            + " 2>/dev/null"
        )
        ch = transport.open_session(timeout=15)
        ch.exec_command(cmd)
        start = time.monotonic()
        while not ch.exit_status_ready():
            if time.monotonic() - start > 680:
                ch.close()
                print("::error::Private-stage TAR extraction exceeded guarded time budget")
                return 1
            time.sleep(3)
        code = ch.recv_exit_status()
        if code:
            print(f"::error::Private-stage TAR extraction failed, exit={code}")
            return 1
        print("PASS: exactly four allowlisted archive members extracted to private staging")
        for name, (limit, starts) in FILES.items():
            path = STAGE + "/domains/solieutaichinh.online/public_html/" + name
            st = sftp.lstat(path)
            if not stat.S_ISREG(st.st_mode):
                print(f"::error::Expected staged file not regular: {name}")
                return 2
            size, first, sha = hash_remote(sftp, path, limit)
            if size < 10 or (starts and starts.lower() not in first.lower()):
                print(f"::error::Invalid content for staged original asset: {name}")
                return 2
            print(f"STAGED: {name}, bytes={size}, sha256={sha}")
        items = sftp.listdir_attr(DATA)
        jsons = [x.filename for x in items if x.filename.endswith(".json")]
        if len(jsons) != 41:
            print(f"::error::Data directory count changed: expected 41 JSON, got {len(jsons)}")
            return 2
        print("PASS: existing 41 JSON files remain in public_html/data")
        print("PASS: private staging complete. No live website files changed.")
        return 0
    except Exception as exc:
        print(f"::error::Frontend staging failed: {type(exc).__name__}")
        return 1
    finally:
        if sftp is not None: sftp.close()
        if transport is not None: transport.close()


if __name__ == "__main__":
    sys.exit(run())
