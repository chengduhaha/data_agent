"""Tests for ask_user clarification tool and interrupt payloads."""

from __future__ import annotations

import asyncio

import pytest

from app.agent.harness import clarification as clarification_mod
from app.agent.harness.clarification import (
    AskUserInput,
    ClarificationQuestion,
    extract_clarification_payload,
    is_clarification_interrupt,
    make_ask_user_tool,
)


def test_extract_clarification_payload_nested() -> None:
    payload = {
        "type": "clarification",
        "reason": "Time range is required.",
        "questions": [{"question": "Which period?", "options": []}],
    }
    assert extract_clarification_payload([{"value": payload}]) == payload
    assert is_clarification_interrupt(payload) is True


def test_ask_user_tool_interrupts_and_resumes() -> None:
    tool = make_ask_user_tool()
    captured: dict[str, object] = {}

    def _interrupt(value):  # type: ignore[no-untyped-def]
        captured["value"] = value
        return {"answers": {"Which period should I analyze?": "FY26 Q1"}}

    original = clarification_mod.interrupt
    clarification_mod.interrupt = _interrupt
    try:
        result = asyncio.run(
            tool.ainvoke(
                {
                    "questions": [
                        {
                            "question": "Which period should I analyze?",
                            "header": "Time range",
                            "options": [
                                {"label": "FY26 Q1", "description": "Jan–Mar 2026"},
                                {"label": "Last month", "description": "Rolling month"},
                            ],
                        }
                    ],
                    "reason": "The question has no reporting period.",
                }
            )
        )
    finally:
        clarification_mod.interrupt = original

    assert captured["value"]["type"] == "clarification"
    assert "FY26 Q1" in result


def test_ask_user_registered_in_builtin_catalog() -> None:
    from app.agent.builtin_tools import BUILTIN_TOOL_CATALOG, get_builtin_tools

    names = {t["name"] for t in BUILTIN_TOOL_CATALOG}
    assert "ask_user" in names

    class _Backend:
        pass

    tools = get_builtin_tools(
        {"web_fetch": False, "web_search": False, "ask_user": True},
        backend=_Backend(),
        include_harness_tools=True,
    )
    assert any(getattr(t, "name", None) == "ask_user" for t in tools)


def test_ask_user_input_schema_accepts_free_text_question() -> None:
    parsed = AskUserInput(
        questions=[
            ClarificationQuestion(
                question="What does PMID refer to in this request?",
                header="Entity",
                options=[],
            )
        ]
    )
    assert parsed.questions[0].allow_free_text is True
