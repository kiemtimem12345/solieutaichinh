#!/usr/bin/env python3
"""Independently diagnose SSH password auth and read-only SFTP via Paramiko.

No remote commands, remote writes, passwords in stdout, or unpinned host keys.
"""
import base64
import hashlib
import os
import socket
import sys

import paramiko

HOST = "195.35.62.53"
PORT = 65002
USERNAME = "u154814653"
DATA_DIR = "/home/u154814653/domains/solieutaichinh.online/public_html/data"
ED25519_SHA256 = "SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"


def run() -> int:
    username = os.environ.get("SFTP_USERNAME", "")
    password = os.environ.get("SFTP_PASSWORD", "")
    path = os.environ.get("SFTP_DATA_DIR", "").rstrip("/")
    if username != USERNAME:
        print("::error::SFTP_USERNAME must equal the Hostinger SSH account")
        return 2
    if not password:
        print("::error::SFTP_PASSWORD GitHub Secret is missing or empty")
        return 2
    if path != DATA_DIR:
        print("::error::SFTP_DATA_DIR must be the exact expected site data directory")
        return 2

    stage = "connect"
    transport = None
    sftp = None
    try:
        sock = socket.create_connection((HOST, PORT), timeout=12)
        sock.settimeout(15)
        transport = paramiko.Transport(sock)
        transport.get_security_options().key_types = ("ssh-ed25519",)
        transport.banner_timeout = 12
        transport.auth_timeout = 15
        transport.start_client(timeout=15)
        stage = "host_identity"
        key = transport.get_remote_server_key()
        fingerprint = "SHA256:" + base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip("=")
        if key.get_name() != "ssh-ed25519" or fingerprint != ED25519_SHA256:
            print("::error::SSH ED25519 host identity mismatch; stopping before authentication")
            return 2
        print("PASS: verified SSH server fingerprint")

        stage = "password_authentication"
        print("CHECK: authenticating SSH password (without echoing credentials)")
        remaining = transport.auth_password(username, password, fallback=False)
        if not transport.is_authenticated():
            print("::error::Hostinger did not complete password authentication")
            if remaining:
                print("::notice::Additional auth factors requested: " + ",".join(remaining))
            return 1
        print("PASS: SSH password authentication accepted")

        stage = "sftp_subsystem"
        sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp is None:
            print("::error::SSH authentication succeeded but SFTP subsystem not opened")
            return 1
        print("PASS: SFTP subsystem opened")

        stage = "remote_directory"
        sftp.listdir(path)
        print("PASS: read-only SFTP listing of configured data directory")
        return 0

    except paramiko.BadAuthenticationType as exc:
        print("::error::SSH server rejected password authentication method")
        print("::notice::Available methods: " + ",".join(exc.allowed_types))
    except paramiko.AuthenticationException:
        print("::error::SSH password authentication rejected: check SSH account password and whether the GitHub Secret was updated")
    except (EOFError, ConnectionResetError, BrokenPipeError):
        print(f"::error::SSH connection closed at stage: {stage}")
    except paramiko.SSHException as exc:
        print(f"::error::SSH protocol failure at stage: {stage}, type: {type(exc).__name__}")
    except OSError as exc:
        print(f"::error::Network/SFTP access failure at stage: {stage}, class: {type(exc).__name__}, errno: {exc.errno}")
    except Exception as exc:
        print(f"::error::Unexpected failure at stage: {stage}, class: {type(exc).__name__}")
    finally:
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()
    print("No remote files were modified.")
    return 1


if __name__ == "__main__":
    sys.exit(run())
