# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_stellr_billing_history_di`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_stellr_billing_history_di
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_stellr_billing_history_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dw_us.dwd_stellr_billing_history_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_stellr_billing_history_di schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `Bitbucket` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `${part_master}` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `dw_${country}.dwd_stellr_billing_order_profile_rt_mi` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `dw_${country}.dwd_stellr_billing_order_header_rt_mi` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `temp_order_header_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **upstream:** `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`
- **downstream:** see L6 Downstream consumers
### Freshness and load path
- Parameters / date window: see ETL `${literal_*}` / `${date_flag}` / `${start_date}` in evidence script.
- Schedule: Not documented in repository

## L2 Declarative Knowledge

### Business purpose
See preserved **Business purpose** below when present (POS contract catalog + linked ETL).

### Audience and use cases
See preserved **Who it helps** section when present.

### Fact key resolution
See preserved **Grain and keys** when present.

### Time field semantics
- Prefer partition / `date_flag` filters documented in preserved sections and L3 Key filters from ETL.

### Metrics served
See preserved Metrics / column groups when present; otherwise L3 column derivations.

### Metric serving map
N/A unless multi-period wide table (see preserved content).

### etl_metrics
No new metric-index formulas appended in this bitbucket-etl upgrade pass.

## L3 Procedural Knowledge

### Query and routing rules
- Reporting: Vertica `dw_us.dwd_stellr_billing_history_di` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `profile_cat='ORDR' and order_type in (125,127,270); CREATE TEMPORARY TABLE temp_order_header_all AS select * from dw_${country}.dwd_stellr_billing_order_header_rt_mi a where order_type in (125,127,...` | Business | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["Bitbucket"] --> T["dw_us.dwd_stellr_billing_history_di"]
  S1["${part_master}"] --> T["dw_us.dwd_stellr_billing_history_di"]
  S2["dw_${country}.dwd_stellr_billing_order_profile_rt_mi"] --> T["dw_us.dwd_stellr_billing_history_di"]
  S3["dw_${country}.dwd_stellr_billing_order_header_rt_mi"] --> T["dw_us.dwd_stellr_billing_history_di"]
  S4["temp_order_header_all"] --> T["dw_us.dwd_stellr_billing_history_di"]
  S5["dw_${country}.dwd_stellr_billing_order_detail_rt_mi"] --> T["dw_us.dwd_stellr_billing_history_di"]
```

### Base tables register
| Object | Role |
|--------|------|
| `Bitbucket` | source / temp (FROM/JOIN) |
| `${part_master}` | source / temp (FROM/JOIN) |
| `dw_${country}.dwd_stellr_billing_order_profile_rt_mi` | source / temp (FROM/JOIN) |
| `dw_${country}.dwd_stellr_billing_order_header_rt_mi` | source / temp (FROM/JOIN) |
| `temp_order_header_all` | source / temp (FROM/JOIN) |
| `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dw_us.dwd_stellr_billing_history_di` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `oh` | `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | many:1 | `oh.order_no` = `od.order_no`; `oh.order_type` = `od.order_type` | etl_sql (`source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:23`) |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_stellr_billing_history_di`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `vend_no` | `vend_no` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `mfg_partno` | `mfg_partno` | `mfg_partno` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `part_no` | `part_no` | `part_no` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `sku_no` | `sku_no` | `sku_no` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `vpl_no` | `vpl_no` | `vpl_no` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `8` | `cast(sug_retail_price as decimal(20,8))` | `sug_retail_price` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | cast | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `short_desc` | `short_desc` | `short_desc` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |
| `long_desc` | `long_desc` | `long_desc` | `${part_master}`, `dw_${country}.dwd_stellr_billing_order_profile_rt_mi`, `dw_${country}.dwd_stellr_billing_order_header_rt_mi`, `temp_order_header_all`, `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql:6` |

### Sentinel and code values
See preserved content and ETL CASE expressions in column derivations.

## L4 Validation

### Resolved partition value
- Partition / date parameters from ETL literals — concrete calendar values Not documented in repository (resolve via Azkaban when flow evidence exists).

### Data quality checks
See preserved Validation SQL when present.

### Validation SQL
Prefer preserved Vertica validation bundle when present; MCP business SQL not re-run during documentation.

### Caveats for interpretation
- Document upgraded additively from POS **contract** MD + **bitbucket-etl** SQL. Prior contract text is under **Preserved pre-L1-L6 content** when present.

### Conflicts and open questions
- Companion loader scripts may also appear under other domain KB folders; see `target/knowledgebase/pos/readme.md` cross-links.

## L5 Runtime View

### Query path and engine preference
| Path | Engine | Evidence |
|------|--------|----------|
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| Report | Vertica | preserved POS contract when present |

### Access constraints
Not documented in repository

### Query risk profile
- Always filter `date_flag` / documented partition keys before wide scans.

## L6 Access and Consumption

### Primary consumers and use cases
See preserved audience / POS report consumers when present.

### Representative query patterns
See preserved Validation SQL / contract examples when present.

### Dependencies and notes

#### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `Bitbucket` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| `${part_master}` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| `dw_${country}.dwd_stellr_billing_order_profile_rt_mi` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| `dw_${country}.dwd_stellr_billing_order_header_rt_mi` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| `temp_order_header_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |
| `dw_${country}.dwd_stellr_billing_order_detail_rt_mi` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/load_dwd_stellr_billing_history_di.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:219` |
| ETL/script ref: `source/contracts/pos/bitbucket-etl/dwd_disty_common_pos_di/loading_pos_data.sql` | `source/contracts/pos/bitbucket-etl/dwd_disty_common_pos_di/loading_pos_data.sql:727` |
| ETL/script ref: `source/contracts/pos/bitbucket-etl/dwd_disty_common_pos_di/z_pos_reload_his_data.py` | `source/contracts/pos/bitbucket-etl/dwd_disty_common_pos_di/z_pos_reload_his_data.py:80` |
| KB / contract ref: `source/contracts/pos/tables/dwd_stellr_billing_history_di.md` | `source/contracts/pos/tables/dwd_stellr_billing_history_di.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_17482.sql:316` |
| ETL/script ref: `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql` | `source/contracts/rds/vertica_pos/etl/pos_scm_reference_hierarchy_rds_8329.sql:316` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_17482.md:174` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md` | `target/knowledgebase/RDS/vertica_pos/pos_scm_reference_hierarchy_rds_8329.md:174` |
| KB / contract ref: `target/knowledgebase/pos/dwd_disty_common_pos_di.md` | `target/knowledgebase/pos/dwd_disty_common_pos_di.md:221` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:78` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_stellr_billing_history_di/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_stellr_billing_history_di.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_stellr_billing_history_di` — FACT layer table used in US POS reporting (`US POS baseline`). |
| **Consumption** | Queried from Vertica for POS/RDS reports, exports, and enrichment joins. |

**Parameters:** Country schema pattern `dw_us` (US baseline documented as `dw_us` / `dim_us`).

---

## Who it helps and how

| Audience | How they benefit |
|----------|-----------------|
| **POS / RDS reporting** | Vertica RDS POS custom reports (499 scripts scanned: US 367, CA 124, MX 7, BR 1) |
| **Sales analytics** | Order, customer, product, and margin attributes at documented grain. |
| **Data engineering** | Stable table contract for joins to POS hub and downstream exports. |

---

## Business query tables (Vertica)

| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | `dw_us.dwd_stellr_billing_history_di` | `dw_us.dwd_stellr_billing_history_di` | overwrite / incremental | POS contract `dwd_stellr_billing_history_di.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_stellr_billing_history_di` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_stellr_billing_history_di`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** `date_flag` — daily business date filter for POS reporting (per POS contract).
- **Natural key:** `vend_no`, `eu_no`, `reseller_no`, `to_acct_no`, `subscription_id`, `customer_id`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT vend_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY vend_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT vend_no, eu_no, reseller_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_stellr_billing_history_di
WHERE date_flag = '${partition_value}'
GROUP BY vend_no, eu_no, reseller_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `order_qty` — order qty
- `msrp` — msrp
- `unit_cost` — unit cost
- `unit_price` — unit price
- `unit_tax` — unit tax
- `unit_rebate` — unit rebate
- `ext_price` — ext price
- `total_price` — total price
- `order_tax` — order tax
- `order_total` — order total
- `fx_msrp` — fx msrp
- `fx_unit_cost` — fx unit cost
- `fx_unit_price` — fx unit price
- `fx_unit_tax` — fx unit tax
- `fx_unit_rebate` — fx unit rebate
- `fx_ext_price` — fx ext price
- `fx_total_price` — fx total price
- `fx_order_tax` — fx order tax
- `fx_order_total` — fx order total
- `rate_to_usd` — rate to usd
- `usd_order_total` — usd order total
- `eu_price` — eu price
- `ext_eu_price` — ext eu price
- `fx_eu_price` — fx eu price
- `fx_ext_eu_price` — fx ext eu price
- ... and 2 additional measure columns (see column register)

### Dimension and key columns

- `vend_no` — vend no
- `vend_name` — vend name
- `eu_no` — eu no
- `eu_name` — eu name
- `reseller_no` — reseller no
- `reseller_name` — reseller name
- `to_acct_no` — to acct no
- `subscription_id` — subscription id
- `customer_id` — customer id
- `domain_name` — domain name
- `local_currency` — local currency
- `fx_currency` — fx currency
- `offer_type` — offer type
- `contract_no` — contract no
- `contract_type` — contract type
- `contract_line_no` — contract line no
- `bill_model` — bill model
- `billing_frequency` — billing frequency
- `fixed_bill_type` — fixed bill type
- `order_no` — order no
- `order_type` — order type
- `order_line_no` — order line no
- `sales_model` — sales model
- `invoice_date` — invoice date
- `close_date` — close date
- `billing_period` — billing period
- `billing_start_date` — billing start date
- `billing_end_date` — billing end date
- `sku_no` — sku no
- `sku_desc` — sku desc

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_stellr_billing_history_di`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_stellr_billing_history_di"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_stellr_billing_history_di` | Primary catalog table documented from POS contract |

---

## Step-by-step logic

Not applicable — this Knowledgebase entry is a **table catalog** converted from POS contract v2. ETL step-by-step logic is not present in this wiki repository.

**Standard POS filters (from contract L3):**

- Standard POS filters inherited from domain-knowledge.md when joining to hub.

---

## Caveats for interpretation

- Derived from POS contract v2; ETL SQL and Azkaban flow names are not verified in this repository unless cited below.
- US schema `dw_us` documented as baseline; CA/MX/BR use same table names with regional scope.
- - Verify grain keys (`order_no`, `order_type`, `order_line_no`) not null for fact joins when applicable.
- For one-to-many partners (SPA/SCM, serial), validate row counts before joining to hub.
- Hub: `extend_net_price` should align with `(unit_net_price * ship_qty)` within rounding tolerance when both populated.
- Validate join cardinality to POS hub before production report use.

---

## Dependencies and notes (verified only)

### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_stellr_billing_history_di.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 100 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_stellr_billing_history_di.md`.*