#!/usr/bin/env bash
# One-time migration: backend/app/users/* -> workspace/*
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEGACY="${ROOT}/backend/app/users"
TARGET="${ROOT}/workspace"

mkdir -p "${TARGET}"

if [[ ! -d "${LEGACY}" ]]; then
  echo "No legacy users dir at ${LEGACY}; nothing to migrate."
  exit 0
fi

shopt -s nullglob
for user_dir in "${LEGACY}"/*; do
  [[ -d "${user_dir}" ]] || continue
  name="$(basename "${user_dir}")"
  dest="${TARGET}/${name}"
  if [[ -d "${dest}" ]]; then
    echo "SKIP ${name}: ${dest} already exists"
    continue
  fi
  echo "==> Migrating ${name} -> ${dest}"
  cp -a "${user_dir}" "${dest}"
done

echo "Migration complete. Workspace root: ${TARGET}"
