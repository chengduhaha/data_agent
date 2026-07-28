# DIM: Historical Exchange Rate Pass-Through (`dim_pub_exchange_rate`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_exchange_rate
- domain: common
- one_line_purpose: This job is a full-refresh copy of all historical exchange rates from the DW production store into the country-specific dimension schema. It provides the complete rate history needed for multi-currency financial conversions, allowing downst...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_exchange_rate`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per currency pair per date.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full table overwrite. - resolved from pipeline (see L4)
- **Natural key:** `local_currency`, `base_currency`, `date_flag`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per currency pair per date.
- **Partition:** none — full table overwrite.
- **Natural key:** `local_currency`, `base_currency`, `date_flag`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_pub_exchange_rate` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_pub_exchange_rate` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_exchange_rate` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full table overwrite.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "common dim_pub_exchange_rate schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | Sole source |

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
This job is a full-refresh copy of all historical exchange rates from the DW production store into
the country-specific dimension schema. It provides the complete rate history needed for multi-currency
financial conversions, allowing downstream jobs to select the rate applicable to any historical date
by joining on `date_flag` and `local_currency`.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Finance / FP&A** | Convert local-currency financial amounts to base currency using the rate on any historical date |
| **Reporting** | Multi-currency fact tables join on `local_currency` + `date_flag` to get the applicable rate |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full table overwrite.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.

### Metrics served
When exposing this table to the business, lead with:

1. **Currency conversion:** `local_currency`, `base_currency`, `rate`
2. **Date lookup:** `date_flag`
3. **Alternate rates:** `rate2`, `rate3`

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Rate:** `local_currency`, `base_currency`, `date_flag`
- **Audit:** `entry_id`, `entry_datetime`

### Exchange rate values

- `rate` — Primary conversion rate
- `rate2` — Secondary rate (alternate period or rounding variant)
- `rate3` — Tertiary rate

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_exchange_rate`

**From:** `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate`

**Filter:** None — all rows.

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `local_currency` | `currency` | Renamed for clarity — the currency being expressed |
| `date_flag` | `to_date(date)` | Cast string date to date type |

**Pass-through columns (as-is):**
`base` (as `base_currency`), `rate`, `rate2`, `rate3`, `entry_id`, `entry_datetime`

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_pub_exchange_rate
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`
**Target table:** `dim_${country_code}.dim_pub_exchange_rate` — full table overwrite.

1. Read all rows from `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate`.
2. **INSERT OVERWRITE** with column renames (`currency` → `local_currency`, `date` → `date_flag`).

```mermaid
flowchart LR
  SRC[ods_dw_prod_dws_dw_exchange_rate] --> INS[INSERT OVERWRITE
dim_pub_exchange_rate
column rename]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Full rate history copy** | Reads every exchange rate row from the DW production source and writes it verbatim to `dim_pub_exchange_rate`, renaming columns for clarity |

**Parameters:** `country_code`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | Sole source — full historical exchange rate series |

**Temporary tables (inside the job only):**
None — direct INSERT with renames.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_exchange_rate`

**From:** `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate`

**Filter:** None — all rows.

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `local_currency` | `currency` | Renamed for clarity — the currency being expressed |
| `date_flag` | `to_date(date)` | Cast string date to date type |

**Pass-through columns (as-is):**
`base` (as `base_currency`), `rate`, `rate2`, `rate3`, `entry_id`, `entry_datetime`

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | 1:1 source scan | — (no JOIN; single FROM) | etl_sql (`source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:11`) |


### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `local_currency` | `currency` | `currency` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | rename | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:3` |
| `date_flag` | `to_date(`date`)` | — | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | udf | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:4` |
| `base_currency` | `base` | `base` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | rename | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:5` |
| `rate` | `rate` | `rate` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:1` |
| `rate2` | `rate2` | `rate2` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:7` |
| `rate3` | `rate3` | `rate3` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:8` |
| `entry_id` | `entry_id` | `entry_id` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:9` |
| `entry_datetime` | `entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | passthrough | `source/etl/sql/common/public_order_scripts/public_common_dimension/script/dim_pub_exchange_rate.sql:10` |

### Sentinel and code values
None identified.

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_exchange_rate
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_exchange_rate
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_exchange_rate
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **Full history:** All historical rate rows are included; downstream consumers must filter to the desired `date_flag`.
- **Three rate variants:** `rate`, `rate2`, `rate3` serve different rounding or period conventions — the correct variant depends on the consuming report's requirements.
- **Full refresh:** Corrections to historical rates in the source are reflected on the next run.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_exchange_rate` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_exchange_rate` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_exchange_rate` in Vertica once MCP verification is completed for this document.

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
| **Finance / FP&A** | Convert local-currency financial amounts to base currency using the rate on any historical date |
| **Reporting** | Multi-currency fact tables join on `local_currency` + `date_flag` to get the applicable rate |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_pub_exchange_rate
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_dw_prod_dws_dw_exchange_rate` | All columns — verbatim copy with renames | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql:11` |

### Downstream consumers (verified)

None identified in repository.

### Operational detail (verified)

- Full table overwrite: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

### Related scripts (verified)

- `dim_pub_exchange_rate_df.sql` — Daily partition snapshot for a country — `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/`
- `dim_pub_exchange_rate_df_us.sql` — Multi-region daily snapshot (US-anchored) — `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/`

---

*Document generated from `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/dim_pub_exchange_rate.sql`.*
