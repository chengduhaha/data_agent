# Domain Routing

## Purpose

Resolve which contract domain applies and map WKB hits to contract table paths.

---

## Supported contract domains

| Domain folder | Typical cues | `knowledge/ref/{domain}/` special-logic set |
|---------------|--------------|-------------------------------------------|
| `b-report-us` | B Report, P&L, NGM, net sales, vendor/customer ranking, `dws_disty_brpt_*`, `dm_disty_brpt_*` | `special_logic.txt`, `table list.txt`, `table relationship.txt` |
| `pos` | POS, point of sale, `dwd_disty_common_pos_di`, SPA/SCM, shipped POS exports | `special_logic.txt`, `table list.txt`, `table relationship.txt` |

Read `knowledge/contracts/{domain}/README.md` when domain is ambiguous.

**This table is a convenience cue, not the source of truth.** Before skipping the special-logic-check stage for any domain, verify live via `knowledge/ref/{domain}/` folder existence (see `special-logic-check.md`) rather than relying solely on this row.

---

## Domain resolution order

1. User explicit domain name
2. Table FQN cues in question (`disty_brpt` → `b-report-us`; `common_pos` → `pos`)
3. `domain-knowledge.md` Business Perspective / hub table mentions
4. WKB rerank domain field on top hit

**No cross-domain fallback:** stay on resolved domain; if no routing → **no data found**.

---

## Contract root paths

```
knowledge/contracts/{domain}/
  domain-knowledge.md
  metric-index.md
  eval/golden_cases.md          # disabled by default; only consult if user explicitly asks (see golden-cases-match.md)
```

Table-level detail is read from `knowledge/knowledgebase/{domain}/{stem}.md`.

**Forbidden — NEVER use:**

- `knowledge/contracts/{domain}/tables/*.md` (i.e. `knowledge/contracts/b-report-us/tables/**`, `knowledge/contracts/pos/tables/**`)
- `knowledge/contracts/{domain}/golden-questions.md`

---

## WKB → knowledgebase path map

Order: `knowledge/ref/{domain}/special_logic.txt` (if present) → `knowledge/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` metadata search → `knowledge/knowledgebase/{domain}/`.

WKB snapshots/`l1_catalog` metadata may reference `knowledge/knowledgebase/{domain}/`. After the storage-layer search, **always** check `knowledge/knowledgebase/{domain}/` for the resolved stem:

| WKB / FQN signal | Knowledgebase table path |
|------------------|---------------------------|
| `qualified_name` e.g. `dw_us.dws_disty_brpt_vend_mtd` | `knowledge/knowledgebase/{domain}/dws_disty_brpt_vend_mtd.md` |
| `table_stem` from index title | `knowledge/knowledgebase/{domain}/{stem}.md` |

- Always check: `knowledge/knowledgebase/{domain}/{stem}.md` (same domain)
- **NEVER** read `knowledge/contracts/{domain}/tables/*.md`
- Record the knowledgebase source consulted in methodology

---

## Sections to read per table (token budget)

Read **only** what the question needs:

| Need | Sections |
|------|----------|
| Metric columns | L1 Column Catalog, L2 Metrics Served |
| Time filter | L3 Standard Time-Filter SQL |
| Entity join | L2 Dimension Lookup, L3 routing rules |
| Certified SQL | L6 Access and Consumption |

Maximum **3** table files per run unless user explicitly requests more.
