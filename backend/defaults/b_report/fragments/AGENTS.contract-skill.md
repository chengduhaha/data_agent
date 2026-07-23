## Contract-guided data analysis

When the user's message matches the **contract-guided-data-analysis** skill (`/skills/org/contract-guided-data-analysis/SKILL.md`):

- **Use when:** KPI lookup, ranking, trend, comparison, variance drivers, POS/B Report metrics, validate numbers, data anomaly
- **Don't use when:** ETL change requests, flow edits, DDL/DML, unrestricted warehouse exploration, email intake

**First:** read the skill (`read_file`, limit ≥ 500), then read `/rules/org/contract-data-analysis-vertica.md` and `/rules/org/AGENTS.analysis-clarification.md` before any Vertica call.

1. Resolve domain per skill `references/domain-routing.md` — commonly `b-report-us` (B Report, P&L, NGM, `disty_brpt`) or `pos` (`common_pos`, POS metrics).
2. **Local research first** — read `/knowledge/org/source/contracts/{domain}/` (`domain-knowledge.md`, `metric-index.md`) and `/knowledge/org/source/ref/{domain}/` before any Vertica call. **Never** read `eval/golden_cases.md`.
3. **WKB retrieval** — use `wkb_query(query=..., intent=nl2sql_metric|find_table_schema)`; then open ≤3 `/knowledge/org/target/knowledgebase/{domain}/{stem}.md` where **`stem = FQN.split(".")[-1]`**. On index failure, route from `metric-index.md` only — do **not** paginate `l1_catalog` JSON with `read_file`.
4. **P&L items in NGM** — formula component columns from `metric-index.md` (`gm_amt`, `btl`, `ap_finance`, …); **not** `pl_item`; vendor scope → `vend_mtd` + `GROUP BY vend_no`; company-wide variance → `pl_extend_mtd`. See skill `references/sql-planning.md`.
5. **MoM Top-N rankings** — one table; default `ORDER BY mom_pct ASC`; month-end via `dim_pub_date` `MAX(date_flag)` per calendar month.
6. **Vertica is execution-only** via MCP server `gateway-vertica-prod` — see `/rules/org/contract-data-analysis-vertica.md`.
7. **Never** read `golden-questions.md`, `eval/golden_cases.md`, or `source/contracts/**/tables/**`.
8. **No cross-domain fallback** — if local routing or Vertica returns nothing, answer **no data found** with scope.
9. **Chat-only answers** — three sections (Summary / Evidence / Analysis approach & confidence). Do **not** write files under `/workspace/target/analysis/`.
10. **Efficiency** — do **not** delegate contract-guided analysis to the `task` subagent. Batch `read_file` when opening multiple contract references; avoid re-reading the same file in one segment.
