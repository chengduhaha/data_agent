# DIM: Sales customer type date-flag snapshot (`dim_${country_code}.dim_pub_sales_cust_type_df`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_sales_cust_type_df
- domain: customer
- one_line_purpose: Partitioned daily snapshot of `dim_pub_sales_cust_type` attributes (cust type, division, credit-risk parameters) for date-flagged reporting and downstream consumers.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_sales_cust_type_df`
- **Layer type:** DIM
- **Canonical / derived:** Derived snapshot — full column copy from `dim_pub_sales_cust_type` into a `date_flag` partition
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per `cust_type` within a `date_flag` partition (same grain as current `dim_pub_sales_cust_type`)
- **Scope:** Country-scoped DIM schema via `${country_code}`; US flow uses `country_code: us`
- **Partition:** `date_flag = ${date_flag}` — see L4
- **Natural key:** `cust_type` (+ partition `date_flag`)
- **Exclusions:** None in this script (no WHERE filter)

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_sales_cust_type_df` | ETL INSERT OVERWRITE target |
| Vertica | pending for `_df` | `dim_${country_code}.dim_pub_sales_cust_type` | Flow syncs non-`_df` table from `dim_pub_sales_cust_type`, not this `_df` target — `public_customer_dimension_us.flow:322-329` |

### Physical schema reference

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_sales_cust_type_df` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_dim_us_dim_pub_sales_cust_type_df.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "customer dim_pub_sales_cust_type_df schema" --intent find_table_schema` |

### Lineage
- **upstream:** `dim_${country_code}.dim_pub_sales_cust_type` — full SELECT passthrough — `dim_pub_sales_cust_type_df.sql:1-17`
- **downstream:** Not documented in repository as a direct `FROM` of this `_df` FQN (Vertica reporting uses non-`_df` sync from `dim_pub_sales_cust_type`)

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | `INSERT OVERWRITE` partition `date_flag = ${date_flag}` |
| Schedule | Flow cron `0 55 0 ? * *` on `public_customer_dimension_us.flow` (flow-level; not job-specific SLA) |
| Parameters | `${country_code}`, `${date_flag}` (depends on `gen_date_parameter` + `dim_pub_sales_cust_type`) |

---

## L2 Declarative Knowledge

### Business purpose
This job copies the current sales customer-type dimension into a date-partitioned snapshot table. It preserves customer-type codes, descriptions, division affiliation, credit-risk and margin parameters, back-order expiry, GL department, and manager IDs so historical or date-flagged loads can read a point-in-time copy without mutating the non-partitioned dimension.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Sales / ops reporting** | Date-flagged cust-type attributes aligned to pipeline `${date_flag}` |
| **Credit & risk** | Snapshot of `min_net_margin`, `credit_risk_rate`, `bo_expire_days` by type |
| **Downstream ETL** | Partitioned DIM feed when a date-scoped cust-type copy is required |

### Identifier search profile
- Primary lookup: `cust_type`
- Always constrain to the intended `date_flag` partition when querying `_df`

### Time field semantics
- **`date_flag`:** load partition from Azkaban/bootstrap `${date_flag}` (see L4); not a business effective-date column derived in this SQL

### Metrics served
| Category | Columns | Business reading |
|----------|---------|------------------|
| Measures | — | No measure columns in this ETL |

### Metric serving map
N/A — not a multi-period serving table.

### etl_metrics
No calculable metrics on this table. Formula authority: [`source/contracts/customer/metric-index.md`](../../source/contracts/customer/metric-index.md).

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Filter reporting queries by `date_flag` to the partition of interest.
**Technical predicates (load only):** Partition clause only — no business WHERE in the SELECT.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| None in this job | — | Single-table SELECT from current DIM | `dim_pub_sales_cust_type_df.sql:17` |

### Key filters and ETL business logic
- **Technical (load only):** `PARTITION (date_flag = ${date_flag})` on INSERT OVERWRITE — `dim_pub_sales_cust_type_df.sql:1`
- No WHERE / HAVING / JOIN-ON business predicates in this script
- **Special logic applied in this ETL:** none beyond full overwrite of the partition from current DIM

### Standard time-filter SQL
```sql
SELECT *
FROM dim_${country_code}.dim_pub_sales_cust_type_df
WHERE date_flag = '${partition_value}';
```

### End-to-end flow
1. Flow job `dim_pub_sales_cust_type` builds current `dim_pub_sales_cust_type`.
2. `gen_date_parameter` supplies `${date_flag}`.
3. This script SELECT * columns from `dim_pub_sales_cust_type` and INSERT OVERWRITE into `dim_pub_sales_cust_type_df` partition `${date_flag}`.

```mermaid
flowchart LR
  CT["dim_pub_sales_cust_type"]
  DF["dim_pub_sales_cust_type_df\npartition date_flag"]
  CT -->|INSERT OVERWRITE passthrough| DF
```

### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dim_${country_code}.dim_pub_sales_cust_type` | Sole source — alias `ct` |
| `dim_${country_code}.dim_pub_sales_cust_type_df` | Target partitioned DIM |

### Step-by-step logic
#### Step 1 — INSERT OVERWRITE partition from current DIM
**Source:** `dim_${country_code}.dim_pub_sales_cust_type ct`  
**Filter:** none  
**Join keys:** none  
**Load:** all listed columns into `dim_pub_sales_cust_type_df` for `${date_flag}` — `dim_pub_sales_cust_type_df.sql:1-17`

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | Not documented in repository |

`source/ref/customer/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cust_type` | `ct.cust_type` | `cust_type` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:3` |
| `cust_type_descr` | `ct.cust_type_descr` | `cust_type_descr` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:4` |
| `entry_datetime` | `ct.entry_datetime` | `entry_datetime` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:5` |
| `entry_id` | `ct.entry_id` | `entry_id` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:6` |
| `min_net_margin` | `ct.min_net_margin` | `min_net_margin` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:7` |
| `credit_risk_rate` | `ct.credit_risk_rate` | `credit_risk_rate` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:8` |
| `bo_expire_days` | `ct.bo_expire_days` | `bo_expire_days` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:9` |
| `gl_dept_no` | `ct.gl_dept_no` | `gl_dept_no` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:10` |
| `sales_group` | `ct.sales_group` | `sales_group` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:11` |
| `division` | `ct.division` | `division` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:12` |
| `division_desc` | `ct.division_desc` | `division_desc` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:13` |
| `manager_id` | `ct.manager_id` | `manager_id` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:14` |
| `backup_id` | `ct.backup_id` | `backup_id` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:15` |
| `end_date` | `ct.end_date` | `end_date` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:16` |
| `ge_leasing` | `ct.ge_leasing` | `ge_leasing` | `dim_${country_code}.dim_pub_sales_cust_type` | passthrough | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:17` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `end_date` / `ge_leasing` | Pass-through from source DIM; meanings not redefined in this script |

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | `gen_date_parameter` job in `public_customer_dimension_us.flow` | Produces `${date_flag}` consumed by this job (`dependsOn: gen_date_parameter`, `dim_pub_sales_cust_type`) — `public_customer_dimension_us.flow:179-185` |
| 2 | INSERT clause | `PARTITION (date_flag = ${date_flag})` — `dim_pub_sales_cust_type_df.sql:1` |

**Plain language:** Do not hardcode calendar dates; use the flow-resolved `${date_flag}`.

### Data quality checks
- Row count for `${date_flag}` should match current `dim_pub_sales_cust_type` (1:1 copy)
- Grain: no duplicate `cust_type` within a partition

### Validation SQL
```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_sales_cust_type_df
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Compare to current DIM
SELECT
  (SELECT COUNT(*) FROM dim_${country_code}.dim_pub_sales_cust_type) AS src_cnt,
  (SELECT COUNT(*) FROM dim_${country_code}.dim_pub_sales_cust_type_df WHERE date_flag = '${partition_value}') AS df_cnt;

-- 3) Grain duplicate check
SELECT cust_type, date_flag, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_sales_cust_type_df
WHERE date_flag = '${partition_value}'
GROUP BY cust_type, date_flag
HAVING COUNT(*) > 1;
```

### Caveats for interpretation
- This is a snapshot of whatever is currently in `dim_pub_sales_cust_type` at run time; historical attribute history beyond stored partitions is Not documented in repository.
- Vertica hive2vertica for cust type reads the non-`_df` table, not this snapshot.

### Conflicts and open questions
- Owner / SLA for this specific job: Not documented in repository
- Whether consumers should prefer `_df` vs Vertica `dim_pub_sales_cust_type`: Not documented beyond flow sync evidence

---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| Partitioned snapshot | `dim_${country_code}.dim_pub_sales_cust_type_df` | Not synced from `_df` in US flow | — | `dim_pub_sales_cust_type_df.sql` | pending |
| Reporting DIM (related) | `dim_${country_code}.dim_pub_sales_cust_type` | `dim_${country_code}.dim_pub_sales_cust_type` | hive2vertica overwrite | `public_customer_dimension_us.flow:322-329` | pending |

### Access constraints
- Schema suffix `${country_code}` / flow `country_code`

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes (`date_flag`) |
| scan_risk_tier | low |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Pipeline / snapshot consumers** | Date-partitioned copy of cust-type dimension |
| **Reporting (Vertica)** | Prefer synced `dim_pub_sales_cust_type` per flow (not this `_df`) |

### Representative query patterns
```sql
SELECT cust_type, cust_type_descr, division_desc, min_net_margin, credit_risk_rate
FROM dim_${country_code}.dim_pub_sales_cust_type_df
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_${country_code}.dim_pub_sales_cust_type` | Sole SELECT source | `dim_pub_sales_cust_type_df.sql:17` |

#### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Flow orchestration only (`dim_pub_sales_cust_type_df` job) | `public_customer_dimension_us.flow:179-185` |
| Direct SQL consumers of `_df` FQN | Not documented in repository |

#### Operational detail (verified)
- Depends on `dim_pub_sales_cust_type` + `gen_date_parameter` — `public_customer_dimension_us.flow:181-183`

#### Not documented in repository
- Owner, job-level SLA
- `source/ref/customer/special_logic.txt` / table relationship
- DDL seed / Vertica MCP verification for `_df`

---

*Evidence: `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql`; flow `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_us.flow`.*
