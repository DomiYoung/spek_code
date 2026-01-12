#!/usr/bin/env bash
set -euo pipefail

APP_PATH="${APP_PATH:-}"

printf "macOS diagnostics (read-only)\n"
if command -v sw_vers >/dev/null 2>&1; then
  sw_vers
fi
uname -a

if [ -n "$APP_PATH" ]; then
  printf "\nApp path: %s\n" "$APP_PATH"
  if [ -e "$APP_PATH" ]; then
    if command -v codesign >/dev/null 2>&1; then
      codesign -dv --verbose=4 "$APP_PATH" 2>&1 | head -n 20
    fi
    if command -v spctl >/dev/null 2>&1; then
      spctl --assess --verbose "$APP_PATH" 2>&1 || true
    fi
    if command -v xattr >/dev/null 2>&1; then
      xattr -l "$APP_PATH" 2>/dev/null || true
    fi
  else
    printf "APP_PATH not found.\n"
  fi
else
  printf "Set APP_PATH to the .app bundle to check codesign/Gatekeeper.\n"
fi

printf "\nSuggested checks (manual):\n"
printf "- log show --last 1h --predicate 'eventMessage CONTAINS \"deny\"'\n"
printf "- launchctl print system/<service>\n"
