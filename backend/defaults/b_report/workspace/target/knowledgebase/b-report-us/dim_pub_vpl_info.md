# DIM: Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group (`dim_us.dim_pub_vpl_info`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_vpl_info
- domain: b-report-us
- one_line_purpose: Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group
- layer_type: DIM
- source_kind: contract_v2
- evidence_source: source/contracts/b-report-us/tables/dim_pub_vpl_info.md
- knowledgebase_path: target/knowledgebase/b-report-us/dim_pub_vpl_info.md
- contract_source: source/contracts/b-report-us/tables/dim_pub_vpl_info.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_vpl_info`
- **Layer type:** DIM
- **Canonical / derived:** Canonical shared dimension (B Report contract catalog)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** dimension key level (one row per business key)
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `vpl_no`, `vend_no`, `entry_id`, `alt_vend_no`, `alt_vpl_no`, `vpc_group_id`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country}.dim_pub_vpl_info` | Documented in B Report contract v2 |
| Vertica | yes | `dim_us.dim_pub_vpl_info` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_vpl_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_vpl_info.json` |
| **column_count** | 22 |
| **partition_keys** | `none` |
| **ddl_source** | B Report contract catalog — `source/contracts/b-report-us/tables/dim_pub_vpl_info.md` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dim_pub_vpl_info schema" --intent find_table_schema` |

### Lineage
- **upstream:** Curated DIM/ODS load jobs (per contract) — `source/contracts/b-report-us/tables/dim_pub_vpl_info.md:L1`
- **downstream:** B Report fact/DM serving tables and dashboards — `source/contracts/b-report-us/tables/dim_pub_vpl_info.md:L1`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | Not documented in repository |
| Schedule | Not documented in repository |
| Expected completion | 02:00-05:00 PT. |

---

## L2 Declarative Knowledge

### Business purpose
Vendor product line (VPL) reference — resolve `vpl_no` from `vpl_code` and link vendor/VPC group

This Knowledgebase entry is derived from the B Report US table contract catalog (`contract_v2`). ETL SQL for the pub_dw dimension load is **not in the b-report-us Bitbucket ETL snapshot**; see cross-domain Knowledgebase references when listed under Related scripts.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: `dim_pub_part_info`, `dws_disty_brpt_vpl_1d`, `pl_extend` VPL attributes. |
| **Sales / PM / finance** | Lookup attributes joined to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` and serving DM/DWS tables. |
| **Data engineering** | Stable dimension contract for join keys and attribute definitions. |

### Identifier search profile
- Primary lookup keys: `vpl_no`, `vend_no`, `entry_id`, `alt_vend_no`, `alt_vpl_no`, `vpc_group_id`
- Join hub facts on documented key columns; use `date_flag` snapshot partitions on `_df` variants when applicable.

### Time field semantics
- **`date_flag`:** primary filter when table is partitioned; otherwise use hub `date_flag` for as-of reporting.
- **Period semantics:** per ETL partition scope.





### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `dsv_min_amt` | `dsv_min_amt` | dsv_min_amt at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `dsv_min_amt` | unspecified | `dsv_min_amt` | Not in metric-index.md |

### etl_metrics

No governed logical metrics from `source/contracts/b-report-us/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
- Use when user provides VPL code/description instead of integer `vpl_no`.
- VPL-level metrics: prefer `dw_us.dws_disty_brpt_vpl_1d` / `*_vpl_mtd` serving tables when available.
- `vpl_code` is not unique — always resolve to `vpl_no` before joining facts; disambiguate with `vend_no` when multiple matches.
- Facts carry `vpl_no` (int); `vpl_code` is on this dimension or denormalized on `pl_extend` / part dim.

### Dimension join patterns
- Primary key: `vpl_no`
- Fact join: `fact.vpl_no = dim_pub_vpl_info.vpl_no`
- Vendor: `dim_pub_vpl_info.vend_no = dim_pub_vendor_info.vend_no`
- Part: `dim_pub_part_info.vpl_no = dim_pub_vpl_info.vpl_no`
- Hierarchy: `dim_pub_vpl_hierarchy_info.vpl_no = dim_pub_vpl_info.vpl_no`
- As-of join: `dim_pub_vpl_info_df` on `vpl_no` AND `date_flag`

### Key filters and ETL business logic
- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard time-filter SQL
```sql
-- See contract L3 Standard Time-Filter SQL in source/contracts/b-report-us/tables/dim_pub_vpl_info.md
```

### End-to-end flow
1. Upstream DIM/ODS load populates `dim_us.dim_pub_vpl_info` (ETL not in b-report-us Bitbucket snapshot).
2. B Report fact and serving jobs join this dimension for attribute enrichment.
3. Vertica consumers query `dim_us.dim_pub_vpl_info` for reporting.

```mermaid
flowchart LR
  upstream["Upstream DIM/ODS loads"]
  dim["dim_us.dim_pub_vpl_info"]
  hub["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  dm["B Report DM/DWS serving"]
  upstream --> dim
  dim --> hub
  hub --> dm
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_vpl_info` | Primary dimension catalog object (contract v2) |

### Step-by-step logic
N/A — catalog-only. Procedural ETL steps for this pub_dw dimension are not present in `source/contracts/b-report-us/bitbicket_etl/`. See cross-domain Knowledgebase paths under L6 Related scripts when available.

### Sentinel and code values
| Value | Type | Meaning |
|-------|------|---------|
| — | — | See contract `domain-knowledge.md` and `metric-index.md` for coded fields |

---

## L4 Validation

### Resolved partition value
| Step | Source | How `partition` is determined |
|------|--------|-----------------------------------------------------|
| 1 | B Report contract L1 | None explicit — full-table dimension or non-partitioned object per contract. |

**Plain language:** Non-partitioned dimension — full-table or as-of join via hub `date_flag`.

### Data quality checks
- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.
- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.
- No active conflicts on dimension grain or key semantics as of 2026-06-25.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vpl_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY vpl_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vpl_no, vend_no, entry_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_vpl_info
WHERE date_flag = '${partition_value}'
GROUP BY vpl_no, vend_no, entry_id, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- Contract-derived catalog; pub_dw ETL script path not verified in b-report-us Bitbucket snapshot.
- Cross-engine parity: compare Hive vs Vertica row counts when auditing.
- No active conflicts on dimension grain or key semantics as of 2026-06-25.

### Conflicts and open questions
- pub_dw Bitbucket ETL path: Not documented in repository (dimension maintained in pub_dw project).
- hive2vertica sync job file:line evidence: Not documented in repository.

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_vpl_info` | `dim_us.dim_pub_vpl_info` | overwrite / incremental | `source/contracts/b-report-us/tables/dim_pub_vpl_info.md:L5` | yes |
| **Hive alternative** | `dim_us.dim_pub_vpl_info` | same as reporting table | — | B Report contract | — |

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access constraints
- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | no |
| scan_risk_tier | low |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Consumer | Use case |
|----------|----------|
| Consumers: `dim_pub_part_info`, `dws_disty_brpt_vpl_1d`, `pl_extend` VPL attributes. | B Report / POS dimension enrichment |
| Use cases: VPL code resolution, vendor linkage, VPC group classification for profitability cuts. | B Report / POS dimension enrichment |

### Representative query patterns
```sql
SELECT vpl_no, vpl_code, vpl_desc, vend_no, vpc_group_id, vpc_group_desc
FROM dim_us.dim_pub_vpl_info
WHERE vpl_code ILIKE 'HP%'
ORDER BY vpl_no
LIMIT 20;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_vpl_info.md` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report hub and serving tables | `source/contracts/b-report-us/tables/dim_pub_vpl_info.md:L6` — see contract L6 |

#### Operational detail (verified)
- Load pattern: Not documented in repository — `source/contracts/b-report-us/tables/dim_pub_vpl_info.md:L1`
- Column count: 22 (B Report contract catalog)

#### Not documented in repository
- pub_dw ETL SQL and Azkaban `.flow` for this dimension
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dim_pub_vpl_info.md` — B Report contract source — `source/contracts/b-report-us/tables/dim_pub_vpl_info.md`
- `target/knowledgebase/vendor/dim_pub_vpl_info.md` — cross-domain Knowledgebase entry for same table object

---

*Document generated from `source/contracts/b-report-us/tables/dim_pub_vpl_info.md` (contract_v2).*
