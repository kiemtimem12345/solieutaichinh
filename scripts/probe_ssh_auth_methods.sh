#!/usr/bin/env bash
# Public read-only SSH authentication-method check.
# Does not use credentials and cannot enter authenticated session.
set -euo pipefail
host=195.35.62.53
port=65002
user=u154814653
expected='SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA'
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
timeout 20 ssh-keyscan -T 12 -t ed25519 -p "$port" "$host" 2>/dev/null >"$tmp/known_hosts"
if [[ ! -s "$tmp/known_hosts" ]]; then
  echo "::error::SSH public key not returned; unable to start authentication probe"; exit 1
fi
fp="$(ssh-keygen -lf "$tmp/known_hosts" -E sha256 | awk '$NF=="(ED25519)"{print $2}' | head -1)"
if [[ "$fp" != "$expected" ]]; then
  echo "::error::SSH fingerprint mismatch; refusing connection"; exit 1
fi
echo "PASS: Hostinger SSH fingerprint validated"
# -N: do not execute any command; public probe tests only advertised auth methods.
# -oPreferredAuthentications=none: no password/keys sent.
timeout 22 ssh -vvv -N -T \
  -p "$port" \
  -oStrictHostKeyChecking=yes \
  -oUserKnownHostsFile="$tmp/known_hosts" \
  -oPasswordAuthentication=no \
  -oKbdInteractiveAuthentication=no \
  -oPubkeyAuthentication=no \
  -oPreferredAuthentications=none \
  -oBatchMode=yes \
  -oConnectTimeout=12 \
  "$user@$host" >"$tmp/out" 2>"$tmp/err" || true
if grep -q 'Authentications that can continue:' "$tmp/err"; then
  methods="$(grep 'Authentications that can continue:' "$tmp/err" | sed 's/.*Authentications that can continue: //' | head -1 | tr -cd '[:alnum:]_,-')"
  echo "PASS: SSH reached authentication negotiation"
  echo "Offered authentication methods: $methods"
  if [[ "$methods" == *password* || "$methods" == *keyboard-interactive* ]]; then
    echo "CONCLUSION: password-capable SSH auth advertised by server"
  else
    echo "CONCLUSION: password auth not advertised for this user or connection"
  fi
elif grep -Eqi 'Connection closed|Connection reset|Received disconnect|Connection refused|kex_exchange_identification' "$tmp/err"; then
  if grep -Eqi 'Connection established' "$tmp/err"; then
    echo "CONCLUSION: SSH TCP connected but server closed before advertising authentication methods"
  else
    echo "CONCLUSION: SSH TCP connection closed/rejected before authentication"
  fi
else
  echo "CONCLUSION: no authentication methods observed; inspect server connection policy"
fi
echo "Probe used no credentials and did not modify remote files."
