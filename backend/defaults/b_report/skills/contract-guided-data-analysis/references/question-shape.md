<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

# Question Shape and Temporal Obligation

## Purpose

This reference defines the first-stage classification for CIS business data questions.

Its purpose is to decide whether:

1. the user already provided time;
2. the user used relative time that can be anchored;
3. the question is eligible for KB-provided default period assembly;
4. the user must specify time before evidence SQL.

This file is domain-agnostic within CIS.

It must not hardcode:

- product-specific rules;
- vendor-specific rules;
- part-specific rules;
- customer-specific rules;
- VPL-specific rules;
- specific table names;
- specific SQL snippets;
- one-off historical bug fixes.

Domain-specific default time logic must come from the active knowledge pack.

---

## Stage-1 Output Contract

Stage-1 must classify the question and produce:

```json
{
  "intent": "optional semantic label — trace/eval only; use rds_report_generation when RDS report SQL is the deliverable",
  "pipeline_mode": "lookup | explore | diagnose | rds_report_generation",
  "query_spec": {
    "metrics": [],
    "group_by_key": null,
    "order_by": null,
    "sort_direction": null,
    "limit": null,
    "time_predicate": null,
    "time_bucket": null,
    "periods": null,
    "filters": [],
    "having_filters": [],
    "required_grain": null
  },
  "entity_anchoring": "pinpoint | label_probe | dimension_filter | open_aggregate | none",
  "dimension_filters": [],
  "temporal_expression": "explicit_period | relative_cue | absent",
  "temporal_obligation": "user_already_specified | kb_anchor_resolve | kb_default_eligible | user_must_specify",
  "time_scope": null,
  "entity_hypotheses": [],
  "metrics": [],
  "needs_clarification": false,
  "clarification_target": null,
  "notes": ""
}
```

`clarification_target` when `needs_clarification=true` should be one of:

| Value | Use when |
|-------|----------|
| `time_range` | `temporal_obligation = user_must_specify` or no safe KB default |
| `breakdown_dimension` | Variance/driver/attribution without a named (or KB-default) analysis angle |
| `grouping_definition` | Vague word like "item"/"line"/"category" with multiple pack-plausible meanings |
| `business_term` | Acronym/label/project cue not resolvable from pack ontology |
| `entity_scope` | Ambiguous entity among candidates |
| `metric_name` | Multiple user-facing metric candidates (name clash — not formula) |
| `grain` / `geography` / `currency_unit` | Underspecified reporting scope |
| `comparison_sense` | “less / lower / low / hurt / worst” (or similar) without a clear baseline (ranking vs MoM/YoY vs negative-only vs peer/target) |
| `population_scope` | Open ranking without clear population (all vs PM/VPC/segment/named list) |

Do **not** set clarification for missing table, formula, flow, or ETL logic — those are KB gaps (fail closed). See [output-contract.md](./output-contract.md) Ambiguity Handling. Workspace rule: [`.cursor/rules/analysis-clarification-before-routing.mdc`](../../../rules/analysis-clarification-before-routing.mdc).

When multiple slots are open (e.g. `comparison_sense` + `time_range`), set `needs_clarification=true` and ask for **all** missing slots in one concise reply; prefer listing `clarification_target` values in `notes` if only one field is allowed.

**`query_spec` is required** before prep-sql (alias `routing_payload` accepted during migration). **`pipeline_mode`** controls orchestration only (single lookup vs multi-round diagnose). **`intent`** and legacy **`answer_shape`** are optional trace labels — they must not control SqlTaskContract assembly.

**Person names:** Stage-1 must always emit `person_name_tokens` (use `[]` when none). Runtime does **not** infer person names from the raw user message — bare names, date-range `and`, and list/top-N scope must come from this LLM output. Do **not** emit `tasks` / pipeline obligations; compile uses `query_spec` + `todo_ids` only (see deprecate-pipeline-tasks spec).

Output layout (tables vs inline metrics) follows [output-contract.md](./output-contract.md) at synthesis time based on **evidence rows and query_spec fields** — not intent labels alone.

Stage-1 must not:

- generate SQL;
- invent table names;
- invent metric formulas;
- invent time filters;
- invent a fiscal year or calendar year when the user omitted time;
- ask for time when `temporal_obligation = kb_default_eligible`;
- ask the user which table, formula, flow, or ETL logic to use (KB-owned — resolve or fail closed);
- proceed to plan evidence SQL when `needs_clarification=true` for a required routing slot.
- invent a `comparison_sense` (e.g. treat “less” as top-N lowest) when the user did not specify the baseline.

---

## Axis 1 — QuerySpec (compile input)

Single structured object; **all fields optional** except `metrics` (required before compile). The SQL compiler assembles clauses from **present** fields only — no `answer_shape` dispatch.

| Field | SQL effect when present |
|-------|-------------------------|
| `metrics` | SELECT aggregates (required) |
| `group_by_key` | GROUP BY dimension |
| `order_by` + `sort_direction` | ORDER BY (any query type — not ranking-exclusive) |
| `limit` | LIMIT |
| `time_predicate` | WHERE time filter |
| `time_bucket` | Time-bucket GROUP BY + ORDER BY time ascending |
| `periods` (≥2) | Side-by-side or unpivoted comparison columns |
| `filters` / `having_filters` | WHERE / HAVING predicates |
| `target_metric` / `breakdown_candidates` / `driver_dimensions` | Attribution-style driver analysis (normalize to metrics + group_by) |

See [sql-compiler-contract.md](./sql-compiler-contract.md) for full schema and examples.

**Probe policy:** only `lookup_table_schema` during plan-queries when KB catalogs are incomplete — never evidence SQL.

---

## Axis 1b — Pipeline Mode (orchestration only)

| pipeline_mode | Behavior |
|---------------|----------|
| `lookup` | Single round: plan → compile → execute → answer (default) |
| `explore` | Multiple evidence queries / parallel slices; no recursive root-cause loop |
| `diagnose` | Multi-round drill-down per [output-contract.md](./output-contract.md) attribution policy |
| `rds_report_generation` | RDS report SQL deliverable: local contract routing unchanged, then compile per [rds-report-sql.md](./rds-report-sql.md) + `.cursor/rules/rds-*.mdc` (`tmp_*` → `rdsetl.rds_tmp` / `_body`). User reply includes fenced SQL. MCP aggregates optional for validation only. |

Top-N, YoY, trend, and scalar KPI questions are typically `lookup`. Use `diagnose` when the user asks why / what drove / root cause.

### Detecting `rds_report_generation`

Set `pipeline_mode` (and/or `intent`) to `rds_report_generation` when **any** of these cues apply:

- Explicit “generate RDS SQL”, “RDS report”, “report generation”, or column lists aimed at `rds_tmp` / RTV
- Inventory / CPO / POS / VPO / Open SO-BO / RMA / AR / AP report SQL for RDS
- `/contract-guided-data-analysis` plus domain pack under `/knowledge/org/source/contracts/rds/**` with report-shaped output columns

**Do not** select this mode when the user only wants a metric answer from an RDS pack (e.g. “what is OH for vendor X?”) without asking for a report/SQL script — keep `lookup` / `explore` / `diagnose` and the standard three-section path (no SQL in user reply).

Defaults when unspecified (from RDS rules): engine **Vertica**, region **US** → `_us`, report# **99999**. Full checklist: [rds-report-sql.md](./rds-report-sql.md).

---

## Deprecated — answer_shape (trace only)

Legacy `answer_shape` values (`scalar_metric`, `ranked_set`, `time_series`, etc.) may appear in traces during migration. Runtime **does not** branch compile logic on them. Prefer expressing requirements in `query_spec` fields instead.

---

## Axis 2 — Entity Anchoring

| Value | Meaning |
|-------|---------|
| `pinpoint` | User provides a token intended to identify a specific business object, such as a stable key, external code, order-like number, SKU-like code, or unique identifier. The token still requires validation. |
| `label_probe` | User provides a human-readable name, label, alias, or partial label that requires Phase-1 entity validation on an Entity Ontology type. At runtime, `entity_anchoring=label_probe` selects the **`identifier_label`** binding profile on the `bind_entity` graph node (see [entity-resolution.md](./entity-resolution.md)). |
| `dimension_filter` | User **explicitly names a reference dimension** from the pack Reference Dimension Lookup Index plus a value (for example dimension cue + label). Scope is a WHERE filter on the indexed label column — not vendor/customer entity anchoring. See [dimension-scope.md](./dimension-scope.md). |
| `open_aggregate` | User asks for a global or broad aggregate without an entity filter. |
| `none` | No entity dimension is relevant to the question. |

### Important

`pinpoint` does not mean the entity is already valid. It only means the user supplied a token shaped like a specific identifier.

`dimension_filter` does not mean the value is a vendor or customer name. Read the pack index row and table doc before binding entity hypotheses.

All user-supplied entity identifiers and labels must still be validated according to [entity-resolution.md](./entity-resolution.md).

Reference dimension filters follow [dimension-scope.md](./dimension-scope.md).

---

## Axis 3 — Temporal Expression

| Value | Meaning |
|-------|---------|
| `explicit_period` | User explicitly states year, month, day, fiscal year, fiscal quarter, reporting period, as-of date, or closed date range. |
| `relative_cue` | User uses relative time, such as last month, this quarter, recent N months, yesterday, current period, YTD, QTD, or similar. |
| `absent` | User provides no time expression. |

---

## Temporal Obligation

`temporal_obligation` tells the agent who is responsible for resolving time.

| Value | Meaning | User clarification? |
|-------|---------|---------------------|
| `user_already_specified` | User gave explicit time. Parse and apply it using CIS calendar and active pack policy. | No, unless internally ambiguous. |
| `kb_anchor_resolve` | User gave relative time. Resolve it using data freshness, runtime anchor, table max date, and active pack Time Scope Ontology. | No, unless no anchor exists. |
| `kb_default_eligible` | User omitted time, but the question shape may allow the active pack to assemble a certified default period. | Do not ask in Stage-1. Stage-2 must verify KB support. |
| `user_must_specify` | User omitted time and the question shape has no safe default path at intake. | Yes. Ask before evidence SQL. |

---

## Stage-1 vs Stage-2 Responsibility

### Stage-1

Stage-1 may conclude:

```text
temporal_obligation = kb_default_eligible
```

This means:

> The question shape is eligible for active-pack default period assembly.

It does not mean:

> A default period definitely exists.

Stage-1 must not choose:

- latest month;
- latest open period;
- latest closed period;
- current fiscal year;
- current calendar year;
- MAX(date).

### Stage-2

Stage-2 must read the active knowledge pack and produce an executable temporal plan.

Possible Stage-2 temporal plan modes:

| temporal_plan.mode | Meaning |
|--------------------|---------|
| `explicit_time_scope` | User-provided explicit period was parsed and applied. |
| `anchored_relative_time_scope` | Relative expression was anchored using CIS/pack policy. |
| `kb_assembly_default` | Active pack provides a certified default period assembly. |
| `clarification_required` | No safe time plan exists; ask the user before evidence SQL. |
| `no_time_required` | The resolved metric/entity lookup is not time-dependent according to the active pack. |

For `kb_assembly_default`, Stage-2 must record:

- source artifact;
- business period label;
- whether the period is latest open, latest closed, current fiscal, etc.;
- SQL predicate or certified snippet source;
- freshness anchor when relevant.

---

## Stage-1 Decision Table

| answer_shape | entity_anchoring | temporal_expression | temporal_obligation |
|-------------|------------------|---------------------|---------------------|
| any | any | `explicit_period` | `user_already_specified` |
| any | any | `relative_cue` (incl. entity-anchored, e.g. "same month as Order#…") | `kb_anchor_resolve` |
| `scalar_snapshot` | `pinpoint` (non-person transaction/key) | `absent` | `kb_default_eligible` |
| `scalar_snapshot` | `label_probe` **without** person portfolio KPI | `absent` | `kb_default_eligible`, after entity validation |
| `scalar_snapshot` / ranking | **person names** (`person_name_tokens` non-empty) or **PM/portfolio** scope | `absent` | `user_must_specify` — do not treat as KB-default-eligible |
| `ranked_set` / hurt-most / high-impact list | PM / portfolio / person scope | `absent` | `user_must_specify` |
| `scalar_snapshot` | `open_aggregate` | `absent` | `user_must_specify` unless active pack defines a certified default reporting period |
| `time_series` | any | `absent` | `user_must_specify` unless active pack defines a default trend window |
| `period_comparison` | any | `absent` | `user_must_specify` |
| `ranked_set` | `pinpoint` or `label_probe` (non-person, non-PM portfolio) | `absent` | `kb_default_eligible` only if active pack defines default ranking period for the resolved scope; otherwise `user_must_specify` |
| `ranked_set` | `open_aggregate` | `absent` | `user_must_specify` unless active pack defines a default ranking period |
| `causal_chain` | any | `absent` | `user_must_specify` unless user refers to a known event or the pack defines a certified comparison window |

**Person / PM portfolio override:** Revenue, margin, or ranking for named people or a PMID/PM book of business with **no** period → always `user_must_specify`. Do not apply KB latest-month default silently.

**Open vendor/customer ranking override:** Questions like “is gm_amt less for vendor level” / “which vendors have lower GM” with **no** period → `user_must_specify` for time, and usually also `needs_clarification` for `comparison_sense` (and `population_scope` if unbound). Do not treat as KB-default-eligible.

**Entity-anchored period:** If the user ties time to a pinpoint object (order/invoice month), classify as `relative_cue` + `kb_anchor_resolve` — resolve from that object; do not ask for a separate range.

---

## Entity Validation Interaction

When `temporal_obligation = kb_default_eligible` and entity filters are present:

1. Validate the entity first.
2. If the entity is invalid, report invalid/unrecognized entity.
3. If the entity is ambiguous, ask entity clarification.
4. Do not ask for time merely because entity validation failed.
5. Apply KB default time only after:
   - the entity scope is valid; and
   - the active pack provides certified default period assembly.

For `label_probe`, default time cannot be applied until Phase-1 entity resolution yields a unique or explicitly accepted entity set.

---

## Relative Time Without Explicit Year

When `temporal_expression = relative_cue`:

1. Set `temporal_obligation = kb_anchor_resolve`.
2. Do not ask the user to provide a year merely because the original message lacks `20XX`.
3. Resolve the period using:
   - active pack Time Scope Ontology;
   - data freshness anchor when available;
   - CIS fiscal calendar;
   - selected table's documented time-filter pattern when needed.
4. If no anchor can be found, ask a concise clarification.

Examples of relative cues:

- last month
- 上个月
- recent 3 months
- 最近三个月
- YTD
- QTD
- current quarter
- this fiscal year

---

## Anti-Patterns

Forbidden:

1. Entity-specific temporal exceptions:
   - "if entity is part, use latest period"
   - "if filter_key is part_identifier, skip time clarification"
   - "if token looks like SKU, default to latest month"

2. Invented time scopes:
   - choosing current calendar year when user omitted time;
   - choosing latest month without KB support;
   - using MAX(date) from an unrelated table;
   - assuming fiscal period boundaries not defined by CIS/pack policy.

3. Premature clarification:
   - asking for time before checking whether `kb_default_eligible` can be confirmed by the active pack.

4. Wrong ambiguity classification:
   - treating invalid entity as time ambiguity;
   - treating missing metric definition as time ambiguity;
   - treating missing table routing as time ambiguity.

5. Silent default:
   - using a KB default period without disclosing it in the final answer.

---

## Illustrations, Not Rules

### Example A — Entity-scoped scalar KPI with no time

User asks for a KPI for a specific business object identifier and provides no time.

Classification:

- answer_shape: `scalar_snapshot`
- entity_anchoring: `pinpoint`
- temporal_expression: `absent`
- temporal_obligation: `kb_default_eligible`

Behavior:

- Do not ask for time in Stage-1.
- Validate the entity.
- Stage-2 must verify whether active pack provides certified default period assembly.
- If confirmed, use the KB default and disclose it.
- If not confirmed, ask for time.

### Example B — Global scalar KPI with no time

User asks for a company-level KPI and provides no time.

Classification:

- answer_shape: `scalar_snapshot`
- entity_anchoring: `open_aggregate`
- temporal_expression: `absent`

Behavior:

- Ask for time unless the active pack defines a certified default reporting period for that metric.

### Example C — Relative time

User asks for last month's KPI.

Classification:

- temporal_expression: `relative_cue`
- temporal_obligation: `kb_anchor_resolve`

Behavior:

- Resolve "last month" using CIS/pack anchor policy.
- Do not ask for the calendar year unless no anchor exists.

---

## Stage-1 JSON Examples

### Entity-scoped scalar KPI with absent time

```json
{
  "intent": "metric_lookup",
  "answer_shape": "scalar_snapshot",
  "entity_anchoring": "pinpoint",
  "temporal_expression": "absent",
  "temporal_obligation": "kb_default_eligible",
  "time_scope": null,
  "temporal_resolution": {
    "stage": "stage1_intake",
    "status": "pending_kb_verification",
    "user_clarification_allowed": false,
    "reason": "Entity-anchored scalar KPI with no user-provided time is eligible for active-pack default period assembly.",
    "required_stage2_action": "Verify certified default period in the active knowledge pack."
  },
  "needs_clarification": false,
  "clarification_target": null
}
```

### Open aggregate with absent time

```json
{
  "intent": "metric_lookup",
  "answer_shape": "scalar_snapshot",
  "entity_anchoring": "open_aggregate",
  "temporal_expression": "absent",
  "temporal_obligation": "user_must_specify",
  "time_scope": null,
  "temporal_resolution": {
    "stage": "stage1_intake",
    "status": "clarification_required",
    "user_clarification_allowed": true,
    "reason": "Open aggregate KPI without explicit time and no default reporting period established at intake."
  },
  "needs_clarification": true,
  "clarification_target": "time_range"
}
```

### Relative time without explicit year

```json
{
  "intent": "metric_lookup",
  "answer_shape": "scalar_snapshot",
  "entity_anchoring": "open_aggregate",
  "temporal_expression": "relative_cue",
  "temporal_obligation": "kb_anchor_resolve",
  "time_scope": null,
  "temporal_resolution": {
    "stage": "stage1_intake",
    "status": "requires_anchor_resolution",
    "relative_expression": "last month",
    "user_clarification_allowed": false,
    "anchor_sources": [
      "data_freshness_through",
      "runtime clock",
      "selected table max business date",
      "Time Scope Ontology"
    ]
  },
  "needs_clarification": false
}
```

### Entity-less top-N with metric band (order/list)

User: "Which orders have positive NGM but below 1000 between 2026-01-01 and 2026-04-30? list top 20."

```json
{
  "intent": "ranking",
  "entity_anchoring": "none",
  "person_name_tokens": [],
  "temporal_expression": "explicit_period",
  "temporal_obligation": "user_already_specified",
  "pipeline_mode": "lookup",
  "query_spec": {
    "metrics": ["ngm_amt"],
    "group_by_key": "order_no",
    "order_by": "ngm_amt",
    "sort_direction": "desc",
    "limit": 20,
    "filters": [
      {"field": "ngm_amt", "operator": ">", "values": ["0"], "apply_at": "where"},
      {"field": "ngm_amt", "operator": "<", "values": ["1000"], "apply_at": "where"}
    ],
    "time_predicate": {
      "kind": "between",
      "field": "date_flag",
      "values": ["2026-01-01", "2026-04-30"]
    },
    "required_grain": "order"
  },
  "needs_clarification": false
}
```

**Critical:** `person_name_tokens` must be `[]` — the date-range `and` is not person scope. Do not emit `tasks` or person task ids.

---

## Stage-2 Temporal Plan Examples

### KB default confirmed

```json
{
  "temporal_plan": {
    "mode": "kb_assembly_default",
    "status": "confirmed",
    "source_artifact": "active-pack table L6 / golden routing-certified pattern / metric-index default policy",
    "business_period_label": "latest certified reporting period",
    "time_predicate_source": "certified KB assembly",
    "requires_user_clarification": false
  }
}
```

### No certified default

```json
{
  "temporal_plan": {
    "mode": "clarification_required",
    "status": "no_certified_default_found",
    "requires_user_clarification": true,
    "clarification_target": "time_range",
    "clarification_question": "请确认要分析的时间范围，例如最近一个月、某个财政季度或某个财年。"
  }
}
```

---

## Evidence grain vs question shape

When classifying question shape and reviewing whether evidence is sufficient:

1. **Dimension ranking/breakdown** (`answer_shape` implies a ranked or grouped dimension): evidence at that dimension grain (product, vendor, customer, region keys) satisfies the question unless the user explicitly requests order-line, transaction, or invoice detail.
2. **Do not auto-escalate grain** in **review-evidence** or follow-up SQL when non-empty evidence already matches the requested breakdown dimension.
3. **Freshness**: when `planning_hints` include `data_freshness_through`, treat it as a runtime warehouse anchor — do not plan redundant `MAX(primary_time_column)` calendar probe SQL (see `sql-planning.md`).
