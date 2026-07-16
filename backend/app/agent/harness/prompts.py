"""Harness system-prompt additions (platform-wide, not contract-specific)."""

HARNESS_SYSTEM_SUFFIX = """
## Execution harness

- Prefer `search_knowledge`, `grep`, or `glob` before `read_file` on `/knowledge/org/` or large files.
- Do not paginate the same file with repeated `read_file` offset loops.
- Never read `conversation_history/` or `large_tool_results/`.
- For contract-guided data analysis, use `wkb_query` instead of shell or JSON catalog pagination.
- The run may pause after a tool-step budget; a wrap-up summary is added when possible. Click Continue or send a narrower follow-up.
- For unrelated new questions in the same chat, prefer starting a new thread.
""".strip()
