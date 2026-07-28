# DIM: US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy (`dim_us.dim_pub_sales_territory`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_sales_territory
- domain: b-report-us
- one_line_purpose: US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy
- layer_type: DIM
- source_kind: contract_v2
- evidence_source: source/contracts/b-report-us/tables/dim_pub_sales_territory.md
- knowledgebase_path: target/knowledgebase/b-report-us/dim_pub_sales_territory.md
- contract_source: source/contracts/b-report-us/tables/dim_pub_sales_territory.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_sales_territory`
- **Layer type:** DIM
- **Canonical / derived:** Canonical shared dimension (B Report contract catalog)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per `sales_terr` per `date_flag` snapshot (Vertica mirror); CIS territory master attributes plus denormalized sub-group/group descriptions.
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** `date_flag` — business date filter per B Report contract.
- **Natural key:** `sales_terr`, `entry_id`, `cust_type`, `group_id`, `primary_id`, `backup_id1`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country}.dim_pub_sales_territory` | Documented in B Report contract v2 |
| Vertica | yes | `dim_us.dim_pub_sales_territory` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_sales_territory` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_sales_territory.json` |
| **column_count** | 33 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog — `source/contracts/b-report-us/tables/dim_pub_sales_territory.md` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dim_pub_sales_territory schema" --intent find_table_schema` |

### Lineage
- **upstream:** Curated DIM/ODS load jobs (per contract) — `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:L1`
- **downstream:** B Report fact/DM serving tables and dashboards — `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:L1`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | Not documented in repository |
| Schedule | Not documented in repository |
| Expected completion | 02:00-03:30 PT. |

---

## L2 Declarative Knowledge

### Business purpose
US sales territory master — resolve `sales_terr` from territory names and enrich sub-group/group hierarchy

This Knowledgebase entry is derived from the B Report US table contract catalog (`contract_v2`). ETL SQL for the pub_dw dimension load is **not in the b-report-us Bitbucket ETL snapshot**; see cross-domain Knowledgebase references when listed under Related scripts.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report `pl_extend` / `cust_mtd` pre-load, `dim_pub_customer_info` territory enrichment, territory serving marts (`dws_disty_brpt_terr_*`). |
| **Sales / PM / finance** | Lookup attributes joined to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` and serving DM/DWS tables. |
| **Data engineering** | Stable dimension contract for join keys and attribute definitions. |

### Identifier search profile
- Primary lookup keys: `sales_terr`, `entry_id`, `cust_type`, `group_id`, `primary_id`, `backup_id1`, `backup_id2`, `backup_id3`
- Join hub facts on documented key columns; use `date_flag` snapshot partitions on `_df` variants when applicable.

### Time field semantics
- **`date_flag`:** primary filter when table is partitioned; otherwise use hub `date_flag` for as-of reporting.
- **Period semantics:** per ETL partition scope.





### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/b-report-us/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
- Use when resolving territory names to `sales_terr` or enriching `cust_terr` with `terr_name`, sub-group/group hierarchy.
- B Report serving tables often denormalize territory labels — prefer `dws_disty_brpt_terr_mtd` / `dws_disty_brpt_cust_mtd` for metric questions when territory attributes are already present.
- As-of joins: use `dim_pub_sales_territory_df` on `sales_terr` AND `date_flag` (B Report `pl_extend` pattern); Vertica `dim_pub_sales_territory` carries the latest synced snapshot day.
- For sales-rep / manager / director / VP labels by territory, prefer `dim_pub_sales_hierarchy_primary_role_by_terr_view` over reconstructing from `primary_id` alone.
- Facts carry `cust_terr` (int); they do **not** have `terr_name` — filter user territory tokens via this dimension or denormalized serving slice.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension join patterns
- Primary key: `sales_terr`
- Fact join: `fact.cust_terr = dim_pub_sales_territory.sales_terr` (and `fact.date_flag = dim.date_flag` for snapshot/as-of)
- Customer master: `dim_pub_customer_info.sales_terr = dim_pub_sales_territory.sales_terr`
- Cust type decode: `dim_pub_sales_territory.cust_type = dim_pub_sales_cust_type.cust_type`
- Sales hierarchy (preferred): `dim_pub_sales_hierarchy_primary_role_by_terr_view.sales_terr = dim_pub_sales_territory.sales_terr`
- High-risk pitfalls: matching user text to integer `sales_terr`; joining without `date_flag` alignment on historical `_df` snapshots; duplicate `terr_name` labels mapping to multiple territories — aggregate at `sales_terr` after resolution

### Key filters and ETL business logic
- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard time-filter SQL
```sql
-- See contract L3 Standard Time-Filter SQL in source/contracts/b-report-us/tables/dim_pub_sales_territory.md
```

### End-to-end flow
1. Upstream DIM/ODS load populates `dim_us.dim_pub_sales_territory` (ETL not in b-report-us Bitbucket snapshot).
2. B Report fact and serving jobs join this dimension for attribute enrichment.
3. Vertica consumers query `dim_us.dim_pub_sales_territory` for reporting.

```mermaid
flowchart LR
  upstream["Upstream DIM/ODS loads"]
  dim["dim_us.dim_pub_sales_territory"]
  hub["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  dm["B Report DM/DWS serving"]
  upstream --> dim
  dim --> hub
  hub --> dm
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_sales_territory` | Primary dimension catalog object (contract v2) |

### Step-by-step logic
N/A — catalog-only. Procedural ETL steps for this pub_dw dimension are not present in `source/contracts/b-report-us/bitbicket_etl/`. See cross-domain Knowledgebase paths under L6 Related scripts when available.

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| — | — | See contract `domain-knowledge.md` and `metric-index.md` for coded fields |

---

## L4 Validation

### Resolved partition value
| Step | Source | How `date_flag` is determined |
|------|--------|-----------------------------------------------------|
| 1 | B Report contract L1 | `date_flag` — business date filter per B Report contract. |

**Plain language:** Partitioned dimension — filter reports on `date_flag` per contract.

### Data quality checks
- Verify row count stability day-over-day on active Vertica snapshot (~2,800 territories; slow growth as CIS adds territories).
- Monitor duplicate-key risk on `sales_terr` — must be unique per `date_flag` snapshot.
- For `terr_name`, spot-check null rate (20 nulls observed) and duplicate labels mapping to multiple `sales_terr` values.
- When joining from facts on `cust_terr`, validate match rate against `date_flag`-aligned `dim_pub_sales_territory_df` for historical months.
- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.
- No active conflicts on dimension grain or key semantics as of 2026-06-26.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT sales_terr, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY sales_terr
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT sales_terr, entry_id, cust_type, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = '${partition_value}'
GROUP BY sales_terr, entry_id, cust_type, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- Contract-derived catalog; pub_dw ETL script path not verified in b-report-us Bitbucket snapshot.
- Cross-engine parity: compare Hive vs Vertica row counts when auditing.
- No active conflicts on dimension grain or key semantics as of 2026-06-26.

### Conflicts and open questions
- pub_dw Bitbucket ETL path: Not documented in repository (dimension maintained in pub_dw project).
- hive2vertica sync job file:line evidence: Not documented in repository.

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_sales_territory` | `dim_us.dim_pub_sales_territory` | overwrite / incremental | `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:L5` | yes |
| **Hive alternative** | `dim_us.dim_pub_sales_territory` | same as reporting table | — | B Report contract | — |

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access constraints
- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes |
| scan_risk_tier | low |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Consumer | Use case |
|----------|----------|
| Consumers: B Report `pl_extend` / `cust_mtd` pre-load, `dim_pub_customer_info` territory enrichment, territory serving marts (`dws_disty_brpt_terr_*`). | B Report / POS dimension enrichment |
| Use cases: territory name resolution, sub-group/group hierarchy labels, credit-territory classification (`cust_type`, `house`), rep assignment metadata on territory master. | B Report / POS dimension enrichment |

### Representative query patterns
```sql
SELECT sales_terr, terr_name, sub_group_desc, group_desc, cust_type, region
FROM dim_us.dim_pub_sales_territory
WHERE date_flag = (SELECT MAX(date_flag) FROM dim_us.dim_pub_sales_territory)
  AND terr_name ILIKE '%Northeast%'
ORDER BY sales_terr
LIMIT 20;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_sales_territory.md` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report hub and serving tables | `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:L6` — see contract L6 |

#### Operational detail (verified)
- Load pattern: Not documented in repository — `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:L1`
- Column count: 33 (B Report contract catalog)

#### Not documented in repository
- pub_dw ETL SQL and Azkaban `.flow` for this dimension
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dim_pub_sales_territory.md` — B Report contract source — `source/contracts/b-report-us/tables/dim_pub_sales_territory.md`
- No additional cross-domain Knowledgebase entries with matching table stem.

---

*Document generated from `source/contracts/b-report-us/tables/dim_pub_sales_territory.md` (contract_v2).*
