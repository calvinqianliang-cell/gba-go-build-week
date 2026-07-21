#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Scanning current files for obvious secrets..."
PATTERN='sk-[A-Za-z0-9_-]{20,}|postgres(ql)?://|redis(s)?://|password[[:space:]]*=|secret[[:space:]]*=|token[[:space:]]*=|api[_-]?key[[:space:]]*=[^[:space:]]+|PRIVATE KEY'

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git grep -nE "$PATTERN" -- . \
    ':!.env.example' \
    ':!.venv/**' \
    ':!demo_runtime/**' \
    ':!SECURITY_SCAN_REPORT.md' \
    ':!scripts/security_scan.sh' || true
else
  grep -RInE "$PATTERN" . \
    --exclude='.env.example' \
    --exclude='SECURITY_SCAN_REPORT.md' \
    --exclude='security_scan.sh' \
    --exclude-dir='.venv' \
    --exclude-dir='.git' \
    --exclude-dir='demo_runtime' \
    --exclude-dir='__pycache__' \
    --exclude-dir='.pytest_cache' || true
fi

echo "Security scan completed. Review any lines above before sharing."
