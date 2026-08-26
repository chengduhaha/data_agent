# ADR-003: Forward Instruction Pattern

## Status
Accepted

## Context
Blocking a tool with a raw error string causes models to retry a different tool
instead of synthesizing. Wrap-up already had evidence; block messages did not.

## Decision
All harness blocks emit a `ForwardInstruction`: reason, expected action, and the
current segment evidence summary. The tone is "what to do next", not "error".

## Consequences
### Positive
- Budget and phase blocks share one format
- Packs can attach `synthesis_guidance`

### Negative
- Slightly longer tool messages
- Tests must accept the structured text (legacy "Blocked:" prefix retained)

## Alternatives Considered
- Raise an exception: rejected (breaks the agent loop)
- Silent drop of the tool call: rejected (model retries)

## References
- `backend/app/agent/harness/forward_instruction.py`
