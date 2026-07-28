# ODS ETL: IDC monthly raw data (`ods_gbl.ods_etl_marketing_idc_raw_data_month`)

- artifact_type: etl_table
- artifact_id: ods_gbl.ods_etl_marketing_idc_raw_data_month
- domain: marketing
- one_line_purpose: This job promotes the latest monthly IDC distributor delivery data from the external Hive staging table into the curated ODS ETL layer. Marketing and analytics teams use the output to analyze distributor revenue, units, product hierarchy, a...
- layer_type: ODS
- source_kind: etl_sql
- evidence_source: source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `ods_gbl.ods_etl_marketing_idc_raw_data_month`
- **Layer type:** ODS
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per IDC delivery record for the latest loaded `month` partition (inferred from SQL — business natural key not documented in repository).
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** `month` — carried from source external table. - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository (likely product/distributor/country/month combination).
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per IDC delivery record for the latest loaded `month` partition (inferred from SQL — business natural key not documented in repository).
- **Partition:** `month` — carried from source external table.
- **Natural key:** Not documented in repository (likely product/distributor/country/month combination).

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `ods_gbl.ods_etl_marketing_idc_raw_data_month` | ETL target / intermediate per evidence script |
| Vertica | pending | `ods_gbl.ods_etl_marketing_idc_raw_data_month` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `ods_gbl.ods_etl_marketing_idc_raw_data_month` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `month` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "marketing ods_etl_marketing_idc_raw_data_month schema" --intent find_table_schema` |

### Lineage
See L6 Dependencies and notes.

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | None in SQL (partition selection is dynamic via `max(month)`). |


---

## L2 Declarative Knowledge

### Business purpose
This job promotes the latest monthly IDC distributor delivery data from the external Hive staging table into the curated ODS ETL layer. Marketing and analytics teams use the output to analyze distributor revenue, units, product hierarchy, and brand performance by country and month for IDC-sourced market intelligence.

---

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| Marketing analytics | Consumes standardized monthly IDC distributor metrics from ODS. |
| Data engineering | Feeds `dm_gbl.dm_idc_raw_data_monthly_view` and Vertica sync (`dm_gbl.dm_idc_raw_data_month`). |
| Product/category governance | Uses `product_group`, `product_category`, `product_name`, `product_detail` hierarchy fields. |

---

### Fact key resolution
- Natural key: Not documented in repository (likely product/distributor/country/month combination).
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** `month` — carried from source external table.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/marketing/metric-index.md`](../../source/contracts/marketing/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/marketing/metric-index.md` are mapped on this table.

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and hierarchy

- `country`, `distributor`, `channel_detail`
- `product_group`, `product_category`, `product_name`, `product_detail`
- `company_name`, `brand_name`, `mpn`, `upc_code`
- `data_year`, `data_month`, `month`

### Measures

- `units` — unit volume (cast to INT)
- `distributor_revenue` — local currency revenue (DECIMAL 20,8)
- `distributor_revenue_usd` — constant USD revenue (DECIMAL 20,8)
- `currency_id`

### Custom IDC attributes

- `ai_pc`, `deployment_type`, `product_type`

---

### etl_metrics

#### `data_year`
- **Source:** [metric-index.md](../../source/contracts/marketing/metric-index.md#data_year)
- **Business definition:** Calendar year as integer
```sql
cast(data_year as int)
```

#### `units`
- **Source:** [metric-index.md](../../source/contracts/marketing/metric-index.md#units)
- **Business definition:** Unit count
```sql
cast(units as int)
```

#### `distributor_revenue`
- **Source:** [metric-index.md](../../source/contracts/marketing/metric-index.md#distributor_revenue)
- **Business definition:** Local currency revenue
```sql
cast(... as DECIMAL(20,8))
```

#### `distributor_revenue_usd`
- **Source:** [metric-index.md](../../source/contracts/marketing/metric-index.md#distributor_revenue_usd)
- **Business definition:** USD revenue
```sql
cast(... as DECIMAL(20,8))
```

#### `etl_timestamp`
- **Source:** [metric-index.md](../../source/contracts/marketing/metric-index.md#etl_timestamp)
- **Business definition:** Load timestamp PST
```sql
from_utc_timestamp(current_timestamp(),'America/Los_Angeles')
```


---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql` |

### Key filters and ETL business logic
### Step 1 — Filter to latest month

**Source:** `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1`

**Filter:**
- `month = (SELECT max(month) FROM ods_gbl.ods_ext_marketing_idc_raw_data_month_v1)`

### Step 2 — Final `INSERT OVERWRITE`

**Derived columns:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `data_year` | `cast(data_year as int)` | Calendar year as integer |
| `units` | `cast(units as int)` | Unit count |
| `distributor_revenue` | `cast(... as DECIMAL(20,8))` | Local currency revenue |
| `distributor_revenue_usd` | `cast(... as DECIMAL(20,8))` | USD revenue |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | Load timestamp PST |

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ods_gbl.ods_etl_marketing_idc_raw_data_month
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Target table:** `ods_gbl.ods_etl_marketing_idc_raw_data_month`  
**Source table:** `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1`

1. Determine `max(month)` from external staging table.
2. `INSERT OVERWRITE` ODS ETL table with all rows matching that month.
3. Cast types and stamp `etl_timestamp`.

```mermaid
flowchart LR
  EXT[ods_ext_marketing_idc_raw_data_month_v1] --> FILT[filter month = max month]
  FILT --> CAST[type cast + etl_timestamp]
  CAST --> OUT[INSERT OVERWRITE<br/>ods_etl_marketing_idc_raw_data_month]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|------------------|
| **Read latest month partition** | Selects only rows from the most recent `month` partition in the external staging table. |
| **Type casting** | Normalizes numeric and timestamp fields (`data_year`, `units`, revenue amounts). |
| **Audit stamp** | Adds `etl_timestamp` in America/Los_Angeles for load traceability. |
| **Full overwrite** | Replaces the entire ODS ETL table with the latest-month snapshot. |

**Parameters:** None in SQL (partition selection is dynamic via `max(month)`).

---


### Base tables register
| Object | Role in this job |
|--------|------------------|
| `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | External Hive staging table populated by `read_hdfs_monthly.py` |
| `ods_gbl.ods_etl_marketing_idc_raw_data_month` | Curated ODS ETL target (full overwrite each run) |

---

### Step-by-step logic
### Step 1 — Filter to latest month

**Source:** `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1`

**Filter:**
- `month = (SELECT max(month) FROM ods_gbl.ods_ext_marketing_idc_raw_data_month_v1)`

### Step 2 — Final `INSERT OVERWRITE`

**Derived columns:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `data_year` | `cast(data_year as int)` | Calendar year as integer |
| `units` | `cast(units as int)` | Unit count |
| `distributor_revenue` | `cast(... as DECIMAL(20,8))` | Local currency revenue |
| `distributor_revenue_usd` | `cast(... as DECIMAL(20,8))` | USD revenue |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | Load timestamp PST |

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/marketing/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `data_year` | `cast(data_year as int)` | `data_year` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:4` |
| `data_month` | `data_month` | `data_month` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:2` |
| `country` | `country` | `country` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:6` |
| `distributor` | `distributor` | `distributor` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:7` |
| `channel_detail` | `channel_detail` | `channel_detail` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:8` |
| `product_group` | `product_group` | `product_group` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:9` |
| `product_category` | `product_category` | `product_category` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:10` |
| `product_name` | `product_name` | `product_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:11` |
| `product_detail` | `product_detail` | `product_detail` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:12` |
| `company_name` | `company_name` | `company_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:13` |
| `brand_name` | `brand_name` | `brand_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:14` |
| `mpn` | `mpn` | `mpn` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:15` |
| `upc_code` | `upc_code` | `upc_code` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:16` |
| `currency_id` | `currency_id` | `currency_id` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:17` |
| `units` | `cast(units as int)` | `units` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:18` |
| `distributor_revenue` | `cast(distributor_revenue as DECIMAL(20,8))` | `distributor_revenue` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:19` |
| `distributor_revenue_usd` | `cast(distributor_revenue_usd as DECIMAL(20,8))` | `distributor_revenue_usd` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:20` |
| `month` | `month` | `month` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:2` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | arithmetic | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:22` |
| `ai_pc` | `ai_pc` | `ai_pc` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:23` |
| `deployment_type` | `deployment_type` | `deployment_type` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:24` |
| `product_type` | `product_type` | `product_type` | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:25` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dm_gbl.dm_idc_raw_data_month
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dm_gbl.dm_idc_raw_data_month
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dm_gbl.dm_idc_raw_data_month
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- Only the **latest `month` partition** from the external table is loaded; prior months in ODS are replaced on each run.
- Upstream CSV schema validation happens in `read_hdfs_monthly.py` before this SQL runs.
- Hive view `dm_gbl.dm_idc_raw_data_monthly_view` definition is not in this repository.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_gbl.dm_idc_raw_data_monthly_view` | `dm_gbl.dm_idc_raw_data_month` | overwrite | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:67-76` | yes (Vertica metadata fallback) |
| **Hive alternative** | `ods_gbl.ods_etl_marketing_idc_raw_data_month` | `dm_gbl.dm_idc_raw_data_month` | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:46-52` | - |
| **ETL internal** | `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | Not synced to Vertica | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:27-32` | - |

Business users should query **`dm_gbl.dm_idc_raw_data_month`** in Vertica (21 columns; WKB seed `vertica_dm_gbl_dm_idc_raw_data_month.json`). Hive target is `ods_gbl.ods_etl_marketing_idc_raw_data_month`; Hive DDL not in `HIVE/snxhive` at `refs/heads/master`.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | unknown |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|------------------|
| Marketing analytics | Consumes standardized monthly IDC distributor metrics from ODS. |
| Data engineering | Feeds `dm_gbl.dm_idc_raw_data_monthly_view` and Vertica sync (`dm_gbl.dm_idc_raw_data_month`). |
| Product/category governance | Uses `product_group`, `product_category`, `product_name`, `product_detail` hierarchy fields. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ods_gbl.ods_etl_marketing_idc_raw_data_month
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_gbl.ods_ext_marketing_idc_raw_data_month_v1` | Source for INSERT | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:27-32` |
| `read_hdfs_monthly.py` | Populates external staging partitions | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:38-44` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| `dm_gbl.dm_idc_raw_data_monthly_view` (Hive view) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:72` |
| `dm_gbl.dm_idc_raw_data_month` (Vertica) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:67-76` |

### Operational detail (verified)

- Load mode: `INSERT OVERWRITE` (full table replace) — `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql:1-2`
- Orchestrated in flow `idc_delivery_month_data` after `read_hdfs_monthly` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:46-52`

### Not documented in repository

- Schedule (defined on flow, not this SQL file in isolation)
- Hive view `dm_idc_raw_data_monthly_view` DDL
- Natural grain key columns
- Bitbucket DDL for marketing IDC Hive tables — not in `HIVE/snxhive` at `refs/heads/master`; Hive WKB seeds skipped. Vertica `dm_gbl.dm_idc_raw_data_month` seeded via metadata fallback (`vertica_dm_gbl_dm_idc_raw_data_month.json`).

### Related scripts (verified)

- `read_hdfs_monthly.py` — loads CSV into external table — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:38-44`
- `literal_parameters.sql` — supplies `start_date` for mail subject — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_month_data.flow:17-20`

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_month.sql`.*
