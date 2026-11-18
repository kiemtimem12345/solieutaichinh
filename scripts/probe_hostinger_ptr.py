#!/usr/bin/env python3
"""Public-only reverse-DNS probe; does not authenticate or mutate Hostinger."""
import socket
import ssl
from ftplib import FTP_TLS

IP = "195.35.62.53"
def main():
    try:
        name, aliases, addresses = socket.gethostbyaddr(IP)
    except OSError as exc:
        print("NOTICE: Reverse DNS lookup unavailable:", type(exc).__name__)
        return
    candidates = sorted(set([name] + aliases))
    print("PTR:", name, "aliases:", ", ".join(aliases) or "none")
    for hostname in candidates:
        if not hostname.endswith(".hstgr.io"):
            print("SKIP: Reverse DNS name outside the certificate wildcard suffix:", hostname)
            continue
        try:
            ips = {entry[4][0] for entry in socket.getaddrinfo(hostname, 21, type=socket.SOCK_STREAM)}
            if IP not in ips:
                print("SKIP: forward DNS mismatch for", hostname)
                continue
            with FTP_TLS(context=ssl.create_default_context(), timeout=12) as ftp:
                ftp.connect(hostname, 21)
                ftp.auth()
                print("PASS: TLS hostname and certificate validated:", hostname)
                ftp.close()
        except (OSError, ssl.SSLError, EOFError) as exc:
            print("NOT VERIFIED:", hostname, type(exc).__name__)
    print("READ ONLY; no usernames or passwords sent, no files changed.")
if __name__ == "__main__":
    main()
