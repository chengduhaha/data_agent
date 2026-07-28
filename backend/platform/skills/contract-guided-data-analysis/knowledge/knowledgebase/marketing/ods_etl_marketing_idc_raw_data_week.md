# ODS ETL: IDC weekly raw data (`ods_gbl.ods_etl_marketing_idc_raw_data_week`)

- artifact_type: etl_table
- artifact_id: ods_gbl.ods_etl_marketing_idc_raw_data_week
- domain: marketing
- one_line_purpose: This job promotes the latest weekly IDC distributor delivery data from the external Hive staging table into the curated ODS ETL layer. Marketing teams use the output for weekly market tracking, brand/category analysis, and downstream sync t...
- layer_type: ODS
- source_kind: etl_sql
- evidence_source: source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `ods_gbl.ods_etl_marketing_idc_raw_data_week`
- **Layer type:** ODS
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per IDC weekly delivery record for latest `week` partition (inferred from SQL).
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** `week` — ISO week identifier from source. - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per IDC weekly delivery record for latest `week` partition (inferred from SQL).
- **Partition:** `week` — ISO week identifier from source.
- **Natural key:** Not documented in repository.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `ods_gbl.ods_etl_marketing_idc_raw_data_week` | ETL target / intermediate per evidence script |
| Vertica | pending | `ods_gbl.ods_etl_marketing_idc_raw_data_week` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `ods_gbl.ods_etl_marketing_idc_raw_data_week` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/marketing_ods_etl_marketing_idc_raw_data_week.json` |
| **column_count** | 24 |
| **partition_keys** | `week` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "marketing ods_etl_marketing_idc_raw_data_week schema" --intent find_table_schema` |

### Lineage
See L6 Dependencies and notes.

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | None in SQL (partition via `max(week)`). |


---

## L2 Declarative Knowledge

### Business purpose
This job promotes the latest weekly IDC distributor delivery data from the external Hive staging table into the curated ODS ETL layer. Marketing teams use the output for weekly market tracking, brand/category analysis, and downstream sync to Vertica and CIS reference tables.

---

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| Marketing analytics | Weekly IDC distributor revenue and unit trends. |
| CIS application | Product category and vendor brand reference sync (via weekly flow). |
| Data engineering | Feeds Vertica `dm_gbl.dm_idc_raw_data_week` through Hive view. |

---

### Fact key resolution
- Natural key: Not documented in repository.
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** `week` — ISO week identifier from source.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.

### Metrics served
1. **Weekly distributor revenue** — `distributor_revenue_usd` by brand and product hierarchy.
2. **Weekly unit volume** — `units` by country and distributor.
3. **Brand rollups** — `brand_name` for CIS `idc_vend_brand` sync (weekly flow).

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Time dimensions

- `iso_year`, `iso_week`, `week_start_date`, `week_end_date`, `week`

### Product and market dimensions

- `country`, `distributor`, `channel_detail`
- `product_group`, `product_category`, `product_name`, `product_detail`
- `company_name`, `brand_name`, `mpn`, `upc_code`, `currency_id`
- `deployment_type`, `ai_pc`, `product_type`

### Measures

- `units`, `distributor_revenue`, `distributor_revenue_usd`

---

### etl_metrics

N/A - no calculable ETL formulas extracted from this document (passthrough / stored measures only, or formulas not documented).

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql` |

### Key filters and ETL business logic
### Step 1 — Filter to latest week

- `week = (SELECT max(week) FROM ods_gbl.ods_ext_marketing_idc_raw_data_week_v1)`

### Step 2 — `INSERT OVERWRITE`

| Column | Transformation |
|--------|----------------|
| `iso_year` | cast to INT |
| `week_start_date`, `week_end_date` | cast to TIMESTAMP |
| `units` | cast to INT |
| `distributor_revenue`, `distributor_revenue_usd` | DECIMAL(20,8) |
| `etl_timestamp` | current timestamp in America/Los_Angeles |

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM ods_gbl.ods_etl_marketing_idc_raw_data_week
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Target:** `ods_gbl.ods_etl_marketing_idc_raw_data_week`  
**Source:** `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1`

1. Find `max(week)` in external staging.
2. `INSERT OVERWRITE` ODS with matching rows, cast types, stamp timestamp.

```mermaid
flowchart LR
  EXT[ods_ext_marketing_idc_raw_data_week_v1] --> FILT[filter week = max week]
  FILT --> CAST[type cast + etl_timestamp]
  CAST --> OUT[INSERT OVERWRITE<br/>ods_etl_marketing_idc_raw_data_week]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|------------------|
| **Read latest week partition** | Selects rows from the most recent `week` partition in external staging. |
| **Type casting** | Normalizes ISO year/week, date range timestamps, units, and revenue fields. |
| **Audit stamp** | Adds `etl_timestamp` in America/Los_Angeles. |
| **Full overwrite** | Replaces entire ODS ETL table with latest-week snapshot. |

**Parameters:** None in SQL (partition via `max(week)`).

---


### Base tables register
| Object | Role |
|--------|------|
| `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | External staging (populated by `read_hdfs.py`) |
| `ods_gbl.ods_etl_marketing_idc_raw_data_week` | ODS ETL target |

---

### Step-by-step logic
### Step 1 — Filter to latest week

- `week = (SELECT max(week) FROM ods_gbl.ods_ext_marketing_idc_raw_data_week_v1)`

### Step 2 — `INSERT OVERWRITE`

| Column | Transformation |
|--------|----------------|
| `iso_year` | cast to INT |
| `week_start_date`, `week_end_date` | cast to TIMESTAMP |
| `units` | cast to INT |
| `distributor_revenue`, `distributor_revenue_usd` | DECIMAL(20,8) |
| `etl_timestamp` | current timestamp in America/Los_Angeles |

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
| `iso_year` | `cast(iso_year as int)` | `iso_year` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:4` |
| `iso_week` | `iso_week` | `iso_week` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:5` |
| `week_start_date` | `cast(week_start_date as TIMESTAMP)` | `week_start_date` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:6` |
| `week_end_date` | `cast(week_end_date as TIMESTAMP)` | `week_end_date` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:7` |
| `country` | `country` | `country` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:8` |
| `distributor` | `distributor` | `distributor` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:9` |
| `channel_detail` | `channel_detail` | `channel_detail` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:10` |
| `product_group` | `product_group` | `product_group` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:11` |
| `product_category` | `product_category` | `product_category` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:12` |
| `product_name` | `product_name` | `product_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:13` |
| `product_detail` | `product_detail` | `product_detail` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:14` |
| `company_name` | `company_name` | `company_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:15` |
| `brand_name` | `brand_name` | `brand_name` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:16` |
| `mpn` | `mpn` | `mpn` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:17` |
| `upc_code` | `upc_code` | `upc_code` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:18` |
| `currency_id` | `currency_id` | `currency_id` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:19` |
| `units` | `cast(units as int)` | `units` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:20` |
| `distributor_revenue` | `cast(distributor_revenue as DECIMAL(20,8))` | `distributor_revenue` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:21` |
| `distributor_revenue_usd` | `cast(distributor_revenue_usd as DECIMAL(20,8))` | `distributor_revenue_usd` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | cast | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:22` |
| `week` | `week` | `week` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:2` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | arithmetic | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:24` |
| `deployment_type` | `deployment_type` | `deployment_type` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:25` |
| `ai_pc` | `ai_pc` | `ai_pc` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:26` |
| `product_type` | `product_type` | `product_type` | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | passthrough | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:27` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dm_gbl.dm_idc_raw_data_week
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dm_gbl.dm_idc_raw_data_week
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dm_gbl.dm_idc_raw_data_week
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- Only the latest `week` partition is retained in ODS after each run (full overwrite).
- Weekly flow also syncs distinct product categories and brands to CIS MySQL tables.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dm_gbl.dm_idc_raw_data_weekly_view` | `dm_gbl.dm_idc_raw_data_week` | overwrite | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:73-74` | yes (Vertica metadata fallback) |
| **Hive alternative** | `ods_gbl.ods_etl_marketing_idc_raw_data_week` | `dm_gbl.dm_idc_raw_data_week` | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:46-52` | - |
| **ETL internal** | `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | Not synced to Vertica | - | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:1-2` | - |

Business users should query **`dm_gbl.dm_idc_raw_data_week`** in Vertica (23 columns; WKB seed `vertica_dm_gbl_dm_idc_raw_data_week.json`). Hive target is `ods_gbl.ods_etl_marketing_idc_raw_data_week`; Hive DDL not in `HIVE/snxhive` at `refs/heads/master`.

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
| Marketing analytics | Weekly IDC distributor revenue and unit trends. |
| CIS application | Product category and vendor brand reference sync (via weekly flow). |
| Data engineering | Feeds Vertica `dm_gbl.dm_idc_raw_data_week` through Hive view. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM ods_gbl.ods_etl_marketing_idc_raw_data_week
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_gbl.ods_ext_marketing_idc_raw_data_week_v1` | Source | `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:29-34` |
| `read_hdfs.py` | Populates staging | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:38-44` |

### Downstream consumers (verified)

| Object | Evidence |
|--------|----------|
| `dm_gbl.dm_idc_raw_data_weekly_view` | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:72` |
| `dm_gbl.dm_idc_raw_data_week` (Vertica) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:67-76` |
| `CIS.idc_prod_category` (MySQL) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:78-89` |
| `CIS.idc_vend_brand` (MySQL) | `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:91-102` |

### Operational detail (verified)

- `INSERT OVERWRITE` — `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql:1-2`

### Not documented in repository

- Hive view DDL for `dm_idc_raw_data_weekly_view`
- Natural grain key
- Bitbucket DDL for marketing IDC Hive tables — not in `HIVE/snxhive` at `refs/heads/master`; Hive WKB seeds skipped. Vertica reporting targets seeded via metadata fallback (see `readme.md`).

### Related scripts (verified)

- `read_hdfs.py` — `source/etl/sql/marketing/marketing_dw/hdfstohive/idc_delivery_week_data.flow:38-44`

---

*Document generated from `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/marketing/marketing_dw/hdfstohive/script/ods_etl_marketing_idc_raw_data_week.sql`.*
