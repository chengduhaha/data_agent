#!/usr/bin/env bash
# Verify organization bundle + secrets for shared runtime mount (no per-user copy).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE="${ROOT}/backend/defaults/b_report"
SECRETS="${ROOT}/.env.secrets"
PYTHON="${ROOT}/.venv/bin/python"
[[ -x "${PYTHON}" ]] || PYTHON="$(command -v python3)"

die() { echo "ERROR: $*" >&2; exit 1; }

[[ -d "${BUNDLE}" ]] || die "bundle missing: ${BUNDLE}"
[[ -d "${BUNDLE}/skills/contract-guided-data-analysis" ]] || die "org skill missing"
[[ -d "${BUNDLE}/workspace" ]] || die "org knowledge missing"

if [[ -f "${SECRETS}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${SECRETS}"
  set +a
  echo "==> Loaded ${SECRETS}"
else
  echo "WARN: ${SECRETS} not found — org Vertica MCP will be unavailable until secrets are configured"
fi

if [[ -n "${VERTICA_API_KEY:-}" ]]; then
  echo "==> Vertica org MCP: configured (server-side injection)"
else
  echo "WARN: VERTICA_API_KEY not set — org Vertica MCP disabled"
fi

echo "==> Organization bundle ready (mounted read-only at runtime)"
echo "    skills: ${BUNDLE}/skills/"
echo "    knowledge: ${BUNDLE}/workspace/"
echo "    rules: ${BUNDLE}/fragments/"
echo "    per-user data: ${ROOT}/workspace/{userid}/"
echo "No per-user copy required. Restart backend after changing bundle or secrets."
