# Analysis Output Contract

## Chat-only runtime (data_agent)

Answers render in the chat thread only. Do **not** write files under `/workspace/target/analysis/`.

Use [`output-contract.md`](output-contract.md) three-section format in the chat response.

---

## Methodology fields (disclose in chat when relevant)

- `local_research_sources` — contract / special-logic / storage-layer (`l1_catalog`) / knowledgebase paths
- `external_mcp_research: none` | `bitbucket_exception` (path + reason)
- `metric-index` entries used (formula + verification status)
- `special_logic_checked: yes|no|not_applicable`
- WKB / `l1_catalog` candidates (top 5 ids)
- SQL strategy (aggregated vs detail)

---

## Forbidden in output

- Never cite or reference `golden-questions.md` or `eval/golden_cases.md`
- Never cite or reference `source/contracts/{domain}/tables/*.md`
- No Bitbucket paths unless documented exception
- No full-row dumps from Vertica

---

## Metric-index citation

Every metric in the answer must cite:

- metric id from `source/contracts/{domain}/metric-index.md`
- `formula_verification_status` when used in SQL

---

## Validation scenarios (post-implementation)

| # | Scenario | Expected |
|---|----------|----------|
| 1 | PM-scoped NGM% MoM comparison with explicit `pm_id` and two calendar months | `metric-index` routes `dm_disty_brpt_pm_comb_mtd`; aggregated Vertica query; `result_status: data_found` or scoped no_data_found |
| 2 | Domain without full metric-index coverage (e.g. pos); hub table routed | metric-index routing; evidence or no_data_found |
| 3 | Scoped Vertica query returns 0 rows | Answer **no data found** with period/filters; no domain hop |
| 4 | Local routing cannot compile SQL | **no data found** before Vertica; list files checked |
| 5 | Research phase | No Bitbucket MCP; no Vertica metadata tools; `external_mcp_research: none` |
| 6 | Forbidden file | Agent never opens `golden-questions.md`, `eval/golden_cases.md`, or `source/contracts/{domain}/tables/*.md` |
| 7 | WKB intent | Only `nl2sql_metric`, `find_table_schema`, `data_engineering` — never `incident_debug` |
| 8 | Token budget | ≤2 domain files + ≤3 table files before SQL |
| 9 | POS domain, table resolved | `special_logic.txt` checked for that table; applied rule (if any) recorded in methodology |
| 10 | Domain with no `source/ref/{domain}/` folder | `special_logic_checked: not_applicable`; proceeds to storage-layer/knowledgebase search |
