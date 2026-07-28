# FIX: Close CPO Header Duplicate Partition Repair (`fix_dwd_disty_sales_close_cpo_header_extend_di`)

- artifact_type: etl_table
- artifact_id: flow_cpo.fix_dwd_disty_sales_close_cpo_header_extend_di
- domain: cpo
- one_line_purpose: This is a **data quality fix script** that repairs the closed CPO header table by removing duplicate CPO rows from older partitions. It reads the duplicate registry (`dwd_disty_sales_close_duplicate_cpo_header_df`) to find which date partit...
- layer_type: FLOW
- source_kind: etl_sql
- evidence_source: source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `flow_cpo.fix_dwd_disty_sales_close_cpo_header_extend_di`
- **Layer type:** FLOW
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** Not documented in repository
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- Reads from `dwd_disty_sales_close_cpo_header_extend_di` (same grain as that table — one row per `(cpo_id, date_flag)`).
- Overwrites only the affected partitions (those listed in the duplicate registry).

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `fix_dwd_disty_sales_close_cpo_header_extend_di` | ETL target / intermediate per evidence script |
| Vertica | pending | `fix_dwd_disty_sales_close_cpo_header_extend_di` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `flow_cpo.fix_dwd_disty_sales_close_cpo_header_extend_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "cpo fix_dwd_disty_sales_close_cpo_header_extend_di schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | Duplicate registry — input |
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | **Source and target** — cleaned in place |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code`, `date_flag` |


---

## L2 Declarative Knowledge

### Business purpose
This is a **data quality fix script** that repairs the closed CPO header table by removing duplicate CPO rows from older partitions. It reads the duplicate registry (`dwd_disty_sales_close_duplicate_cpo_header_df`) to find which date partitions contain duplicates, then re-writes those affected partitions with the duplicate rows excluded. The result is a cleaned `dwd_disty_sales_close_cpo_header_extend_di` where each CPO appears in only one date partition.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Data engineering / data quality** | Ensures each CPO header appears in exactly one date partition in the main close CPO table, preventing double-counting in downstream reports. |

---

### Fact key resolution
- Natural key: Not documented in repository
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/cpo/metric-index.md`](../../source/contracts/cpo/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/cpo/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql` |

### Key filters and ETL business logic
### Step 1 — `temp_cpo_header_duplicate_date`

**Source:** `dwd_disty_sales_close_duplicate_cpo_header_df WHERE date_flag = '${date_flag}'`

**Output:** `DISTINCT last_date_flag` — the specific older partition dates that need cleaning.

---

### Step 2 — Final `INSERT OVERWRITE`

**From:** `dwd_disty_sales_close_cpo_header_extend_di` (`cd`)

**INNER JOIN** `temp_cpo_header_duplicate_date` (`dd`) ON `cd.date_flag = dd.last_date_flag` — limits processing to only the affected partitions.

**LEFT JOIN** `dwd_disty_sales_close_duplicate_cpo_header_df` (`du`) ON `cd.cpo_id = du.cpo_id AND cd.date_flag = du.last_date_flag AND du.date_flag = '${date_flag}'`

**Filter:** `WHERE du.cpo_id IS NULL` — keeps only rows where no duplicate record exists, i.e. the non-duplicate rows survive.

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM fix_dwd_disty_sales_close_cpo_header_extend_di
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`, `date_flag`
**Target table:** `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` (same table — repairs its own partitions).

1. Build `temp_cpo_header_duplicate_date`: `SELECT DISTINCT last_date_flag FROM dwd_disty_sales_close_duplicate_cpo_header_df WHERE date_flag = '${date_flag}'` — the list of partition dates that contain duplicates.
2. **INSERT OVERWRITE** the affected partitions: join `dwd_disty_sales_close_cpo_header_extend_di` (inner join to `temp_cpo_header_duplicate_date` on `date_flag = last_date_flag`) LEFT JOIN the duplicate registry (`dwd_disty_sales_close_duplicate_cpo_header_df`). Exclude rows where the left join finds a match (`WHERE du.cpo_id IS NULL`) — the surviving rows are the non-duplicate ones.

```mermaid
flowchart LR
  DUP_DF[dwd_disty_sales_close_duplicate_cpo_header_df
date_flag=param] --> TDD[temp_cpo_header_duplicate_date
DISTINCT last_date_flag]
  SRC[dwd_disty_sales_close_cpo_header_extend_di] --> J1[INNER JOIN on date_flag=last_date_flag]
  TDD --> J1
  J1 --> J2[LEFT JOIN duplicate registry
WHERE du.cpo_id IS NULL = not a duplicate]
  J2 --> INS[INSERT OVERWRITE
dwd_disty_sales_close_cpo_header_extend_di
affected partitions only]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Identify affected partitions** | Reads `dwd_disty_sales_close_duplicate_cpo_header_df` for the current `date_flag` to get the distinct `last_date_flag` values — the older partitions containing duplicates. |
| **Re-write clean partitions** | For each affected partition, re-inserts rows from `dwd_disty_sales_close_cpo_header_extend_di` **excluding** CPOs that appear in the duplicate registry for that partition. |

**Parameters:** `country_code`, `date_flag`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | Duplicate registry — identifies which partitions contain duplicates and which CPO IDs to exclude. |
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | **Both source and target** — read to get current data; overwritten with cleaned rows for affected partitions. |

**Temporary tables:** `temp_cpo_header_duplicate_date`

---

### Step-by-step logic
### Step 1 — `temp_cpo_header_duplicate_date`

**Source:** `dwd_disty_sales_close_duplicate_cpo_header_df WHERE date_flag = '${date_flag}'`

**Output:** `DISTINCT last_date_flag` — the specific older partition dates that need cleaning.

---

### Step 2 — Final `INSERT OVERWRITE`

**From:** `dwd_disty_sales_close_cpo_header_extend_di` (`cd`)

**INNER JOIN** `temp_cpo_header_duplicate_date` (`dd`) ON `cd.date_flag = dd.last_date_flag` — limits processing to only the affected partitions.

**LEFT JOIN** `dwd_disty_sales_close_duplicate_cpo_header_df` (`du`) ON `cd.cpo_id = du.cpo_id AND cd.date_flag = du.last_date_flag AND du.date_flag = '${date_flag}'`

**Filter:** `WHERE du.cpo_id IS NULL` — keeps only rows where no duplicate record exists, i.e. the non-duplicate rows survive.

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | `temp_cpo_header_duplicate_date` | many:1 | `cd.date_flag = dd.last_date_flag` | etl_sql (source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:1) |
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | many:1 | `cd.cpo_id = du.cpo_id and cd.date_flag=du.last_date_flag and du.date_flag='${date_flag}'` | etl_sql (source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:1) |

`source/ref/cpo/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cpo_id` | `cd.cpo_id` | `cpo_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:10` |
| `cpo_no` | `cd.cpo_no` | `cpo_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:11` |
| `cpo_cust_no` | `cd.cpo_cust_no` | `cpo_cust_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:12` |
| `cpo_cust_name` | `cd.cpo_cust_name` | `cpo_cust_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:13` |
| `cpo_sales_terr` | `cd.cpo_sales_terr` | `cpo_sales_terr` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:14` |
| `cpo_entry_id` | `cd.cpo_entry_id` | `cpo_entry_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:15` |
| `cpo_entry_name` | `cd.cpo_entry_name` | `cpo_entry_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:16` |
| `cpo_entry_datetime` | `cd.cpo_entry_datetime` | `cpo_entry_datetime` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:17` |
| `cpo_from_ref_type` | `cd.cpo_from_ref_type` | `cpo_from_ref_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:18` |
| `cpo_from_ref_type_desc` | `cd.cpo_from_ref_type_desc` | `cpo_from_ref_type_desc` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:19` |
| `system_type` | `cd.system_type` | `system_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:20` |
| `cpo_pay_meth` | `cd.cpo_pay_meth` | `cpo_pay_meth` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:21` |
| `cpo_total_taxable` | `cd.cpo_total_taxable` | `cpo_total_taxable` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:22` |
| `cpo_total_notax` | `cd.cpo_total_notax` | `cpo_total_notax` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:23` |
| `cpo_sales_tax` | `cd.cpo_sales_tax` | `cpo_sales_tax` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:24` |
| `cpo_freight` | `cd.cpo_freight` | `cpo_freight` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:25` |
| `cpo_other` | `cd.cpo_other` | `cpo_other` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:26` |
| `cpo_so_total` | `cd.cpo_so_total` | `cpo_so_total` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:27` |
| `cpo_bo_total` | `cd.cpo_bo_total` | `cpo_bo_total` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:28` |
| `po_total` | `cd.po_total` | `po_total` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:29` |
| `cpo_ship_method` | `cd.cpo_ship_method` | `cpo_ship_method` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:30` |
| `cpo_ship_loc_type` | `cd.cpo_ship_loc_type` | `cpo_ship_loc_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:31` |
| `end_user_po_no` | `cd.end_user_po_no` | `end_user_po_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:32` |
| `special_handle` | `cd.special_handle` | `special_handle` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:33` |
| `ship_to_name` | `cd.ship_to_name` | `ship_to_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:34` |
| `ship_to_addr1` | `cd.ship_to_addr1` | `ship_to_addr1` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:35` |
| `ship_to_addr2` | `cd.ship_to_addr2` | `ship_to_addr2` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:36` |
| `ship_to_zipcode` | `cd.ship_to_zipcode` | `ship_to_zipcode` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:37` |
| `ship_to_country` | `cd.ship_to_country` | `ship_to_country` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:38` |
| `ship_to_city` | `cd.ship_to_city` | `ship_to_city` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:39` |
| `ship_to_state` | `cd.ship_to_state` | `ship_to_state` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:40` |
| `ship_to_contact` | `cd.ship_to_contact` | `ship_to_contact` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:41` |
| `ship_to_phone_no` | `cd.ship_to_phone_no` | `ship_to_phone_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:42` |
| `frt_pay_type` | `cd.frt_pay_type` | `frt_pay_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:43` |
| `convert_datetime` | `cd.convert_datetime` | `convert_datetime` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:44` |
| `convert_user` | `cd.convert_user` | `convert_user` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:45` |
| `convert_user_name` | `cd.convert_user_name` | `convert_user_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:46` |
| `sales_model` | `cd.sales_model` | `sales_model` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:47` |
| `reseller_cust_no` | `cd.reseller_cust_no` | `reseller_cust_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:48` |
| `shopping_mode` | `cd.shopping_mode` | `shopping_mode` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:49` |
| `end_user_no` | `cd.end_user_no` | `end_user_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:50` |
| `cpo_swl_flag` | `cd.cpo_swl_flag` | `cpo_swl_flag` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:51` |
| `cpo_spa_type` | `cd.cpo_spa_type` | `cpo_spa_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:52` |
| `cpo_change_id` | `cd.cpo_change_id` | `cpo_change_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:53` |
| `cpo_change_name` | `cd.cpo_change_name` | `cpo_change_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:54` |
| `cpo_change_date` | `cd.cpo_change_date` | `cpo_change_date` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:55` |
| `cpo_delete_id` | `cd.cpo_delete_id` | `cpo_delete_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:56` |
| `cpo_delete_name` | `cd.cpo_delete_name` | `cpo_delete_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:57` |
| `cpo_delete_datetime` | `cd.cpo_delete_datetime` | `cpo_delete_datetime` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:58` |
| `cpo_status` | `cd.cpo_status` | `cpo_status` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:59` |
| `company_no` | `cd.company_no` | `company_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:60` |
| `opportunity_id` | `cd.opportunity_id` | `opportunity_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:61` |
| `probability` | `cd.probability` | `probability` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:62` |
| `cpo_comment` | `cd.cpo_comment` | `cpo_comment` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:63` |
| `cpo_delete_reason` | `cd.cpo_delete_reason` | `cpo_delete_reason` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:64` |
| `eu_company_name` | `cd.eu_company_name` | `eu_company_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:65` |
| `eu_loc_name` | `cd.eu_loc_name` | `eu_loc_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:66` |
| `eu_loc_address1` | `cd.eu_loc_address1` | `eu_loc_address1` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:67` |
| `eu_loc_address2` | `cd.eu_loc_address2` | `eu_loc_address2` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:68` |
| `eu_loc_city` | `cd.eu_loc_city` | `eu_loc_city` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:69` |
| `eu_loc_contact` | `cd.eu_loc_contact` | `eu_loc_contact` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:70` |
| `eu_loc_country` | `cd.eu_loc_country` | `eu_loc_country` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:71` |
| `eu_contact_email` | `cd.eu_contact_email` | `eu_contact_email` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:72` |
| `eu_contact_phone` | `cd.eu_contact_phone` | `eu_contact_phone` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:73` |
| `eu_loc_state` | `cd.eu_loc_state` | `eu_loc_state` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:74` |
| `eu_zipcode` | `cd.eu_zipcode` | `eu_zipcode` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:75` |
| `etl_timestamp` | `cd.etl_timestamp` | `etl_timestamp` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:76` |
| `last_update_comb` | `cd.last_update_comb` | `last_update_comb` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:77` |
| `ec_comment` | `cd.ec_comment` | `ec_comment` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:78` |
| `cpo_terr_name` | `cd.cpo_terr_name` | `cpo_terr_name` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:79` |
| `res_contact` | `cd.res_contact` | `res_contact` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:80` |
| `res_contact_email` | `cd.res_contact_email` | `res_contact_email` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:81` |
| `res_contact_phone` | `cd.res_contact_phone` | `res_contact_phone` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:82` |
| `so` | `cd.so` | `so` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:83` |
| `bo` | `cd.bo` | `bo` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:84` |
| `reason_code_desc` | `cd.reason_code_desc` | `reason_code_desc` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:85` |
| `int_ref_type` | `cd.int_ref_type` | `int_ref_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:86` |
| `close_date` | `cd.close_date` | `close_date` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:87` |
| `reason_code` | `cd.reason_code` | `reason_code` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:85` |
| `reason_code_other` | `cd.reason_code_other` | `reason_code_other` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:89` |
| `budgetary` | `cd.budgetary` | `budgetary` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:90` |
| `eu_type` | `cd.eu_type` | `eu_type` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:91` |
| `contract_no` | `cd.contract_no` | `contract_no` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:92` |
| `wf_request_id` | `cd.wf_request_id` | `wf_request_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:93` |
| `ea_proposal_id` | `cd.ea_proposal_id` | `ea_proposal_id` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:94` |
| `date_flag` | `cd.date_flag` | `date_flag` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di`, `temp_cpo_header_duplicate_date`, `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | passthrough | `source/etl/sql/cpo/public_order_scripts/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql:95` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `du.cpo_id IS NULL` | Row is NOT in the duplicate registry — safe to keep. |
| `du.date_flag = '${date_flag}'` | Limits the duplicate lookup to the current fix run's registry partition. |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Self-modifying table** — this script reads from and writes to the same table. Only affected partitions are overwritten; unaffected partitions are not touched.
- **Run order dependency** — must run after `dwd_disty_sales_close_duplicate_cpo_header_df.sql` has been executed for the same `date_flag`.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` in Vertica once MCP verification is completed for this document.

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | unknown |
| scan_risk_tier | medium |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Data engineering / data quality** | Ensures each CPO header appears in exactly one date partition in the main close CPO table, preventing double-counting in downstream reports. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM fix_dwd_disty_sales_close_cpo_header_extend_di
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `dw_${country_code}.dwd_disty_sales_close_duplicate_cpo_header_df` | Duplicate registry lookup | `fix_dwd_disty_sales_close_cpo_header_extend_di.sql:4,101,105` |
| `dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di` | Source rows to filter | `fix_dwd_disty_sales_close_cpo_header_extend_di.sql:97` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| None identified in repository. | — |

### Operational detail (verified)

- Partition overwrite: `INSERT OVERWRITE TABLE dw_${country_code}.dwd_disty_sales_close_cpo_header_extend_di PARTITION (date_flag)` — `fix_dwd_disty_sales_close_cpo_header_extend_di.sql:8`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

### Related scripts (verified)

- `dwd_disty_sales_close_duplicate_cpo_header_df.sql` — must run first to populate the duplicate registry — `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/dwd_disty_sales_close_duplicate_cpo_header_df.sql`
- `fix_duplicate_close_cpo_header_di_vertica.sql` — companion Vertica DELETE for the same cleanup — `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_duplicate_close_cpo_header_di_vertica.sql`

---

*Document generated from `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/csource/etl/sql/po/source/etl/flows/public_order_tools/ingest/public_cpo_dw/script/fix_dwd_disty_sales_close_cpo_header_extend_di.sql`.*
