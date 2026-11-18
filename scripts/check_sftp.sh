#!/usr/bin/env bash
# Verify SFTP access read-only using pinned SSH host key.
set -euo pipefail
: "${SFTP_USERNAME:?Set SFTP_USERNAME secret}"
: "${SFTP_PRIVATE_KEY:?Set SFTP_PRIVATE_KEY secret}"
: "${SFTP_KNOWN_HOSTS:?Set SFTP_KNOWN_HOSTS secret with independently verified server public key}"
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
printf '%s\n' "$SFTP_PRIVATE_KEY" > "$tmp/id_key"
chmod 600 "$tmp/id_key"
printf '%s\n' "$SFTP_KNOWN_HOSTS" > "$tmp/known_hosts"
chmod 600 "$tmp/known_hosts"
if ! ssh-keygen -F "[$HOST]:$PORT" -f "$tmp/known_hosts" >/dev/null; then
  echo "::error::Pinned SSH host key for [$HOST]:$PORT missing"; exit 2
fi
# Batch operations do not modify remote files. 'ls' must succeed.
printf 'pwd\nls "%s"\n' "$SFTP_DATA_DIR" | timeout 40s sftp -q -b - \
  -P "$PORT" \
  -i "$tmp/id_key" \
  -oBatchMode=yes \
  -oIdentitiesOnly=yes \
  -oStrictHostKeyChecking=yes \
  -oUserKnownHostsFile="$tmp/known_hosts" \
  -oConnectTimeout=15 \
  "$SFTP_USERNAME@$HOST"
echo "PASS: verified SSH host identity, authenticated, read-only SFTP access to data directory"
