"""Generate a final user-facing answer when the agent hits the step budget."""

from __future__ import annotations

import logging
import re
from collections.abc import AsyncIterator
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agent.harness.config import HarnessConfig, load_harness_config
from app.agent.harness.evidence import get_evidence_snapshot
from app.store.chat_history import fold_checkpoint_messages

logger = logging.getLogger(__name__)

_VERTICA_QUERY_TOOLS = frozenset({
    "run_query_safely",
    "execute_query_paginated",
    "execute_query_stream",
    "profile_query",
})

_RESEARCH_TOOLS = frozenset({
    "read_file",
    "grep",
    "glob",
    "ls",
    "wkb_query",
    "search_knowledge",
})

WRAPUP_SYSTEM = """You are finishing an incomplete agent run.
The agent ran tools but did not deliver a complete user-facing answer (step budget exhausted, stopped early, or the draft was truncated mid-sentence).

Write a clear, complete final response for the user based ONLY on:
- the user's latest question
- tool outputs and partial assistant messages already in the transcript
- the evidence snapshot below, if present

Rules:
- Do NOT call tools or ask to run more tools.
- Do NOT include intermediate research narration ("Let me…", schema checks, failed query attempts).
- If a partial answer already exists but was cut off mid-sentence, CONTINUE and complete it — do not discard or restart that analysis.
- Start with `## Summary`, then `## Evidence` (use a proper GFM markdown table when 2+ rows), then `## Analysis approach & confidence`.
- GFM tables: header row, `| :--- |` separator row, data rows — each on its own line with a blank line before the table.
- State any limitations if evidence is incomplete.
- Use markdown headings and tables when helpful.
- Match the user's language when the transcript is clearly non-English.
- If queries were run against a data source, cite key numbers and note validation gaps.
- Prefer a short conclusion, supporting evidence, and caveats.

Finalization checklist (also apply when completing constraint-incomplete answers):
- Answer every part the user explicitly asked for.
- Retain dates, filters, sort direction, and any requested N.
- Confirm results are supported by tool evidence in the transcript.
- Do not present exploration or tool narration as the final answer.
- State limitations for anything you cannot confirm; do not invent facts.
- Do not call tools or expand the user's request scope.
"""


def _has_synthesis_headings(text: str) -> bool:
    """True when the assistant already wrote a user-facing synthesis section."""
    if re.search(r"(?:^|\n)\s*#{0,3}\s*结论\b", text) or re.search(
        r"(?:^|\n)\s*结论\s*[:：]", text
    ):
        return True
    if "结论" in text and len(text.strip()) > 200:
        # Avoid treating a single mid-sentence mention as a finished answer when truncated.
        if not looks_truncated(text):
            return True
    if re.search(
        r"^##\s+(?:summary|conclusion|synthesis|answer|findings|分析)\b",
        text,
        re.I | re.M,
    ):
        return True
    # Level-2 headings only (`## Title`), not `###` planning stubs.
    if re.search(r"^##\s+[^\n#]", text, re.M):
        return True
    return False


def looks_truncated(text: str) -> bool:
    """Heuristic: answer stops mid-clause (common when max_tokens cuts a long report)."""
    t = (text or "").strip()
    if not t or len(t) < 80:
        return False
    last = t[-1]
    if last in ".!?。！？…:：;；」』》)）]】|":
        return False
    # Ends on a markdown heading / bullet — usually intentional mid-structure, not truncation.
    last_line = t.rsplit("\n", 1)[-1].strip()
    if re.match(r"^(?:#{1,6}\s+\S|[-*]\s+\S|\d+\.\s+\S)", last_line):
        return False
    # CJK / Latin word char at end after a long body → likely cut off.
    if re.search(r"[\w\u4e00-\u9fff]$", t):
        # Require some structure so short replies without punctuation are not flagged.
        if len(t) >= 120 or t.count("|") >= 4 or re.search(
            r"(?:^|\n)\s*[A-D][\.、]\s+\S", t
        ):
            return True
    return False


def looks_like_substantial_answer(text: str) -> bool:
    """True when streamed/checkpoint text is already a user-facing analysis body."""
    t = (text or "").strip()
    if not t:
        return False
    if _has_synthesis_headings(t) and not looks_truncated(t):
        return True
    if looks_truncated(t):
        return False
    table_pipes = t.count("|")
    sectioned = bool(re.search(r"(?:^|\n)\s*[A-D][\.、]\s+\S{2,}", t))
    headed = bool(re.search(r"(?:^|\n)#{2,3}\s+\S+", t))
    cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
    based = bool(
        re.search(r"\bBased\s*on\s+the\s+(?:database|query|evidence|contract)", t, re.I)
    )
    # Structured analysis can be shorter than a prose essay.
    if sectioned and (table_pipes >= 6 or cjk >= 40) and len(t) >= 100:
        return True
    if len(t) < 200:
        return False
    if table_pipes >= 8:
        return True
    if sectioned and len(t) > 280:
        return True
    if headed and len(t) > 280:
        return True
    if cjk >= 120 and len(t) > 400:
        return True
    if based and len(t) > 280:
        return True
    return False


def messages_for_current_turn(messages: list[Any]) -> list[Any]:
    """Slice checkpoint messages to the latest user turn only."""
    human_idxs = [
        i
        for i, m in enumerate(messages)
        if str(getattr(m, "type", None) or getattr(m, "role", "")).lower()
        in ("human", "user")
    ]
    if not human_idxs:
        return list(messages)
    return list(messages[human_idxs[-1] :])


def needs_synthesis_wrapup(prior: str, *, query_count: int = 0, min_chars: int = 400) -> bool:
    """True when Vertica/SQL evidence exists but the last assistant text is not a synthesis."""
    if query_count <= 0:
        return False
    text = (prior or "").strip()
    if not text:
        return True
    if _has_synthesis_headings(text):
        return False
    lower = text.lower()
    if re.search(r"^##\s+(?:summary|conclusion)\b", text, re.I | re.M):
        return False
    planning_prefixes = (
        "let me ",
        "now let me ",
        "now i ",
        "i'll ",
        "i will ",
        "the dwd ",
        "the dws ",
    )
    if any(lower.startswith(p) for p in planning_prefixes):
        return True
    if re.search(r"\blet me\b", text, re.I) and query_count >= 3:
        return True
    if (
        re.search(r"Based\s*on\s+the\s+(?:database|query|evidence|contract)", text, re.I)
        and not _has_synthesis_headings(text)
        and (re.search(r"\blet me\b", text, re.I) or query_count >= 5)
    ):
        return True
    if "###" in text and not _has_synthesis_headings(text):
        return True
    if query_count >= 8:
        return True
    return len(text) < min_chars


def needs_final_answer_wrapup(
    prior: str,
    *,
    query_count: int = 0,
    require_synthesis: bool = False,
    research_tool_count: int = 0,
    min_research_without_sql: int = 8,
    streamed_text: str = "",
) -> bool:
    """True when the run should get a user-facing final answer via wrap-up."""
    combined = (streamed_text or prior or "").strip()
    # Already have a complete substantial answer in the stream or checkpoint.
    if looks_like_substantial_answer(combined) and not looks_truncated(combined):
        return False
    text = (prior or "").strip()
    if _has_synthesis_headings(text) and not looks_truncated(text):
        return False
    # Truncated synthesis still needs a completion pass.
    if looks_truncated(combined) and (
        query_count > 0 or research_tool_count > 0 or len(combined) > 400
    ):
        return True
    if needs_synthesis_wrapup(text, query_count=query_count):
        return True
    if require_synthesis and (text or research_tool_count > 0 or query_count > 0):
        return True
    if (
        query_count <= 0
        and research_tool_count >= min_research_without_sql
        and text
    ):
        return True
    return False


def missing_answer_in_stream(streamed: str, checkpoint: str) -> str:
    """Return checkpoint answer text that still needs to be streamed, or ""."""
    streamed_text = (streamed or "").strip()
    ckpt = (checkpoint or "").strip()
    if not ckpt:
        return ""
    if streamed_text == ckpt:
        return ""
    if streamed_text and ckpt in streamed_text:
        return ""
    if streamed_text and streamed_text in ckpt:
        if ckpt.startswith(streamed_text):
            return ckpt[len(streamed_text) :]
        return ckpt
    # Prefer the more complete of streamed vs checkpoint when both look like answers.
    if looks_like_substantial_answer(streamed_text) and not looks_truncated(streamed_text):
        if looks_truncated(ckpt) or len(streamed_text) >= len(ckpt):
            return ""
    if _has_synthesis_headings(ckpt) and not _has_synthesis_headings(streamed_text):
        return ckpt
    if not streamed_text:
        return ckpt
    if len(ckpt) > len(streamed_text) + 200:
        return ckpt
    return ""


def _message_text(content: Any, *, strip: bool = True) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip() if strip else content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        text = "".join(parts)
        return text.strip() if strip else text
    text = str(content)
    return text.strip() if strip else text


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

    # Only the latest user turn — avoid leaking prior-question answers into wrap-up.
    turn_messages = messages_for_current_turn(list(raw_messages))
    context = _build_wrapup_context(turn_messages)
    thread_id = str(config.get("configurable", {}).get("thread_id") or "default")
    run_segment = int(config.get("configurable", {}).get("run_segment") or 1)
    evidence_text = get_evidence_snapshot(thread_id, run_segment).as_text()
    if evidence_text:
        context = f"{context}\n\n{evidence_text}"
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
            text = _message_text(getattr(chunk, "content", chunk), strip=False)
            if text:
                yield text
    except Exception:
        logger.exception("wrap-up model call failed")
        yield (
            "\n\n---\n**Run paused** (tool-step limit). "
            "Partial work is saved in this thread — click **Continue** to keep going, "
            "or ask a narrower follow-up."
        )


async def stream_completeness_finalization(
    model: Any,
    agent: Any,
    config: dict[str, Any],
    report: Any,
    constraints: Any,
    draft_answer: str,
    *,
    harness_cfg: HarnessConfig | None = None,
) -> AsyncIterator[str]:
    """One bounded finalization pass when a substantial answer misses generic constraints."""
    from app.agent.harness.completeness import build_finalization_human

    cfg = harness_cfg or load_harness_config(
        extended_run=bool(config.get("configurable", {}).get("extended_run"))
    )
    try:
        state = await agent.aget_state(config)
        values = getattr(state, "values", None) or {}
        raw_messages = values.get("messages") or []
    except Exception:
        logger.debug("completeness finalization could not load state", exc_info=True)
        raw_messages = []

    turn_messages = messages_for_current_turn(list(raw_messages))
    context = _build_wrapup_context(turn_messages)
    thread_id = str(config.get("configurable", {}).get("thread_id") or "default")
    run_segment = int(config.get("configurable", {}).get("run_segment") or 1)
    evidence_text = get_evidence_snapshot(thread_id, run_segment).as_text()
    if evidence_text:
        context = f"{context}\n\n{evidence_text}"

    human = build_finalization_human(
        report, constraints, draft_answer=draft_answer
    )
    human = f"{human}\n\n### Transcript\n{context}"

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
            text = _message_text(getattr(chunk, "content", chunk), strip=False)
            if text:
                yield text
    except Exception:
        logger.exception("completeness finalization model call failed")


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


def last_ai_text(messages: list[Any], *, current_turn_only: bool = True) -> str:
    """Last non-empty assistant text (skips trailing empty AI turns after tool calls)."""
    scoped = messages_for_current_turn(messages) if current_turn_only else messages
    for msg in reversed(scoped):
        role = getattr(msg, "type", None) or getattr(msg, "role", "")
        if str(role).lower() not in ("ai", "assistant"):
            continue
        text = _message_text(getattr(msg, "content", ""))
        if text:
            return text
    return ""


def count_research_tool_calls(messages: list[Any], *, current_turn_only: bool = True) -> int:
    """Count filesystem / KB research tool invocations in checkpoint messages."""
    scoped = messages_for_current_turn(messages) if current_turn_only else messages
    count = 0

    def _maybe_add(tool: str) -> None:
        nonlocal count
        name = (tool or "").lower()
        if name in _RESEARCH_TOOLS:
            count += 1

    for msg in scoped:
        for tc in getattr(msg, "tool_calls", None) or []:
            if isinstance(tc, dict):
                _maybe_add(str(tc.get("name") or ""))
            else:
                _maybe_add(str(getattr(tc, "name", "")))
    return count


def count_sql_evidence_in_messages(messages: list[Any], *, current_turn_only: bool = True) -> int:
    """Count distinct SQL queries invoked in checkpoint messages (cross-turn evidence)."""
    scoped = messages_for_current_turn(messages) if current_turn_only else messages
    seen: set[str] = set()

    def _maybe_add(tool: str, raw_args: Any) -> None:
        name = (tool or "").lower()
        if not (
            name in _VERTICA_QUERY_TOOLS
            or "run_query" in name
            or name.startswith("execute_query")
        ):
            return
        args = raw_args
        if isinstance(args, str):
            try:
                import json

                args = json.loads(args)
            except Exception:
                args = {}
        if not isinstance(args, dict):
            return
        for key in ("query", "sql"):
            sql = args.get(key)
            if isinstance(sql, str) and sql.strip():
                seen.add(sql.strip())

    for msg in scoped:
        for tc in getattr(msg, "tool_calls", None) or []:
            if isinstance(tc, dict):
                _maybe_add(str(tc.get("name") or ""), tc.get("args"))
            else:
                _maybe_add(str(getattr(tc, "name", "")), getattr(tc, "args", None))
    return len(seen)


async def check_completeness_enhanced(
    user_message: str,
    draft_answer: str,
    thread_id: str,
    run_segment: int,
) -> object | None:
    """Use agent-completeness when installed; otherwise return None for regex fallback."""
    cfg = load_harness_config()
    if not cfg.enable_completeness_enhanced:
        return None
    try:
        from agent_completeness import CompletenessEvaluator
        from agent_completeness.integrations.data_agent import DataAgentCompletenessAdapter
    except ImportError:
        return None
    adapter = DataAgentCompletenessAdapter(evaluator=CompletenessEvaluator())
    return await adapter.evaluate_from_segment(
        thread_id=thread_id,
        run_segment=run_segment,
        draft_answer=draft_answer,
        user_message=user_message,
    )


async def check_completeness_enhanced(
    user_message: str,
    draft_answer: str,
    thread_id: str,
    run_segment: int,
) -> object | None:
    """Use agent-completeness when installed; otherwise return None for regex fallback."""
    cfg = load_harness_config()
    if not cfg.enable_completeness_enhanced:
        return None
    try:
        from agent_completeness import CompletenessEvaluator
        from agent_completeness.integrations.data_agent import DataAgentCompletenessAdapter
    except ImportError:
        return None
    adapter = DataAgentCompletenessAdapter(evaluator=CompletenessEvaluator())
    return await adapter.evaluate_from_segment(
        thread_id=thread_id,
        run_segment=run_segment,
        draft_answer=draft_answer,
        user_message=user_message,
    )
