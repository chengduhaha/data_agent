# DIM: US vendor master — resolve `vend_no` from vendor names and enrich segment/master-vendor hierarchy (`dim_us.dim_pub_vendor_info`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_vendor_info
- domain: b-report-us
- one_line_purpose: US vendor master — resolve `vend_no` from vendor names and enrich segment/master-vendor hierarchy
- layer_type: DIM
- source_kind: contract_v2
- evidence_source: source/contracts/b-report-us/tables/dim_pub_vendor_info.md
- knowledgebase_path: target/knowledgebase/b-report-us/dim_pub_vendor_info.md
- contract_source: source/contracts/b-report-us/tables/dim_pub_vendor_info.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_vendor_info`
- **Layer type:** DIM
- **Canonical / derived:** Canonical shared dimension (B Report contract catalog)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** dimension key level (one row per business key)
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `vend_no`, `entry_id`, `buyer_no`, `company_no`, `universal_vend_no`, `master_vend_no`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country}.dim_pub_vendor_info` | Documented in B Report contract v2 |
| Vertica | yes | `dim_us.dim_pub_vendor_info` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_vendor_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_vendor_info.json` |
| **column_count** | 49 |
| **partition_keys** | `none` |
| **ddl_source** | B Report contract catalog — `source/contracts/b-report-us/tables/dim_pub_vendor_info.md` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dim_pub_vendor_info schema" --intent find_table_schema` |

### Lineage
- **upstream:** Curated DIM/ODS load jobs (per contract) — `source/contracts/b-report-us/tables/dim_pub_vendor_info.md:L1`
- **downstream:** B Report fact/DM serving tables and dashboards — `source/contracts/b-report-us/tables/dim_pub_vendor_info.md:L1`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | Not documented in repository |
| Schedule | Not documented in repository |
| Expected completion | 02:00-04:00 PT. |

---

## L2 Declarative Knowledge

### Business purpose
US vendor master — resolve `vend_no` from vendor names and enrich segment/master-vendor hierarchy

This Knowledgebase entry is derived from the B Report US table contract catalog (`contract_v2`). ETL SQL for the pub_dw dimension load is **not in the b-report-us Bitbucket ETL snapshot**; see cross-domain Knowledgebase references when listed under Related scripts.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report order-line and vendor serving marts, `dim_pub_part_info` vendor enrichment. |
| **Sales / PM / finance** | Lookup attributes joined to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` and serving DM/DWS tables. |
| **Data engineering** | Stable dimension contract for join keys and attribute definitions. |

### Identifier search profile
- Primary lookup keys: `vend_no`, `entry_id`, `buyer_no`, `company_no`, `universal_vend_no`, `master_vend_no`, `pur_vend_no`
- Join hub facts on documented key columns; use `date_flag` snapshot partitions on `_df` variants when applicable.

### Time field semantics
- **`date_flag`:** primary filter when table is partitioned; otherwise use hub `date_flag` for as-of reporting.
- **Period semantics:** per ETL partition scope.





### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `vend_pay_frt_amt` | `vend_pay_frt_amt` | vend_pay_frt_amt at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `vend_pay_frt_amt` | unspecified | `vend_pay_frt_amt` | Not in metric-index.md |

### etl_metrics

No governed logical metrics from `source/contracts/b-report-us/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
- Use for vendor name → `vend_no` resolution when serving table lacks denormalized `vend_name`.
- Vendor ranking metrics: prefer `dw_us.dws_disty_brpt_vend_mtd` — see golden `jan-vendor-top5-ranking`.
- Master-vendor roll-up: filter or group by `master_vend_no` / `master_vend_name` when user asks about manufacturer family.
- Facts carry `vend_no` (int); label columns are on this dimension or denormalized on serving marts.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension join patterns
- Primary key: `vend_no`
- Fact join: `fact.vend_no = dim_pub_vendor_info.vend_no`
- Master roll-up: `fact.master_vend_no = dim.master_vend_no` or join on `dim.master_vend_no`
- Part enrichment: `dim_pub_part_info.vend_no = dim_pub_vendor_info.vend_no`
- As-of join: `dim_pub_vendor_info_df` on `vend_no` AND `date_flag`
- High-risk pitfalls: `GROUP BY vend_name`; conflating `vend_no` with `master_vend_no`

### Key filters and ETL business logic
- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard time-filter SQL
```sql
-- See contract L3 Standard Time-Filter SQL in source/contracts/b-report-us/tables/dim_pub_vendor_info.md
```

### End-to-end flow
1. Upstream DIM/ODS load populates `dim_us.dim_pub_vendor_info` (ETL not in b-report-us Bitbucket snapshot).
2. B Report fact and serving jobs join this dimension for attribute enrichment.
3. Vertica consumers query `dim_us.dim_pub_vendor_info` for reporting.

```mermaid
flowchart LR
  upstream["Upstream DIM/ODS loads"]
  dim["dim_us.dim_pub_vendor_info"]
  hub["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  dm["B Report DM/DWS serving"]
  upstream --> dim
  dim --> hub
  hub --> dm
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_vendor_info` | Primary dimension catalog object (contract v2) |

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
FROM dim_us.dim_pub_vendor_info
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vend_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_vendor_info
WHERE date_flag = '${partition_value}'
GROUP BY vend_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vend_no, entry_id, buyer_no, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_vendor_info
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, entry_id, buyer_no, date_flag
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
| **Query for reporting** | `dim_us.dim_pub_vendor_info` | `dim_us.dim_pub_vendor_info` | overwrite / incremental | `source/contracts/b-report-us/tables/dim_pub_vendor_info.md:L5` | yes |
| **Hive alternative** | `dim_us.dim_pub_vendor_info` | same as reporting table | — | B Report contract | — |

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
| Consumers: B Report order-line and vendor serving marts, `dim_pub_part_info` vendor enrichment. | B Report / POS dimension enrichment |
| Use cases: vendor name resolution, master-vendor roll-ups, segment classification. | B Report / POS dimension enrichment |

### Representative query patterns
```sql
SELECT vend_no, vend_name, master_vend_no, master_vend_name, vend_seg_code, vend_segment
FROM dim_us.dim_pub_vendor_info
WHERE vend_name ILIKE '%CISCO%'
   OR master_vend_name ILIKE '%CISCO%'
ORDER BY vend_no
LIMIT 20;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_vendor_info.md` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report hub and serving tables | `source/contracts/b-report-us/tables/dim_pub_vendor_info.md:L6` — see contract L6 |

#### Operational detail (verified)
- Load pattern: Not documented in repository — `source/contracts/b-report-us/tables/dim_pub_vendor_info.md:L1`
- Column count: 49 (B Report contract catalog)

#### Not documented in repository
- pub_dw ETL SQL and Azkaban `.flow` for this dimension
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dim_pub_vendor_info.md` — B Report contract source — `source/contracts/b-report-us/tables/dim_pub_vendor_info.md`
- `target/knowledgebase/vendor/dim_pub_vendor_info.md` — cross-domain Knowledgebase entry for same table object

---

*Document generated from `source/contracts/b-report-us/tables/dim_pub_vendor_info.md` (contract_v2).*
