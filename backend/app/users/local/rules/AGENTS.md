# Agent Rules

## Identity
You are a general-purpose assistant running in a browser-based agent workspace.

## Workspace
- User files live under `/workspace/`. Prefer reading and writing there.
- Skills are available under `/skills/builtin/` and `/skills/user/`.
- Follow this AGENTS.md for project-specific conventions.

## Safety
- Ask before destructive shell commands when approval is required.
- Do not exfiltrate secrets or credentials.
- Prefer minimal, reversible changes.

## Style
- Be concise and actionable.
- Show your plan for multi-step work.

## Contract-guided data analysis

When the user's question matches the **contract-guided-data-analysis** skill (`/skills/user/contract-guided-data-analysis/SKILL.md`):

- **Use when:** KPI lookup, ranking, trend, comparison, variance drivers, POS/B Report metrics, validate numbers, data anomaly
- **Don't use when:** ETL change requests, flow edits, DDL/DML, unrestricted warehouse exploration, email intake

**First:** read the skill (`read_file`, limit ≥ 500), then read `/rules/contract-data-analysis-vertica.md` before any Vertica call.

1. Resolve domain per skill `references/domain-routing.md` — commonly `b-report-us` (B Report, P&L, NGM, `disty_brpt`) or `pos` (`common_pos`, POS metrics).
2. **Local research first** — read `/workspace/source/contracts/{domain}/` (`domain-knowledge.md`, `metric-index.md`, optional `eval/golden_cases.md`) and `/workspace/source/ref/{domain}/` before any Vertica call.
3. **WKB retrieval** — from cwd `/workspace`, run `python -m tools.wkb.indexing.run_query --query "..." --intent nl2sql_metric` (or `find_table_schema`). Then open ≤3 `/workspace/target/knowledgebase/{domain}/{stem}.md` files where **`stem = FQN.split(".")[-1]`**. Never open schema-prefixed filenames like `dw_us.xxx.md`. On 404, `ls` the knowledgebase folder and retry.
4. **P&L items in NGM** — formula component columns from `metric-index.md` (`gm_amt`, `btl`, `ap_finance`, …); **not** `pl_item`; vendor scope → `vend_mtd` + `GROUP BY vend_no`; company-wide variance → `pl_extend_mtd`. See skill `references/sql-planning.md`.
5. **MoM Top-N rankings** — one table; default `ORDER BY mom_pct ASC`; month-end via `dim_pub_date` `MAX(date_flag)` per calendar month.
6. **Vertica is execution-only** via MCP server `gateway-vertica-prod` — see `/rules/contract-data-analysis-vertica.md`.
7. **Never** read `golden-questions.md` or `source/contracts/**/tables/**`.
8. **No cross-domain fallback** — if local routing or Vertica returns nothing, answer **no data found** with scope.
9. **Chat-only answers** — three sections (Summary / Evidence / Analysis approach & confidence). Do **not** write files under `/workspace/target/analysis/`.
