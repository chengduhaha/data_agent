---
name: contract-guided-data-analysis
description: |
  Contract-first business data analysis with local md/WKB research before Vertica evidence SQL.
  Use when: KPI lookup, ranking, trend, comparison, variance drivers, POS/B Report metrics, validate numbers, data anomaly.
  Routes via source/contracts domain-knowledge → metric-index → source/ref special_logic → storage-layer (l1_catalog) → knowledgebase.
  Don't use when: ETL change requests, flow edits, DDL/DML, unrestricted warehouse exploration, email intake (use etl-email-change-intake).
extensions:
  rules:
    - /rules/org/AGENTS.contract-skill.md
    - /rules/org/AGENTS.analysis-clarification.md
    - /rules/org/contract-data-analysis-vertica.md
  tools: [wkb_query]
  mcp: [gateway-vertica-prod]
harness:
  phases: [research, execute, synthesize]
  tool_budgets:
    run_query_safely: 12
    execute_query_paginated: 12
    wkb_query: 8
  require_synthesis: true
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
| `read_question` | Intent, domain cue, `query_spec`, temporal obligation; detect `rds_report_generation` |
| `local_research` | Local-first gate; forbidden MCP discovery |
| `resolve_domain` | Contract paths for resolved domain |
| `special_logic_check` | `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` |
| `plan_queries` | Metric/table routing, SQL plan, fiscal time; RDS rule load when `rds_report_generation` |
| `retrieve_tables` | Storage-layer (`l1_catalog`) short-list → ≤3 knowledgebase table sections |
| `compile_sql` | Local column catalog only; gate before MCP; RDS-shaped compile when `rds_report_generation` |
| `execute_evidence` | Vertica `run_query_safely` aggregate-first (optional validation only in RDS report mode) |
| `synthesis` | Three-section answer or **no data found**; RDS mode also requires fenced report SQL |

## Workflow (router)

0. **Clarification gate** — if the question is unclear for routing (comparison sense, time, breakdown, grouping, entity/scope, …), ask first and **stop** ([`references/output-contract.md`](references/output-contract.md) § Ambiguity Handling; [`.cursor/rules/analysis-clarification-before-routing.mdc`](../../rules/analysis-clarification-before-routing.mdc)). Do not invent “less” = top-N lowest. If already clear, proceed.
1. Classify intent + domain — [`references/question-shape.md`](references/question-shape.md)
2. **Local research gate** — no Bitbucket/Vertica until routing complete
3. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md` — entity/time disambiguation
4. `/knowledge/org/source/contracts/{domain}/metric-index.md` — metrics + `dimension_slice_routing`
6. Special logic check — [`references/special-logic-check.md`](references/special-logic-check.md) → `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` (when present for domain); always check `special_logic.txt` for logic tied to the resolved table(s)
7. Storage layer metadata search — [`references/wkb-retrieval.md`](references/wkb-retrieval.md) → `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` (search columns/table metadata) before opening knowledgebase docs
8. Knowledgebase table docs → `/knowledge/org/target/knowledgebase/{domain}/{stem}.md` (L2/L3/L6 sections); **NEVER** read `/knowledge/org/source/contracts/{domain}/tables/*.md`
9. Compile SQL from local contracts; cannot compile → **no data found**
10. Entity Phase-1 (if labels) — bounded dim probe per [`references/entity-resolution.md`](references/entity-resolution.md)
11. Execute — [`references/vertica-query.md`](references/vertica-query.md); zero rows → **no data found**
12. Synthesize — [`references/output-contract.md`](references/output-contract.md)

### Branch — `rds_report_generation`

When the question is **RDS SQL / report generation** (not a KPI-only lookup), after steps 0–8 (local routing unchanged):

1. Load [`references/rds-report-sql.md`](references/rds-report-sql.md) and apply the ordered `.cursor/rules/rds-*.mdc` gate **before** `compile_sql`.
2. Compile multi-step working `tmp_*` tables → final `rdsetl.rds_tmp` + `rdsetl.rds_tmp_body` (StarRocks: `tempdb.*` only if requested). Defaults when unspecified: engine **Vertica**, region **US** (`_us`), report# **99999**.
3. Primary deliverable is **RDS report SQL** (fenced SQL in the user reply + saved `target/analysis/{slug}_{YYYYMMDD}.sql`). Keep Summary / Evidence / Approach for assumptions and optional validation totals.
4. Vertica MCP remains **optional validation only** (aggregates / row counts). Do **not** execute DDL that creates `rdsetl.rds_tmp` on prod via MCP unless the user explicitly asks. Do **not** treat a large evidence `WITH` CTE as the report deliverable.

**Isolation:** B Report / POS / other-domain KPI lookup, ranking, trend, variance, and attribution stay on the existing path (no SQL in user reply; aggregate-first evidence). Using an RDS pack only to answer a metric (“what is OH for vendor X?”) without asking for a report/SQL script also stays on the existing path — **RDS `rds-*.mdc` gate not applied**.

**Conditional:** [azkaban-parameter-jobs](../azkaban-parameter-jobs/SKILL.md) only when WKB/knowledgebase already names a `.flow` file.

## Source priority (summary)

1. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md`
2. `/knowledge/org/source/contracts/{domain}/metric-index.md`
4. `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` (if present for domain) — see [`references/special-logic-check.md`](references/special-logic-check.md)
5. `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` metadata (columns, table JSON) via `run_query.py`
6. `/knowledge/org/target/knowledgebase/{domain}/*.md` (always check after storage-layer short-list, same domain)

For RDS report generation, prefer `/knowledge/org/source/contracts/rds/**` + `/knowledge/org/source/ref/RDS/**` (this repo). Do not invent tables/columns from absent `RDS_Workspace/` paths.

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
