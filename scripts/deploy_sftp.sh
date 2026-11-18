#!/usr/bin/env bash
# Manually upload only the 41 validated JSON files via SFTP.
# No remote deletion, no UI file changes. Host identity is pinned.
set -euo pipefail

: "${SFTP_USERNAME:?Missing SFTP_USERNAME secret}"
: "${SFTP_PRIVATE_KEY:?Missing SFTP_PRIVATE_KEY secret}"
: "${SFTP_DATA_DIR:?Missing SFTP_DATA_DIR variable}"

if [[ "${SFTP_DEPLOY_ENABLED:-}" != "YES_AFTER_UI_RESTORE" ]]; then
  echo "::error::SFTP deployment blocked: set variable SFTP_DEPLOY_ENABLED to YES_AFTER_UI_RESTORE only after UI restoration and verified backups"
  exit 2
fi

HOST="195.35.62.53"
PORT="65002"
EXPECTED_USER="u154814653"
TARGET="/home/u154814653/domains/solieutaichinh.online/public_html/data"
EXPECTED_FINGERPRINT="SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA"

if [[ "$SFTP_USERNAME" != "$EXPECTED_USER" ]]; then
  echo "::error::Unexpected SFTP username; aborting"; exit 2
fi
if [[ "$SFTP_DATA_DIR" != "$TARGET" && "$SFTP_DATA_DIR" != "$TARGET/" ]]; then
  echo "::error::Unexpected destination path; aborting"; exit 2
fi

shopt -s nullglob
files=(deploy/data/*.json)
if (( ${#files[@]} != 41 )); then
  echo "::error::Expected exactly 41 staged JSON files, found ${#files[@]}"; exit 2
fi
financial=0
for f in "${files[@]}"; do
  if [[ ! "$(basename "$f")" =~ ^[A-Za-z0-9_-]+\.json$ ]]; then
    echo "::error::Unexpected JSON filename"; exit 2
  fi
  [[ "$(basename "$f")" == financials-* ]] && ((financial+=1)) || true
done
if (( financial != 32 )); then
  echo "::error::Expected 32 financial JSON files"; exit 2
fi

tmp="$(mktemp -d)"
chmod 700 "$tmp"
trap 'rm -rf "$tmp"' EXIT
printf '%s\n' "$SFTP_PRIVATE_KEY" > "$tmp/id_key"
chmod 600 "$tmp/id_key"

timeout 20 ssh-keyscan -T 12 -p "$PORT" -t ed25519 "$HOST" 2>/dev/null > "$tmp/known_hosts"
if [[ ! -s "$tmp/known_hosts" ]]; then
  echo "::error::SSH host key unavailable"; exit 2
fi
fingerprint="$(ssh-keygen -lf "$tmp/known_hosts" -E sha256 | awk '$NF == "(ED25519)" {print $2}' | head -1)"
if [[ "$fingerprint" != "$EXPECTED_FINGERPRINT" ]]; then
  echo "::error::SSH identity mismatch; aborting"; exit 2
fi
chmod 600 "$tmp/known_hosts"
echo "PASS: Hostinger SSH host fingerprint verified"

# A read-only list confirms the target exists before upload; never create parent directories.
printf 'ls "%s"\n' "$TARGET" > "$tmp/read_only.batch"
timeout 45 sftp -q -b "$tmp/read_only.batch" -P "$PORT" \
  -i "$tmp/id_key" -oBatchMode=yes -oIdentitiesOnly=yes \
  -oStrictHostKeyChecking=yes -oUserKnownHostsFile="$tmp/known_hosts" \
  -oConnectTimeout=15 "$SFTP_USERNAME@$HOST"
echo "PASS: SFTP authentication and target directory existence"

# The target is absolute and fixed; only the validated staged files are uploaded.
: > "$tmp/upload.batch"
for f in "${files[@]}"; do
  printf 'put "%s" "%s/%s"\n' "$f" "$TARGET" "$(basename "$f")" >> "$tmp/upload.batch"
done
timeout 180 sftp -q -b "$tmp/upload.batch" -P "$PORT" \
  -i "$tmp/id_key" -oBatchMode=yes -oIdentitiesOnly=yes \
  -oStrictHostKeyChecking=yes -oUserKnownHostsFile="$tmp/known_hosts" \
  -oConnectTimeout=15 "$SFTP_USERNAME@$HOST"
echo "PASS: Uploaded 41 validated JSON snapshots via pinned SFTP; no files deleted."
