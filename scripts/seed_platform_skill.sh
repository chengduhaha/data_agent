#!/usr/bin/env bash
# Seed platform contract-guided-data-analysis skill from wiki source tree.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${DATA_AGENT_SKILL_SOURCE:-/data/workplace/bigdata_wiki_llm_1/contract-guided-data-analysis}"
DEST="$ROOT/backend/platform/skills/contract-guided-data-analysis"

if [[ ! -f "$SRC/SKILL.md" ]]; then
  echo "ERROR: skill source missing SKILL.md at $SRC" >&2
  exit 1
fi

echo "==> Seeding platform skill from $SRC"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -a "$SRC" "$DEST"

if [[ ! -f "$DEST/pack.yaml" ]]; then
  echo "ERROR: seeded skill missing pack.yaml" >&2
  exit 1
fi

echo "==> Platform skill installed at $DEST"
echo "==> Verify Vertica secrets in .env.secrets (VERTICA_API_KEY, VERTICA_HOST, ...)"
if [[ -f "$ROOT/.env.secrets" ]]; then
  echo "    .env.secrets present"
else
  echo "    WARN: .env.secrets not found — platform Vertica MCP will stay inactive"
fi

echo "Done."
