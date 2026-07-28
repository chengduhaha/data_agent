# DIM: Company Master Pass-Through (`dim_pub_company_info`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_company_info
- domain: common
- one_line_purpose: This job is a full-refresh copy of the CIS company master table into the country-specific dimension schema. It exposes all company attributes — fiscal calendar quarter-end dates, default GL account segments, currency settings, and system co...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_company_info`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per company.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full table overwrite. - resolved from pipeline (see L4)
- **Natural key:** `company_no`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per company.
- **Partition:** none — full table overwrite.
- **Natural key:** `company_no`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_pub_company_info` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_pub_company_info` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_company_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full table overwrite.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "common dim_pub_company_info schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_company_info` | Sole source |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code` |


---

## L2 Declarative Knowledge

### Business purpose
This job is a full-refresh copy of the CIS company master table into the country-specific dimension
schema. It exposes all company attributes — fiscal calendar quarter-end dates, default GL account
segments, currency settings, and system configuration flags — to downstream fact tables and reports
through a single stable join point on `company_no`.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Finance** | `fy_begin`, `qtr1_end` … `qtr4_end` define the fiscal calendar for each company; `curr_period_begin/end` marks the current accounting period |
| **GL / accounting** | `ra_ap`, `ra_ar`, `ra_inv`, `ra_aphold`, `ra_earnings` are the default GL account ranges per company |
| **Operations** | `currency`, `payroll_currency`, `multi_curr_flag`, `company_timezone`, `sys_timezone` for financial and operational configuration |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full table overwrite.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.

### Metrics served
When exposing this table to the business, lead with:

1. **Company identification:** `company_no`, `company_name`, `country_code`
2. **Fiscal periods:** `fy_begin`, `qtr1_end` … `qtr4_end`, `curr_period_begin/end`
3. **Currency settings:** `currency`, `payroll_currency`, `multi_curr_flag`

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Company:** `company_no`, `company_name`, `parent_company`, `resales_no`, `country_code`
- **Location:** `primary_location`, `def_div`, `def_dep`, `def_loc`, `def_funct`, `def_proj`

### Dimension columns

Use these for **filters, group-bys, and star-schema joins**:

- `company_name` — Company display name
- `currency` — Company's base currency code
- `payroll_currency` — Payroll currency code
- `multi_curr_flag` — Multi-currency enabled flag
- `activeflag` — Company active/inactive status
- `company_timezone`, `sys_timezone` — Time zone settings
- `default_cis` — Default CIS server for the company

### Fiscal calendar building blocks

- `fy_begin` — Fiscal year start date
- `qtr1_end`, `qtr2_end`, `qtr3_end`, `qtr4_end` — Fiscal quarter end dates
- `curr_period_begin`, `curr_period_end` — Current accounting period boundaries

### GL account defaults

- `ra_ap`, `ra_ar`, `ra_inv`, `ra_aphold`, `ra_earnings` — Default GL account segments
- `earnings_roll` — Earnings rollover account

---

### etl_metrics

#### `etl_timestamp`
- **Source:** [metric-index.md](../../source/contracts/common/metric-index.md#etl_timestamp)
- **Business definition:** Load timestamp in Pacific time
```sql
from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')
```


---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_company_info`

**From:** `ods_${country_code}.ods_cis_corp_company_info`

**Filter:** None — all rows.

**Pass-through columns:**
`company_no`, `company_name`, `primary_location`, `parent_company`, `fy_begin`, `qtr1_end`,
`qtr2_end`, `qtr3_end`, `qtr4_end`, `curr_period_begin`, `curr_period_end`, `ra_ap`, `ra_ar`,
`ra_inv`, `ra_aphold`, `ra_earnings`, `earnings_roll`, `def_div`, `def_dep`, `def_loc`,
`def_funct`, `def_proj`, `entry_datetime`, `entry_id`, `voucher_variance`, `ap_beg_bal`,
`ap_hold_beg_bal`, `resales_no`, `currency`, `country_code`, `activeflag`, `multi_curr_flag`,
`intranet_url`, `company_logo`, `payroll_currency`, `company_timezone`, `sys_timezone`,
`default_cis`

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')` | Load timestamp in Pacific time |

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_pub_company_info
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`
**Target table:** `dim_${country_code}.dim_pub_company_info` — full table overwrite.

1. Read all rows from `ods_${country_code}.ods_cis_corp_company_info`.
2. **INSERT OVERWRITE** all columns verbatim; add `etl_timestamp` at insert time.

```mermaid
flowchart LR
  SRC[ods_cis_corp_company_info] --> INS[INSERT OVERWRITE
dim_pub_company_info]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Full company copy** | Reads every row and all columns from `ods_cis_corp_company_info` and writes them verbatim to `dim_pub_company_info`; no filtering or transformation applied except adding an ETL timestamp |

**Parameters:** `country_code`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_${country_code}.ods_cis_corp_company_info` | Sole source — all company master attributes |

**Temporary tables (inside the job only):**
None — direct INSERT from source.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_company_info`

**From:** `ods_${country_code}.ods_cis_corp_company_info`

**Filter:** None — all rows.

**Pass-through columns:**
`company_no`, `company_name`, `primary_location`, `parent_company`, `fy_begin`, `qtr1_end`,
`qtr2_end`, `qtr3_end`, `qtr4_end`, `curr_period_begin`, `curr_period_end`, `ra_ap`, `ra_ar`,
`ra_inv`, `ra_aphold`, `ra_earnings`, `earnings_roll`, `def_div`, `def_dep`, `def_loc`,
`def_funct`, `def_proj`, `entry_datetime`, `entry_id`, `voucher_variance`, `ap_beg_bal`,
`ap_hold_beg_bal`, `resales_no`, `currency`, `country_code`, `activeflag`, `multi_curr_flag`,
`intranet_url`, `company_logo`, `payroll_currency`, `company_timezone`, `sys_timezone`,
`default_cis`

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')` | Load timestamp in Pacific time |

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_company_info` | `ods_${country_code}.ods_cis_corp_company_info` | 1:1 source scan | — (no JOIN; single FROM) | etl_sql (`source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:42`) |


### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `company_no` | `company_no` | `company_no` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:3` |
| `company_name` | `company_name` | `company_name` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:4` |
| `primary_location` | `primary_location` | `primary_location` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:5` |
| `parent_company` | `parent_company` | `parent_company` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:6` |
| `fy_begin` | `fy_begin` | `fy_begin` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:7` |
| `qtr1_end` | `qtr1_end` | `qtr1_end` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:8` |
| `qtr2_end` | `qtr2_end` | `qtr2_end` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:9` |
| `qtr3_end` | `qtr3_end` | `qtr3_end` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:10` |
| `qtr4_end` | `qtr4_end` | `qtr4_end` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:11` |
| `curr_period_begin` | `curr_period_begin` | `curr_period_begin` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:12` |
| `curr_period_end` | `curr_period_end` | `curr_period_end` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:13` |
| `ra_ap` | `ra_ap` | `ra_ap` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:14` |
| `ra_ar` | `ra_ar` | `ra_ar` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:15` |
| `ra_inv` | `ra_inv` | `ra_inv` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:16` |
| `ra_aphold` | `ra_aphold` | `ra_aphold` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:17` |
| `ra_earnings` | `ra_earnings` | `ra_earnings` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:18` |
| `earnings_roll` | `earnings_roll` | `earnings_roll` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:19` |
| `def_div` | `def_div` | `def_div` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:20` |
| `def_dep` | `def_dep` | `def_dep` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:21` |
| `def_loc` | `def_loc` | `def_loc` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:22` |
| `def_funct` | `def_funct` | `def_funct` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:23` |
| `def_proj` | `def_proj` | `def_proj` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:24` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:25` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:26` |
| `voucher_variance` | `voucher_variance` | `voucher_variance` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:27` |
| `ap_beg_bal` | `ap_beg_bal` | `ap_beg_bal` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:28` |
| `ap_hold_beg_bal` | `ap_hold_beg_bal` | `ap_hold_beg_bal` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:29` |
| `resales_no` | `resales_no` | `resales_no` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:30` |
| `currency` | `currency` | `currency` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:31` |
| `country_code` | `country_code` | `country_code` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:1` |
| `activeflag` | `activeflag` | `activeflag` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:33` |
| `multi_curr_flag` | `multi_curr_flag` | `multi_curr_flag` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:34` |
| `intranet_url` | `intranet_url` | `intranet_url` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:35` |
| `company_logo` | `company_logo` | `company_logo` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:36` |
| `payroll_currency` | `payroll_currency` | `payroll_currency` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:37` |
| `company_timezone` | `company_timezone` | `company_timezone` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:38` |
| `sys_timezone` | `sys_timezone` | `sys_timezone` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:39` |
| `default_cis` | `default_cis` | `default_cis` | `ods_${country_code}.ods_cis_corp_company_info` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:40` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `ods_${country_code}.ods_cis_corp_company_info` | arithmetic | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_company_info.sql:41` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `activeflag` values | Company active/inactive status (domain-defined in source CIS) |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_company_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_company_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_company_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Verbatim copy:** All data is passed through without transformation; errors in the source propagate directly.
- **Full refresh:** Deletes or corrections in the source are reflected on the next run.
- **`etl_timestamp`** is in Pacific time regardless of the country being processed.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_company_info` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_company_info` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_company_info` in Vertica once MCP verification is completed for this document.

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
| **Finance** | `fy_begin`, `qtr1_end` … `qtr4_end` define the fiscal calendar for each company; `curr_period_begin/end` marks the current accounting period |
| **GL / accounting** | `ra_ap`, `ra_ar`, `ra_inv`, `ra_aphold`, `ra_earnings` are the default GL account ranges per company |
| **Operations** | `currency`, `payroll_currency`, `multi_curr_flag`, `company_timezone`, `sys_timezone` for financial and operational configuration |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_pub_company_info
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_company_info` | All columns — verbatim pass-through | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql:42` |

### Downstream consumers (verified)

None identified in repository.

### Operational detail (verified)

- Full table overwrite: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

---

*Document generated from `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_company_info.sql`.*
