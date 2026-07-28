# SQL Planning (Contract Skill)

Contract-skill SQL planning. **golden-questions.md removed** from priority chain.

## KB-Assembled Default Time

When `temporal_obligation = kb_default_eligible`, verify certified default period assembly in contracts.

### Priority for default-period assembly

Check in this order:

1. `knowledge/contracts/{domain}/eval/golden_cases.md` routing-certified case — **skip by default** (disabled; see [`golden-cases-match.md`](golden-cases-match.md)); only check when the user explicitly asks to use golden cases
2. `knowledge/contracts/{domain}/metric-index.md` default reporting period or metric-specific time policy
3. Selected table L6 routing-certified snippets in `knowledge/knowledgebase/{domain}/{stem}.md`
4. Entity Resolution Assembly in table docs
5. `knowledge/contracts/{domain}/domain-knowledge.md` Time Scope Ontology
6. Table L3 Standard Time-Filter SQL (`knowledge/knowledgebase/{domain}/{stem}.md`)

**Forbidden:** `golden-questions.md`. Do not borrow time logic from unrelated domains.

### If certified default exists

```json
{
  "mode": "kb_assembly_default",
  "status": "confirmed",
  "source_artifact": "knowledge/contracts/{domain}/...",
  "requires_user_clarification": false
}
```

### If no certified default

Ask concise time clarification **only** when the question/data leaves time ambiguous or missing for this shape (`user_must_specify` / no safe assembly). Otherwise proceed or answer **no data found** if scope cannot be assembled locally — do **not** ask for KB-owned period rules.

---

## Schema and column policy

- Column names from contract L1 Column Catalog, confirmed against `knowledge/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/columns.parquet` when available
- Metric expressions from `metric-index.md` `final_effective_formula_sql`
- Forbidden aliases: see `domain-knowledge.md` Forbidden Column Aliases
- Partition filter from table L3 time snippets
- Filter/join exceptions from `knowledge/ref/{domain}/special_logic.txt` and `table relationship.txt` (see [`special-logic-check.md`](special-logic-check.md)) take precedence over assumed defaults when a matching rule exists

---

## Anti-duplication before SUM

Per [`metric-table-routing.md`](metric-table-routing.md): verify pre-aggregated grain before summing DWS/DM tables.

---

## Related local references

- [`metric-table-routing.md`](metric-table-routing.md) — metric/table routing and pre-aggregate grain checks
- [`fiscal-calendar.md`](fiscal-calendar.md) — fiscal / calendar time assembly
- [`entity-resolution.md`](entity-resolution.md) — Phase-1 entity probes
- [`special-logic-check.md`](special-logic-check.md) — domain special_logic filter exceptions
