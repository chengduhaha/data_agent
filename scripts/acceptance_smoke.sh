#!/usr/bin/env bash
# Acceptance smoke checks (run after ./scripts/service.sh restart).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BASE="${DATA_AGENT_BACKEND_URL:-http://127.0.0.1:8000}"

echo "==> Backend health"
curl -sf "${BASE}/health" | head -c 200
echo ""

echo "==> API acceptance (pytest — oauth-independent)"
cd backend && PYTHONPATH=. OAUTH2_ENABLED=false ../.venv/bin/pytest tests/test_api_acceptance.py -q --tb=no

echo "==> Contract skill extensions (pytest)"
PYTHONPATH=. OAUTH2_ENABLED=false ../.venv/bin/pytest tests/test_extensions.py::test_parse_manifest_extensions_and_harness -q --tb=no

echo "==> Backend pytest (full)"
PYTHONPATH=. OAUTH2_ENABLED=false ../.venv/bin/pytest -q --tb=no

echo "==> Frontend unit tests"
cd "$ROOT/frontend" && npm test

echo "==> Frontend E2E (Playwright — uses running dev server on :6641)"
curl -sf "${FRONTEND_URL:-http://127.0.0.1:6641}/" >/dev/null
cd "$ROOT/frontend" && npx playwright install chromium 2>/dev/null || true
cd "$ROOT/frontend" && PLAYWRIGHT_SKIP_WEBSERVER=1 npm run test:e2e

echo "==> Frontend production build"
cd "$ROOT/frontend" && npm run build

echo ""
echo "All acceptance smoke checks passed."
