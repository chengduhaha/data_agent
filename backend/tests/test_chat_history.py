"""Tests for folding LangGraph checkpoint messages into chat UI turns."""

from __future__ import annotations

from types import SimpleNamespace

from app.store.chat_history import fold_checkpoint_messages


def test_folds_tool_only_ai_turns_into_final_answer() -> None:
    messages = [
        SimpleNamespace(type="human", content="What is NGM?", id="u1", tool_calls=[]),
        SimpleNamespace(
            type="ai",
            content="",
            id="a1",
            tool_calls=[{"id": "tc1", "name": "read_file", "args": {"path": "/x"}}],
        ),
        SimpleNamespace(type="tool", content="file contents", tool_call_id="tc1", id="t1"),
        SimpleNamespace(
            type="ai",
            content="",
            id="a2",
            tool_calls=[{"id": "tc2", "name": "run_query_safely", "args": {"query": "SELECT 1"}}],
        ),
        SimpleNamespace(type="tool", content='[{"n":1}]', tool_call_id="tc2", id="t2"),
        SimpleNamespace(
            type="ai",
            content="### Summary\nNGM dropped.",
            id="a3",
            tool_calls=[],
        ),
    ]

    folded = fold_checkpoint_messages(messages)
    assert len(folded) == 2
    assert folded[0]["role"] == "user"
    assert folded[0]["content"] == "What is NGM?"
    assert folded[1]["role"] == "assistant"
    assert "NGM dropped" in folded[1]["content"]
    tools = folded[1]["tools"] or []
    assert len(tools) == 2
    assert tools[0]["tool"] == "read_file"
    assert tools[0]["output"] == "file contents"
    assert tools[1]["tool"] == "run_query_safely"


def test_skips_empty_assistant_without_tools() -> None:
    messages = [
        SimpleNamespace(type="human", content="hi", id="u1", tool_calls=[]),
        SimpleNamespace(type="ai", content="", id="a1", tool_calls=[]),
        SimpleNamespace(type="ai", content="Hello!", id="a2", tool_calls=[]),
    ]
    folded = fold_checkpoint_messages(messages)
    assert len(folded) == 2
    assert folded[1]["content"] == "Hello!"
    assert folded[1].get("tools") is None


def test_extracts_text_from_content_blocks() -> None:
    messages = [
        SimpleNamespace(
            type="ai",
            content=[{"type": "text", "text": "Block answer"}],
            id="a1",
            tool_calls=[],
        )
    ]
    folded = fold_checkpoint_messages(messages)
    assert len(folded) == 1
    assert folded[0]["content"] == "Block answer"
