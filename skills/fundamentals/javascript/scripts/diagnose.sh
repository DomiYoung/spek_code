#!/usr/bin/env bash
set -euo pipefail

printf "JavaScript diagnostics (read-only)\n"

if command -v node >/dev/null 2>&1; then
  node -v
  node -p "process.versions"

  printf "\nEvent loop order demo (Node):\n"
  node -e "console.log('sync'); setTimeout(()=>console.log('macrotask'),0); Promise.resolve().then(()=>console.log('microtask'));"
else
  printf "Node.js not found. Install Node to run runtime checks.\n"
fi

printf "\nSuggested checks (manual):\n"
printf "- Verify this binding and closure scope in minimal repro\n"
printf "- Compare microtask vs macrotask order with console logs\n"
printf "- Validate module type (ESM/CJS) and default export behavior\n"
