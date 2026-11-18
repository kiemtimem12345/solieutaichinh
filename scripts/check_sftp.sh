#!/usr/bin/env bash
# Verify SFTP access read-only using pinned SSH host key.
set -euo pipefail
: "${SFTP_USERNAME:?Set SFTP_USERNAME secret}"
: "${SFTP_PASSWORD:?Set SFTP_PASSWORD secret}"
: "${SFTP_DATA_DIR:?Set SFTP_DATA_DIR repository variable}"
HOST="195.35.62.53"
PORT="65002"
ROOT_PREFIX="/home/u154814653/domains/solieutaichinh.online/public_html"
# Prevent accidentally targeting another website or a parent folder.
if [[ "$SFTP_DATA_DIR" != "$ROOT_PREFIX/data" && "$SFTP_DATA_DIR" != "$ROOT_PREFIX/data/" ]]; then
  echo "::error::Invalid SFTP_DATA_DIR. Expected $ROOT_PREFIX/data"; exit 2
fi
if [[ ! "$SFTP_USERNAME" =~ ^[a-zA-Z0-9_.-]+$ ]]; then
  echo "::error::Invalid SFTP username"; exit 2
fi
tmp="$(mktemp -d)"
chmod 700 "$tmp"
trap 'rm -rf "$tmp"' EXIT
# Compare the presented public key with the Hostinger hPanel fingerprint.
# This fingerprint was verified independently in GitHub Actions run 44324833181.
EXPECTED="SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"
timeout 20 ssh-keyscan -T 12 -p "$PORT" -t ed25519 "$HOST" 2>/dev/null > "$tmp/known_hosts"
chmod 600 "$tmp/known_hosts"
if [[ ! -s "$tmp/known_hosts" ]]; then
  echo "::error::SSH ED25519 host key unavailable"; exit 2
fi
ACTUAL="$(ssh-keygen -lf "$tmp/known_hosts" -E sha256 | awk '$NF == "(ED25519)" {print $2}' | head -1)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "::error::Hostinger SSH fingerprint mismatch; refusing connection"; exit 2
fi
echo "PASS: SSH host fingerprint matches independently verified Hostinger key"
# Batch operations do not modify remote files. 'ls' must succeed.
export SSHPASS="$SFTP_PASSWORD"
printf 'pwd\nls "%s"\n' "$SFTP_DATA_DIR" | timeout 40s sshpass -e sftp -q -b - \
  -P "$PORT" \
  -oBatchMode=no \
  -oPubkeyAuthentication=no \
  -oPreferredAuthentications=password,keyboard-interactive \
  -oStrictHostKeyChecking=yes \
  -oUserKnownHostsFile="$tmp/known_hosts" \
  -oConnectTimeout=15 \
  "$SFTP_USERNAME@$HOST"
unset SSHPASS
echo "PASS: verified SSH host identity, password-authenticated, read-only SFTP access to data directory"
