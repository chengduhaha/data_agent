# ADR-002: Run Segment Isolation

## Status
Accepted

## Context
LangChain `run_limit` / `thread_limit` are process-wide or thread-wide. Enterprise
agent turns need isolation of budgets, evidence, and caches without resetting the
whole thread checkpoint.

A single user thread may contain multiple follow-up questions. Each question should
reset tool budgets, clear evidence snapshots, and prevent cache pollution from
prior turns — while preserving conversation history in the checkpointer.

## Decision
State is keyed by `(thread_id, segment_id)`. `RunSegment` is the public object;
`SegmentManager` owns lifecycle, eviction (max 10 per thread), and hooks.

This is intentionally finer-grained than LangChain thread limits: a user follow-up
increments `run_segment` while keeping checkpoint history.

`RunSegment.to_dw_context()` and `RunSegment.to_evidence_set()` provide stable
integration surfaces for `dw-agent-governance` and `agent-completeness`.

## Consequences
### Positive
- Budgets reset per question
- Evidence snapshots cannot leak across turns
- External libraries can import one type
- `SegmentManager.evict_old_segments()` prevents in-memory leaks

### Negative
- In-memory map must be evicted (otherwise leak)
- Segment id still lives in thread meta, not the checkpointer
- Middleware must read segment from `contextvars` harness context

## Alternatives Considered

### LangChain `run_limit` / `thread_limit`
LangChain middleware can cap total tool calls per run or thread. However:
- A "run" in LangGraph spans the entire agent loop for one user message, but
  budgets need to reset on *follow-up* questions within the same thread.
- `thread_limit` is too coarse — it accumulates across all turns in a session.
- No built-in evidence isolation or spill-file tracking per turn.

**Rejected:** granularity too coarse for per-question budget reset.

### deepagents `FilesystemMiddleware`
deepagents provides filesystem-scoped isolation for agent file operations.
- Good for preventing cross-user file access.
- Does **not** track tool call counts, evidence items, or DW governance state.
- No integration point for `ForwardInstruction` or completeness checks.

**Rejected:** file-level isolation ≠ budget/evidence isolation.

### Global counter (single dict per process)
A module-level `tool_call_counts: dict[str, int]` shared across all users.
- Simple to implement.
- **Cross-talk:** user A's query budget consumes user B's allowance on the same worker.
- Cannot key by `(thread_id, segment_id)` without reinventing `SegmentManager`.

**Rejected:** multi-tenant safety failure.

### SQLite-persisted segments
Store `RunSegment` state in SQLite alongside the checkpointer.
- Survives process restarts.
- Adds schema migration burden and write latency on every tool call.
- v1 checkpointer already stores full message history; segment state is ephemeral
  by design (budgets reset each question).

**Deferred:** v1 uses in-memory `SegmentManager` with LRU eviction.

### Comparison

| Approach | Per-question reset | Multi-tenant safe | Evidence isolation |
|----------|-------------------|-------------------|-------------------|
| LangChain run_limit | Partial | Yes | No |
| FilesystemMiddleware | No | Yes (files) | No |
| Global counter | No | **No** | No |
| **RunSegment (chosen)** | **Yes** | **Yes** | **Yes** |
| SQLite segments | Yes | Yes | Yes (persistent) |

## References
- `backend/app/agent/harness/segment.py`
- `backend/app/agent/harness/segment_manager.py`
- `backend/app/agent/harness/context.py`
