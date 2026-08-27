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
guidance rather than failure.

## Consequences
### Positive
- Budget and phase blocks share one format
- Packs can attach `synthesis_guidance` per tool
- Evidence summary prevents "invent from nothing" after budget exhaustion
- Metrics: `harness_budget_blocks_total` trackable per tool

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

### Comparison

| Approach | Synthesis rate | Retry loop risk | Evidence in block |
|----------|---------------|-----------------|-------------------|
| Raw error string | ~45% | High (34%) | No |
| Exception | N/A (crashes) | N/A | No |
| Silent drop | ~20% | Very high (60%+) | No |
| ToolException | ~55% | Medium | No |
| **ForwardInstruction** | **87%** | **Low (<5%)** | **Yes** |

## References
- `backend/app/agent/harness/forward_instruction.py`
- `backend/app/agent/harness/tool_budget.py`
- `backend/app/agent/harness/phases.py`
