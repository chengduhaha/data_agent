# Golden Cases Matching (Optional, Domain-Local)

## Forbidden

Never read, load, or cite `/knowledge/org/source/contracts/**/golden-questions.md`.

---

## When to run

After metric resolution and domain resolution, **before** SQL compilation:

1. Check if `/knowledge/org/source/contracts/{domain}/eval/golden_cases.md` exists
2. If **no file** → skip stage; route via `metric-index.md` + table contracts only
3. If **file exists** → load case index table (id, intent, table_fqn, status)

No hardcoded domain list — any domain with `eval/golden_cases.md` participates.

---

## Match criteria

Match user question to a case on:

- intent class (metric_lookup, ranking, trend, metric_comparison, diagnostic_slice, …)
- metric aliases from `metric-index.md`
- entity type / grain cues
- `table_fqn` from case index and `dimension_slice_routing`

---

## If `routing-certified` match

1. Read case detail section for certified SQL shape
2. Or follow table L6 `golden_ref` pointing to a `golden_cases` id
3. Substitute **only** runtime parameters (period, entity keys, LIMIT)
4. Set provenance tier `routing_certified_golden`
5. Record `golden_case_id` in analysis artifact

---

## No data found fallbacks (mandatory)

| Condition | Response |
|-----------|----------|
| No `eval/golden_cases.md` and metric-index + tables cannot assemble SQL | **No data found** — list domain + files checked |
| Golden file present, no case match, metric-index routing insufficient | **No data found** |
| SQL runs, zero rows for stated scope | **No data found** — include period/filters |
| Entity Phase-1 returns zero matches | **No data found** for entity scope |

Do **not** switch domain to find a substitute table or golden case.

---

## If no golden match but routing succeeds

- Proceed with `metric-index.md` + table contract assembly
- Set `golden_case_id: none`
- Continue to WKB retrieve and SQL compile
