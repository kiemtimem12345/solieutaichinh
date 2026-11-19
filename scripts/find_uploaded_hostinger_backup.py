#!/usr/bin/env python3
"""Read-only, bounded SFTP location scan for a large backup uploaded to Hostinger.

No file contents downloaded, no edits. Only scans the user's named website and
its immediate account home. Sanitizes file names to report sizes and locations.
"""
import base64
import hashlib
import os
import socket
import stat
import sys
from datetime import datetime, timezone
import paramiko

HOST, PORT, USER = "195.35.62.53", 65002, "u154814653"
HOME = "/home/u154814653"
DOMAIN = HOME + "/domains/solieutaichinh.online"
EXPECTED = DOMAIN + "/restore-source"
FINGERPRINT = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
ARCHIVES = (".tar.gz", ".tgz", ".zip", ".tar", ".7z", ".rar", ".tar.zst",
            ".tar.xz", ".gz", ".zst", ".xz", ".part", ".tmp")
LOCATIONS = [
    EXPECTED,
    DOMAIN,
    DOMAIN + "/public_html",
    DOMAIN + "/public_html/restore-source",
    DOMAIN + "/public_html/uploads",
    DOMAIN + "/backup",
    DOMAIN + "/backups",
    DOMAIN + "/.builds",
    DOMAIN + "/private_html",
    DOMAIN + "/tmp",
    HOME,
    HOME + "/restore-source",
    HOME + "/backups",
    HOME + "/tmp",
]
MAX_ITEMS = 1200
MIN_SIZE = 100 * 1024 * 1024

def fingerprint(key):
    return "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")

def size_label(n):
    return f"{n / (1024 ** 3):.2f} GiB"

def main():
    if os.getenv("SFTP_USERNAME") != USER or not os.getenv("SFTP_PASSWORD"):
        print("::error::SSH username/password secrets are missing")
        return 2
    transport = None
    sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        transport = paramiko.Transport(sock)
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.banner_timeout = 15
        transport.auth_timeout = 15
        transport.start_client(timeout=15)
        k = transport.get_remote_server_key()
        if k.get_name() != "ssh-ed25519" or fingerprint(k) != FINGERPRINT:
            print("::error::Hostinger SSH fingerprint mismatch, refusing access")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::SSH password authentication failed")
            return 2
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("PASS: connected to Hostinger via pinned SSH fingerprint, read-only SFTP")
        all_found = []
        for folder in LOCATIONS:
            try:
                attrs = sftp.listdir_attr(folder)
            except FileNotFoundError:
                print("DIR_MISSING:", folder)
                continue
            except PermissionError:
                print("DIR_DENIED:", folder)
                continue
            except OSError:
                print("DIR_UNAVAILABLE:", folder)
                continue
            print(f"DIR_CHECK: {folder}, entries={len(attrs)}")
            if folder == EXPECTED and attrs:
                print(f"INFO: restore-source contains {len(attrs)} entries (not necessarily archive files)")
            for item in attrs[:MAX_ITEMS]:
                if not stat.S_ISREG(item.st_mode):
                    continue
                lower = item.filename.lower()
                is_archive = lower.endswith(ARCHIVES)
                if item.st_size < MIN_SIZE and not (folder == EXPECTED and is_archive):
                    continue
                # Do not print full unknown filenames: a backup might contain
                # account identifiers or names. Output relative folder, extension and size.
                ext = next((ext for ext in ARCHIVES if lower.endswith(ext)), "(other)")
                print(f"FILE_CANDIDATE: folder={folder}, ext={ext}, size={size_label(item.st_size)}")
                all_found.append((folder, item.filename, item.st_size, is_archive))
        print(f"SUMMARY: {len(all_found)} large/archive candidates in {len(LOCATIONS)} searched folders.")
        for folder, name, size, is_archive in all_found:
            if is_archive and size > MIN_SIZE:
                print(f"ARCHIVE_FOUND: use inspector for folder={folder}, size={size_label(size)}")
        print("No remote files changed.")
        return 0
    except Exception as exc:
        print(f"::error::SFTP inventory failed: {type(exc).__name__}")
        return 1
    finally:
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()

if __name__ == "__main__":
    sys.exit(main())
