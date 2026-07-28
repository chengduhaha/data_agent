# RDS Report SQL Generation (`rds_report_generation`)

Apply this reference **only** when Stage-1 classifies the question as RDS SQL / report generation. Other domains and KPI-only lookups stay on the standard contract-guided path — do **not** apply a host-environment RDS rule gate for those.

## Intent detection checklist

Set `pipeline_mode` / intent to `rds_report_generation` when **any** cue matches:

| Cue | Example |
|-----|---------|
| Explicit RDS SQL / report wording | "generate RDS SQL", "RDS report", "report generation" |
| Domain report for RDS | "inventory / CPO / POS report for RDS" |
| Output aimed at RDS deliverable | column lists for `rds_tmp`, `rdsetl.rds_tmp`, RTV wording |
| Contract pack + report columns | this skill with `knowledge/contracts/rds/**` and report-shaped output |

**Not this mode** (keep existing three-section + aggregate evidence; no SQL in user reply):

- B Report / POS KPI lookup, ranking, trend, variance, attribution
- Non-RDS domain analysis under `knowledge/contracts/b-report-us`, `pos`, etc.
- RDS pack used only for a metric answer (e.g. "what is OH for vendor X?") without asking for a report/SQL script

Defaults when unspecified (from RDS conventions): engine **Vertica**, region **US** → `_us`, report# **99999**.

## Rule load order (mandatory before `compile_sql`)

Read and apply in this order, when the host environment provides these RDS rules (e.g. Cursor `rds-*.mdc`). Load **exactly one** engine dialect + temp-table pair. If the host environment does not provide these rules, fall back to the general structure/aggregation/safety/formatting expectations described in the Compile checklist below.

```text
1. rds-target-engine
2. rds-region-schema-routing
3. Engine-neutral:
   - rds-report-query-structure
   - rds-report-aggregation
   - rds-report-safety-and-output
   - rds-sql-formatting
4. Vertica (default):
   - rds-engine-vertica-dialect
   - rds-engine-vertica-temp-tables
   OR StarRocks (only if user requested SR):
   - rds-engine-starrocks-dialect
   - rds-engine-starrocks-temp-tables
5. Compile tmp_ steps → rds_tmp + body
6. Optional aggregate MCP validation
7. Save SQL + analysis artifact
```

This skill does **not** embed those rule bodies (dialect, temp-table, formatting, region-routing) — they remain outside this skill package.

Business columns / filters / joins still come from local contracts:

- `knowledge/contracts/rds/**`
- `knowledge/ref/RDS/**`
- `knowledge/knowledgebase/RDS/**` after storage-layer short-list (if present for the domain)

Do **not** invent tables or columns from absent knowledge paths.

## Compile checklist

Hard constraints:

1. **No giant multi-CTE report script.** Prefer multiple working tables:
   `CREATE LOCAL TEMP TABLE tmp_… ON COMMIT PRESERVE ROWS AS` (Vertica).
2. **Temp naming:** `tmp_<business_step>_<region>_<report#>` (defaults: region `us`, report# `99999`). Do not embed vendor/customer numbers in `tmp_` names — put those filters in `WHERE`.
3. **Grain** explicit (e.g. sku × inv_type × location). Every non-aggregated selected column in `GROUP BY`.
4. **Filters** close to the first reduce step that reads source facts.
5. **Final deliverables:**
   - Vertica: `DROP`/`CREATE` `rdsetl.rds_tmp` then `rdsetl.rds_tmp_body`
   - StarRocks: `tempdb.rds_tmp` / `tempdb.rds_tmp_body`
6. **Body table:** `flag = 1`, `body_type = 'Standard'`, `cnt = COUNT(*)` from detail output.
7. **Cleanup:** after deliverables, `DROP` every working `tmp_*`; never drop final `rds_tmp` / `_body`.
8. **Region schemas:** default suffix `_us`. Never invent region schemas.
9. **Safety:** never invent tables/columns/metrics; SELECT-only on physical sources except allowed temp/output DDL for the RDS pattern.
10. **Formatting:** uppercase keywords; explicit join types; `SUM(ifnull(...))` / dialect-equivalent null handling per engine rules.

## Deliverable override vs `output-contract.md`

| Concern | Standard KPI path | `rds_report_generation` |
|---------|-------------------|-------------------------|
| User-facing SQL | **Do not** include SQL | **Do** include final fenced report SQL |
| Primary artifact | Three-section answer + analysis md | RDS-shaped script + analysis md |
| Evidence MCP | Aggregate-first required for numbers | Optional SELECT aggregates / counts only |
| Script shape | Evidence CTE / single SELECT OK | Must be `tmp_*` → `rds_tmp` + `_body` |

Still include **Summary** / **Evidence** / **Analysis approach & confidence** for business assumptions, scope, and any validation totals. Evidence CTE extracts are **not** valid RDS report deliverables.

Save paths for this skill:

- Analysis: `{output_dir}/{slug}_{YYYYMMDD}.md`
- SQL sidecar: `{output_dir}/{slug}_{YYYYMMDD}.sql` (prefer this over classic `Output/vertica/` unless the user asks for that folder)

If an output file already exists, rename the existing file before writing the new one.

## MCP validation policy

**Server:** `vertica-prod` — `run_query_safely` only.

| Allowed | Forbidden |
|---------|-----------|
| SELECT aggregates / row counts to validate filters and grain | Using MCP as a substitute for the report script shape |
| Bounded validation of vendor / snapshot totals | Executing DDL that creates `rdsetl.rds_tmp` / `_body` on prod unless the user explicitly asks |
| | Schema discovery tools; inventing columns from live metadata |

The **script is the deliverable**. Validation numbers may appear in Evidence; full row dumps must not.
