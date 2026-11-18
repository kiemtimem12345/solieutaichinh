#!/usr/bin/env python3
"""Probe SSH/SFTP reachability without credentials or filesystem writes."""
import socket
import sys

HOST = "195.35.62.53"
PORT = 65002

def main():
    try:
        with socket.create_connection((HOST, PORT), timeout=12) as sock:
            sock.settimeout(8)
            banner = sock.recv(256)
            if banner.startswith(b"SSH-"):
                # SSH banner is publicly disclosed; no authentication occurs.
                print("PASS: TCP port 65002 reachable, SSH banner received:", banner.decode("ascii", errors="replace").strip())
                print("NEXT: Enable SSH access in Hostinger and configure secure SSH key auth.")
                return 0
            print("BLOCKED: Port reachable but no SSH identification banner")
            return 2
    except OSError as exc:
        print("BLOCKED: SSH/SFTP port 65002 not reachable:", type(exc).__name__)
        return 1

if __name__ == "__main__":
    sys.exit(main())
