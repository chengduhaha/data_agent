"""Per-turn rolling summaries for multi-question threads."""

from __future__ import annotations

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.harness.config import HarnessConfig, load_harness_config
from app.agent.harness.wrapup import _build_wrapup_context
from app.store.chat_history import fold_checkpoint_messages

logger = logging.getLogger(__name__)

TURN_SUMMARY_SYSTEM = """Summarize ONE completed user turn from an analytics agent session.
Output markdown with sections:
## Question
## Answer (concise)
## Key SQL / queries (if any)
## Artifacts / files (paths)
## Open items

Keep under 800 words. Do not invent data not present in the transcript."""


async def summarize_turn(
    model: Any,
    messages: list[Any],
    *,
    harness_cfg: HarnessConfig | None = None,
) -> str:
    """Summarize messages belonging to a single user turn."""
    _ = harness_cfg or load_harness_config()
    context = _build_wrapup_context(messages, max_chars=18_000)
    if not context.strip():
        return ""
    try:
        llm = model
        try:
            llm = model.bind(max_tokens=2048)
        except Exception:
            pass
        result = await llm.ainvoke(
            [
                SystemMessage(content=TURN_SUMMARY_SYSTEM),
                HumanMessage(content=f"### Turn transcript\n{context}"),
            ]
        )
        content = getattr(result, "content", result)
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = [
                str(b.get("text", ""))
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
            return "".join(parts).strip()
        return str(content).strip()
    except Exception:
        logger.exception("turn summary failed")
        folded = fold_checkpoint_messages(list(messages))
        last_user = next((t for t in reversed(folded) if t.get("role") == "user"), None)
        last_asst = next((t for t in reversed(folded) if t.get("role") == "assistant"), None)
        q = (last_user or {}).get("content", "")[:200]
        a = (last_asst or {}).get("content", "")[:500]
        return f"## Question\n{q}\n\n## Answer (concise)\n{a}\n\n_(auto fallback summary)_"


def slice_messages_for_turn(messages: list[Any], turn_index: int) -> list[Any]:
    """Return messages belonging to turn_index (0-based user turns)."""
    if turn_index < 0:
        return []
    human_idxs = [
        i
        for i, m in enumerate(messages)
        if str(getattr(m, "type", None) or getattr(m, "role", "")).lower()
        in ("human", "user")
    ]
    if turn_index >= len(human_idxs):
        return []
    start = human_idxs[turn_index]
    end = human_idxs[turn_index + 1] if turn_index + 1 < len(human_idxs) else len(messages)
    return list(messages[start:end])
