"""Tests for task / Command output humanization."""

from __future__ import annotations

from app.agent.harness.task_output import extract_command_messages_text, humanize_task_tool_output


def test_extract_command_messages_text_from_spill_preview() -> None:
    raw = (
        "Tool result too large (29607 chars). Full output saved at /workspace/x.txt.\n\n"
        "--- preview (task) ---\n"
        "Command(update={'files': {}, 'messages': [ToolMessage(content='\\n\\n## Domain\\n\\nNGM formula', "
        "tool_call_id='1')]})"
    )
    text = extract_command_messages_text(raw)
    assert "## Domain" in text
    assert "NGM formula" in text
    assert "Command(update=" not in text


def test_humanize_task_tool_output_from_toolmessage() -> None:
    class Msg:
        content = (
            "--- preview (task) ---\n"
            "Command(update={'messages': [ToolMessage(content='Subagent finished analysis.', tool_call_id='1')]})"
        )

    text = humanize_task_tool_output(Msg(), limit=500)
    assert "Subagent finished analysis." in text
