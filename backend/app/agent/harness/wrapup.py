"""Generate a final user-facing answer when the agent hits the step budget."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agent.harness.config import HarnessConfig, load_harness_config
from app.store.chat_history import fold_checkpoint_messages

logger = logging.getLogger(__name__)

WRAPUP_SYSTEM = """You are finishing an incomplete agent run for a contract-guided data-analysis assistant.
The agent ran tools but did not deliver a complete user-facing answer (step budget exhausted or stopped early).

Write a clear, complete final response for the user based ONLY on:
- the user's latest question
- tool outputs and partial assistant messages already in the transcript

Rules:
- Do NOT call tools or ask to run more tools.
- State any limitations if evidence is incomplete.
- Use markdown headings and tables when helpful.
- If SQL was run, cite key numbers and note validation gaps.
- Follow contract-guided output: short conclusion, evidence tables, and caveats.
"""


def needs_synthesis_wrapup(prior: str, *, query_count: int = 0, min_chars: int = 400) -> bool:
    """True when Vertica/SQL evidence exists but the last assistant text is not a synthesis."""
    if query_count <= 0:
        return False
    text = (prior or "").strip()
    if not text:
        return True
    if "##" in text or "结论" in text or "summary" in text.lower():
        return False
    if len(text) >= min_chars:
        return False
    lower = text.lower()
    planning_prefixes = (
        "let me ",
        "now let me ",
        "now i ",
        "i'll ",
        "i will ",
        "the dwd ",
        "the dws ",
    )
    if any(lower.startswith(p) for p in planning_prefixes) and "##" not in text:
        return True
    if query_count >= 8 and len(text) < min_chars:
        return True
    return len(text) < 200


def _message_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "".join(parts).strip()
    return str(content).strip()


def _build_wrapup_context(messages: list[Any], *, max_chars: int = 24_000) -> str:
    folded = fold_checkpoint_messages(list(messages))
    lines: list[str] = []
    for turn in folded[-8:]:
        role = turn.get("role", "assistant")
        content = str(turn.get("content") or "").strip()
        if content:
            lines.append(f"## {role}\n{content}")
        for tool in turn.get("tools") or []:
            name = tool.get("tool", "tool")
            inp = tool.get("input")
            out = tool.get("output")
            preview_out = str(out)
            limit = 4000 if "run_query" in str(name) else 1500
            if len(preview_out) > limit:
                preview_out = preview_out[:limit] + "…"
            lines.append(f"### tool:{name}\ninput: {inp}\noutput: {preview_out}")
    text = "\n\n".join(lines).strip()
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n…[transcript truncated for wrap-up]"
    return text or "(no prior transcript)"


async def stream_wrapup_tokens(
    model: Any,
    agent: Any,
    config: dict[str, Any],
    *,
    harness_cfg: HarnessConfig | None = None,
) -> AsyncIterator[str]:
    """Yield plain text chunks for a budget-limit wrap-up answer."""
    cfg = harness_cfg or load_harness_config(
        extended_run=bool(config.get("configurable", {}).get("extended_run"))
    )
    try:
        state = await agent.aget_state(config)
        values = getattr(state, "values", None) or {}
        raw_messages = values.get("messages") or []
    except Exception:
        logger.debug("wrap-up could not load agent state", exc_info=True)
        raw_messages = []

    context = _build_wrapup_context(list(raw_messages))
    human = (
        "Produce the final answer for the user now.\n\n"
        f"### Transcript\n{context}"
    )
    llm = model
    if cfg.wrapup_max_tokens:
        try:
            llm = model.bind(max_tokens=cfg.wrapup_max_tokens)
        except Exception:
            llm = model

    try:
        async for chunk in llm.astream(
            [
                SystemMessage(content=WRAPUP_SYSTEM),
                HumanMessage(content=human),
            ]
        ):
            text = _message_text(getattr(chunk, "content", chunk))
            if text:
                yield text
    except Exception:
        logger.exception("wrap-up model call failed")
        yield (
            "\n\n---\n**Run paused** (tool-step limit). "
            "Partial work is saved in this thread — click **Continue** to keep going, "
            "or ask a narrower follow-up."
        )


async def invoke_wrapup(
    model: Any,
    agent: Any,
    config: dict[str, Any],
    *,
    harness_cfg: HarnessConfig | None = None,
) -> str:
    parts: list[str] = []
    async for piece in stream_wrapup_tokens(model, agent, config, harness_cfg=harness_cfg):
        parts.append(piece)
    return "".join(parts).strip()


def last_ai_text(messages: list[Any]) -> str:
    for msg in reversed(messages):
        role = getattr(msg, "type", None) or getattr(msg, "role", "")
        if str(role).lower() in ("ai", "assistant"):
            text = _message_text(getattr(msg, "content", ""))
            if text:
                return text
    return ""
