# DIM: `dim_pub_vpl_pm_hierarchy_info`

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vpl_pm_hierarchy_info
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` loads `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` (layer `DIM`). Purpose inferred from SQL only.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`)
- **Partition:** `See L4 / ETL partition clause`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `See L4 / ETL partition clause` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_pub_vpl_pm_hierarchy_info schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`
- **upstream:** `dim_${country_code}.dim_pub_vpl_hierarchy_info` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`
- **upstream:** `dim_us.dim_pub_manager` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`
- **upstream:** `dim_${country_code}.dim_pub_manager` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` loads `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` (layer `DIM`). Purpose inferred from SQL only.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| Data / BI consumers | Use target table produced by this ETL |
| Data Engineering | Maintain load logic in evidence script |

### Fact key resolution
- Keys follow target INSERT column list / GROUP BY in evidence SQL.

### Time field semantics
- Partition / date fields: `See L4 / ETL partition clause`

### Metrics served
- See L3 column derivations for measure expressions when present.

### Metric serving map
N/A — not a multi-period wide serving table (or not documented).

### etl_metrics
No calculable business metrics registered in metric-index for this create run.

## L3 Procedural Knowledge

### Query and routing rules
- Prefer querying the target `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["dim_${country_code}.dim_pub_vpl_hierarchy_info"] --> T["dim_${country_code}.dim_pub_vpl_pm_hierarchy_info"]
  S1["dim_us.dim_pub_manager"] --> T["dim_${country_code}.dim_pub_vpl_pm_hierarchy_info"]
  S2["dim_${country_code}.dim_pub_manager"] --> T["dim_${country_code}.dim_pub_vpl_pm_hierarchy_info"]
```

### Base tables register

| Object | Role |
|--------|------|
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | source / temp (from ETL FROM/JOIN) |
| `dim_us.dim_pub_manager` | source / temp (from ETL FROM/JOIN) |
| `dim_${country_code}.dim_pub_manager` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dim_${country_code}.dim_pub_vpl_pm_hierarchy_info`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | `dim_us.dim_pub_manager` | many:1 (LEFT) | `vh.pm_vp_id` = `vp.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:43`) |
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | `dim_${country_code}.dim_pub_manager` | many:1 (LEFT) | `vh.pm_director_id` = `dir.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:45`) |
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | `dim_${country_code}.dim_pub_manager` | many:1 (LEFT) | `vh.pm_manager_id` = `mgr.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:47`) |
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | `dim_${country_code}.dim_pub_manager` | many:1 (LEFT) | `vh.pm_id` = `pm.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:49`) |
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | `dim_${country_code}.dim_pub_manager` | many:1 (LEFT) | `vh.pm_primary_backup_id` = `bak.userid` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:51`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_${country_code}.dim_pub_vpl_pm_hierarchy_info`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `vh.vend_no` | `vend_no` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:3` |
| `vpl_no` | `vh.vpl_no` | `vpl_no` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:4` |
| `pm_vp_id` | `vh.pm_vp_id` | `pm_vp_id` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:5` |
| `pm_vp_name` | `case when vh.pm_vp_id is null then 'No Assignment' when vp.termdate is null then vh.pm_vp_name else concat(vh.pm_vp_n...` | `pm_vp_id`, `No`, `Assignment`, `termdate`, `pm_vp_name`, `Termed` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | case | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:2` |
| `pm_vp_email` | `vh.pm_vp_email` | `pm_vp_email` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:11` |
| `pm_director_id` | `vh.pm_director_id` | `pm_director_id` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:12` |
| `pm_director_name` | `case when vh.pm_director_id is null then 'No Assignment' when dir.termdate is null then vh.pm_director_name else conc...` | `pm_director_id`, `No`, `Assignment`, `termdate`, `pm_director_name`, `Termed` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | case | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:2` |
| `pm_director_email` | `vh.pm_director_email` | `pm_director_email` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:18` |
| `pm_manager_id` | `vh.pm_manager_id` | `pm_manager_id` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:19` |
| `pm_manager_name` | `case when vh.pm_manager_id is null then 'No Assignment' when mgr.termdate is null then pm_manager_name else concat(vh...` | `pm_manager_id`, `No`, `Assignment`, `termdate`, `pm_manager_name`, `Termed` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | case | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:2` |
| `pm_manager_email` | `vh.pm_manager_email` | `pm_manager_email` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:25` |
| `pm_id` | `vh.pm_id` | `pm_id` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:26` |
| `pm_name` | `case when vh.pm_id is null then 'No Assignment' when pm.termdate is null then vh.pm_name else concat(pm_name, ' (Term...` | `pm_id`, `No`, `Assignment`, `termdate`, `pm_name`, `Termed` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | case | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:2` |
| `pm_email` | `vh.pm_email` | `pm_email` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:32` |
| `pm_primary_backup_id` | `vh.pm_primary_backup_id` | `pm_primary_backup_id` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:33` |
| `pm_primary_backup_name` | `case when vh.pm_primary_backup_id is null then 'No Assignment' when bak.termdate is null then vh.pm_primary_backup_na...` | `pm_primary_backup_id`, `No`, `Assignment`, `termdate`, `pm_primary_backup_name`, `Termed` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | case | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:2` |
| `pm_primary_backup_email` | `vh.pm_primary_backup_email` | `pm_primary_backup_email` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:39` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `dim_${country_code}.dim_pub_vpl_hierarchy_info`, `dim_us.dim_pub_manager`, `dim_${country_code}.dim_pub_manager` | arithmetic | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql:40` |

### Sentinel and code values
Not documented in repository beyond CASE/exp_code predicates in ETL SQL.

## L4 Validation

### Resolved partition value
- Partition expression from ETL: `See L4 / ETL partition clause`
- Runtime values: Not documented in repository (resolve via Azkaban params when flow evidence exists).

### Data quality checks
Not documented in repository

### Validation SQL
N/A — Vertica MCP not executed during documentation (Vertica no-run policy).

### Caveats for interpretation
- Generated from ETL SQL evidence only; business definitions may need `source/ref` enrichment.

### Conflicts and open questions
None identified in repository

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |
| Serving | Vertica (when synced) | Not documented in repository |

### Access constraints
Not documented in repository

### Query risk profile
- Scan risk depends on partition pruning; always filter partition keys when present.

## L6 Access and Consumption

### Primary consumers and use cases
Not documented in repository

### Representative query patterns
Not documented in repository

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `dim_${country_code}.dim_pub_vpl_hierarchy_info` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |
| `dim_us.dim_pub_manager` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |
| `dim_${country_code}.dim_pub_manager` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_vpl_pm_hierarchy_info/dim_pub_vpl_pm_hierarchy_info.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:116` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_vpl_pm_hierarchy_info.md` | `source/contracts/pos/tables/dim_pub_vpl_pm_hierarchy_info.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql` | `source/contracts/rds/vertica_inventory/etl/inv_rollover_witypestu_stock_rotation_rds_11722.sql:772` |
| ETL/script ref: `source/contracts/rds/vertica_inventory/etl/inv_upc_part_aging_qty_rds_19269.sql` | `source/contracts/rds/vertica_inventory/etl/inv_upc_part_aging_qty_rds_19269.sql:48` |
| ETL/script ref: `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql` | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_request_dates_freight_pm_rds_19390.sql:56` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_br.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_br.flow:145` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_ca.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_ca.flow:134` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hycn.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hycn.flow:111` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyuk.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyuk.flow:111` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyus.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyus.flow:110` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyww.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_hyww.flow:93` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_us.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_us.flow:78` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_wcla.flow` | `source/etl/flows/public_order_scripts/public_vpl_dimension/public_vpl_dimension_wcla.flow:155` |
| ETL/script ref: `source/etl/sql/vendor/public_order_scripts/public_vpl_dimension/script/dim_pub_vpl_pm_hierarchy_info.sql` | `source/etl/sql/vendor/public_order_scripts/public_vpl_dimension/script/dim_pub_vpl_pm_hierarchy_info.sql:1` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_rollover_witypestu_stock_rotation_rds_11722.md` | `target/knowledgebase/RDS/vertica_inventory/inv_rollover_witypestu_stock_rotation_rds_11722.md:179` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_inventory/inv_upc_part_aging_qty_rds_19269.md` | `target/knowledgebase/RDS/vertica_inventory/inv_upc_part_aging_qty_rds_19269.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_request_dates_freight_pm_rds_19390.md` | `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_request_dates_freight_pm_rds_19390.md:53` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:108` |
| KB / contract ref: `target/knowledgebase/vendor/dim_pub_vpl_hierarchy_info.md` | `target/knowledgebase/vendor/dim_pub_vpl_hierarchy_info.md:83` |
| KB / contract ref: `target/knowledgebase/vendor/dim_pub_vpl_pm_hierarchy_info.md` | `target/knowledgebase/vendor/dim_pub_vpl_pm_hierarchy_info.md:1` |

#### Operational detail (verified)
- Partition clause: `See L4 / ETL partition clause`

#### Not documented in repository
- Schedule, owner, SLA
