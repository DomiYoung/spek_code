#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${TARGET_URL:-https://example.com}"

printf "Browser diagnostics (read-only)\n" 
printf "OS: %s %s\n" "$(uname -s)" "$(uname -r)"

if command -v sw_vers >/dev/null 2>&1; then
  sw_vers
fi

if command -v google-chrome >/dev/null 2>&1; then
  google-chrome --version
elif command -v chromium >/dev/null 2>&1; then
  chromium --version
elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version
fi

printf "\nSuggested checks (manual):\n"
printf "- DevTools Performance: record long tasks and layout/paint cost\n"
printf "- DevTools Memory: heap snapshot + detached DOM tree\n"
printf "- DevTools Network: waterfall, blocking, TTFB\n"

if command -v lighthouse >/dev/null 2>&1; then
  printf "\nOptional: lighthouse %s --only-categories=performance --output=json\n" "$TARGET_URL"
else
  printf "\nOptional: install lighthouse and run performance audit\n"
fi
