#!/usr/bin/env python3
"""Check candidate FTPS hostnames without FTP credentials or remote writes."""
import socket
import ssl
from ftplib import FTP_TLS

EXPECTED_IP = "195.35.62.53"
HOST = "ftp.solieutaichinh.online"
PORT = 21

def main():
    print("Candidate:", HOST)
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(HOST, PORT, type=socket.SOCK_STREAM)})
    print("DNS addresses:", ", ".join(addresses))
    print("Expected Hostinger IP matches:", EXPECTED_IP in addresses)
    if EXPECTED_IP not in addresses:
        raise SystemExit("BLOCKED: FTP hostname does not resolve to Hostinger FTP IP")
    context = ssl.create_default_context()
    with FTP_TLS(context=context, timeout=12) as ftp:
        ftp.connect(HOST, PORT)
        ftp.auth()
        print("PASS: certificate trusted and hostname matches")
        print("FTP server remote address matches:", ftp.sock.getpeername()[0] == EXPECTED_IP)
        ftp.close()
    print("READ ONLY: did not send credentials or modify any files")

if __name__ == "__main__":
    main()
