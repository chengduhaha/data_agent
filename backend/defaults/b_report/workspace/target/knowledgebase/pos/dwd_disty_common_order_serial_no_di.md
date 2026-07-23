# DWD: `dwd_disty_common_order_serial_no_di`

- artifact_type: etl_table
- artifact_id: dw_${country_code}.dwd_disty_common_order_serial_no_di
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` loads `dw_${country_code}.dwd_disty_common_order_serial_no_di` (layer `DWD`). Purpose inferred from SQL only.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_${country_code}.dwd_disty_common_order_serial_no_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`)
- **Partition:** `date_flag`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country_code}.dwd_disty_common_order_serial_no_di` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_${country_code}.dwd_disty_common_order_serial_no_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_common_order_serial_no_di schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **upstream:** `dw_${country_code}.dwd_disty_brpt_orders_pl_etl_mi` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **upstream:** `dw_orders_pl_temp` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_history_serial_nbr` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **upstream:** `ods_${country_code}.ods_etl_order_detail_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_cws_rma_ser` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` loads `dw_${country_code}.dwd_disty_common_order_serial_no_di` (layer `DWD`). Purpose inferred from SQL only.

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
- Prefer querying the target `dw_${country_code}.dwd_disty_common_order_serial_no_di` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `dt_month >= DATE_FORMAT('${last_180_date}','yyyy-MM') and date_flag >= '${last_180_date}' and date_flag < '${end_date}'; insert overwrite table dw_${country_code}.dwd_disty_common_order_serial_no_d...` | Technical (load only) / Business | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["dw_${country_code}.dwd_disty_brpt_orders_pl_etl_mi"] --> T["dw_${country_code}.dwd_disty_common_order_serial_no_di"]
  S1["dw_orders_pl_temp"] --> T["dw_${country_code}.dwd_disty_common_order_serial_no_di"]
  S2["ods_${country_code}.ods_cis_corp_history_serial_nbr"] --> T["dw_${country_code}.dwd_disty_common_order_serial_no_di"]
  S3["ods_${country_code}.ods_etl_order_detail_all"] --> T["dw_${country_code}.dwd_disty_common_order_serial_no_di"]
  S4["ods_${country_code}.ods_cis_corp_cws_rma_ser"] --> T["dw_${country_code}.dwd_disty_common_order_serial_no_di"]
```

### Base tables register

| Object | Role |
|--------|------|
| `dw_${country_code}.dwd_disty_brpt_orders_pl_etl_mi` | source / temp (from ETL FROM/JOIN) |
| `dw_orders_pl_temp` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_history_serial_nbr` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_etl_order_detail_all` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_cws_rma_ser` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dw_${country_code}.dwd_disty_common_order_serial_no_di`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_etl_order_detail_all` | `ods_${country_code}.ods_cis_corp_cws_rma_ser` | many:1 | `c.int_ref_no` = `a.rma_no`; `c.int_ref_line_no` = `a.rma_line_no` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql:23`) |

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
| `b` | `b.*` | `b` | `dw_orders_pl_temp`, `ods_${country_code}.ods_cis_corp_history_serial_nbr`, `ods_${country_code}.ods_etl_order_detail_all`, `ods_${country_code}.ods_cis_corp_cws_rma_ser` | arithmetic | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql:11` |
| `date_flag` | `a.date_flag` | `date_flag` | `dw_orders_pl_temp`, `ods_${country_code}.ods_cis_corp_history_serial_nbr`, `ods_${country_code}.ods_etl_order_detail_all`, `ods_${country_code}.ods_cis_corp_cws_rma_ser` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql:12` |

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
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |
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
| `dw_${country_code}.dwd_disty_brpt_orders_pl_etl_mi` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |
| `dw_orders_pl_temp` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |
| `ods_${country_code}.ods_cis_corp_history_serial_nbr` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |
| `ods_${country_code}.ods_etl_order_detail_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |
| `ods_${country_code}.ods_cis_corp_cws_rma_ser` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_common_order_serial_no_di/dwd_disty_common_order_serial_no_di.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:165` |
| KB / contract ref: `source/contracts/pos/golden-questions.md` | `source/contracts/pos/golden-questions.md:26` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_common_order_serial_no_di.md` | `source/contracts/pos/tables/dwd_disty_common_order_serial_no_di.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:451` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql:451` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql` | `source/contracts/rds/vertica_pos/etl/pos_serial_authorization_rds_5378.sql:49` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_spa_horizontal_rds_16358.sql` | `source/contracts/rds/vertica_pos/etl/pos_spa_horizontal_rds_16358.sql:233` |
| ETL/script ref: `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql` | `source/contracts/rds/vertica_vpo/etl/vpo_pos_doc_fallback_cedm_serial_rds_610.sql:251` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_br_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_br_level3.flow:134` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_ca_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_ca_level3.flow:135` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hycn_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hycn_level3.flow:174` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyuk_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyuk_level3.flow:173` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyus_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyus_level3.flow:172` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyww_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_hyww_level3.flow:171` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_us_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_us_level3.flow:134` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_wcla_level3.flow` | `source/etl/flows/public_order_scripts/public_order_dw/level3/public_order_dw_wcla_level3.flow:133` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_br.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_br.flow:213` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_ca.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_ca.flow:211` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hycn.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hycn.flow:211` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyuk.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyuk.flow:211` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyus.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyus.flow:211` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyww.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_hyww.flow:212` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_us.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_us.flow:211` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_wcla.flow` | `source/etl/flows/public_order_scripts/public_order_dw/public_order_dw_wcla.flow:211` |
| ETL/script ref: `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_order_serial_no_di.sql` | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_order_serial_no_di.sql:10` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md:176` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md:176` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_serial_authorization_rds_5378.md` | `target/knowledgebase/RDS/vertica_pos/pos_serial_authorization_rds_5378.md:54` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_spa_horizontal_rds_16358.md` | `target/knowledgebase/RDS/vertica_pos/pos_spa_horizontal_rds_16358.md:53` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_vpo/vpo_pos_doc_fallback_cedm_serial_rds_610.md` | `target/knowledgebase/RDS/vertica_vpo/vpo_pos_doc_fallback_cedm_serial_rds_610.md:171` |
| KB / contract ref: `target/knowledgebase/order/dwd_disty_common_order_serial_no_di.md` | `target/knowledgebase/order/dwd_disty_common_order_serial_no_di.md:1` |
| KB / contract ref: `target/knowledgebase/order/dwd_pub_common_history_serial_nbr_df.md` | `target/knowledgebase/order/dwd_pub_common_history_serial_nbr_df.md:338` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:110` |

#### Operational detail (verified)
- Partition clause: `date_flag`

#### Not documented in repository
- Schedule, owner, SLA
