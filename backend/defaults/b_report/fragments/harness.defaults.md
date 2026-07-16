## Agent harness (all skills)

Platform execution rules — apply to every conversation unless a skill overrides.

### Knowledge discovery

- Prefer `search_knowledge`, `grep`, or `glob` before `read_file` on large trees under `/knowledge/org/` or `/workspace/`.
- Single `read_file` call: use `limit` ≤ 200; do not paginate with repeated `offset` loops on the same file.
- Never read paths under `conversation_history/` or `large_tool_results/` (compressed artifacts).

### Efficiency

- Do not re-read the same file path in one run segment unless the user asks.
- Do not write `analyze_*.py` or other scratch scripts unless the user explicitly requests code execution.
- Limit `task` subagent to at most one call per run segment.

### Run segments

- The agent may pause after ~100 tool steps and ask you to **Continue** for another segment.
- When Continue appears, synthesize a final answer if you already have enough evidence; do not restart local research from scratch.

### Timeouts

- Shell and MCP tools may time out at ~60s; split work or simplify queries instead of retrying the same long call.
