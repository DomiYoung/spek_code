#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${TARGET_URL:-https://example.com}"
TARGET_HOST="${TARGET_HOST:-example.com}"

printf "Network diagnostics (read-only)\n"
printf "Target URL: %s\n" "$TARGET_URL"
printf "Target Host: %s\n\n" "$TARGET_HOST"

if command -v curl >/dev/null 2>&1; then
  curl -I "$TARGET_URL"
else
  printf "curl not found\n"
fi

if command -v dig >/dev/null 2>&1; then
  dig +stats "$TARGET_HOST"
elif command -v nslookup >/dev/null 2>&1; then
  nslookup "$TARGET_HOST"
else
  printf "dig/nslookup not found\n"
fi

if command -v ping >/dev/null 2>&1; then
  ping -c 4 "$TARGET_HOST"
fi

if command -v openssl >/dev/null 2>&1; then
  printf "\nTLS handshake summary:\n"
  echo | openssl s_client -connect "$TARGET_HOST:443" -servername "$TARGET_HOST" 2>/dev/null | openssl x509 -noout -dates
fi

printf "\nOptional: traceroute %s\n" "$TARGET_HOST"
