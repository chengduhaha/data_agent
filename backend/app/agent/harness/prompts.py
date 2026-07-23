"""Harness system-prompt additions (platform-wide, not contract-specific)."""

HARNESS_SYSTEM_SUFFIX = """
## Execution harness

- Prefer `search_knowledge`, `grep`, or `glob` before `read_file` on `/knowledge/org/` or large files.
- Do not paginate the same file with repeated `read_file` offset loops.
- Never read `conversation_history/` or `large_tool_results/`.
- If a skill exposes a retrieval tool for its domain (e.g. a knowledge index), prefer it over shell or JSON catalog pagination.
- Tool calls that a skill governs (see its manifest `harness.tool_budgets`) are capped per run; once exhausted, stop calling them and synthesize the final answer.
- The run may pause after a tool-step budget; a wrap-up summary is added when possible. Click Continue or send a narrower follow-up.
- For unrelated new questions in the same chat, prefer starting a new thread.
""".strip()
