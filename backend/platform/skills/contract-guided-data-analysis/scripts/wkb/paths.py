"""Portable paths for WKB indexing inside the skill package."""

from __future__ import annotations

from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_ROOT = SKILL_ROOT / "knowledge"
WKB_ROOT = KNOWLEDGE_ROOT / "storage" / "wkb"
SNAPSHOT_DIR = WKB_ROOT / "snapshots" / "_snapshot_id_template"
SPARSE_INDEX_DIR = WKB_ROOT / "indexes" / "sparse_prefilter"
SEMANTIC_INDEX_DIR = WKB_ROOT / "indexes" / "semantic"
LAYERS = ["l1_catalog", "l2_usage", "l3_code", "l4_flow", "l5_eval"]
