# DIM: US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy (`dim_us.dim_pub_customer_info`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_customer_info
- domain: b-report-us
- one_line_purpose: US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy
- layer_type: DIM
- source_kind: contract_v2
- evidence_source: source/contracts/b-report-us/tables/dim_pub_customer_info.md
- knowledgebase_path: target/knowledgebase/b-report-us/dim_pub_customer_info.md
- contract_source: source/contracts/b-report-us/tables/dim_pub_customer_info.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_customer_info`
- **Layer type:** DIM
- **Canonical / derived:** Canonical shared dimension (B Report contract catalog)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** dimension key level (one row per business key)
- **Scope:** US disty B Report shipped-order P&L and performance metrics.
- **Partition:** None explicit — full-table dimension or non-partitioned object per contract.
- **Natural key:** `mcust_no`, `cust_no`, `lead_id`, `resale_no`, `store_no`, `collector_id`
- **Exclusions:** Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country}.dim_pub_customer_info` | Documented in B Report contract v2 |
| Vertica | yes | `dim_us.dim_pub_customer_info` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_customer_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_customer_info.json` |
| **column_count** | 111 |
| **partition_keys** | `none` |
| **ddl_source** | B Report contract catalog — `source/contracts/b-report-us/tables/dim_pub_customer_info.md` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dim_pub_customer_info schema" --intent find_table_schema` |

### Lineage
- **upstream:** Curated DIM/ODS load jobs (per contract) — `source/contracts/b-report-us/tables/dim_pub_customer_info.md:L1`
- **downstream:** B Report fact/DM serving tables and dashboards — `source/contracts/b-report-us/tables/dim_pub_customer_info.md:L1`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | Not documented in repository |
| Schedule | Not documented in repository |
| Expected completion | 02:00-04:00 PT (before B Report common load). |

---

## L2 Declarative Knowledge

### Business purpose
US customer master — resolve `cust_no`/`mcust_no` from customer names and enrich territory/credit hierarchy

This Knowledgebase entry is derived from the B Report US table contract catalog (`contract_v2`). ETL SQL for the pub_dw dimension load is **not in the b-report-us Bitbucket ETL snapshot**; see cross-domain Knowledgebase references when listed under Related scripts.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Consumers: B Report order-line fact enrichment, `dws_disty_brpt_cust_mtd`, `pl_extend` customer labels. |
| **Sales / PM / finance** | Lookup attributes joined to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` and serving DM/DWS tables. |
| **Data engineering** | Stable dimension contract for join keys and attribute definitions. |

### Identifier search profile
- Primary lookup keys: `mcust_no`, `cust_no`, `lead_id`, `resale_no`, `store_no`, `collector_id`
- Join hub facts on documented key columns; use `date_flag` snapshot partitions on `_df` variants when applicable.

### Time field semantics
- **`date_flag`:** primary filter when table is partitioned; otherwise use hub `date_flag` for as-of reporting.
- **Period semantics:** per ETL partition scope.





### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `pending_amt` | `pending_amt` | pending_amt at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `pending_amt` | unspecified | `pending_amt` | Not in metric-index.md |

### etl_metrics

No governed logical metrics from `source/contracts/b-report-us/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
- Use for customer name → `cust_no`/`mcust_no` resolution when serving tables lack denormalized names.
- Master-customer questions: filter `mcust_name` (or `mcust_no`), aggregate at `cust_no` for sub-customer breakdown — see golden `cdw-sub-customer-ranking`.
- Sub-customer questions: resolve `cust_name` → `cust_no`; never `GROUP BY cust_name` alone when keys are available.
- Facts carry `cust_no` (int); they do **not** reliably carry `cust_name` at all grains — join this dimension or use `dws_disty_brpt_cust_mtd` when names are denormalized.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension join patterns
- Primary key: `cust_no`
- Fact join: `fact.cust_no = dim_pub_customer_info.cust_no`
- Master roll-up: `fact.mcust_no = dim_pub_customer_info.mcust_no` (many sub-customers per master)
- Territory context: `sales_terr` links to `dim_pub_sales_territory` for rep hierarchy
- As-of join: `dim_pub_customer_info_df` on `cust_no` AND `date_flag`
- High-risk pitfalls: `GROUP BY cust_name` (duplicate names); filtering integer `cust_no` with text tokens

### Key filters and ETL business logic
- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard time-filter SQL
```sql
-- See contract L3 Standard Time-Filter SQL in source/contracts/b-report-us/tables/dim_pub_customer_info.md
```

### End-to-end flow
1. Upstream DIM/ODS load populates `dim_us.dim_pub_customer_info` (ETL not in b-report-us Bitbucket snapshot).
2. B Report fact and serving jobs join this dimension for attribute enrichment.
3. Vertica consumers query `dim_us.dim_pub_customer_info` for reporting.

```mermaid
flowchart LR
  upstream["Upstream DIM/ODS loads"]
  dim["dim_us.dim_pub_customer_info"]
  hub["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  dm["B Report DM/DWS serving"]
  upstream --> dim
  dim --> hub
  hub --> dm
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_customer_info` | Primary dimension catalog object (contract v2) |

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
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT mcust_no, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY mcust_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT mcust_no, cust_no, lead_id, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_customer_info
WHERE date_flag = '${partition_value}'
GROUP BY mcust_no, cust_no, lead_id, date_flag
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
| **Query for reporting** | `dim_us.dim_pub_customer_info` | `dim_us.dim_pub_customer_info` | overwrite / incremental | `source/contracts/b-report-us/tables/dim_pub_customer_info.md:L5` | yes |
| **Hive alternative** | `dim_us.dim_pub_customer_info` | same as reporting table | — | B Report contract | — |

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
| Consumers: B Report order-line fact enrichment, `dws_disty_brpt_cust_mtd`, `pl_extend` customer labels. | B Report / POS dimension enrichment |
| Use cases: customer name resolution, master/sub-customer hierarchy, territory and credit analyst attributes. | B Report / POS dimension enrichment |

### Representative query patterns
```sql
SELECT cust_no, cust_name, mcust_no, mcust_name, sales_terr, sales_terr_name
FROM dim_us.dim_pub_customer_info
WHERE mcust_name ILIKE '%CDW LOGISTICS%'
ORDER BY cust_no
LIMIT 20;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_customer_info.md` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report hub and serving tables | `source/contracts/b-report-us/tables/dim_pub_customer_info.md:L6` — see contract L6 |

#### Operational detail (verified)
- Load pattern: Not documented in repository — `source/contracts/b-report-us/tables/dim_pub_customer_info.md:L1`
- Column count: 111 (B Report contract catalog)

#### Not documented in repository
- pub_dw ETL SQL and Azkaban `.flow` for this dimension
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dim_pub_customer_info.md` — B Report contract source — `source/contracts/b-report-us/tables/dim_pub_customer_info.md`
- `target/knowledgebase/customer/dim_pub_customer_info.md` — cross-domain Knowledgebase entry for same table object

---

*Document generated from `source/contracts/b-report-us/tables/dim_pub_customer_info.md` (contract_v2).*
