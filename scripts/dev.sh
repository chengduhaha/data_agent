#!/usr/bin/env bash
# Foreground dev mode — wrapper around service.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/scripts/service.sh" start --foreground "$@"
