# Special Logic Check

Runs **after** `metric-index.md` and **before** the storage-layer (`l1_catalog`) metadata search. Applies whenever the resolved domain has a `/workspace/source/ref/{domain}/` reference set.

---

## Files

| Path | Use |
|------|-----|
| `/workspace/source/ref/{domain}/special_logic.txt` | Historical exception patterns for filters/columns (e.g. `order_line_type`, `order_type`, RMA/int_ref tracing) tied to specific tables. **Always check** for any table resolved in this run. |
| `/workspace/source/ref/{domain}/table list.txt` | Physical source table inventory for the domain (region placeholder `xx`). |
| `/workspace/source/ref/{domain}/table relationship.txt` | Verified join cardinality/columns between domain tables (grain, driving table, join keys). |

Currently populated for `pos` (`/workspace/source/ref/pos/`) and `b-report-us` (`/workspace/source/ref/b-report-us/`).

**Do not trust this list alone — it goes stale when new `/workspace/source/ref/{domain}/` folders are added.** Before marking this stage `not_applicable`, check live whether `/workspace/source/ref/{domain}/` exists (e.g. list the directory) for the resolved domain. Only skip and record `special_logic_checked: not_applicable` if that live check confirms no folder is present.

---

## Procedure

1. After metric/table candidates are identified from `metric-index.md` (and `domain-knowledge.md`), open `/workspace/source/ref/{domain}/special_logic.txt`.
2. Search for the resolved table name(s) or the columns/filters the plan will use (e.g. `order_line_type`, `order_type`, `int_ref_type`).
3. If a matching special-logic rule exists:
   - Apply the documented default (e.g. exclude `Comp` unless the request matches a listed exception).
   - Note the applied rule and its default vs. exception status in the analysis methodology.
   - For `b-report-us` / `dwd_disty_brpt_orders_pl_etl_mi`: `segment_exclude = 'N'` is the default profitability filter. Do **not** also apply `dim_pub_order_type.sales = 'Y'`, `virtual_type = 0`, or `order_type = 1` unless the question explicitly asks for shipped orders only (or that specific scope).
   - For `b-report-us` vendor-number questions on tables that have `dim_vend_no` (notably `dwd_disty_brpt_orders_pl_etl_mi`): always use `dim_vend_no`, not `vend_no` (see `special_logic.txt` rule #18). On tables that only expose `vend_no`, keep using `vend_no`.
4. If the plan involves a join or grain not already confirmed by `metric-index.md`/`domain-knowledge.md`, cross-check `table relationship.txt` for the certified join columns and cardinality (many-to-one, one-to-many) before compiling SQL.
5. Use `table list.txt` only to confirm a physical table is in-scope for the domain; it is not a substitute for column-level detail (use `l1_catalog` / knowledgebase for that).
6. Record in methodology: `special_logic_checked: yes|no|not_applicable` and which rule(s), if any, were applied.

---

## Interaction with other stages

- Runs before storage-layer (`l1_catalog`) search and before knowledgebase docs are opened — special logic can change which table/columns you even need to look up.
- Does not replace `metric-index.md` routing; it only supplies filter/join exceptions and verified relationships that contracts and knowledgebase docs may not restate.
- If `special_logic.txt` contradicts a knowledgebase L3 filter snippet, prefer the more specific/recent source and flag the conflict as an **Open question** rather than silently picking one.
