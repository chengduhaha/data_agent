<!-- Local copy for contract-guided-data-analysis. Paths adapted to source/contracts. Do not depend on external skill trees. -->

## Reference dimension filters vs entity filters

When the user explicitly scopes by a reference dimension (pack **Reference Dimension Lookup Index** `cue_keywords` + value), this is **not** entity anchoring.

- Emit `dimension_filter=<filter_label>=<token>` per [dimension-scope.md](./dimension-scope.md).
- Do **not** map the value token to `vendor_label`, `customer_label`, or other Entity Ontology filter keys.
- Phase-1 validation runs on the reference dimension table (`table_ref` in the index), not on vendor/customer dims unless the user also scopes an entity.

When metrics are resolved and only a reference dimension filter is active, proceed with serving-table evidence SQL on the indexed filter column — do not stall on entity clarification.

### Semantic scope stage (person/org)

During **read-question** (`load_context` graph node, before warehouse probes):

- Load the pack **Person and Organization Scope Policy**, **Person Organization Lookup Index**, and **Entity Ontology** person-org rows (synthesized from table ISP).
- Return `person_name_tokens` for each bare person name in the question (split multiple people into separate entries).
- For each `person_name_tokens` entry, emit competing `entity_hypotheses` covering **every person-org `entity_type` in Entity Ontology** with similar priors.
- Do **not** bind bare person names to integer filter keys (`pm_id`, `sales_rep_id`, …) before Phase-1 validation.
- The runtime **bind_entity** step runs mechanical Phase-1 probes across lookup families before KB table routing.

---

## Entity Resolution and Temporal Defaults

When user-provided entity filters are present, entity resolution must happen before fact aggregation.

This is especially important when `temporal_obligation = kb_default_eligible`.

### Rules

1. Validate entity identifiers or labels in Phase-1 before querying facts.
2. If Phase-1 returns zero rows:
   - report invalid or unrecognized entity;
   - do not ask for time as a workaround.
3. If Phase-1 returns multiple ambiguous matches:
   - ask entity clarification;
   - do not aggregate across ambiguous matches silently.
4. If Phase-1 resolves entity keys:
   - proceed to Stage-2 temporal default verification.
5. Apply KB-assembled default time only after:
   - entity scope is valid; and
   - the active pack provides certified default-period assembly.

### Label Probe

For `entity_anchoring = label_probe`:

- exact match first;
- documented fuzzy match second;
- ask entity clarification if multiple plausible matches remain;
- only then apply default time if certified.

### Invalid entity vs no activity

- Phase-1 fails: invalid/unrecognized entity.
- Phase-1 succeeds but fact query returns zero rows: valid entity with no activity data in the resolved period.

## Entity Identifier Resolution (Mandatory)

When the user scopes analysis with a human-readable identifier (letters, dashes, mixed alphanumeric — not a pure numeric key):

1. Read KB column catalog `data_type` for every candidate filter column before writing `WHERE`.
2. **Never** use an `entity_filter` `filter_key` (for example `vendor_label`, `vpc_group_label`) as a SQL column name — filter keys route scope only; resolve physical columns from the dim table **Identifier Search Profile** in `tables/*.md`.
3. **Never** compare an alphanumeric user token to an `int` / `numeric` column (for example `*_no`, `*_id`, `prod_code` when typed integer).
4. Route user tokens to KB-documented **searchable label columns** (`varchar` / `text`) listed in dim Identifier Search Profile, Entity Key Registry `searchable_labels`, or denormalized serving-table varchar keys.
5. Resolve label → join key on the dimension table, then filter facts on the integer FK documented in `dimension_reference`.
6. If the selected fact table lacks the varchar label column, **join the dimension** per `dimension_reference` — do not assume the column exists on the fact.
7. Prefer dimension-slice serving tables that already denormalize searchable labels when `metric-index.md` `dimension_slice_routing` matches the entity scope.

Supported user token patterns (map to Entity Key Registry before SQL):

- `order#123` / `order no. 123` → `order_no` (numeric)
- `cust#123` / `customer#123` → `cust_no` (numeric)
- `part ENN-525` / `part#ENN-525` / `SKU ABC-123` → `part_identifier` (alphanumeric label)
- `vpl#123` → `vpl_no` (numeric); `vpl code XYZ` → `vpl_code` (varchar label)

## Entity Scope Pre-Validation (Mandatory)

When the user scopes analysis with entity identifiers (`order#`, `cust#`, `part#`, `vpl#`, or names/labels), run a **two-phase** workflow. Do not query fact/serving tables for metrics until Phase-1 identifier validation succeeds.

### Step 1: Classify tokens

**Done when:** every user token is mapped to Entity Key Registry entry (numeric key vs varchar label).

1. Classify user tokens using `domain-knowledge.md` Entity Key Registry:
   - numeric keys: `order_no`, `cust_no`, `vpl_no`, `vend_no`, `pm_id`
   - alphanumeric labels: `part_no`, `mfg_partno`, `cust_name`, `vend_name`, `vpl_code`, `mcust_name`

### Step 2: Select serving table from KB

**Done when:** candidate fact/serving table is chosen from `metric-index.md` routing — not from warehouse catalog.

2. Select candidate serving/fact table from `metric-index.md` `dimension_slice_routing` and table role — never from warehouse catalog discovery.
3. Resolve fact↔dim linkage from KB only:
   - `dimension_reference` on fact/serving columns (for example `sku_no` → `dim_us.dim_pub_part_info`)
   - Entity Key Registry join keys when `dimension_reference` is absent

### Step 3: Phase-1 identifier validation

**Done when:** identifier resolves to FK(s) or is reported invalid.

4. **Phase-1 probe (identifier validation)** — run before any fact aggregation:
   - Query the KB-named dimension with documented searchable varchar columns, or validate numeric keys on the appropriate dim/fact key column
   - Exact match first; if zero rows, retry `ILIKE '%token%'` on the same varchar columns (see Fuzzy Match Retry)
   - **Outcomes:**
     - 0 rows after fuzzy retry → report **invalid/unrecognized identifier**; do **not** query facts for metrics
     - Multiple rows → surface top candidates in evidence or ask clarification
     - 1+ resolved keys → proceed to Phase-2 using integer FK (`sku_no`, `cust_no`, `vpl_no`, …)

### Step 4: Phase-2 metric retrieval

**Done when:** metric SQL returns or reports no-activity for valid identifier.

5. **Phase-2 probe (metric retrieval)** — only after Phase-1 succeeds:
   - Join serving/fact table on resolved FK; apply time scope and aggregate metrics
6. **Zero-row fact result after valid identifier** → report **no activity data** for scope/period (distinct from invalid identifier).

Example (part-scoped metric lookup): Phase-1 on `dim_us.dim_pub_part_info` (`part_no`, `mfg_partno`) → resolve `sku_no` → Phase-2 on `dw_us.dws_disty_brpt_part_mtd` joined on `sku_no`. See golden `part-enn-525-revenue-margin`.

## Dimension Table Authority (Mandatory)

1. Use **only** `referenced_dimension_table_fqn` values from KB `dimension_reference` / Dimension Lookup blocks in retrieved table docs.
2. **Forbidden**: inventing `dim_*` table names not present in retrieved KB files (for example generic `dim_sku` when KB names a different dim).
3. If the correct dimension is unclear, use `lookup_table_schema` on a KB-named dimension — never guess table names from naming patterns alone.
4. When multiple dimension candidates appear in KB, follow `domain-knowledge.md` Entity Key Registry and table L3 routing before choosing.
5. **Forbidden catalog discovery**:
   - `SELECT ... FROM v_catalog.tables WHERE ...` to find tables by name pattern
6. **Forbidden invented tables** (unless present in retrieved KB for the active pack):
   - `dim_pub_sku`, `dim_pub_product`, `dim_pub_sku_xref_all`, `dim_pub_prod_code`, `dim_disty_cws_part`
7. **Forbidden cross-pack tables**: do not use tables from other knowledge packs (for example POS `dim_pub_sku_xref_all`) when `b-report-us` is active.
8. SQL may reference only tables in the retrieved KB allowlist for the current turn (plus `dim_us.dim_pub_date` when time filtering requires it).

## Fuzzy Match Retry (Mandatory)

User-supplied identifiers may be partial, truncated, or slightly misspelled.

For likely typos in vendor/customer/product/person names (for example `CICSO` → `CISCO`), apply [typo-tolerance.md](./typo-tolerance.md): auto-correct before Phase-1 probe, record `original → corrected`, and disclose in the final confidence section.

1. First attempt exact match (`=`) on KB-documented searchable varchar columns.
2. If the scoped query returns zero rows, retry with case-insensitive partial match (`ILIKE '%token%'` or domain-documented `match_mode`) on the **same** searchable columns before changing table or strategy.
3. If multiple rows match after fuzzy search, surface top candidates in evidence or ask clarification — do not silently aggregate ambiguous matches without stating the assumption.
4. When fuzzy match is used in the final answer, state that explicitly in assumptions or the confidence line.

## Loop Prevention and Stop Rules

1. **Identifier retry limit:** At most **2** fuzzy-match variants per varchar column set before reporting invalid identifier.
2. **Table pivot limit:** Do not change primary table more than **once** per turn for the same intent unless strategy error is confirmed.
3. **Hypothesis backtracking (ReAct):** When Phase-1 or metric evidence fails for the current entity scope, read `entity_guesses=` and `tried_entities=` from planning hints. If a ranked alternate remains, **pivot entity scope and replan** before asking the user. The **review-evidence** node may set `needs_hypothesis_pivot` with `next_entity_filters`; the runtime replans with KB context — do not treat the first hypothesis as final.
4. **STOP and ask user** when:
   - Phase-1 returns zero rows after fuzzy retry **and** no untried semantic hypotheses remain
   - Multiple ambiguous entity matches cannot be resolved from KB
   - Required dimension is absent from retrieved KB files
5. **Avoid infinite loops:** MUST NOT re-run identical or near-identical probe SQL. State what was tried, then ask for clarification.

## Troubleshooting

### Column does not exist (SQLState 42703)

- **Cause:** Wrong column name on a KB-named table.
- **Fix:** Re-read KB column catalog; use `lookup_table_schema` on the **same** table only.
- **Stop Rule:** Do not discover alternate tables via `v_catalog.tables`.

### Invented dimension table

- **Cause:** Guessed `dim_*` name not in KB `dimension_reference`.
- **Fix:** Reload linked dim from table doc L3; use Entity Key Registry.
- **Stop Rule:** If dim still unclear, ask user — do not pattern-guess table names.

### Zero rows after exact match

- **Cause:** Partial/truncated user identifier.
- **Fix:** Retry `ILIKE` on same searchable varchar columns (max 2 variants).
- **Stop Rule:** After retry, treat as invalid identifier — do not query facts.

### Invalid identifier vs no activity

- **Cause:** Phase-1 failed vs Phase-1 succeeded but Phase-2 returned zero rows.
- **Fix:** State which case applies explicitly in the answer.
- **Stop Rule:** Never conflate "bad token" with "no sales in period".

---

## Generic Scope Resolution

Soft user tokens must not be used directly in fact SQL. They are resolved by
KB-certified lookup recipes into `validated_scope_sets`.

`validated_scope_sets` is the only runtime scope contract consumed by
`evidence_loop` and `compile_sql`. Legacy hints such as person-org or label
scope hints may be adapted during migration, but they are not planner/SQL
contracts.

---

## Entity scope and compile binding (no PipelineTask)

Person/org and label-probe scope are resolved on a single graph node **`bind_entity`** (replacing the former `check_entity` → `resolve_entity` pair), writing `retrieval.entity_filters` and `person_org_validated` / `entity_validated` planning hints.

`bind_entity` runs two internal phases — **prepare** (select binding profiles from structural scope signals: `person_name_tokens`, `entity_anchoring`) and **probe** (execute KB-certified Phase-1 dim SQL) — in one graph node. Binding profiles are KB-driven, not Python entity enums:

- `person_org_lookup` — Person Organization Lookup Index families; emits `binding_status=ready|ambiguous|invalid`.
- `identifier_label` — `entity_anchoring=label_probe` (vendor/VPL/part names); maps `entity_hypotheses` to Entity Key Registry, runs `build_phase1_probe_sql`, records `tried_entities=` on miss.

### `binding_status` enum (graph routing)

| Status | Meaning | Route |
|--------|---------|-------|
| `not_needed` | pinpoint integer key already in filters, no probe | → `plan_queries` |
| `deferred` | `scope_ambiguity=high`; slot filters not promoted but person probe may still run | → probe if profiles pending, else `plan_queries` |
| `pending_probe` | profiles selected, probe about to run | internal (prepare → probe) |
| `ready` | Phase-1 resolved FK / integer key | → `plan_queries` |
| `ambiguous` | multiple candidates after fuzzy retry | → `ask_user` (entity clarify) |
| `invalid` | zero hits across all hypotheses | → `ask_user` (entity clarify) |

`deferred` means "do not trust soft slot filters" — **not** "skip probe". Person/org probes still run when tokens are present.

### Planner must stop on unbound scope

The planner must **not** create Phase-1 lookup evidence rows for human-readable entity labels. If `binding_status` is absent or not in `{ready, not_needed}` while `person_name_tokens` or `entity_anchoring=label_probe` is present, the planner must stop and return a bind gap — the runtime routes back to `bind_entity` instead of executing fact SQL. Fact evidence planning is only allowed after `bind_entity` writes `binding_status=ready` (or `not_needed` for pinpoint integer keys).

### Multi-candidate label is a fact, not ambiguity

When Phase-1 label probing returns multiple candidate rows, `bind_entity` does **not** judge this at bind time. It records every matching row as a fact — `binding_status=ready` plus an `entity_scope_set` hint (entity type, token, filter key, join key, all matching values, row count) — and moves on. There is no bind-time adjudication round-trip; Python's job here is limited to running the KB-certified probe and writing the fact.

Whether the candidate set means "one true intended entity", "a valid business scope set" (e.g. `HP` covers `HP INC` and `HEWLETT PACKARD ENTERPRISE`), or "genuinely ambiguous — ask the user" is decided **downstream**, by the LLM, at whichever stage first needs to act on it:

- **planner** — treats `entity_scope_set` as a resolved set of join-key values and encodes it as a structured `IN` filter in `query_spec.filters` when the question's grain matches an aggregate/breakdown over the label (see [sql-planning.md](./sql-planning.md)); or asks a clarifying question first when the candidates look like genuinely different business meanings the user must pick between.
- **write-answer / double-check** — if the planner proceeded with the full set, judges from the actual evidence rows whether the answer should be reported per-candidate, summed across the set, or caveated.

Python must not hard-code business labels, entity names, or domain-specific multi-hit rules, and must not pre-emptively route straight to `ask_user` just because a probe returned more than one row.

The planner must encode entity filters in `query_spec.filters` after resolution — **do not** emit `tasks`, `obligations[]`, or `metric_by_person_*` ids.

Evidence binds via opaque `todo_ids` (`routing_1`, …) on `evidence_queries` and `evidence_results`. Sufficiency is judged in `review_evidence` from evidence rows — not from a parallel obligation state machine.

See [sql-compiler-contract.md](./sql-compiler-contract.md) for planner/compiler boundaries.
