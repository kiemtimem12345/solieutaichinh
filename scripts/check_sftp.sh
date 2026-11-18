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
# Avoid leaking SSH verbosity/remote names; print only vetted diagnostic categories.
# A failure may be password rejection, SSH policy, missing SFTP subsystem, or bad path.
if [[ "$SFTP_USERNAME" != "u154814653" ]]; then
  echo "::error::SFTP username is not the Hostinger SSH account u154814653"
  exit 2
fi
export SSHPASS="$SFTP_PASSWORD"
printf 'pwd\nls "%s"\n' "$SFTP_DATA_DIR" > "$tmp/read_only.batch"
if timeout 45s sshpass -e sftp -vv -q -b "$tmp/read_only.batch" \
  -P "$PORT" \
  -oBatchMode=no \
  -oPubkeyAuthentication=no \
  -oPreferredAuthentications=password,keyboard-interactive \
  -oNumberOfPasswordPrompts=1 \
  -oStrictHostKeyChecking=yes \
  -oUserKnownHostsFile="$tmp/known_hosts" \
  -oConnectTimeout=15 \
  "$SFTP_USERNAME@$HOST" >"$tmp/sftp.out" 2>"$tmp/sftp.err"; then
  unset SSHPASS
  echo "PASS: Password authentication and read-only directory listing succeeded"
  exit 0
fi
unset SSHPASS
if grep -Eq 'Authenticated to |Authentication succeeded' "$tmp/sftp.err"; then
  echo "::notice::SSH authentication succeeded; failure occurred after login (SFTP subsystem or remote path)"
elif grep -Eqi 'Permission denied|Authentication failed|Too many authentication failures' "$tmp/sftp.err"; then
  echo "::error::SSH rejected authentication: check SSH username and the actual Hostinger SSH password"
elif grep -Eqi 'Connection closed|Connection reset|Received disconnect' "$tmp/sftp.err"; then
  echo "::error::SSH/SFTP connection was closed before confirmed successful authentication; this may be server policy, unsupported password authentication, or invalid credentials"
elif grep -Eqi 'Could not resolve hostname|Connection timed out|No route to host' "$tmp/sftp.err"; then
  echo "::error::Network/DNS timeout before authentication"
else
  echo "::error::SFTP failed; inspect SSH authentication methods and hosting policy"
fi
if grep -Eq 'Authentications that can continue: ' "$tmp/sftp.err"; then
  methods="$(grep -Eo 'Authentications that can continue: [A-Za-z0-9,_-]+' "$tmp/sftp.err" | sort -u | paste -sd ';' -)"
  echo "::notice::SSH server offered: $methods"
fi
if grep -Eq 'Next authentication method: ' "$tmp/sftp.err"; then
  method="$(grep -Eo 'Next authentication method: [a-z-]+' "$tmp/sftp.err" | tail -1)"
  echo "::notice::$method"
fi
if grep -q 'subsystem request failed' "$tmp/sftp.err"; then
  echo "::error::SFTP subsystem request was refused after SSH connection"
fi
echo "No remote files were changed; password and raw SSH logs were not printed."
exit 1
