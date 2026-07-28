# DIM: Shared calendar dimension for B Report date_flag and fiscal joins (`dim_us.dim_pub_date`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_date
- domain: b-report-us
- one_line_purpose: Shared calendar dimension for B Report date_flag and fiscal joins
- layer_type: DIM
- source_kind: contract_v2
- evidence_source: source/contracts/b-report-us/tables/dim_pub_date.md
- knowledgebase_path: target/knowledgebase/b-report-us/dim_pub_date.md
- contract_source: source/contracts/b-report-us/tables/dim_pub_date.md

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_date`
- **Layer type:** DIM
- **Canonical / derived:** Canonical shared dimension (B Report contract catalog)
- **Owner team:** Disty analytics / POS reporting

### Grain, scope, exclusions
- **Grain:** dimension key level
- **Scope:** US POS reporting (`dim_us` baseline)
- **Partition:** `date_flag` — business date filter per B Report contract.
- **Natural key:** `key`, `level`
- **Exclusions:** Component lines (`order_line_type = 'Comp'`) excluded by default in standard POS revenue reports; credit order_type 114 excluded unless adjustment report

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country}.dim_pub_date` | Documented in B Report contract v2 |
| Vertica | yes | `dim_us.dim_pub_date` | Contract marks Vertica verified |

### Physical schema reference
| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_date` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_date.json` |
| **column_count** | 32 |
| **partition_keys** | `date_flag` |
| **ddl_source** | B Report contract catalog — `source/contracts/b-report-us/tables/dim_pub_date.md` |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "b-report-us dim_pub_date schema" --intent find_table_schema` |

### Lineage
- **upstream:** Curated DWD/DIM/ODS load jobs in disty common pipeline — `source/contracts/b-report-us/tables/dim_pub_date.md:L1`
- **downstream:** Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports — `source/contracts/b-report-us/tables/dim_pub_date.md:L1`

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | Daily incremental by `date_flag` |
| Schedule | Not documented in repository |
| Expected completion | 05:00-07:30 PT (daily disty load dependency chain) |

---

## L2 Declarative Knowledge

### Business purpose
Shared calendar dimension for B Report date_flag and fiscal joins

This Knowledgebase entry is derived from the B Report US table contract catalog (`contract_v2`). ETL SQL for the pub_dw dimension load is **not in the b-report-us Bitbucket ETL snapshot**; see cross-domain Knowledgebase references when listed under Related scripts.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **B Report / P&L analytics** | Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1) |
| **Sales / PM / finance** | Lookup attributes joined to `dw_us.dwd_disty_brpt_orders_pl_etl_mi` and serving DM/DWS tables. |
| **Data engineering** | Stable dimension contract for join keys and attribute definitions. |

### Identifier search profile
- Primary lookup keys: `date_flag`
- Join hub facts on documented key columns; use `date_flag` snapshot partitions on `_df` variants when applicable.

### Time field semantics
- **`date_flag`:** primary filter when table is partitioned; otherwise use hub `date_flag` for as-of reporting.
- **Period semantics:** per ETL partition scope.





### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Governed profitability | `sales` | `net_sales` | net_sales at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `net_sales` | unspecified | `sales` | `source/contracts/b-report-us/metric-index.md#net_sales` |

### etl_metrics

Formulas below are sourced from [`source/contracts/b-report-us/metric-index.md`](../../source/contracts/b-report-us/metric-index.md) for logical metrics present on this table.
Index formulas are canonical: this enricher copies them into KB and never overwrites `final_effective_formula_sql` in the metric-index.

#### `net_sales`
- **Source:** [metric-index.md](../../source/contracts/b-report-us/metric-index.md#net_sales)
- **Business definition:** Shipped quantity times unit price plus per-unit sum expense (net of returns scope per order_type filter).
```sql
nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0))
```

---

## L3 Procedural Knowledge

### Query and routing rules
- Prefer this table when POS report requires its attributes at documented grain.
- For metric questions on sales amount/qty, route to hub unless SPA/SCM enrichment explicitly needed.

### Dimension join patterns
- See domain-knowledge.md join graph when used with POS hub.

### Key filters and ETL business logic
- Standard POS filters inherited from domain-knowledge.md when joining to hub.

### Standard time-filter SQL
```sql
-- See contract L3 Standard Time-Filter SQL in source/contracts/b-report-us/tables/dim_pub_date.md
```

### End-to-end flow
1. Upstream DIM/ODS load populates `dim_us.dim_pub_date` (ETL not in b-report-us Bitbucket snapshot).
2. B Report fact and serving jobs join this dimension for attribute enrichment.
3. Vertica consumers query `dim_us.dim_pub_date` for reporting.

```mermaid
flowchart LR
  upstream["Upstream DIM/ODS loads"]
  dim["dim_us.dim_pub_date"]
  hub["dw_us.dwd_disty_brpt_orders_pl_etl_mi"]
  dm["B Report DM/DWS serving"]
  upstream --> dim
  dim --> hub
  hub --> dm
```

### Base tables register
| Object | Role in this job |
|--------|------------------|
| `dim_us.dim_pub_date` | Primary dimension catalog object (contract v2) |

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
- Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_date
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT key, COUNT(*) AS row_cnt
FROM dim_us.dim_pub_date
WHERE date_flag = '${partition_value}'
GROUP BY key
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT key, level, order_line_no, date_flag, COUNT(*) AS cnt
FROM dim_us.dim_pub_date
WHERE date_flag = '${partition_value}'
GROUP BY key, level, order_line_no, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- Contract-derived catalog; pub_dw ETL script path not verified in b-report-us Bitbucket snapshot.
- Cross-engine parity: compare Hive vs Vertica row counts when auditing.
- Validate join cardinality to POS hub before production report use.

### Conflicts and open questions
- pub_dw Bitbucket ETL path: Not documented in repository (dimension maintained in pub_dw project).
- hive2vertica sync job file:line evidence: Not documented in repository.

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dim_us.dim_pub_date` | `dim_us.dim_pub_date` | overwrite / incremental | `source/contracts/b-report-us/tables/dim_pub_date.md:L5` | yes |
| **Hive alternative** | `dim_us.dim_pub_date` | same as reporting table | — | B Report contract | — |

- Primary consumption: Vertica (`dim_us.dim_pub_date`)
- Hive available for reconciliation and Spark-side debugging

### Access constraints
- Standard disty US schema access policies apply

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
| Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1) | B Report / POS dimension enrichment |
| Vendor/customer POS exports, SPA/SCM claim detail, serial/RMA tracing reports | B Report / POS dimension enrichment |

### Representative query patterns
```sql
SELECT *
FROM dim_us.dim_pub_date
LIMIT 100;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| B Report contract | Table metadata, grain, columns | `source/contracts/b-report-us/tables/dim_pub_date.md` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| B Report hub and serving tables | `source/contracts/b-report-us/tables/dim_pub_date.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

#### Operational detail (verified)
- Load pattern: Daily incremental by `date_flag` — `source/contracts/b-report-us/tables/dim_pub_date.md:L1`
- Column count: 32 (B Report contract catalog)

#### Not documented in repository
- pub_dw ETL SQL and Azkaban `.flow` for this dimension
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

#### Related scripts (verified)
- `dim_pub_date.md` — B Report contract source — `source/contracts/b-report-us/tables/dim_pub_date.md`
- `target/knowledgebase/common/dim_pub_date/dim_pub_date.md` — cross-domain Knowledgebase entry for same table object

---

*Document generated from `source/contracts/b-report-us/tables/dim_pub_date.md` (contract_v2).*
