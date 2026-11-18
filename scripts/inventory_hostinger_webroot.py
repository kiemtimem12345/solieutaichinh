#!/usr/bin/env python3
"""Read-only safe inventory of Hostinger website root, with pinned SSH fingerprint.

Do not print secrets, hidden files, filenames of private files, file bodies, or remote contents.
"""
import base64, hashlib, os, socket, stat, sys
import paramiko

HOST, PORT, USER = "195.35.62.53", 65002, "u154814653"
BASE = "/home/u154814653/domains/solieutaichinh.online/public_html"
FINGERPRINT = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
WHITELIST = {
    "index.html", "index.htm", "index.php", "home.html", "home.php",
    "assets", "data", "css", "js", "static", "dist", "build",
    "backup", "backups", "archive", "archives", "public", "CNAME",
    "robots.txt", "sitemap.xml", ".htaccess", ".git"
}
SENSITIVE_MARKER = ".git"

def main():
    if os.getenv("SFTP_USERNAME") != USER or not os.getenv("SFTP_PASSWORD"):
        print("::error::Missing or invalid SSH credentials configuration")
        return 2
    transport = None
    sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), 12)
        transport = paramiko.Transport(sock)
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.banner_timeout = 12
        transport.auth_timeout = 15
        transport.start_client(timeout=15)
        key = transport.get_remote_server_key()
        got = "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")
        if key.get_name() != "ssh-ed25519" or got != FINGERPRINT:
            print("::error::SSH host identity changed; abort")
            return 2
        transport.auth_password(USER, os.environ["SFTP_PASSWORD"], fallback=False)
        if not transport.is_authenticated():
            print("::error::SSH authentication not completed")
            return 1
        sftp = paramiko.SFTPClient.from_transport(transport)
        if not sftp:
            print("::error::SFTP subsystem unavailable")
            return 1
        root = sftp.stat(BASE)
        if not stat.S_ISDIR(root.st_mode):
            print("::error::Expected website root is not directory")
            return 2
        print("PASS: SSH password, pinned fingerprint, SFTP and webroot verified")
        entries = sftp.listdir_attr(BASE)
        print(f"Website root entries: {len(entries)} (only public-safe whitelist reported)")
        known = {item.filename: item for item in entries}
        for name in sorted(WHITELIST):
            item = known.get(name)
            if item is None:
                print(f"CHECK: {name} = MISSING")
                continue
            kind = "DIR" if stat.S_ISDIR(item.st_mode) else "FILE"
            if name in (".htaccess", ".git"):
                print(f"CHECK: {name} = PRESENT ({kind}; content not inspected)")
            else:
                print(f"CHECK: {name} = {kind}, bytes={item.st_size}")
        if "assets" in known and stat.S_ISDIR(known["assets"].st_mode):
            for name in ["app.js", "index.js", "style.css", "styles.css", "main.css"]:
                try:
                    a = sftp.stat(f"{BASE}/assets/{name}")
                    print(f"CHECK: assets/{name} = {'DIR' if stat.S_ISDIR(a.st_mode) else 'FILE'}, bytes={a.st_size}")
                except FileNotFoundError:
                    print(f"CHECK: assets/{name} = MISSING")
        if "data" not in known:
            print("CONCLUSION: public_html/data missing; no directory created or files modified")
        return 0
    except Exception as exc:
        print(f"::error::Website inventory failed: {type(exc).__name__}")
        return 1
    finally:
        if sftp is not None: sftp.close()
        if transport is not None: transport.close()

if __name__ == "__main__":
    sys.exit(main())
