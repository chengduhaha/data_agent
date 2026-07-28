# DIM: `dim_pub_date`

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_date
- domain: pos
- one_line_purpose: ETL script `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` loads `dim_${country_code}.dim_pub_date` (layer `DIM`). Purpose inferred from SQL only.
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dim_pub_date/

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_date`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- **Grain:** Not documented in repository (see SELECT/GROUP BY in `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql`)
- **Partition:** `See L4 / ETL partition clause`
- **Exclusions:** See L3 Key filters

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_date` | ETL target |
| Vertica | Not documented in repository | — | Confirm via hive2vertica flow |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_date` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `See L4 / ETL partition clause` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dim_pub_date schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_dw_calendar` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 INSERT / OVERWRITE in evidence script |
| Schedule | Not documented in repository |
| Parameters | Parsed from ETL literals / `${...}` in `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` |

## L2 Declarative Knowledge

### Business purpose
ETL script `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` loads `dim_${country_code}.dim_pub_date` (layer `DIM`). Purpose inferred from SQL only.

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
- Prefer querying the target `dim_${country_code}.dim_pub_date` after successful ETL load.

### Dimension join patterns
- See Relationship map and Base tables register.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| — | — | No WHERE clause parsed from `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` |

### Standard time-filter SQL
```sql
-- See partition / date predicates in source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql
```

### End-to-end flow

```mermaid
flowchart LR
  S0["ods_${country_code}.ods_cis_corp_dw_calendar"] --> T["dim_${country_code}.dim_pub_date"]
```

### Base tables register

| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | source / temp (from ETL FROM/JOIN) |

### Step-by-step logic
1. Read sources listed in Base tables register (`source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql`).
2. Apply filters documented under Key filters.
3. INSERT OVERWRITE / write target `dim_${country_code}.dim_pub_date`.

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dim_${country_code}.dim_pub_date`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `date_flag` | `date_flag` | `date_flag` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:7` |
| `u_version` | `u_version` | `u_version` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:8` |
| `q` | `q` | `q` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `fq` | `fq` | `fq` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `m` | `m` | `m` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `w` | `w` | `w` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `d` | `d` | `d` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `year` | `year` | `year` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:2` |
| `qtr` | `qtr` | `qtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:15` |
| `month` | `month` | `month` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `week` | `week` | `week` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:1` |
| `day` | `day` | `day` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:2` |
| `doy` | `doy` | `doy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:19` |
| `fyear` | `fyear` | `fyear` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:20` |
| `fqtr` | `fqtr` | `fqtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:21` |
| `fdoy` | `fdoy` | `fdoy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:22` |
| `dow` | `dow` | `dow` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:23` |
| `dname` | `dname` | `dname` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:24` |
| `bonuswk` | `bonuswk` | `bonuswk` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:25` |
| `holiday` | `holiday` | `holiday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:26` |
| `payroll` | `payroll` | `payroll` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:27` |
| `sales` | `sales` | `sales` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:28` |
| `comment` | `comment` | `comment` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:29` |
| `weekday` | `weekday` | `weekday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:30` |
| `week_flag` | `case when week >=10 then concat(YEAR ,'-W',WEEK ) else concat(YEAR ,'-W0',WEEK ) end` | `week`, `YEAR`, `W`, `WEEK`, `W0` | `ods_${country_code}.ods_cis_corp_dw_calendar` | case | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:31` |
| `month_flag` | `case when month >=10 then concat(YEAR ,'-',month ) else concat(YEAR ,'-0',month ) end` | `month`, `YEAR` | `ods_${country_code}.ods_cis_corp_dw_calendar` | case | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:32` |
| `quarter_flag` | `concat(YEAR,'-Q',qtr )` | `YEAR`, `Q`, `qtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | arithmetic | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:33` |
| `fquarter_flag` | `concat(fyear,'-Q',fqtr )` | `fyear`, `Q`, `fqtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | arithmetic | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:34` |
| `month_name` | `date_format(DATE_FLAG,'MMMMM')` | `DATE_FLAG`, `MMMMM` | `ods_${country_code}.ods_cis_corp_dw_calendar` | udf | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:35` |
| `dt_week` | `case when week2 >=10 then concat(YEAR ,'-W',week2 ) else concat(YEAR ,'-W0',week2 ) end` | `week2`, `YEAR`, `W`, `W0` | `ods_${country_code}.ods_cis_corp_dw_calendar` | case | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:36` |
| `w2` | `w2` | `w2` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:3` |
| `week2` | `week2` | `week2` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql:3` |

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
| ETL load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` |
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
| `ods_${country_code}.ods_cis_corp_dw_calendar` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dim_pub_date/dim_pub_date.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| KB / contract ref: `source/contracts/b-report-us/A PL_ITEM_LOGIC 1.md` | `source/contracts/b-report-us/A PL_ITEM_LOGIC 1.md:982` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_bd_rep_wtd/BD/python/dm_disty_brpt_bd_rep_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_bd_rep_wtd/BD/python/dm_disty_brpt_bd_rep_wtd.py:142` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_wtd/Product/python/dm_disty_brpt_buyer_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_buyer_wtd/Product/python/dm_disty_brpt_buyer_wtd.py:154` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_pm_mtd/Product/python/dm_disty_brpt_pm_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_pm_mtd/Product/python/dm_disty_brpt_pm_mtd.py:14` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_pm_wtd/Product/python/dm_disty_brpt_pm_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_pm_wtd/Product/python/dm_disty_brpt_pm_wtd.py:155` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_comb_mtd/Customer/python/dm_disty_brpt_sales_comb_mtd.py:10` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_wtd/Customer/python/dm_disty_brpt_sales_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dm_disty_brpt_sales_wtd/Customer/python/dm_disty_brpt_sales_wtd.py:145` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_cust_comb_mtd/BD/python/dws_disty_brpt_bd_cust_comb_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_cust_comb_mtd/BD/python/dws_disty_brpt_bd_cust_comb_mtd.py:9` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_cust_wtd/BD/python/dws_disty_brpt_bd_cust_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_cust_wtd/BD/python/dws_disty_brpt_bd_cust_wtd.py:150` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_part_comb_mtd/BD/python/dws_disty_brpt_bd_part_comb_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_part_comb_mtd/BD/python/dws_disty_brpt_bd_part_comb_mtd.py:9` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_part_wtd/BD/python/dws_disty_brpt_bd_part_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_part_wtd/BD/python/dws_disty_brpt_bd_part_wtd.py:148` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_proj_task_comb_mtd/BD/python/dws_disty_brpt_bd_proj_task_comb_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_proj_task_comb_mtd/BD/python/dws_disty_brpt_bd_proj_task_comb_mtd.py:10` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_proj_task_wtd/BD/python/dws_disty_brpt_bd_proj_task_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_proj_task_wtd/BD/python/dws_disty_brpt_bd_proj_task_wtd.py:144` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vend_wtd/BD/python/dws_disty_brpt_bd_vend_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vend_wtd/BD/python/dws_disty_brpt_bd_vend_wtd.py:140` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_bd_vpl_wtd/BD/python/dws_disty_brpt_bd_vpl_wtd.py:144` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_cvv_wtd/Cross/python/dws_disty_brpt_cross_cvv_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_cvv_wtd/Cross/python/dws_disty_brpt_cross_cvv_wtd.py:161` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_wtd/Cross/python/dws_disty_brpt_cross_dccv_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_dccv_wtd/Cross/python/dws_disty_brpt_cross_dccv_wtd.py:147` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_mpc_wtd/Cross/python/dws_disty_brpt_cross_mpc_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_mpc_wtd/Cross/python/dws_disty_brpt_cross_mpc_wtd.py:152` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_svddc_wtd/Cross/python/dws_disty_brpt_cross_svddc_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cross_svddc_wtd/Cross/python/dws_disty_brpt_cross_svddc_wtd.py:140` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_type_wtd/Customer/python/dws_disty_brpt_cust_type_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_type_wtd/Customer/python/dws_disty_brpt_cust_type_wtd.py:134` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_wtd/Customer/python/dws_disty_brpt_cust_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_cust_wtd/Customer/python/dws_disty_brpt_cust_wtd.py:149` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_division_wtd/Customer/python/dws_disty_brpt_division_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_division_wtd/Customer/python/dws_disty_brpt_division_wtd.py:132` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_comb_mtd/Product/python/dws_disty_brpt_part_comb_mtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_comb_mtd/Product/python/dws_disty_brpt_part_comb_mtd.py:11` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_wtd/Product/python/dws_disty_brpt_part_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_part_wtd/Product/python/dws_disty_brpt_part_wtd.py:167` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_pl_extend_wtd/Common/python/dws_disty_brpt_pl_extend_wtd.py:159` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_terr_wtd/Customer/python/dws_disty_brpt_terr_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_terr_wtd/Customer/python/dws_disty_brpt_terr_wtd.py:145` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_vend_wtd/Product/python/dws_disty_brpt_vend_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_vend_wtd/Product/python/dws_disty_brpt_vend_wtd.py:155` |
| ETL/script ref: `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_vpl_wtd/Product/python/dws_disty_brpt_vpl_wtd.py` | `source/contracts/b-report-us/bitbicket_etl/dws_disty_brpt_vpl_wtd/Product/python/dws_disty_brpt_vpl_wtd.py:163` |
| KB / contract ref: `source/contracts/b-report-us/bitbicket_etl/readme.md` | `source/contracts/b-report-us/bitbicket_etl/readme.md:36` |
| KB / contract ref: `source/contracts/b-report-us/domain-knowledge.md` | `source/contracts/b-report-us/domain-knowledge.md:48` |
| KB / contract ref: `source/contracts/b-report-us/eval/golden_cases.md` | `source/contracts/b-report-us/eval/golden_cases.md:71` |
| KB / contract ref: `source/contracts/b-report-us/golden-questions.md` | `source/contracts/b-report-us/golden-questions.md:90` |
| KB / contract ref: `source/contracts/b-report-us/metric-index.md` | `source/contracts/b-report-us/metric-index.md:182` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_disty_bd_project_user.md` | `source/contracts/b-report-us/tables/dim_disty_bd_project_user.md:178` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_customer_info.md` | `source/contracts/b-report-us/tables/dim_pub_customer_info.md:352` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_date.md` | `source/contracts/b-report-us/tables/dim_pub_date.md:5` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_order_type.md` | `source/contracts/b-report-us/tables/dim_pub_order_type.md:182` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_part_info.md` | `source/contracts/b-report-us/tables/dim_pub_part_info.md:366` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_sales_cust_type.md` | `source/contracts/b-report-us/tables/dim_pub_sales_cust_type.md:173` |
| KB / contract ref: `source/contracts/b-report-us/tables/dim_pub_sales_division.md` | `source/contracts/b-report-us/tables/dim_pub_sales_division.md:166` |

#### Operational detail (verified)
- Partition clause: `See L4 / ETL partition clause`

#### Not documented in repository
- Schedule, owner, SLA
