# SQL Planning (Contract Skill)

Contract-skill SQL planning. **golden-questions.md removed** from priority chain.

## KB-Assembled Default Time

When `temporal_obligation = kb_default_eligible`, verify certified default period assembly in contracts.

### Priority for default-period assembly

Check in this order:

1. `/knowledge/org/source/contracts/{domain}/eval/golden_cases.md` routing-certified case (when file exists and matches)
2. `/knowledge/org/source/contracts/{domain}/metric-index.md` default reporting period or metric-specific time policy
3. Selected table L6 routing-certified snippets in `/knowledge/org/target/knowledgebase/{domain}/{stem}.md`
4. Entity Resolution Assembly in table docs
5. `/knowledge/org/source/contracts/{domain}/domain-knowledge.md` Time Scope Ontology
6. Table L3 Standard Time-Filter SQL (`/knowledge/org/target/knowledgebase/{domain}/{stem}.md`)

**Forbidden:** `golden-questions.md`. Do not borrow time logic from unrelated domains.

### If certified default exists

```json
{
  "mode": "kb_assembly_default",
  "status": "confirmed",
  "source_artifact": "source/contracts/{domain}/...",
  "requires_user_clarification": false
}
```

### If no certified default

Ask concise time clarification or answer **no data found** if scope cannot be assembled locally.

---

## Schema and column policy

- Column names from contract L1 Column Catalog, confirmed against `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/columns.parquet` when available
- Metric expressions from `metric-index.md` `final_effective_formula_sql`
- Forbidden aliases: see `domain-knowledge.md` Forbidden Column Aliases
- Partition filter from table L3 time snippets
- Filter/join exceptions from `/knowledge/org/source/ref/{domain}/special_logic.txt` and `table relationship.txt` (see [`special-logic-check.md`](special-logic-check.md)) take precedence over assumed defaults when a matching rule exists

---

## Anti-duplication before SUM

Per [`metric-table-routing.md`](metric-table-routing.md): verify pre-aggregated grain before summing DWS/DM tables.

---

## Related local references

- [`metric-table-routing.md`](metric-table-routing.md) — metric/table routing and pre-aggregate grain checks
- [`fiscal-calendar.md`](fiscal-calendar.md) — fiscal / calendar time assembly
- [`entity-resolution.md`](entity-resolution.md) — Phase-1 entity probes
- [`special-logic-check.md`](special-logic-check.md) — domain special_logic filter exceptions

---

## P&L item semantics (NGM decomposition) — data_agent

When the user asks for **P&L items** (or "Profit&Loss items") in the context of NGM / margin / B Report P&L:

| Interpretation | Guidance |
|----------------|----------|
| **Correct** | Physical **additive component columns** of `ngm_amt` per `/knowledge/org/source/contracts/{domain}/metric-index.md` (`final_effective_formula_sql` + `formula_component_breakdown`) — e.g. `gm_amt`, `btl`, `trans_btl`, `one_time_btl`, `pdt`, `ap_finance`, `cust_rebate`, freight/warehouse/finance/overhead columns |
| **Wrong — no such column** | `pl_item`, `pl_item_code`, `pl_item_desc` — **not** present on DWS serving tables |
| **Wrong — unless user says product line / VPL** | `vpl_no`, `vpl_code`, `vpc_group_desc` breakdown |

**Column discovery (local only):**

1. Read `ngm_amt` `formula_component_breakdown` in `metric-index.md`
2. Cross-check physical column names on the routed table via WKB `l1_catalog/vertica_dw_us_<stem>.json` or knowledgebase **Core measures**
3. Use only columns confirmed in both formula semantics and catalog — never invent dimensions

### Table routing for P&L decomposition

| Question scope | Preferred table | Aggregation notes |
|----------------|-----------------|-------------------|
| Vendor (`vend_no`, brand) | `dw_us.dws_disty_brpt_vend_mtd` | Filter `vend_no`; **`SUM(ifnull(col,0))` per period with `GROUP BY vend_no`** |
| Company-wide (no entity filter) | `dw_us.dws_disty_brpt_pl_extend_mtd` | Sum each component column per month-end `date_flag`; rank by `ABS(apr - mar)` |
| Customer slice | `dw_us.dws_disty_brpt_cust_mtd` | `GROUP BY cust_no`, `WHERE cust_no > 0` |

### SQL pattern — component period comparison

Build one CTE per period (month-end `date_flag` from `dim_us.dim_pub_date`), each `SELECT SUM(ifnull(gm_amt,0)) AS gm_amt, SUM(ifnull(btl,0)) AS btl, ...` with appropriate entity filter (or none for company-wide).

**Vertica MCP constraint (data_agent / gateway):** `run_query_safely` may **reject** queries with many `UNION ALL` branches. Use **wide period CTEs** (`mar_agg` / `apr_agg` / `apr25_agg`) and present components in the answer table — **never** use a column named `pl_item`.

---

## MoM / YoY ranking — data_agent

| User phrasing | Rank by |
|---------------|---------|
| "MoM %" / "MoM Top N" (default) | `mom_pct ASC` for largest **decrease**; `DESC` for increase/growth |
| "absolute variance" / "delta" | `ABS(delta)` |

Customer NGM MoM top-N: `dws_disty_brpt_cust_mtd` + **`SUM(ngm_amt) GROUP BY cust_no`** before period pivot.

**Month-end dates:** `dim_us.dim_pub_date` — `MAX(date_flag)` per calendar month; **do not** use `month_flag = 'Y'`.

---

## MTD vs comb_mtd — data_agent

Prefer `*_mtd` + month-end `date_flag` for explicit calendar months. Avoid `*_comb_mtd` for vendor/customer P&L decomposition unless question requires comb columns.
