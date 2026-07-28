#!/usr/bin/env python3
"""Rebuild WKB sparse + semantic indexes from knowledge/storage/wkb snapshots."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wkb.index_builder import build_indexes

if __name__ == "__main__":
    build_indexes()
    print("WKB indexes rebuilt under knowledge/storage/wkb/indexes/")
