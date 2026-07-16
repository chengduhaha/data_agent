#!/usr/bin/env bash
# Setup data_agent: Python venv, deps, Node (nvm preferred), frontend deps, default user.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> data_agent setup"
echo "    root: $ROOT"

# --- Python ---
if [[ ! -d .venv ]]; then
  echo "==> Creating Python venv"
  python3 -m venv .venv || /data/miniconda3/bin/python -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
echo "==> Installing backend requirements"
pip install -U pip
pip install -r backend/requirements.txt

# --- Node (prefer nvm local install; fall back to conda / system) ---
export NVM_DIR="${NVM_DIR:-$ROOT/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  # shellcheck disable=SC1091
  . "$NVM_DIR/nvm.sh"
  nvm install 22 >/dev/null
  nvm use 22 >/dev/null
elif ! command -v node >/dev/null 2>&1; then
  echo "==> Installing Node via conda-forge"
  if command -v conda >/dev/null 2>&1; then
    conda install -y -c conda-forge nodejs || true
  fi
  if ! command -v node >/dev/null 2>&1; then
    echo "Node.js not found. Install Node 20+ or nvm, then re-run."
    exit 1
  fi
fi

# Prefer nvm node over broken conda node if both exist
if [[ -d "$NVM_DIR/versions/node" ]]; then
  NODE_BIN="$(find "$NVM_DIR/versions/node" -maxdepth 2 -type f -name node | sort | tail -1)"
  if [[ -n "$NODE_BIN" ]]; then
    export PATH="$(dirname "$NODE_BIN"):$PATH"
  fi
fi

echo "==> Node $(node --version) / npm $(npm --version)"

# --- Frontend ---
if [[ ! -f frontend/package.json ]]; then
  echo "==> Scaffolding Next.js frontend (first run expects package.json already present)"
fi
echo "==> Installing frontend dependencies"
(cd frontend && npm install)

# --- Default user workspace ---
echo "==> Ensuring default user workspace"
PYTHONPATH=backend .venv/bin/python - <<'PY'
from app.store.paths import ensure_user_layout, DEFAULT_USER_ID
ensure_user_layout(DEFAULT_USER_ID)
print(f"user workspace ready: {DEFAULT_USER_ID}")
PY

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "==> Created .env from .env.example"
fi

echo ""
echo "Setup complete."
echo "  Configure a model in the UI (Settings → Model) or edit workspace/local/config.json"
echo "  Run: ./scripts/service.sh start   (or ./scripts/dev.sh for foreground dev)"
