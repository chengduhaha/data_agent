# DIM: `dim_pub_sales_cust_type`

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_sales_cust_type
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` loads `dim_${country_code}.dim_pub_sales_cust_type` (layer `DIM`). Purpose inferred from SQL only.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_sales_cust_type`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql`)
- **Partition:** `See L4 / ETL partition clause`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_sales_cust_type` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_sales_cust_type` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `See L4 / ETL partition clause` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_pub_sales_cust_type schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_cust_type` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_division` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` loads `dim_${country_code}.dim_pub_sales_cust_type` (layer `DIM`). Purpose inferred from SQL only.

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
- Prefer querying the target `dim_${country_code}.dim_pub_sales_cust_type` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["ods_${country_code}.ods_cis_corp_cust_type"] --> T["dim_${country_code}.dim_pub_sales_cust_type"]
  S1["ods_${country_code}.ods_cis_corp_division"] --> T["dim_${country_code}.dim_pub_sales_cust_type"]
```

### Base tables register

| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_cust_type` | source / temp (from ETL FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_division` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dim_${country_code}.dim_pub_sales_cust_type`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_cust_type` | `ods_${country_code}.ods_cis_corp_division` | many:1 (LEFT) | `ct.division` = `dv.division` | etl_sql (`source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:19`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_${country_code}.dim_pub_sales_cust_type`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `cust_type` | `ct.cust_type` | `cust_type` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:3` |
| `cust_type_descr` | `ct.cust_type_descr` | `cust_type_descr` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:4` |
| `entry_datetime` | `ct.entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:5` |
| `entry_id` | `ct.entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:6` |
| `min_net_margin` | `ct.min_net_margin` | `min_net_margin` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:7` |
| `credit_risk_rate` | `ct.credit_risk_rate` | `credit_risk_rate` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:8` |
| `bo_expire_days` | `ct.bo_expire_days` | `bo_expire_days` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:9` |
| `gl_dept_no` | `ct.gl_dept_no` | `gl_dept_no` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:10` |
| `sales_group` | `ct.sales_group` | `sales_group` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:11` |
| `division` | `ct.division` | `division` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:12` |
| `division_desc` | `dv.division_desc` | `division_desc` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:13` |
| `manager_id` | `ct.manager_id` | `manager_id` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:14` |
| `backup_id` | `ct.backup_id` | `backup_id` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:15` |
| `end_date` | `ct.end_date` | `end_date` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:16` |
| `ge_leasing` | `ct.ge_leasing` | `ge_leasing` | `ods_${country_code}.ods_cis_corp_cust_type`, `ods_${country_code}.ods_cis_corp_division` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql:17` |

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
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` |
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
| `ods_${country_code}.ods_cis_corp_cust_type` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` |
| `ods_${country_code}.ods_cis_corp_division` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_sales_cust_type/dim_pub_sales_cust_type.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/b-report-us/bitbicket_etl/readme.md` | `source/contracts/b-report-us/bitbicket_etl/readme.md:39` |
| KB / contract ref: `source/contracts/b-report-us/domain-knowledge.md` | `source/contracts/b-report-us/domain-knowledge.md:108` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_sales_cust_type.md` | `source/contracts/b-report-us/tables/dim_pub_sales_cust_type.md:1` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_sales_division.md` | `source/contracts/b-report-us/tables/dim_pub_sales_division.md:68` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_sales_territory.md` | `source/contracts/b-report-us/tables/dim_pub_sales_territory.md:50` |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:86` |
| KB / contract ref: `source/contracts/pos/tables/dim_disty_bd_project_cust.md` | `source/contracts/pos/tables/dim_disty_bd_project_cust.md:44` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_customer_info.md` | `source/contracts/pos/tables/dim_pub_customer_info.md:45` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_customer_info_rt.md` | `source/contracts/pos/tables/dim_pub_customer_info_rt.md:45` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_sales_cust_type.md` | `source/contracts/pos/tables/dim_pub_sales_cust_type.md:5` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_sales_hierarchy_by_terr_user_role.md` | `source/contracts/pos/tables/dim_pub_sales_hierarchy_by_terr_user_role.md:53` |
| KB / contract ref: `source/contracts/pos/tables/dim_pub_sales_hierarchy_primary_role_by_terr_view.md` | `source/contracts/pos/tables/dim_pub_sales_hierarchy_primary_role_by_terr_view.md:46` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_ar_cust_doc_df.md` | `source/contracts/pos/tables/dwd_disty_ar_cust_doc_df.md:80` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_brpt_bo_detail_df.md` | `source/contracts/pos/tables/dwd_disty_brpt_bo_detail_df.md:48` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_brpt_orders_pl_etl_mi.md` | `source/contracts/pos/tables/dwd_disty_brpt_orders_pl_etl_mi.md:49` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_common_dw_orders_pl_extend_di.md` | `source/contracts/pos/tables/dwd_disty_common_dw_orders_pl_extend_di.md:86` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_common_pos_di.md` | `source/contracts/pos/tables/dwd_disty_common_pos_di.md:97` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_sales_open_order_detail.md` | `source/contracts/pos/tables/dwd_disty_sales_open_order_detail.md:68` |
| KB / contract ref: `source/contracts/pos/tables/dws_disty_brpt_cust_mtd.md` | `source/contracts/pos/tables/dws_disty_brpt_cust_mtd.md:48` |
| ETL/script ref: `source/contracts/rds/vertica_b_report/etl/b_report_acq_cloud_legacy_invoice_rds_1241.sql` | `source/contracts/rds/vertica_b_report/etl/b_report_acq_cloud_legacy_invoice_rds_1241.sql:153` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_br.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_br.flow:154` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_ca.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_ca.flow:154` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hycn.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hycn.flow:281` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyuk.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyuk.flow:283` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyus.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyus.flow:283` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyww.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_hyww.flow:283` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_us.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_us.flow:171` |
| FLOW ref: `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_wcla.flow` | `source/etl/flows/public_order_scripts/public_customer_dimension/public_customer_dimension_wcla.flow:154` |
| ETL/script ref: `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type.sql` | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type.sql:1` |
| ETL/script ref: `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql` | `source/etl/sql/customer/public_order_scripts/public_customer_dimension/script/dim_pub_sales_cust_type_df.sql:1` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_b_report/b_report_acq_cloud_legacy_invoice_rds_1241.md` | `target/knowledgebase/RDS/vertica_b_report/b_report_acq_cloud_legacy_invoice_rds_1241.md:59` |
| KB / contract ref: `target/knowledgebase/b-report-us/dim_pub_sales_cust_type.md` | `target/knowledgebase/b-report-us/dim_pub_sales_cust_type.md:1` |
| KB / contract ref: `target/knowledgebase/b-report-us/dim_pub_sales_territory.md` | `target/knowledgebase/b-report-us/dim_pub_sales_territory.md:118` |
| KB / contract ref: `target/knowledgebase/customer/dim_pub_sales_cust_type.md` | `target/knowledgebase/customer/dim_pub_sales_cust_type.md:1` |
| KB / contract ref: `target/knowledgebase/customer/dim_pub_sales_cust_type_df.md` | `target/knowledgebase/customer/dim_pub_sales_cust_type_df.md:1` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:102` |

#### Operational detail (verified)
- Partition clause: `See L4 / ETL partition clause`

#### Not documented in repository
- Schedule, owner, SLA
