#!/usr/bin/env bash
set -euo pipefail

printf ".NET diagnostics (read-only)\n"

if command -v dotnet >/dev/null 2>&1; then
  dotnet --info
else
  printf "dotnet not found. Install .NET SDK/runtime.\n"
fi

printf "\nSuggested checks (manual):\n"
printf "- dotnet-counters monitor --process-id <PID> System.Runtime\n"
printf "- dotnet-trace collect --process-id <PID>\n"
printf "- check GC pause time and allocation rate\n"
