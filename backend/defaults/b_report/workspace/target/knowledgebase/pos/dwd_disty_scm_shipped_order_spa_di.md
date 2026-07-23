# DWD: `dwd_disty_scm_shipped_order_spa_di`

- artifact_type: etl_table
- artifact_id: dw_${country_code}.dwd_disty_scm_shipped_order_spa_di
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` loads `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` (layer `DWD`). Purpose inferred from SQL only.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`)
- **Partition:** `date_flag`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_scm_shipped_order_spa_di schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `order_header` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_etl_order_detail_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `dw_${country_code}.dwd_pub_shipped_order_header_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `dw_${country_code}.dwd_pub_shipped_order_detail_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `tmp_order_header_detail` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_etl_order_exp_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `dw_${country_code}.dwd_pub_shipped_order_exp_di` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `tmp_order_profile_rebatre_adj` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_cis_corp_cust_profile` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_cust_profile` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_cis_corp_pm_claim` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_pm_claim` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `tmp_dwd_scm_shipped_spa_order` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_spa_detail` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_spa_header` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `temp_cust_profile` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `ods_${country_code}.ods_etl_spa_cust_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **upstream:** `temp_pm_claim` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` loads `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` (layer `DWD`). Purpose inferred from SQL only.

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| Data / BI consumers | Use target table produced by this ETL |
| Data Engineering | Maintain load logic in evidence script |

### Fact key resolution
- Keys follow target INSERT column list / GROUP BY in evidence SQL.

### Time field semantics
- Partition / date fields: `date_flag`

### Metrics served
- See L3 column derivations for measure expressions when present.

### Metric serving map
N/A — not a multi-period wide serving table (or not documented).

### etl_metrics
No calculable business metrics registered in metric-index for this create run.

## L3 Procedural Knowledge

### Query and routing rules
- Prefer querying the target `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `date_flag>= '${start_date}' and date_flag< '${end_date}') oh join (Select * from dw_${country_code}.dwd_pub_shipped_order_detail_di where date_flag>= '${start_date}' and date_flag< '${end_date}') o...` | Technical (load only) / Business | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["order_header"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S1["ods_${country_code}.ods_etl_order_detail_all"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S2["dw_${country_code}.dwd_pub_shipped_order_header_di"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S3["dw_${country_code}.dwd_pub_shipped_order_detail_di"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S4["tmp_order_header_detail"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S5["ods_${country_code}.ods_etl_order_exp_all"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S6["dw_${country_code}.dwd_pub_shipped_order_exp_di"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S7["tmp_order_profile_rebatre_adj"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S8["ods_cis_corp_cust_profile"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S9["ods_${country_code}.ods_cis_corp_cust_profile"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S10["ods_cis_corp_pm_claim"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
  S11["ods_${country_code}.ods_cis_corp_pm_claim"] --> T["dw_${country_code}.dwd_disty_scm_shipped_order_spa_di"]
```

### Base tables register

| Object | Role |
|--------|------|
| `order_header` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_etl_order_detail_all` | source / temp (from ETL FROM/JOIN) |
| `dw_${country_code}.dwd_pub_shipped_order_header_di` | source / temp (from ETL FROM/JOIN) |
| `dw_${country_code}.dwd_pub_shipped_order_detail_di` | source / temp (from ETL FROM/JOIN) |
| `tmp_order_header_detail` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_etl_order_exp_all` | source / temp (from ETL FROM/JOIN) |
| `dw_${country_code}.dwd_pub_shipped_order_exp_di` | source / temp (from ETL FROM/JOIN) |
| `tmp_order_profile_rebatre_adj` | source / temp (from ETL FROM/JOIN) |
| `ods_cis_corp_cust_profile` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_cust_profile` | source / temp (from ETL FROM/JOIN) |
| `ods_cis_corp_pm_claim` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_pm_claim` | source / temp (from ETL FROM/JOIN) |
| `tmp_dwd_scm_shipped_spa_order` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_spa_detail` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_spa_header` | source / temp (from ETL FROM/JOIN) |
| `temp_cust_profile` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_etl_spa_cust_all` | source / temp (from ETL FROM/JOIN) |
| `temp_pm_claim` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dw_${country_code}.dwd_disty_scm_shipped_order_spa_di`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dw_${country_code}.dwd_pub_shipped_order_header_di` | `ods_${country_code}.ods_etl_order_detail_all` | many:1 | — | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:17`) |
| `dw_${country_code}.dwd_pub_shipped_order_header_di` | `ods_${country_code}.ods_etl_order_exp_all` | many:1 (LEFT) | — | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:70`) |
| `ods_${country_code}.ods_etl_order_exp_all` | `tmp_order_profile_rebatre_adj` | many:1 (LEFT) | `he.order_no` = `op.order_no`; `he.order_type` = `op.order_type`; `he.order_line_no` = `op.order_line_no`; `he.order_expense_line_no` = `op.profile_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:77`) |
| `so` | `ods_${country_code}.ods_cis_corp_spa_detail` | many:1 (LEFT) | `so.spa_no` = `sd.spa_no`; `so.sku_no_exp` = `sd.sku_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:139`) |
| `so` | `ods_${country_code}.ods_cis_corp_spa_header` | many:1 (LEFT) | `so.spa_no` = `sh.spa_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:142`) |
| `so` | `temp_cust_profile` | many:1 (LEFT) | `so.cust_no` = `cp.cust_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:145`) |
| `so` | `ods_${country_code}.ods_etl_spa_cust_all` | many:1 (LEFT) | `sc.cust_no` = `so.cust_no`; `sc.spa_no` = `sh.spa_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:147`) |
| `so` | `temp_pm_claim` | many:1 (LEFT) | `so.scm_no` = `tpc.project_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:150`) |

### Special logic (embedded)

Provenance: `source/ref/pos/special_logic.txt`

#### Applicable rule excerpt 1

```
# POS special logic reference

# Scope
# - Derived from existing Vertica POS rds_xxx_rtv.sp scripts.
# - POS scripts were identified by dw_*/dwd_disty_common_pos_di usage.
# - Vertica scripts were identified by rdsetl.rds_tmp output usage.
# - Scan result used for this file: 499 scripts; regions: BR=1, CA=124, MX=7, US=367.
# - Use xx as the region placeholder, matching table list.txt and table relationship.txt.

# 1. Order line type is not always a simple Comp exclusion
# Default POS reports normally exclude component lines:
#   order_line_type <> 'Comp'
#
# Historical exception patterns:
# - Some vendor/customer sales reports include order_line_type IN ('Comp', 'Single').
# - Some kit-level reports include order_line_type IN ('Comp', 'Kit', 'Single').
# - Component inclusion is usually intentional when the report needs kit components, bundle economics, or vendor/manufacturer line detail.
#
# Rule:
# - Default to excluding Comp unless the request mentions kit components, component detail, bundle detail, or the historical report pattern explicitly includes Comp.
# - Never include Kit, Single, and Comp together unless the report grain and business request require all sold and com...
```

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `order_type` | `so.order_type` | `order_type` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:108` |
| `order_no` | `so.order_no` | `order_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:109` |
| `order_line_no` | `so.order_line_no` | `order_line_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:110` |
| `spa_no` | `so.spa_no` | `spa_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:111` |
| `spa_ref_no` | `so.spa_ref_no` | `spa_ref_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:112` |
| `scm_no` | `so.scm_no` | `scm_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:113` |
| `cust_no` | `so.cust_no` | `cust_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:114` |
| `sku_no` | `so.sku_no` | `sku_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:115` |
| `sku_no_exp` | `so.sku_no_exp` | `sku_no_exp` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:116` |
| `order_qty` | `so.order_qty` | `order_qty` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:117` |
| `sales_adj_amt` | `so.sales_adj_amt` | `sales_adj_amt` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:118` |
| `unit_exp` | `so.unit_exp` | `unit_exp` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:119` |
| `extended_exp` | `so.extended_exp` | `extended_exp` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:120` |
| `exp_code` | `so.exp_code` | `exp_code` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:121` |
| `spa_type` | `sh.spa_type` | `spa_type` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:122` |
| `spa_desc` | `sh.spa_desc` | `spa_desc` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:123` |
| `claim_type` | `tpc.claim_type` | `claim_type` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:124` |
| `approved_cost` | `sd.approved_cost` | `approved_cost` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:125` |
| `rebate_amt` | `sd.rebate_amt` | `rebate_amt` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:126` |
| `spa_keep` | `sc.spa_keep` | `spa_keep` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:127` |
| `customer_spa_keep` | `cp.profile_f` | `profile_f` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | rename | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:128` |
| `vendor_appr_ref_no` | `case when tpc.claim_type = 37 then tpc.pri_approv_ref_no else null end` | `claim_type`, `pri_approv_ref_no` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | case | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:89` |
| `ship_date` | `so.ship_date` | `ship_date` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:133` |
| `invoice_date` | `so.invoice_date` | `invoice_date` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:134` |
| `order_entry_date` | `so.order_entry_date` | `order_entry_date` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:135` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | arithmetic | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:136` |
| `date_flag` | `so.date_flag` | `date_flag` | `tmp_dwd_scm_shipped_spa_order`, `ods_${country_code}.ods_cis_corp_spa_detail`, `ods_${country_code}.ods_cis_corp_spa_header`, `temp_cust_profile`, `ods_${country_code}.ods_etl_spa_cust_all`, `temp_pm_claim` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql:137` |

### Sentinel and code values
Not documented in repository beyond CASE/exp_code predicates in ETL SQL.

## L4 Validation

### Resolved partition value
- Partition expression from ETL: `date_flag`
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
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
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
| `order_header` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_etl_order_detail_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `dw_${country_code}.dwd_pub_shipped_order_header_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `dw_${country_code}.dwd_pub_shipped_order_detail_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `tmp_order_header_detail` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_etl_order_exp_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `dw_${country_code}.dwd_pub_shipped_order_exp_di` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `tmp_order_profile_rebatre_adj` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_cis_corp_cust_profile` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_cis_corp_cust_profile` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_cis_corp_pm_claim` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_cis_corp_pm_claim` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `tmp_dwd_scm_shipped_spa_order` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_cis_corp_spa_detail` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_cis_corp_spa_header` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `temp_cust_profile` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `ods_${country_code}.ods_etl_spa_cust_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |
| `temp_pm_claim` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_scm_shipped_order_spa_di/dwd_disty_scm_shipped_order_spa_di.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:208` |
| KB / contract ref: `source/contracts/pos/golden-questions.md` | `source/contracts/pos/golden-questions.md:14` |
| KB / contract ref: `source/contracts/pos/metric-index.md` | `source/contracts/pos/metric-index.md:135` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_scm_shipped_order_spa_di.md` | `source/contracts/pos/tables/dwd_disty_scm_shipped_order_spa_di.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql` | `source/contracts/rds/vertica_cpo/etl/cpo_pos_open_close_vendor_quote_rds_18556.sql:18` |
| ETL/script ref: `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_union_brpt_scm_spa_rds_17956.sql` | `source/contracts/rds/vertica_open_so_bo/etl/open_so_bo_union_brpt_scm_spa_rds_17956.sql:25` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_bo_shipping_multisheet_rds_9127.sql` | `source/contracts/rds/vertica_pos/etl/pos_bo_shipping_multisheet_rds_9127.sql:46` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_spa_scm_claim_rds_5380.sql` | `source/contracts/rds/vertica_pos/etl/pos_spa_scm_claim_rds_5380.sql:32` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_br_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_br_level1.flow:281` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_ca_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_ca_level1.flow:274` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hycn_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hycn_level1.flow:262` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyuk_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyuk_level1.flow:262` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyus_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyus_level1.flow:270` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyww_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_hyww_level1.flow:262` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_us_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_us_level1.flow:288` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_wcla_level1.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level1/public_order_dw_wcla_level1.flow:271` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_br.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_br.flow:73` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_ca.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_ca.flow:71` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hycn.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hycn.flow:71` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyuk.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyuk.flow:71` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyus.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyus.flow:71` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyww.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyww.flow:72` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_us.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_us.flow:71` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_wcla.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_wcla.flow:71` |
| ETL/script ref: `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_scm_shipped_order_spa_di.sql` | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_scm_shipped_order_spa_di.sql:106` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_cpo/cpo_pos_open_close_vendor_quote_rds_18556.md` | `target/knowledgebase/RDS/vertica_cpo/cpo_pos_open_close_vendor_quote_rds_18556.md:52` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_union_brpt_scm_spa_rds_17956.md` | `target/knowledgebase/RDS/vertica_open_so_bo/open_so_bo_union_brpt_scm_spa_rds_17956.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_bo_shipping_multisheet_rds_9127.md` | `target/knowledgebase/RDS/vertica_pos/pos_bo_shipping_multisheet_rds_9127.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_spa_scm_claim_rds_5380.md` | `target/knowledgebase/RDS/vertica_pos/pos_spa_scm_claim_rds_5380.md:52` |
| KB / contract ref: `target/knowledgebase/order/dwd_disty_scm_open_order_spa_df.md` | `target/knowledgebase/order/dwd_disty_scm_open_order_spa_df.md:559` |
| KB / contract ref: `target/knowledgebase/order/dwd_disty_scm_shipped_order_spa_di.md` | `target/knowledgebase/order/dwd_disty_scm_shipped_order_spa_di.md:1` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:112` |

#### Operational detail (verified)
- Partition clause: `date_flag`

#### Not documented in repository
- Schedule, owner, SLA
