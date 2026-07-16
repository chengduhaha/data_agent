---
name: contract-guided-data-analysis
description: |
  Contract-first business data analysis with local md/WKB research before Vertica evidence SQL.
  Use when: KPI lookup, ranking, trend, comparison, variance drivers, POS/B Report metrics, validate numbers, data anomaly.
  Routes via source/contracts domain-knowledge → metric-index → optional eval/golden_cases → source/ref special_logic → storage-layer (l1_catalog) → knowledgebase.
  Don't use when: ETL change requests, flow edits, DDL/DML, unrestricted warehouse exploration, email intake (use etl-email-change-intake).
---

# Contract-Guided Data Analysis

## Purpose

Answer business data questions using **local contracts + WKB index**, then **Vertica MCP** for aggregated evidence only. Not free-form exploration or email intake.

**Governance:** Research from local md first. Never read `golden-questions.md`. Never use Bitbucket or Vertica metadata for discovery. Never read `/knowledge/org/source/contracts/{domain}/tables/*.md`. See [`references/local-research-first.md`](references/local-research-first.md).

**Answers render in chat only** — do not write analysis files under `/workspace/target/analysis/`.

## Progressive loading

Policy lives in [`references/_manifest.yaml`](references/_manifest.yaml). Load only references listed for the current stage.

| Stage | Responsibility |
|-------|----------------|
| `read_question` | Intent, domain cue, `query_spec`, temporal obligation |
| `local_research` | Local-first gate; forbidden MCP discovery |
| `resolve_domain` | Contract paths for resolved domain |
| `golden_cases_match` | Optional `eval/golden_cases.md`; no data found fallbacks |
| `special_logic_check` | `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` |
| `plan_queries` | Metric/table routing, SQL plan, fiscal time |
| `retrieve_tables` | Storage-layer (`l1_catalog`) short-list → ≤3 knowledgebase table sections |
| `compile_sql` | Local column catalog only; gate before MCP |
| `execute_evidence` | Vertica `run_query_safely` aggregate-first |
| `synthesis` | Three-section answer or **no data found** |

## Workflow (router)

1. Classify intent + domain — [`references/question-shape.md`](references/question-shape.md)
2. **Local research gate** — no Bitbucket/Vertica until routing complete
3. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md` — entity/time disambiguation
4. `/knowledge/org/source/contracts/{domain}/metric-index.md` — metrics + `dimension_slice_routing`
5. Optional `/knowledge/org/source/contracts/{domain}/eval/golden_cases.md` — [`references/golden-cases-match.md`](references/golden-cases-match.md)
6. Special logic check — [`references/special-logic-check.md`](references/special-logic-check.md) → `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` (when present); always check `special_logic.txt` for logic tied to the resolved table(s)
7. Storage layer metadata search — [`references/wkb-retrieval.md`](references/wkb-retrieval.md) → use `wkb_query` before opening knowledgebase docs (no `l1_catalog` JSON pagination)
8. Knowledgebase table docs → `/knowledge/org/target/knowledgebase/{domain}/{stem}.md` where **`stem = FQN.split(".")[-1]`**. On 404, `ls` the knowledgebase folder and retry. **NEVER** read `/knowledge/org/source/contracts/{domain}/tables/*.md`
9. Compile SQL from local contracts; cannot compile → **no data found**
10. Entity Phase-1 (if labels) — bounded dim probe per [`references/entity-resolution.md`](references/entity-resolution.md)
11. Execute — [`references/vertica-query.md`](references/vertica-query.md); zero rows → **no data found**
12. Synthesize three-section chat answer — [`references/output-contract.md`](references/output-contract.md) and [`references/confidence-provenance.md`](references/confidence-provenance.md)

**Conditional:** [azkaban-parameter-jobs](../azkaban-parameter-jobs/SKILL.md) only when WKB/knowledgebase already names a `.flow` file.

## Source priority (summary)

1. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md`
2. `/knowledge/org/source/contracts/{domain}/metric-index.md`
3. `/knowledge/org/source/contracts/{domain}/eval/golden_cases.md` (if exists; never `golden-questions.md`)
4. `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` (if present for domain) — see [`references/special-logic-check.md`](references/special-logic-check.md)
5. `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` metadata (columns, table JSON) via `run_query.py`
6. `/knowledge/org/target/knowledgebase/{domain}/*.md` (always check after storage-layer short-list, same domain)

**NEVER** use `/knowledge/org/source/contracts/b-report-us/tables/**` or `/knowledge/org/source/contracts/pos/tables/**` for any analysis, regardless of stage.

**No cross-domain fallback.** Missing local routing or empty Vertica → **no data found** with scope.

**Path note:** Org contracts / WKB / knowledgebase live under `/knowledge/org/` (mounted read-only from `backend/defaults/b_report/workspace/`). Personal writable files are under `/workspace/`. Do not look for host paths under `defaults/` at runtime.

## Output (chat only)

- Do **not** write files under `/workspace/target/analysis/`
- Include `metric-index.md` citations; `result_status: data_found | no_data_found`
- Three sections: **Summary** / **Evidence** / **Analysis approach & confidence** — no SQL in those sections
- Executed Vertica SQL is appended automatically by the platform under **## Vertica validation**; reference it instead of pasting SQL
- Vertica rule: `/rules/org/contract-data-analysis-vertica.md`

## Validation checklist

See [`references/analysis-output.md`](references/analysis-output.md) § Validation scenarios.
