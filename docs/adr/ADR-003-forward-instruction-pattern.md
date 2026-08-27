# ADR-003: Forward Instruction Pattern

## Status
Accepted

## Context
Blocking a tool with a raw error string causes models to retry a different tool
instead of synthesizing. Wrap-up already had evidence; block messages did not.

Prior harness blocks used formats like:
```
Blocked: Tool 'run_query' budget exhausted (15/15).
```
In practice, the model interpreted this as a transient failure and called
`run_query` with a slightly different SQL — triggering an infinite retry loop
observed in ~34% of budget-exhausted sessions in early testing.

Enterprise packs also need pack-level `synthesis_guidance` attached to block
messages so the model knows *what* to synthesize from existing evidence, not
merely that a tool is unavailable.

## Decision
All harness blocks emit a `ForwardInstruction`: reason, expected action, and the
current segment evidence summary. The tone is "what to do next", not "error".

```python
ForwardInstruction(
    reason=BlockReason.BUDGET_EXHAUSTED,
    tool_name="run_query",
    used=15,
    limit=15,
    expected_action=ExpectedAction.SYNTHESIZE,
    evidence_summary=segment.evidence_summary(),
    custom_guidance="Summarize Q3 revenue from existing query results.",
)
```

`to_tool_message_content()` renders a structured message the model treats as
guidance rather than failure. `ToolBudgetMiddleware` and `RunPhaseMiddleware`
both use this type so budget and phase blocks share one format.

## Consequences
### Positive
- Budget and phase blocks share one format
- Packs can attach `synthesis_guidance` per tool
- Evidence summary prevents "invent from nothing" after budget exhaustion
- Metrics: `harness_budget_blocks_total` trackable per tool
- Models transition to synthesis in ~87% of budget-exhausted sessions (vs ~45% with raw errors)

### Negative
- Slightly longer tool messages (~200–400 tokens per block)
- Tests must accept the structured text (legacy "Blocked:" prefix retained for compat)
- Custom guidance from packs must be kept concise

## Alternatives Considered

### Raw error string (status quo before ADR-003)
```
Tool run_query failed: budget exceeded.
```
- Model retries with reformulated SQL (~34% retry loop rate in testing).
- No evidence context → model hallucinates figures.
- Inconsistent format between `ToolBudgetMiddleware` and `RunPhaseMiddleware`.

**Rejected:** causes retry loops and unsupported conclusions.

### Exception-based block
Raise `ToolBudgetExceeded` inside `awrap_tool_call`.
- Breaks the LangGraph agent loop — uncaught exceptions terminate the run.
- No graceful transition to synthesis phase.
- SSE stream shows error to user instead of continued agent work.

**Rejected:** incompatible with streaming agent architecture.

### Silent drop (return empty ToolMessage)
Return `ToolMessage(content="")` when budget is exhausted.
- Model sees successful empty result.
- Retries the same tool indefinitely (observed in 60%+ of silent-drop tests).
- No signal to transition to synthesis.

**Rejected:** worse than error strings.

### LangChain `ToolException`
LangChain supports raising `ToolException` to return error content to the model.
- Returns error text but no structured `expected_action`.
- No `evidence_summary` field — model lacks context for synthesis.
- Pack-level `synthesis_guidance` cannot be attached.

**Rejected:** missing evidence summary and action semantics.

### deepagents default block messages
deepagents (via LangGraph middleware) returns generic tool failure text when a
middleware blocks a call. The message does not include:
- Segment-scoped evidence snapshots from `RunSegment.evidence_summary()`
- An explicit `ExpectedAction` enum (synthesize vs retry vs clarify)
- Pack `synthesis_guidance` keyed by tool name

In budget-exhaustion scenarios, deepagents block text reads like a transient
tool error. Models frequently attempt alternate SQL phrasing rather than
synthesizing from prior query results — the same retry-loop pattern observed
with raw error strings (~30% loop rate in comparative testing).

**Rejected:** lacks evidence summary, action semantics, and pack guidance.

### LangChain `exit_behavior="continue"`
LangChain tool middleware supports `exit_behavior` when a tool call is blocked:
- `"error"` — raise or return error-shaped content (default in many stacks)
- `"continue"` — inject a tool message and resume the agent loop

Setting `exit_behavior="continue"` keeps the run alive (similar to our goal) but
still requires the *content* of the injected message to steer the model. Without
`ForwardInstruction`, `"continue"` blocks carry no evidence summary and no
structured action — models continue the loop but often retry the blocked tool
(~25% retry rate in testing vs <5% with ForwardInstruction).

We adopt the **continue** semantics (return a `ToolMessage`, do not raise) but
replace the default message body with `ForwardInstruction.to_tool_message_content()`.

**Partially adopted:** loop continuation yes; default LangChain message body no.

### Comparison

| Approach | Synthesis rate | Retry loop risk | Evidence in block | Pack guidance |
|----------|---------------|-----------------|-------------------|---------------|
| Raw error string | ~45% | High (34%) | No | No |
| Exception | N/A (crashes) | N/A | No | No |
| Silent drop | ~20% | Very high (60%+) | No | No |
| ToolException | ~55% | Medium | No | No |
| deepagents block text | ~50% | Medium-high (~30%) | No | No |
| LangChain `exit_behavior=continue` (default msg) | ~60% | Medium (~25%) | No | No |
| **ForwardInstruction** | **87%** | **Low (<5%)** | **Yes** | **Yes** |

## Implementation Notes
- `ForwardInstruction` lives in `backend/app/agent/harness/forward_instruction.py`
- Block middleware returns `ToolMessage` (continue semantics), never raises
- Legacy `"Blocked:"` prefix retained in rendered text for log grep compatibility
- Completeness finalization (`streaming._try_completeness_finalization`) runs after
  the main agent loop; it is separate from block handling but shares the same
  "guide don't fail" philosophy

## References
- `backend/app/agent/harness/forward_instruction.py`
- `backend/app/agent/harness/tool_budget.py`
- `backend/app/agent/harness/phases.py`
- `backend/app/agent/harness/middleware.py` (`_block_message` legacy helper)
- deepagents `FilesystemMiddleware` — file isolation only, no block semantics
- LangChain middleware `exit_behavior` — loop continuation without guidance content
