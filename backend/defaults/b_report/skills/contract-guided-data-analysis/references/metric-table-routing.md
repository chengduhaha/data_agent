<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

## Composite Business Terms (Metric Bundles)

When the user names a composite business term (for example "KPI", "key metrics") without listing individual metrics:

1. Read the active pack `domain-knowledge.md` → **Business Term Registry** before atomic metric resolution.
2. If registry entries include `role_cues`, resolve organizational role (PM, Sales, BD, or entity-only default) from explicit user wording, person/org lookup, or serving-table grain — then select the matching bundle.
3. Expand `expands_to_metrics` into SELECT columns; honor `excludes` (for example PM bundles must not include metrics listed there such as `oplgm_plus_amt`).
4. For ranking without a named sort metric, use `default_sort_metric` and `default_sort_direction` from the matched bundle.
5. Do not register composite terms as single metrics in `metric-index.md` and do not hardcode bundle expansion in Python.

## Metric Resolution Rules

When the question references a metric:

1. Locate metric definition and extraction logic in KB first.
2. If the metric appears in multiple tables, select table by KB selection guidance and requested grain.
3. Prefer pre-aggregated DWS/DM tables when grain matches.
4. Do not recompute from lower-detail tables if an approved pre-aggregated table already serves the request.
5. If multiple definitions conflict, ask clarification.
6. Metric name and physical column name are not assumed equivalent:
   - Before writing SQL, verify from KB column catalog whether the metric exists as a physical column in the selected table.
   - If not a physical column, use the KB-approved metric formula/expression for computation.
   - Do not issue SQL that references an unverified metric identifier as a direct column.

## Table Routing Hard Constraints (Mandatory)

Do not select tables by "queryable" or "has metric column" alone. Enforce semantic role first.

1. Table role classification first:
   - Determine table role from KB metadata and semantics first (for example: canonical total-serving table vs dimension-slice table vs detail table).
   - Use naming patterns only as weak hints when KB role tags are missing.
   - Unless user explicitly requests a slice dimension, do not use dimension-slice tables to answer global-total questions.
2. Global-total question default:
   - For metric total/trend questions without explicit slice constraints, route to KB-marked canonical serving table first.
   - Use slice tables only when the user explicitly asks for a corresponding dimensional breakdown.
3. Canonical-over-available principle:
   - "Can return a number" is not sufficient.
   - "Metric definition and business scope match" is required.

## Anti-Duplication Check Before Aggregation (Mandatory)

Before any `SUM`/aggregation, run anti-dup validation on chosen table semantics:

1. If table carries many organizational dimensions, treat as potential multi-row-per-business-grain table.
2. Verify whether requested metric is already pre-aggregated at target grain in that table.
3. If duplication risk exists, do not directly `SUM` blindly:
   - switch to canonical total table, or
   - aggregate at correct deduplicated key grain first, then roll up.
4. If dedup logic cannot be determined from KB, ask clarification instead of guessing.

## Deterministic Planner Tools

When intent and parameters match, prefer deterministic planner tools over ad-hoc SQL.

| Intent | Tool | When to use |
|--------|------|-------------|
| `metric_lookup` | `metric_lookup` | Single scalar KPI for metric plus optional entity. Time may be user-specified, relative anchored, or KB-assembled default according to temporal plan. |
| `ranking` | `ranking_top_n` | Top-N or bottom-N breakdown by a documented business key when metric, dimension, and time plan are resolved or safely defaulted. Pass `sort_direction=asc` for hurt/worst/bottom phrasing. Supports composite scope: entity filter plus `GROUP BY` breakdown key on one routed table. **Before hand-written SQL**, read `metric-index` `dimension_slice_routing`, preferred/avoid tables, and routed table Column Catalog + negative assertions. Label-only entity filters (e.g. generic product scope) are routing signals — do not place them in SQL `WHERE`. |
| `metric_comparison` | `period_comparison` | Two-period comparison or YoY% when periods are user-specified, relative anchored, or certified by a golden pattern. |

If a deterministic tool returns unsupported, fall back to KB-certified SQL planning. Do not invent tables through catalog discovery.

## Time Dependency

Metric routing must consume the resolved temporal plan.

Do not require a user-provided time range when:

- Stage-1 produced `kb_default_eligible`; and
- Stage-2 confirmed `temporal_plan.mode = kb_assembly_default`.

Do require clarification when:

- `temporal_obligation = user_must_specify`; or
- Stage-2 cannot find certified default-period assembly.
