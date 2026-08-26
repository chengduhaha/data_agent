# ADR-001: Selective Budget Governance

## Status
Accepted

## Context
Dynamic MCP tools and subagents make a global tool-call cap too blunt. Some tools
must be bounded (SQL); others (read_file, HITL writes) must stay ungated.

## Decision
`BudgetRegistry` is the only gate. A tool is governed iff it has a declared budget.
Undeclared tools are fully allowed and uncounted (C2).

## Consequences
### Positive
- Zero false blocks on ungated tools
- Skill manifests declare intent next to the tool list

### Negative
- Coverage is only as complete as the declarations
- MCP tools need `evidence_tools` if they should still feed wrap-up

## Alternatives Considered
- Govern every tool: rejected (breaks HITL and exploratory reads)
- Allow-list of free tools: rejected (high maintenance)

## References
- `backend/app/agent/harness/budget_registry.py`
- `backend/app/agent/harness/tool_budget.py`
