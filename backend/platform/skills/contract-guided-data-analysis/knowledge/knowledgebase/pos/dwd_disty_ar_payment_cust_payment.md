# FACT: Supplemental fact/context table used by select POS reports (`dw_us.dwd_disty_ar_payment_cust_payment`)

- artifact_type: etl_table
- artifact_id: dw_us.dwd_disty_ar_payment_cust_payment
- domain: pos
- one_line_purpose: POS-domain table with load SQL under bitbucket-etl (see L3); prior contract narrative preserved below when present.
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql
- bitbucket_etl_bundle: source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/
- related_etl_scripts:
- None

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_us.dwd_disty_ar_payment_cust_payment`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3 from bitbucket-etl)
- **Owner team:** Not documented in repository

### Grain, scope, exclusions
- See preserved **Grain and keys** section below when present (POS contract narrative retained).
- Otherwise infer from SELECT / GROUP BY / INSERT column list in `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`.

### Cross-engine presence
| Engine | Present | Notes |
|--------|---------|-------|
| Hive | yes | ETL load target |
| Vertica | yes when POS contract documents Vertica sync | See preserved Business query tables |

### Physical schema reference

| Field | Value |
|-------|-------|
| **entity_id** | `dw_us.dwd_disty_ar_payment_cust_payment` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | See preserved Grain / L4 / ETL PARTITION clause |
| **ddl_source** | pending |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "pos dwd_disty_ar_payment_cust_payment schema" --intent find_table_schema` |

### Lineage

- **Primary load:** `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`
- **upstream:** `Bitbucket` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`
- **upstream:** `ods_${country_code}.ods_cis_corp_cust_payment` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`
- **upstream:** `ods_${country_code}.ods_his_corp_cust_payment` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`
- **upstream:** `t_ods_cust_payment_all` — FROM/JOIN — `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`
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
- Reporting: Vertica `dw_us.dwd_disty_ar_payment_cust_payment` when synced (see preserved Business query tables).
- Load logic: bitbucket-etl evidence `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`.

### Dimension join patterns
See Relationship map (ETL JOIN edges) and preserved contract join notes.

### Key filters and ETL business logic

| Predicate | Kind | Evidence |
|-----------|------|----------|
| `aa.rn=1; insert overwrite table dw_${country_code}.dwd_disty_ar_payment_cust_payment_di PARTITION (date_flag) select a.pay_no, a.u_version, a.batch_no, a.batch_date, a.cust_no, a.loc_no, a.check_no...` | Technical (load only) / Business | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |

### Standard time-filter SQL
```sql
-- Prefer date_flag / literal_start_date / literal_end_date as used in source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql
```

### End-to-end flow
```mermaid
flowchart LR
  S0["Bitbucket"] --> T["dw_us.dwd_disty_ar_payment_cust_payment"]
  S1["ods_${country_code}.ods_cis_corp_cust_payment"] --> T["dw_us.dwd_disty_ar_payment_cust_payment"]
  S2["ods_${country_code}.ods_his_corp_cust_payment"] --> T["dw_us.dwd_disty_ar_payment_cust_payment"]
  S3["t_ods_cust_payment_all"] --> T["dw_us.dwd_disty_ar_payment_cust_payment"]
```

### Base tables register
| Object | Role |
|--------|------|
| `Bitbucket` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_cis_corp_cust_payment` | source / temp (FROM/JOIN) |
| `ods_${country_code}.ods_his_corp_cust_payment` | source / temp (FROM/JOIN) |
| `t_ods_cust_payment_all` | source / temp (FROM/JOIN) |

### Step-by-step logic
1. Execute load SQL / python in `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/`.
2. Apply date / business filters from ETL (Key filters).
3. Write target `dw_us.dwd_disty_ar_payment_cust_payment` (see INSERT/OVERWRITE in evidence).

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| — | — | — | — | No JOIN edges parsed from ETL (`source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql`); see Base tables register / step-by-step |

### Special logic (embedded)

`source/ref/pos/special_logic.txt` exists but no rule naming this FQN/stem (`dw_us.dwd_disty_ar_payment_cust_payment`).

Not documented in repository


### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `pay_no` | `a.pay_no` | `pay_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `u_version` | `a.u_version` | `u_version` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `batch_no` | `a.batch_no` | `batch_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `batch_date` | `a.batch_date` | `batch_date` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `cust_no` | `a.cust_no` | `cust_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `loc_no` | `a.loc_no` | `loc_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `check_no` | `a.check_no` | `check_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `gl_acct_no` | `a.gl_acct_no` | `gl_acct_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `disc_gl_acct_no` | `a.disc_gl_acct_no` | `disc_gl_acct_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `pay_amt` | `a.pay_amt` | `pay_amt` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `disc_amt_taken` | `a.disc_amt_taken` | `disc_amt_taken` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `entry_datetime` | `a.entry_datetime` | `entry_datetime` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `entry_id` | `a.entry_id` | `entry_id` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `void_flag` | `a.void_flag` | `void_flag` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `chk_rcv_date` | `a.chk_rcv_date` | `chk_rcv_date` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `usd_pay_amt` | `a.usd_pay_amt` | `usd_pay_amt` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `usd_disc_taken` | `a.usd_disc_taken` | `usd_disc_taken` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `company_no` | `a.company_no` | `company_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `fx_currency` | `a.fx_currency` | `fx_currency` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `cust_check_no` | `a.cust_check_no` | `cust_check_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `je_no` | `a.je_no` | `je_no` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `source` | `a.source` | `source` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `payment_type` | `a.payment_type` | `payment_type` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `pay_currency` | `a.pay_currency` | `pay_currency` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `pay_rate` | `a.pay_rate` | `pay_rate` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `cust_bank_id` | `a.cust_bank_id` | `cust_bank_id` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `receive_bank_id` | `a.receive_bank_id` | `receive_bank_id` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `value_date` | `a.value_date` | `value_date` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `batch_date_system` | `a.batch_date_system` | `batch_date_system` | `t_ods_cust_payment_all` | passthrough | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |
| `date_flag` | `TO_DATE(a.entry_datetime)` | `entry_datetime` | `t_ods_cust_payment_all` | udf | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql:15` |

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
| Load | Hive/Spark | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |
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
| `Bitbucket` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |
| `ods_${country_code}.ods_cis_corp_cust_payment` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |
| `ods_${country_code}.ods_his_corp_cust_payment` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |
| `t_ods_cust_payment_all` | FROM/JOIN | `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/dwd_disty_ar_payment_prepare_us.sql` |

#### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS / RDS reports (contract) | preserved sections when present |
| Related loaders | see related_etl_scripts header |
| KB / contract ref: `source/contracts/pos/bitbucket-etl/MANIFEST.md` | `source/contracts/pos/bitbucket-etl/MANIFEST.md:149` |
| KB / contract ref: `source/contracts/pos/tables/dwd_disty_ar_payment_cust_payment.md` | `source/contracts/pos/tables/dwd_disty_ar_payment_cust_payment.md:5` |
| ETL/script ref: `source/contracts/rds/vertica_ar/etl/ar_discount_payment_timing_rds_19383.sql` | `source/contracts/rds/vertica_ar/etl/ar_discount_payment_timing_rds_19383.sql:145` |
| KB / contract ref: `target/knowledgebase/RDS/vertica_ar/ar_discount_payment_timing_rds_19383.md` | `target/knowledgebase/RDS/vertica_ar/ar_discount_payment_timing_rds_19383.md:57` |
| KB / contract ref: `target/knowledgebase/pos/readme.md` | `target/knowledgebase/pos/readme.md:55` |

#### Operational detail (verified)
- Bundle: `source/contracts/pos/bitbucket-etl/dwd_disty_ar_payment_cust_payment/`
- Manifest: `source/contracts/pos/bitbucket-etl/MANIFEST.md`

#### Not documented in repository
- Schedule, owner, SLA

---

## Preserved pre-L1-L6 content

> Retained verbatim from the prior POS contract knowledgebase document (nothing removed). ETL load evidence above supplements this catalog narrative.


**Domain:** pos  
**Source contract:** `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_payment_cust_payment.md`  
**Knowledgebase path:** `target/knowledgebase/pos/dwd_disty_ar_payment_cust_payment.md`

## Business purpose

Supplemental fact/context table used by select POS reports

This document is derived from the POS table contract catalog. ETL script lineage for load jobs is **not documented in this repository** unless listed under verified dependencies below.

---

## What the process does (high level)

| Stage | Business meaning |
|-------|------------------|
| **Catalog object** | `dw_us.dwd_disty_ar_payment_cust_payment` — FACT layer table used in US POS reporting (`US POS baseline`). |
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
| **Query for reporting** | `dw_us.dwd_disty_ar_payment_cust_payment` | `dw_us.dwd_disty_ar_payment_cust_payment` | overwrite / incremental | POS contract `dwd_disty_ar_payment_cust_payment.md:L1` | yes (POS contract v2 — Vertica verified in source catalog) |
| **Hive alternative** | `dw_us.dwd_disty_ar_payment_cust_payment` | same as reporting table | - | POS contract cross-engine note | - |
| **ETL internal** | n/a | n/a | - | ETL not in wiki repo | - |

Business users should query **`dw_us.dwd_disty_ar_payment_cust_payment`** in Vertica for POS-domain reporting aligned to this contract.

---

## Grain and keys

- **Grain:** See natural key columns from POS contract column catalog.
- **Partition:** None explicit — full-table dimension or non-partitioned object per POS contract.
- **Natural key:** `pay_no`, `batch_no`, `cust_no`, `loc_no`, `check_no`, `gl_acct_no`
- **Exclusions (reporting):** None documented in POS contract.

---

## Validation SQL (Vertica)

```sql
-- 1) Row count by partition
SELECT date_flag, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_ar_payment_cust_payment
WHERE date_flag = '${partition_value}'
GROUP BY date_flag;

-- 2) Metric sum by business dimension (top N)
SELECT pay_no, COUNT(*) AS row_cnt
FROM dw_us.dwd_disty_ar_payment_cust_payment
WHERE date_flag = '${partition_value}'
GROUP BY pay_no
ORDER BY COUNT(*) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT pay_no, batch_no, cust_no, date_flag, COUNT(*) AS cnt
FROM dw_us.dwd_disty_ar_payment_cust_payment
WHERE date_flag = '${partition_value}'
GROUP BY pay_no, batch_no, cust_no, date_flag
HAVING COUNT(*) > 1;
```

Replace `${partition_value}` with the resolved business date or period from the report scope.

---

## Data you can fetch and use downstream

### Core measures

- `pay_amt` — pay amt
- `disc_amt_taken` — disc amt taken
- `usd_pay_amt` — usd pay amt
- `usd_disc_taken` — usd disc taken
- `pay_rate` — pay rate

### Dimension and key columns

- `pay_no` — pay no
- `u_version` — u version
- `batch_no` — batch no
- `batch_date` — batch date
- `cust_no` — cust no
- `loc_no` — loc no
- `check_no` — check no
- `gl_acct_no` — gl acct no
- `disc_gl_acct_no` — disc gl acct no
- `entry_datetime` — entry datetime
- `entry_id` — entry id
- `void_flag` — void flag
- `chk_rcv_date` — chk rcv date
- `company_no` — company no
- `fx_currency` — fx currency
- `cust_check_no` — cust check no
- `je_no` — je no
- `source` — source
- `payment_type` — payment type
- `pay_currency` — pay currency
- `cust_bank_id` — cust bank id
- `receive_bank_id` — receive bank id
- `value_date` — value date
- `batch_date_system` — batch date system
- `local_currency` — local currency
- `cust_name` — cust name
- `entry_name` — entry name
- `trading_partner` — trading partner
- `internal_reference` — internal reference
- `download_file` — download file

---

## Metrics business users typically care about

When exposing this table to the business, lead with measure and key columns from the POS contract catalog (see **Data you can fetch** above).

---

## End-to-end flow (summary)

**Target table:** `dw_us.dwd_disty_ar_payment_cust_payment`  
**Load pattern:** Not documented in repository

1. Upstream: Curated DWD/DIM/ODS load jobs in disty common pipeline
2. Table available in Hive and Vertica for POS consumption.
3. Downstream: Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports

```mermaid
flowchart LR
  upstream[Upstream POS or DIM loads]
  tgt["dw_us.dwd_disty_ar_payment_cust_payment"]
  rds[Vertica RDS POS reports]
  upstream --> tgt
  tgt --> rds
```

---

## Base tables register

| Object | Role in this job |
|--------|-----------------|
| `dw_us.dwd_disty_ar_payment_cust_payment` | Primary catalog table documented from POS contract |

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
| POS contract source | Table metadata, grain, columns | `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_payment_cust_payment.md` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| POS RDS / export consumers | `dwd_disty_ar_payment_cust_payment.md:L6` — Vertica RDS POS report scripts (`rds_*_rtv`), ad-hoc POS exports |

### Operational detail (verified)

- Freshness: Not documented in repository
- Column count: 38 (POS contract catalog)

### Not documented in repository

- ETL SQL load script and Azkaban `.flow` for this table
- hive2vertica sync job file:line evidence
- Schedule, owner, SLA

### Related scripts (verified)

None identified in repository.

---

*Document generated from POS contract `C:\Users\T154858D.TDSNX\Desktop\git_repo_v1\data_analysis_agent_brpt\knowledge\POS\tables\dwd_disty_ar_payment_cust_payment.md`.*