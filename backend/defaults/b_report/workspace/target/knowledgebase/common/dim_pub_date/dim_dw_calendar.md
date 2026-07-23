# DIM: CIS DW Calendar Pass-Through (`dim_dw_calendar`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_dw_calendar
- domain: common
- one_line_purpose: This job is a direct full-refresh copy of the corporate DW calendar from the CIS operational store into the country-specific dimension schema. It makes all calendar attributes — fiscal periods, quarters, weeks, bonus weeks, holidays, payrol...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_dw_calendar`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per calendar date.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full table overwrite. - resolved from pipeline (see L4)
- **Natural key:** `date_flag`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per calendar date.
- **Partition:** none — full table overwrite.
- **Natural key:** `date_flag`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_dw_calendar` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_dw_calendar` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_dw_calendar` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full table overwrite.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "common dim_dw_calendar schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | Sole source |

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
This job is a direct full-refresh copy of the corporate DW calendar from the CIS operational store
into the country-specific dimension schema. It makes all calendar attributes — fiscal periods,
quarters, weeks, bonus weeks, holidays, payroll flags, and sales flags — available in the dimension
layer without transformation, so that fact tables can join on `date_flag` to obtain any calendar
attribute needed for reporting.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **BI / reporting** | Join any fact table on `date_flag` to get fiscal week, quarter, year, bonus-week flag, and holiday flag for time-series aggregation |
| **Finance** | `fyear`, `fqtr`, `fdoy` support fiscal-year reporting distinct from the calendar year |
| **Sales / payroll** | `sales`, `payroll`, `bonuswk` flags mark days/weeks significant for commission and payroll calculations |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full table overwrite.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.

### Metrics served
When exposing this table to the business, lead with:

1. **Time hierarchy:** `year`, `qtr`, `month`, `week`, `day`
2. **Fiscal hierarchy:** `fyear`, `fqtr`, `fdoy`
3. **Special flags:** `holiday`, `payroll`, `bonuswk`, `sales`

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Date:** `date_flag`
- **Version:** `u_version`

### Dimension columns

Use these for **filters, group-bys, and star-schema joins**:

- `q` — calendar quarter flag
- `fq` — fiscal quarter flag
- `m` — month flag
- `w` — week flag
- `d` — day flag
- `year` — calendar year
- `qtr` — calendar quarter number
- `month` — month number
- `week` — week number
- `day` — day of month
- `doy` — day of year
- `fyear` — fiscal year
- `fqtr` — fiscal quarter
- `fdoy` — fiscal day of year
- `dow` — day of week (numeric)
- `dname` — day name
- `weekday` — weekday indicator
- `bonuswk` — bonus week flag
- `holiday` — holiday flag
- `payroll` — payroll flag
- `sales` — sales-active flag
- `comment` — calendar comment/note

---

### etl_metrics

N/A - no calculable ETL formulas extracted from this document (passthrough / stored measures only, or formulas not documented).

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_dw_calendar`

**From:** `ods_${country_code}.ods_cis_corp_dw_calendar`

**Filter:** None — all rows.

**Pass-through columns:**
`date_flag`, `u_version`, `q`, `fq`, `m`, `w`, `d`, `year`, `qtr`, `month`, `week`, `day`, `doy`,
`fyear`, `fqtr`, `fdoy`, `dow`, `dname`, `bonuswk`, `holiday`, `payroll`, `sales`, `comment`, `weekday`

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_dw_calendar
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`
**Target table:** `dim_${country_code}.dim_dw_calendar` — no partition (full overwrite).

1. Read all rows from `ods_cis_corp_dw_calendar`.
2. **INSERT OVERWRITE** all columns verbatim into `dim_dw_calendar`.

```mermaid
flowchart LR
  SRC[ods_cis_corp_dw_calendar] --> INS[INSERT OVERWRITE
dim_dw_calendar]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Full calendar copy** | Reads every row from `ods_cis_corp_dw_calendar` and writes it verbatim to `dim_dw_calendar`; no transformation or filtering applied |

**Parameters:** `country_code`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | Sole source — all calendar date attributes |

**Temporary tables (inside the job only):**
None — direct INSERT from source.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_dw_calendar`

**From:** `ods_${country_code}.ods_cis_corp_dw_calendar`

**Filter:** None — all rows.

**Pass-through columns:**
`date_flag`, `u_version`, `q`, `fq`, `m`, `w`, `d`, `year`, `qtr`, `month`, `week`, `day`, `doy`,
`fyear`, `fqtr`, `fdoy`, `dow`, `dname`, `bonuswk`, `holiday`, `payroll`, `sales`, `comment`, `weekday`

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | `ods_${country_code}.ods_cis_corp_dw_calendar` | 1:1 source scan | — (no JOIN; single FROM) | etl_sql (`source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:28`) |


### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `date_flag` | `date_flag` | `date_flag` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:4` |
| `u_version` | `u_version` | `u_version` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:5` |
| `q` | `q` | `q` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:6` |
| `fq` | `fq` | `fq` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:7` |
| `m` | `m` | `m` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:2` |
| `w` | `w` | `w` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:2` |
| `d` | `d` | `d` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:2` |
| `year` | `year` | `year` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:11` |
| `qtr` | `qtr` | `qtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:12` |
| `month` | `month` | `month` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:13` |
| `week` | `week` | `week` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:14` |
| `day` | `day` | `day` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:15` |
| `doy` | `doy` | `doy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:16` |
| `fyear` | `fyear` | `fyear` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:17` |
| `fqtr` | `fqtr` | `fqtr` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:18` |
| `fdoy` | `fdoy` | `fdoy` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:19` |
| `dow` | `dow` | `dow` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:20` |
| `dname` | `dname` | `dname` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:21` |
| `bonuswk` | `bonuswk` | `bonuswk` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:22` |
| `holiday` | `holiday` | `holiday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:23` |
| `payroll` | `payroll` | `payroll` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:24` |
| `sales` | `sales` | `sales` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:25` |
| `comment` | `comment` | `comment` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:26` |
| `weekday` | `weekday` | `weekday` | `ods_${country_code}.ods_cis_corp_dw_calendar` | passthrough | `source/etl/sql/common/public_order_scripts/dim_pub_date/dim_dw_calendar.sql:27` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `holiday` | The date is a recognized corporate holiday |
| `payroll` | Payroll-relevant date |
| `bonuswk` | Date falls in a bonus week |
| `sales` | Date is a valid sales day |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_dw_calendar
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_dw_calendar
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_dw_calendar
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Verbatim copy:** All data is passed through without transformation. Any errors in the source calendar propagate directly.
- **No derived period labels:** For formatted labels (e.g., `YYYY-W01`), use `dim_pub_date` which adds `week_flag`, `month_flag`, `quarter_flag`, and `fquarter_flag`.
- **Full refresh:** Calendar deletes or corrections in the source are reflected on next run.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_dw_calendar` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_dw_calendar` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_dw_calendar` in Vertica once MCP verification is completed for this document.

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
| **BI / reporting** | Join any fact table on `date_flag` to get fiscal week, quarter, year, bonus-week flag, and holiday flag for time-series aggregation |
| **Finance** | `fyear`, `fqtr`, `fdoy` support fiscal-year reporting distinct from the calendar year |
| **Sales / payroll** | `sales`, `payroll`, `bonuswk` flags mark days/weeks significant for commission and payroll calculations |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_dw_calendar
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_dw_calendar` | All columns — verbatim pass-through | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql:3` |

### Downstream consumers (verified)

None identified in repository.

### Operational detail (verified)

- Full table overwrite on every run: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

### Related scripts (verified)

- `dim_pub_date.sql` — enriched version with derived label columns — `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/`

---

*Document generated from `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/dim_pub_date/dim_dw_calendar.sql`.*
