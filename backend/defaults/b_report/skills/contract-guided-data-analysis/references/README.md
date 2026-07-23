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
| `special-logic-check.md` | `/knowledge/org/source/ref/{domain}/special_logic.txt` procedure |
| `sql-planning.md` | SQL compile plan and time defaults |
| `wkb-retrieval.md` | Storage-layer / WKB short-list |
| `vertica-query.md` | Vertica MCP execution-only rules |
| `analysis-output.md` | `target/analysis/` artifact contract |

## Path conventions

- Prefer `/knowledge/org/source/contracts/{domain}/**` (domain-knowledge, metric-index, eval/golden_cases).
- Prefer `/knowledge/org/source/ref/{domain}/special_logic.txt` for filter exceptions.
- Prefer `/knowledge/org/target/knowledgebase/{domain}/*.md` and `/knowledge/org/target/storage/wkb/` for table detail.
- **Never** read `/knowledge/org/source/contracts/**/golden-questions.md`.
- **Never** read `/knowledge/org/source/contracts/b-report-us/tables/**` or `/knowledge/org/source/contracts/pos/tables/**`.
