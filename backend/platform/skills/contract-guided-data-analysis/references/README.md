# Contract-guided data analysis — local references

All progressive-load policies for this skill live **in this folder** — including clarification policy ([`analysis-clarification.md`](analysis-clarification.md)) and Vertica/MCP execution policy ([`vertica-rules.md`](vertica-rules.md)). This skill has **no Cursor rule dependency**: it does not read or require `.cursor/rules/*.mdc` for its own routing/clarification/execution policy. Load files listed for the current stage in [`_manifest.yaml`](_manifest.yaml). Do not load policies from outside this skill package.

## Local policy files

| File | Role |
|------|------|
| `question-shape.md` | Intent / query_spec / temporal obligation |
| `metric-table-routing.md` | Metric-to-table routing and anti-duplication |
| `entity-resolution.md` | Phase-1 entity label probes |
| `dimension-scope.md` | Dimension slice scope |
| `fiscal-calendar.md` | Fiscal / calendar time assembly |
| `analysis-clarification.md` | Ask only when question/data ambiguity blocks routing; else do not ask |
| `output-contract.md` | Fixed answer shape and ambiguity handling |
| `confidence-provenance.md` | Source tier / confidence |
| `typo-tolerance.md` | Label typo handling |
| `local-research-first.md` | Local-first gate; forbidden MCP discovery |
| `scope-guardrail.md` | Non-bypassable contract scope |
| `domain-routing.md` | Domain resolution and KB path map |
| `golden-cases-match.md` | `eval/golden_cases.md` matching — **disabled by default**; only used when the user explicitly asks |
| `special-logic-check.md` | `knowledge/ref/{domain}/special_logic.txt` procedure |
| `sql-planning.md` | SQL compile plan and time defaults |
| `wkb-retrieval.md` | Storage-layer / WKB short-list |
| `vertica-query.md` | Vertica MCP execution-only rules |
| `vertica-rules.md` | Full Vertica MCP execution rules (allowed/forbidden tool usage) + clarification pointer + RDS mode pointer |
| `rds-report-sql.md` | Optional mode reference for `rds_report_generation` intent (RDS SQL / report generation) — intent checklist, rule-load order, deliverable shape; does not embed the RDS dialect/temp-table rule bodies |
| `analysis-output.md` | `{output_dir}/` artifact contract |
| `mcp-setup.md` | Vertica MCP server configuration |

## Path conventions

- Prefer `knowledge/contracts/{domain}/**` (domain-knowledge, metric-index). `eval/golden_cases.md` is disabled by default — only consult when the user explicitly asks.
- Prefer `knowledge/ref/{domain}/special_logic.txt` for filter exceptions.
- Prefer `knowledge/knowledgebase/{domain}/*.md` and `knowledge/storage/wkb/` for table detail.
- **Never** read `knowledge/contracts/**/golden-questions.md`.
- **Never** read `knowledge/contracts/b-report-us/tables/**` or `knowledge/contracts/pos/tables/**`.
