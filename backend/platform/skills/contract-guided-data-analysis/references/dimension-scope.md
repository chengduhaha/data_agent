<!-- Local copy for contract-guided-data-analysis. Paths adapted to knowledge/contracts. Do not depend on external skill trees. -->

# Reference Dimension Scope

## Purpose

Distinguish **entity anchoring** from **reference dimension filtering** when classifying user scope.

This reference is domain-agnostic within CIS. Dimension names, cue keywords, and table pointers come from the active pack `domain-knowledge.md` **Reference Dimension Lookup Index** — not from this file.

---

## Two scope models

| Model | User pattern | Resolution path | Examples (illustrative) |
|-------|--------------|-----------------|-------------------------|
| **Entity anchoring** | User scopes by a business object in Entity Ontology | Phase-1 dim probe on entity dim → integer join key → fact filter | vendor brand, customer name, VPL label, part number |
| **Reference dimension filter** | User **explicitly names a reference dimension** plus a value | Filter on the dimension's searchable label column (or join key after dim probe) on serving slice or fact | `cust type X`, `division Y` when indexed in pack |

Entity Ontology types (vendor, customer, vpl, product, territory, order, pm) use entity anchoring.

Reference dimensions listed in the pack index are **not** entity types. Do not map their value tokens to `vendor_label`, `customer_label`, or other entity filter keys.

---

## Mandatory rules

1. **Explicit dimension cue wins over entity disambiguation**
   - When the user question matches a `cue_keywords` entry in the pack Reference Dimension Lookup Index, treat the scope as a reference dimension filter.
   - Do **not** apply bare-token entity disambiguation (for example OEM brand → vendor) to the value token when the dimension cue is explicit.

2. **Progressive KB load**
   - Read the matched index row only at scope-planning time.
   - Use `read_kb_file` on `table_ref` (and `serving_ref` when present) before writing evidence SQL.
   - Do not assume column names beyond what the index and table Column Catalog document.

3. **Metrics resolved, entity not anchored**
   - When metrics are resolved and a reference dimension filter is active, prefer filtering on the indexed `filter_label` column in metric-routed serving tables.
   - Do not exhaust planner rounds on vendor/customer entity probes when dimension filter scope is already established.

4. **Phase-1 for reference dimensions**
   - When the user supplies a label value for a reference dimension, Phase-1 may validate on the dimension table (`filter_label` exact / fuzzy match) before fact aggregation — same discipline as entity label probes, but on the reference dim, not Entity Ontology dims.

5. **Breakdown vs filter**
   - `breakdown_dimension` = GROUP BY a column across rows.
   - Reference dimension filter = WHERE on a specific dimension value.
   - A question may use both; do not conflate them.

---

## Output hints (runtime)

When reference dimension scope is inferred, emit planning hints:

```text
dimension_filter=<filter_label>=<user_token>
reference_dimension_index_hit=<join_key>
```

Optional when index match is mechanical:

```text
reference_dimension_table_ref=tables/<dim_doc>.md
```

---

## Related references

- [entity-resolution.md](./entity-resolution.md) — entity Phase-1 and label probes
- [question-shape.md](./question-shape.md) — `entity_anchoring = dimension_filter`
- [metric-table-routing.md](./metric-table-routing.md) — serving table selection after scope is known
