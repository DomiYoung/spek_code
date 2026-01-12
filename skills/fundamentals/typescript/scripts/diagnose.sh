#!/usr/bin/env bash
set -euo pipefail

TS_CONFIG="${TS_CONFIG:-tsconfig.json}"
SHOW_CONFIG="${SHOW_CONFIG:-0}"

printf "TypeScript diagnostics (read-only)\n"

if command -v tsc >/dev/null 2>&1; then
  tsc -v
  if [ -f "$TS_CONFIG" ]; then
    printf "\nConfig: %s\n" "$TS_CONFIG"
    if [ "$SHOW_CONFIG" = "1" ]; then
      tsc --showConfig -p "$TS_CONFIG"
    else
      printf "(set SHOW_CONFIG=1 to print resolved config)\n"
    fi
  else
    printf "No %s found in %s\n" "$TS_CONFIG" "$(pwd)"
  fi
else
  printf "tsc not found. Install TypeScript to run compiler checks.\n"
fi

printf "\nSuggested checks (manual):\n"
printf "- tsc --noEmit\n"
printf "- tsc --traceResolution\n"
printf "- confirm moduleResolution/paths/exports\n"
