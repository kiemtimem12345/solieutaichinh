#!/usr/bin/env bash
# Compare the Hostinger-reported SSH ED25519 fingerprint to the real server key.
# Public-key read only; no credentials and no writes to Hostinger.
set -euo pipefail
HOST="195.35.62.53"
PORT=65002
EXPECTED="SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
timeout 20 ssh-keyscan -T 12 -p "$PORT" -t ed25519 "$HOST" 2>/dev/null > "$TMP"
if [[ ! -s "$TMP" ]]; then
  echo "::error::Hostinger SSH public key not accessible"; exit 1
fi
ACTUAL="$(ssh-keygen -lf "$TMP" -E sha256 | awk '$NF == "(ED25519)" {print $2}' | head -1)"
if [[ -z "$ACTUAL" ]]; then
  echo "::error::ED25519 key missing from SSH response"; exit 1
fi
echo "Host key type: ED25519"
echo "Fingerprint from SSH server: $ACTUAL"
echo "Fingerprint provided by Hostinger hPanel: $EXPECTED"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "::error::SSH host key fingerprint MISMATCH. Stop SFTP configuration."; exit 1
fi
echo "PASS: SSH ED25519 host key matches Hostinger control panel"
echo "No credentials used. No website files changed."
