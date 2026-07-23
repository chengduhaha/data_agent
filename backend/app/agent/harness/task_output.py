"""Human-readable summaries for DeepAgents `task` tool / Command payloads."""

from __future__ import annotations

import ast
import re
from typing import Any


def _decode_repr_string(raw: str) -> str:
    try:
        return ast.literal_eval(f'"{raw}"') if '"' in raw else ast.literal_eval(f"'{raw}'")
    except Exception:
        return raw.replace("\\n", "\n").replace("\\t", "\t")


def extract_command_messages_text(text: str, *, limit: int = 4000) -> str:
    """Pull readable text from a Command(...) repr or spill preview."""
    if not text:
        return ""
    if "--- preview (task) ---" in text:
        text = text.split("--- preview (task) ---", 1)[1]
    if "--- preview truncated" in text:
        text = text.split("…[preview truncated]", 1)[0]

    parts: list[str] = []
    for pattern in (
        r"ToolMessage\(content=(?:'([^']*(?:\\.[^']*)*)'|\"([^\"]*(?:\\.[^\"]*)*)\")",
        r"AIMessage\(content=(?:'([^']*(?:\\.[^']*)*)'|\"([^\"]*(?:\\.[^\"]*)*)\")",
    ):
        for match in re.finditer(pattern, text, flags=re.DOTALL):
            raw = match.group(1) or match.group(2) or ""
            if raw:
                parts.append(_decode_repr_string(raw))

    if parts:
        joined = "\n\n".join(parts).strip()
        if joined:
            return joined[:limit]

    if text.strip().startswith("Command("):
        return "Subagent completed (large result saved to workspace)."
    return text[:limit]


def humanize_task_tool_output(output: Any, *, limit: int = 4000) -> str:
    """Format task tool output for SSE / UI previews."""
    if output is None:
        return ""
    if hasattr(output, "content"):
        text = output.content
    else:
        text = output
    if not isinstance(text, str):
        text = str(text)
    if "Command(update=" in text or "--- preview (task) ---" in text:
        return extract_command_messages_text(text, limit=limit)
    return text[:limit]


__all__ = ["extract_command_messages_text", "humanize_task_tool_output"]
