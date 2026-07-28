#!/usr/bin/env python3
"""WKB candidate retrieval for contract-guided-data-analysis."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wkb.run_query import main

if __name__ == "__main__":
    main()
