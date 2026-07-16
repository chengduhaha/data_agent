# Analysis Output Contract

## Path and naming

```
target/analysis/{slug}_{YYYYMMDD}.md
```

- `slug`: lowercase, underscores, ~60 chars from problem statement
- Optional sidecar: `{slug}_{YYYYMMDD}.sql` when query is reusable
- Update `target/analysis/readme.md` index row per new artifact

---

## Required header metadata

```markdown
# {Title}

| Field | Value |
|-------|-------|
| analysis_id | {slug}_{YYYYMMDD} |
| generated | {ISO date} |
| domain | {resolved domain} |
| request_type | metric_lookup \| ranking \| trend \| diagnostic \| attribution \| comparison |
| data_source | Vertica MCP \| none |
| knowledge_routing | {table FQNs used} |
| golden_case_id | {id or none} |
| metrics_used | {metric ids from metric-index.md} |
| result_status | data_found \| no_data_found |
```

---

## Required sections

### Problem statement

User verbatim question.

### Answer

Per [`output-contract.md`](output-contract.md) three-section format:

- **Summary** / **Evidence** / **Analysis approach & confidence**

When `result_status: no_data_found`:

- State **No data found** with scope (domain, period, filters, entity)
- Do not invent numbers

### Methodology

- `local_research_sources` — contract / special-logic / storage-layer (`l1_catalog`) / knowledgebase paths
- `external_mcp_research: none` | `bitbucket_exception` (path + reason)
- `domain-knowledge` sections used
- `metric-index` entries used (formula + verification status)
- `golden_case_id` or `skipped`
- `special_logic_checked: yes|no|not_applicable` — rule(s) applied, if any, from `/workspace/source/ref/{domain}/special_logic.txt`
- WKB / `l1_catalog` candidates (top 5 ids)
- SQL strategy (aggregated vs detail)

### Vertica validation

Query count, `verified_shape`, key aggregates — no large raw dumps.

Omit section when no Vertica run (local routing failed).

### Open questions

KB gaps only — files checked, missing artifact.

---

## Forbidden in output

- Never cite or reference `golden-questions.md`
- Never cite or reference `/workspace/source/contracts/{domain}/tables/*.md`
- No Bitbucket paths unless documented exception
- No full-row dumps from Vertica

---

## Metric-index citation

Every metric in the answer must cite:

- metric id from `/workspace/source/contracts/{domain}/metric-index.md`
- `formula_verification_status` when used in SQL

---

## Validation scenarios (post-implementation)

Use these to verify the skill behaves correctly:

| # | Scenario | Expected |
|---|----------|------------|
| 1 | Domain with `eval/golden_cases.md`; question matches certified case | `golden_case_id` set; aggregated Vertica query; `result_status: data_found` |
| 2 | Domain without `eval/golden_cases.md` (e.g. pos); metric-index routes hub table | `golden_case_id: none`; metric-index routing; evidence or no_data_found |
| 3 | Scoped Vertica query returns 0 rows | Answer **no data found** with period/filters; no domain hop |
| 4 | Local routing cannot compile SQL | **no data found** before Vertica; list files checked |
| 5 | Research phase | No Bitbucket MCP; no Vertica metadata tools; `external_mcp_research: none` |
| 6 | Forbidden file | Agent never opens `golden-questions.md` or `/workspace/source/contracts/{domain}/tables/*.md` |
| 7 | WKB intent | Only `nl2sql_metric`, `find_table_schema`, `data_engineering` — never `incident_debug` |
| 8 | Token budget | ≤2 domain files + ≤3 table files before SQL |
| 9 | POS domain, table resolved | `special_logic.txt` checked for that table; applied rule (if any) recorded in methodology |
| 10 | Domain with no `/workspace/source/ref/{domain}/` folder | `special_logic_checked: not_applicable`; proceeds to storage-layer/knowledgebase search |

---

## Relation to enrich output-structure

Based on [`table-enrich-6layer-context` output-structure](../../../../) field conventions (`contract_version`, artifact metadata) but **analysis deliverable** — not a knowledge package. Omit `golden-questions.md` from layout.
