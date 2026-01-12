#!/usr/bin/env bash
set -euo pipefail

printf "Database diagnostics (read-only)\n"

if command -v psql >/dev/null 2>&1; then
  psql --version
fi

if command -v mysql >/dev/null 2>&1; then
  mysql --version
fi

if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 --version
fi

printf "\nSuggested checks (manual):\n"
printf "- EXPLAIN (ANALYZE, BUFFERS) <query>\n"
printf "- check slow query log / lock waits\n"
printf "- review index selectivity and statistics freshness\n"
