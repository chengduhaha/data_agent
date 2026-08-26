from __future__ import annotations

from app.agent.harness.forward_instruction import (
    BlockReason,
    ExpectedAction,
    ForwardInstruction,
)
from app.platform.pack import merge_pack_into_manifest
from app.agent.extensions.manifest import parse_skill_manifest
from pathlib import Path


def test_forward_instruction_keeps_blocked_keyword() -> None:
    text = ForwardInstruction(
        reason=BlockReason.BUDGET_EXHAUSTED,
        tool_name="run_query_safely",
        used=12,
        limit=12,
        expected_action=ExpectedAction.SYNTHESIZE,
        evidence_summary="1. tool=run_query_safely",
    ).to_tool_message_content()
    assert "Blocked" in text
    assert "budget exceeded" in text.lower()
    assert "Evidence collected so far" in text


def test_merge_pack_injects_contract_harness() -> None:
    skill_md = Path(
        "/data/workplace/data_agent/backend/defaults/b_report/skills/"
        "contract-guided-data-analysis/SKILL.md"
    )
    if not skill_md.exists():
        return
    manifest = parse_skill_manifest(skill_md.read_text(encoding="utf-8"))
    merged = merge_pack_into_manifest(manifest, skill_md, source="org")
    assert merged.harness.tool_budgets.get("run_query_safely") == 12
    assert "wkb_query" in merged.extensions.tools
