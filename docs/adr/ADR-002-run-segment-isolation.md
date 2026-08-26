# ADR-002: Run Segment Isolation

## Status
Accepted

## Context
LangChain `run_limit` / `thread_limit` are process-wide or thread-wide. Enterprise
agent turns need isolation of budgets, evidence, and caches without resetting the
whole thread checkpoint.

## Decision
State is keyed by `(thread_id, segment_id)`. `RunSegment` is the public object;
`SegmentManager` owns lifecycle, eviction (max 10 per thread), and hooks.

This is intentionally finer-grained than LangChain thread limits: a user follow-up
increments `run_segment` while keeping checkpoint history.

## Consequences
### Positive
- Budgets reset per question
- Evidence snapshots cannot leak across turns
- External libraries can import one type

### Negative
- In-memory map must be evicted (otherwise leak)
- Segment id still lives in thread meta, not the checkpointer

## Alternatives Considered
- One global counter: rejected (cross-talk between users)
- Persist segments in SQLite: deferred (v1 checkpointer already stores messages)

## References
- `backend/app/agent/harness/segment.py`
- `backend/app/agent/harness/segment_manager.py`
