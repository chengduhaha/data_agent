# Local-First Research Gate

## Purpose

All routing, semantics, grain, joins, metric formulas, and SQL shape must be resolved from **local repository artifacts** before any external MCP call.

**Research** = what to query, which table, columns, filters, certified SQL pattern.  
**Execution** = running a designed SELECT for evidence numbers.

---

## Allowed local sources (in order)

| Step | Path |
|------|------|
| Domain | `/knowledge/org/source/contracts/{domain}/domain-knowledge.md` |
| Metrics | `/knowledge/org/source/contracts/{domain}/metric-index.md` |
| Special logic | `/knowledge/org/source/ref/{domain}/special_logic.txt`, `table list.txt`, `table relationship.txt` (if present for domain) — always check `special_logic.txt` for the resolved table(s), see [`special-logic-check.md`](special-logic-check.md) |
| Storage metadata | `/knowledge/org/target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/` (table/column metadata), `/knowledge/org/target/storage/wkb/indexes/**` |
| Tables | `/knowledge/org/target/knowledgebase/{domain}/{stem}.md` (L1/L2/L3/L6 as needed); **NEVER** read `/knowledge/org/source/contracts/{domain}/tables/*.md` |

WKB catalogue is local — use `python /knowledge/org/target/storage/wkb/indexing/run_query.py`, not full-tree grep.

---

## Forbidden for research

| Tool / path | Rule |
|-------------|------|
| `/knowledge/org/source/contracts/**/golden-questions.md` | **Never** read, cite, or match |
| `/knowledge/org/source/contracts/b-report-us/tables/**`, `/knowledge/org/source/contracts/pos/tables/**` | **NEVER** read for any request in this skill, at any stage |
| Bitbucket MCP (`user-gateway-bitbucket-prod`) | No remote fetch for table/metric/schema/join discovery |
| Vertica metadata tools | No `get_table_structure`, `get_schema_tables`, `get_schema_views`, `get_table_projections`, `get_database_schemas` |
| Exploratory Vertica | No `SELECT *` or schema sampling to learn semantics |
| Broad `source/etl/**` grep | Only via WKB `l3_code`/`l4_flow` hit with known path |
| Cross-domain hop | Do not switch domain to force an answer |

---

## MCP allowed only after compile plan exists

### Vertica (`gateway-vertica-prod`)

- `run_query_safely` — aggregated evidence SQL from local contracts
- Bounded Phase-1 entity label probe on **contract-named** dim varchar columns (`LIMIT 20`)

### Bitbucket (exception only)

- User explicitly requests ETL source review **and**
- WKB `l3_code`/`l4_flow` or knowledgebase L4 already names the flow/script path

---

## KB gap stop

If local stack cannot resolve a required field:

1. Record **Open questions** with files checked
2. Do **not** backfill via Bitbucket or Vertica discovery
3. Answer **no data found** when metric/table/SQL cannot be assembled

---

## Methodology disclosure

Analysis artifact must include:

- `local_research_sources`: list of contract/WKB/knowledgebase paths used
- `external_mcp_research: none` unless documented Bitbucket exception

---

## Gate before MCP

At `compile_sql` stage, confirm:

- [ ] Domain resolved
- [ ] Metric id(s) from `metric-index.md`
- [ ] Special logic checked (`/knowledge/org/source/ref/{domain}/special_logic.txt`, if present for domain)
- [ ] Table FQN(s) from contracts, golden case, or storage-layer `l1_catalog` metadata
- [ ] Partition filter column from local L1/L3
- [ ] SQL compile plan documented

If any unchecked → stop with **no data found** or open questions; do not call Vertica for discovery.
