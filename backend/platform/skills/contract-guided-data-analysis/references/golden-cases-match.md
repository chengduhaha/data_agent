# Golden Cases Matching (Optional, Domain-Local)

## Disabled by default

**Do not read, load, or match against `eval/golden_cases.md` for any analysis right now**, even when the file exists for the resolved domain. Skip this stage entirely and route directly from `metric-index.md` + table contracts (see [`domain-routing.md`](domain-routing.md), [`metric-table-routing.md`](metric-table-routing.md)).

- Set `golden_case_id: not_consulted` (not `none`) in the analysis artifact while this gate is active — `none` implies the file was checked and had no match; `not_consulted` records that the stage was intentionally skipped.
- **Exception:** only consult `eval/golden_cases.md` when the user explicitly asks, in that turn, to use/refer to golden cases (e.g. "use the golden case for this", "check golden_cases.md"). In that case, follow the rest of this file normally.
- This gate does not change the separate, permanent **Forbidden** rule below (`golden-questions.md` stays forbidden regardless).

---

## Forbidden

Never read, load, or cite `knowledge/contracts/**/golden-questions.md`.

---

## When to run (only if the user explicitly asked to use golden cases — see gate above)

After metric resolution and domain resolution, **before** SQL compilation:

1. Check if `knowledge/contracts/{domain}/eval/golden_cases.md` exists
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
