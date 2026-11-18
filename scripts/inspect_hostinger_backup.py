#!/usr/bin/env python3
"""Read-only audit of a large Hostinger backup uploaded outside the public webroot.

No archive bytes downloaded to runner for .tar/.tar.gz files: tar lists contents
server-side using SSH. ZIP central directory is read via random-access SFTP.
Never extract, upload, overwrite, execute archive contents, or show secrets.
"""
import base64
import hashlib
import os
import re
import shlex
import socket
import sys
import zipfile
from pathlib import PurePosixPath

import paramiko

HOST = "195.35.62.53"
PORT = 65002
USER = "u154814653"
DOMAIN_ROOT = "/home/u154814653/domains/solieutaichinh.online"
UPLOAD_DIR = DOMAIN_ROOT + "/restore-source"
FINGERPRINT = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
EXTENSIONS = (".tar.gz", ".tgz", ".zip", ".tar")
PUBLIC_LAYOUT = re.compile(
    r"(^|/)(?:domains/solieutaichinh[.]online/)?public_html/"
    r"(?:index[.]html|index[.]php|index[.]htm|assets/|css/|js/|"
    r"static/|.*[.]css$|.*[.]php$)",
    re.IGNORECASE,
)
MAX_SHOW = 35


def sha256_fingerprint(key):
    digest = hashlib.sha256(key.asbytes()).digest()
    return "SHA256:" + base64.b64encode(digest).decode().rstrip("=")


def matches(filename):
    # Strip ./ prefixes, reject non-file information and unrelated sites.
    normalized = filename.replace("\\", "/").lstrip("./")
    if "solieutaichinh.online/" not in normalized and not (
        normalized.startswith("public_html/")
    ):
        return False
    return bool(PUBLIC_LAYOUT.search(normalized))


def list_tar_via_remote_ssh(transport, path, compressed):
    # The archive path is derived from a directory listing, quoted as one arg.
    # Read-only: tar -t lists entries, never tar -x.
    options = "-tzf" if compressed else "-tf"
    command = "timeout 540 tar " + options + " " + shlex.quote(path)
    channel = transport.open_session(timeout=15)
    channel.settimeout(30)
    channel.exec_command(command)
    hits = []
    count = 0
    # Process entries in memory only; do not log unrelated/private archive paths.
    buffered = b""
    while True:
        try:
            chunk = channel.recv(65536)
        except socket.timeout:
            print("::error::Archive listing stalled; not extracting or modifying files.")
            channel.close()
            return 1
        if not chunk:
            break
        buffered += chunk
        lines = buffered.split(b"\n")
        buffered = lines.pop()
        for line in lines:
            name = line.decode("utf-8", "replace").strip()
            if matches(name):
                count += 1
                if len(hits) < MAX_SHOW:
                    hits.append(name[:220])
    if buffered and matches(buffered.decode("utf-8", "replace")):
        count += 1
    status = channel.recv_exit_status()
    print(f"ARCHIVE_SCAN: tar command exit={status}; matching UI paths={count}")
    for name in hits:
        print("FRONTEND_CANDIDATE:", name)
    if status != 0:
        print("::warning::Server-side archive enumeration incomplete; no files extracted.")
    if count == 0:
        print("::warning::No UI paths matched known layouts. Archive may use a different structure.")
    return 0 if status == 0 else 1


def list_zip_via_sftp(sftp, path):
    with sftp.open(path, "rb") as src:
        with zipfile.ZipFile(src) as archive:
            matches_list = [x.filename for x in archive.infolist() if matches(x.filename)]
            print(f"ARCHIVE_SCAN: ZIP central directory read; matching UI paths={len(matches_list)}")
            for name in matches_list[:MAX_SHOW]:
                print("FRONTEND_CANDIDATE:", name[:220])
    return 0


def main():
    if os.getenv("SFTP_USERNAME") != USER or not os.getenv("SFTP_PASSWORD"):
        print("::error::SFTP_USERNAME or SFTP_PASSWORD is unset or incorrect.")
        return 2
    transport = None
    sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        transport = paramiko.Transport(sock)
        transport.banner_timeout = 15
        transport.auth_timeout = 15
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.start_client(timeout=15)
        key = transport.get_remote_server_key()
        if key.get_name() != "ssh-ed25519" or sha256_fingerprint(key) != FINGERPRINT:
            print("::error::Host identity mismatch; abort.")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::Hostinger password authentication failed.")
            return 2
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("PASS: Pinned SSH identity, password auth, and read-only SFTP.")
        try:
            entries = sftp.listdir_attr(UPLOAD_DIR)
        except FileNotFoundError:
            print("WAITING: create folder restore-source beside public_html, then upload backup archive.")
            print("No remote files changed.")
            return 0
        candidates = [
            x for x in entries
            if x.filename.lower().endswith(EXTENSIONS)
            and not x.filename.startswith(".")
            and x.st_size >= 1024 * 1024
        ]
        if not candidates:
            print("WAITING: no .tar.gz/.tgz/.tar/.zip archive found in private restore-source folder.")
            print("No remote files changed.")
            return 0
        candidates.sort(key=lambda x: (x.st_mtime, x.st_size), reverse=True)
        item = candidates[0]
        print(f"FOUND: private backup archive, file size {item.st_size:,} bytes, "
              f"extension={next(x for x in EXTENSIONS if item.filename.lower().endswith(x))}.")
        if len(candidates) > 1:
            print(f"NOTE: {len(candidates)} archives found; inspecting newest only.")
        path = UPLOAD_DIR + "/" + item.filename
        lower = item.filename.lower()
        if lower.endswith(".zip"):
            return list_zip_via_sftp(sftp, path)
        return list_tar_via_remote_ssh(
            transport, path, lower.endswith((".tar.gz", ".tgz"))
        )
    except Exception as exc:
        print(f"::error::Read-only backup inspection failed: {type(exc).__name__}.")
        print("Archive not extracted. Existing website/data files unchanged.")
        return 1
    finally:
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()


if __name__ == "__main__":
    sys.exit(main())
