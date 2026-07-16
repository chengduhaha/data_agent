# Contract-guided data analysis — local references

All progressive-load policies for this skill live **in this folder**. Load files listed for the current stage in [`_manifest.yaml`](_manifest.yaml). Do not load policies from outside this skill package.

## Local policy files

| File | Role |
|------|------|
| `question-shape.md` | Intent / query_spec / temporal obligation |
| `metric-table-routing.md` | Metric-to-table routing and anti-duplication |
| `entity-resolution.md` | Phase-1 entity label probes |
| `dimension-scope.md` | Dimension slice scope |
| `fiscal-calendar.md` | Fiscal / calendar time assembly |
| `output-contract.md` | Fixed answer shape and ambiguity handling |
| `confidence-provenance.md` | Source tier / confidence |
| `typo-tolerance.md` | Label typo handling |
| `local-research-first.md` | Local-first gate; forbidden MCP discovery |
| `scope-guardrail.md` | Non-bypassable contract scope |
| `domain-routing.md` | Domain resolution and KB path map |
| `golden-cases-match.md` | Optional `eval/golden_cases.md` matching |
| `special-logic-check.md` | `/workspace/source/ref/{domain}/special_logic.txt` procedure |
| `sql-planning.md` | SQL compile plan and time defaults |
| `wkb-retrieval.md` | Storage-layer / WKB short-list |
| `vertica-query.md` | Vertica MCP execution-only rules |
| `analysis-output.md` | `target/analysis/` artifact contract |

## Path conventions

- Prefer `/workspace/source/contracts/{domain}/**` (domain-knowledge, metric-index, eval/golden_cases).
- Prefer `/workspace/source/ref/{domain}/special_logic.txt` for filter exceptions.
- Prefer `/workspace/target/knowledgebase/{domain}/*.md` and `/workspace/target/storage/wkb/` for table detail.
- **Never** read `/workspace/source/contracts/**/golden-questions.md`.
- **Never** read `/workspace/source/contracts/b-report-us/tables/**` or `/workspace/source/contracts/pos/tables/**`.
