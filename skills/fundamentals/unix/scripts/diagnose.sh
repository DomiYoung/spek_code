#!/usr/bin/env bash
set -euo pipefail

PID="${PID:-}"

printf "Unix diagnostics (read-only)\n"
uname -a
uptime || true
ulimit -n || true

if [ -n "$PID" ]; then
  printf "\nProcess snapshot (PID=%s)\n" "$PID"
  ps -o stat,ppid,pid,comm -p "$PID" || true
  if command -v lsof >/dev/null 2>&1; then
    printf "Open file descriptors: "
    lsof -p "$PID" 2>/dev/null | wc -l
  fi
fi

printf "\nSuggested checks (manual):\n"
printf "- strace -p <PID> (Linux) or dtruss -p <PID> (macOS)\n"
printf "- iostat/vmstat for I/O pressure\n"
printf "- check ulimit -n for fd exhaustion\n"
