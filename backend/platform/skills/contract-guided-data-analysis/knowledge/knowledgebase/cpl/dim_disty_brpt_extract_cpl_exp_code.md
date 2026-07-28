# DIM: CPL Expense Code Dimension (`dim_disty_brpt_extract_cpl_exp_code`)

- artifact_type: etl_table
- artifact_id: dim_us.dim_disty_brpt_extract_cpl_exp_code
- domain: cpl
- one_line_purpose: This dimension table maintains the set of expense codes seen in the CPL (Customer Profitability & Loss) reporting extract. It resolves a human-readable description from the CIS corporate expense code reference and enriches each code with tw...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_disty_brpt_extract_cpl_exp_code`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per distinct `exp_code`.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full overwrite each run. - resolved from pipeline (see L4)
- **Natural key:** `exp_code`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per distinct `exp_code`.
- **Partition:** none — full overwrite each run.
- **Natural key:** `exp_code`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_disty_brpt_extract_cpl_exp_code` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_disty_brpt_extract_cpl_exp_code` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_disty_brpt_extract_cpl_exp_code` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full overwrite each run.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "cpl dim_disty_brpt_extract_cpl_exp_code schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `dws_disty_brpt_extract_cpl_stage` | Primary source of distinct `exp_code` values. |
| `ods_cis_corp_exp_codes` | CIS reference for description and validation. |
| `dim_disty_brpt_extract_cpl_exp_code` | Target dimension — read back to carry forward existing rows. |
| `ods_breport_mydaas_dw_frt_exp_codes` | MyDaaS freight reference — final freight flag enrichment. |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `${literal_target_db}`, `${literal_source_db}`, `${literal_dim_db}` |


---

## L2 Declarative Knowledge

### Business purpose
This dimension table maintains the set of expense codes seen in the CPL (Customer Profitability & Loss) reporting extract. It resolves a human-readable description from the CIS corporate expense code reference and enriches each code with two freight-related classification flags: whether the expense is charged out to the customer (`frt_out_chg_to_cust_flag`) and whether it represents an outbound freight expense (`frt_out_exp_flag`). These flags are used in CPL P&L reports to categorize and separate freight-related expense lines from non-freight expenses.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **CPL Reporting** | Provides description and freight classification for every expense code, enabling P&L reports to separate freight expense lines from other expense categories. |
| **Data Engineers** | Controlled incremental dimension — only CIS-validated new codes are inserted; freight flags are refreshed from MyDaaS on every run. |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full overwrite each run.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/cpl/metric-index.md`](../../source/contracts/cpl/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/cpl/metric-index.md` are mapped on this table.

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Expense code:** `exp_code`

### Dimension columns (reporting-ready, pre-computed from source)

Use these for **filters, group-bys, and star-schema joins**:

- `exp_code` — expense code as it appears in transaction data
- `exp_code_desc` — human-readable description from `ods_cis_corp_exp_codes`
- `frt_out_chg_to_cust_flag` — `'Y'` if the expense is charged out to the deal/customer (sourced from `ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag`)
- `frt_out_exp_flag` — `'Y'` if the expense represents outbound freight (sourced from `ods_breport_mydaas_dw_frt_exp_codes.frt_out_flag`)

> **Note:** Newly inserted rows receive `frt_out_chg_to_cust_flag = 'N'` and `frt_out_exp_flag = 'N'` as defaults in the candidate set, but these are overridden by the MyDaaS join in the final INSERT.

---

### etl_metrics

#### `refer_flag`
- **Source:** [metric-index.md](../../source/contracts/cpl/metric-index.md#refer_flag)
- **Business definition:** `'Y'` if code exists in CIS expense reference.
```sql
CASE WHEN ods_cis_corp_exp_codes.exp_code IS NOT NULL THEN 'Y' ELSE 'N' END
```

#### `insert_flag`
- **Source:** [metric-index.md](../../source/contracts/cpl/metric-index.md#insert_flag)
- **Business definition:** `'Y'` if code is not yet in the dim.
```sql
CASE WHEN dim_disty_brpt_extract_cpl_exp_code.exp_code IS NOT NULL THEN 'N' ELSE 'Y' END
```

#### `frt_out_chg_to_cust_flag`
- **Source:** [metric-index.md](../../source/contracts/cpl/metric-index.md#frt_out_chg_to_cust_flag)
- **Business definition:** `'Y'` if MyDaaS marks this code as charged to the deal.
```sql
CASE WHEN e.chg_to_deal_flag = 'Y' THEN 'Y' ELSE 'N' END
```

#### `frt_out_exp_flag`
- **Source:** [metric-index.md](../../source/contracts/cpl/metric-index.md#frt_out_exp_flag)
- **Business definition:** `'Y'` if MyDaaS marks this code as outbound freight.
```sql
CASE WHEN e.frt_out_flag = 'Y' THEN 'Y' ELSE 'N' END
```


---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql` |

### Key filters and ETL business logic
### Step 1 — `CPL_exp_code_STAGE`

**Source:** `dws_disty_brpt_extract_cpl_stage`

**Filter:** Distinct `exp_code` values only; no date or partition filter.

**Derived columns:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `refer_flag` | `CASE WHEN ods_cis_corp_exp_codes.exp_code IS NOT NULL THEN 'Y' ELSE 'N' END` | `'Y'` if code exists in CIS expense reference. |
| `insert_flag` | `CASE WHEN dim_disty_brpt_extract_cpl_exp_code.exp_code IS NOT NULL THEN 'N' ELSE 'Y' END` | `'Y'` if code is not yet in the dim. |

---

### Step 2 — `CPL_exp_code_DIM`

**Sources:** `dim_disty_brpt_extract_cpl_exp_code` (existing rows), `CPL_exp_code_STAGE`, `ods_cis_corp_exp_codes`

**Branch A (existing rows):** Pass through `exp_code`, `exp_code_desc`, `frt_out_chg_to_cust_flag`, `frt_out_exp_flag` unchanged.

**Branch B (new codes):** Only rows with `refer_flag='Y'` AND `insert_flag='Y'`. Joined to `ods_cis_corp_exp_codes` for `exp_descr` (aliased `exp_code_desc`). Default `frt_out_chg_to_cust_flag = 'N'`, `frt_out_exp_flag = 'N'`.

---

### Step 3 — Final `INSERT OVERWRITE` into `dim_disty_brpt_extract_cpl_exp_code`

**From:** `CPL_exp_code_DIM` (left-joined to `ods_breport_mydaas_dw_frt_exp_codes` on `exp_code`)

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `frt_out_chg_to_cust_flag` | `CASE WHEN e.chg_to_deal_flag = 'Y' THEN 'Y' ELSE 'N' END` | `'Y'` if MyDaaS marks this code as char...

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_disty_brpt_extract_cpl_exp_code
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `${literal_target_db}`, `${literal_source_db}`, `${literal_dim_db}`
**Target table:** `dim_disty_brpt_extract_cpl_exp_code` (non-partitioned dimension).

1. Read distinct `exp_code` from CPL staging and determine `refer_flag` / `insert_flag` against CIS reference and existing dim.
2. Build `CPL_exp_code_DIM`: UNION of existing dim rows and new CIS-matched codes with default freight flags.
3. **INSERT OVERWRITE**: Write combined view, left-joining to `ods_breport_mydaas_dw_frt_exp_codes` to set final freight flags.

```mermaid
flowchart LR
  subgraph src [Source tables]
    STAGE[dws_disty_brpt_extract_cpl_stage]
    CIS[ods_cis_corp_exp_codes]
    DIM_OLD[dim_disty_brpt_extract_cpl_exp_code
existing rows]
    MYDAAS[ods_breport_mydaas_dw_frt_exp_codes]
  end
  STAGE --> V1[CPL_exp_code_STAGE
refer_flag / insert_flag]
  CIS --> V1
  DIM_OLD --> V1
  V1 --> V2[CPL_exp_code_DIM
existing UNION ALL new codes]
  DIM_OLD --> V2
  CIS --> V2
  V2 --> INS[INSERT OVERWRITE
dim_disty_brpt_extract_cpl_exp_code]
  MYDAAS --> INS
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Stage check** | Scans the CPL staging table for distinct `exp_code` values and determines which ones exist in the CIS expense codes reference (`refer_flag`) and which are new to the dimension (`insert_flag`). |
| **Build candidate set** | Merges existing dim rows with newly-discovered codes (enriched with CIS descriptions and default flags) into a combined view. |
| **Final INSERT OVERWRITE** | Writes all rows back, enriching each record's freight flags from the MyDaaS DW freight expense codes reference table. |

**Parameters:** `${literal_target_db}`, `${literal_source_db}`, `${literal_dim_db}`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dws_disty_brpt_extract_cpl_stage` | Primary source — provides distinct `exp_code` values from current CPL data. |
| `ods_cis_corp_exp_codes` | CIS reference — validates code existence (`refer_flag`) and supplies `exp_descr`. |
| `dim_disty_brpt_extract_cpl_exp_code` | Target and read-back source — existing rows carried forward. |
| `ods_breport_mydaas_dw_frt_exp_codes` | MyDaaS freight enrichment — provides `chg_to_deal_flag` and `frt_out_flag` at INSERT time. |

**Temporary views (inside the job only):**
`CPL_exp_code_STAGE` → `CPL_exp_code_DIM` → (final `INSERT OVERWRITE`)

---

### Step-by-step logic
### Step 1 — `CPL_exp_code_STAGE`

**Source:** `dws_disty_brpt_extract_cpl_stage`

**Filter:** Distinct `exp_code` values only; no date or partition filter.

**Derived columns:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `refer_flag` | `CASE WHEN ods_cis_corp_exp_codes.exp_code IS NOT NULL THEN 'Y' ELSE 'N' END` | `'Y'` if code exists in CIS expense reference. |
| `insert_flag` | `CASE WHEN dim_disty_brpt_extract_cpl_exp_code.exp_code IS NOT NULL THEN 'N' ELSE 'Y' END` | `'Y'` if code is not yet in the dim. |

---

### Step 2 — `CPL_exp_code_DIM`

**Sources:** `dim_disty_brpt_extract_cpl_exp_code` (existing rows), `CPL_exp_code_STAGE`, `ods_cis_corp_exp_codes`

**Branch A (existing rows):** Pass through `exp_code`, `exp_code_desc`, `frt_out_chg_to_cust_flag`, `frt_out_exp_flag` unchanged.

**Branch B (new codes):** Only rows with `refer_flag='Y'` AND `insert_flag='Y'`. Joined to `ods_cis_corp_exp_codes` for `exp_descr` (aliased `exp_code_desc`). Default `frt_out_chg_to_cust_flag = 'N'`, `frt_out_exp_flag = 'N'`.

---

### Step 3 — Final `INSERT OVERWRITE` into `dim_disty_brpt_extract_cpl_exp_code`

**From:** `CPL_exp_code_DIM` (left-joined to `ods_breport_mydaas_dw_frt_exp_codes` on `exp_code`)

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `frt_out_chg_to_cust_flag` | `CASE WHEN e.chg_to_deal_flag = 'Y' THEN 'Y' ELSE 'N' END` | `'Y'` if MyDaaS marks this code as charged to the deal. |
| `frt_out_exp_flag` | `CASE WHEN e.frt_out_flag = 'Y' THEN 'Y' ELSE 'N' END` | `'Y'` if MyDaaS marks this code as outbound freight. |

**Pass-through columns:** `exp_code`, `exp_code_desc`

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `${literal_target_db}.dws_disty_brpt_extract_cpl_stage` | `${literal_source_db}.ods_cis_corp_exp_codes` | many:1 | `i.exp_code = m.exp_code` | etl_sql (source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:1) |
| `${literal_target_db}.dws_disty_brpt_extract_cpl_stage` | `${literal_dim_db}.dim_disty_brpt_extract_cpl_exp_code` | many:1 | `i.exp_code = d.exp_code; DROP VIEW IF EXISTS CPL_exp_code_DIM; CREATE TEMPORARY VIEW CPL_exp_code_DIM AS` | etl_sql (source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:1) |
| `${literal_target_db}.dws_disty_brpt_extract_cpl_stage` | `${literal_source_db}.ods_cis_corp_exp_codes` | many:1 | `Not documented in repository` | etl_sql (source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:1) |
| `${literal_dim_db}.dim_disty_brpt_extract_cpl_exp_code` | `${literal_source_db}.ods_breport_mydaas_dw_frt_exp_codes` | many:1 | `d.exp_code = e.exp_code;` | etl_sql (source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:1) |

`source/ref/cpl/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `exp_code` | `d.exp_code` | `exp_code` | `CPL_exp_code_DIM`, `${literal_source_db}.ods_breport_mydaas_dw_frt_exp_codes` | passthrough | `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:5` |
| `exp_code_desc` | `d.exp_code_desc` | `exp_code_desc` | `CPL_exp_code_DIM`, `${literal_source_db}.ods_breport_mydaas_dw_frt_exp_codes` | passthrough | `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:32` |
| `frt_out_chg_to_cust_flag` | `CASE WHEN e.chg_to_deal_flag = 'Y' THEN 'Y' ELSE 'N' END` | `chg_to_deal_flag`, `Y`, `N` | `CPL_exp_code_DIM`, `${literal_source_db}.ods_breport_mydaas_dw_frt_exp_codes` | case | `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:33` |
| `frt_out_exp_flag` | `CASE WHEN e.frt_out_flag = 'Y' THEN 'Y' ELSE 'N' END` | `frt_out_flag`, `Y`, `N` | `CPL_exp_code_DIM`, `${literal_source_db}.ods_breport_mydaas_dw_frt_exp_codes` | case | `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql:34` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `frt_out_chg_to_cust_flag = 'N'` (default) | Newly inserted code has no MyDaaS freight-charge mapping at candidate build time; overridden by final INSERT join. |
| `frt_out_exp_flag = 'N'` (default) | Newly inserted code has no MyDaaS outbound freight mapping at candidate build time; overridden by final INSERT join. |
| `refer_flag = 'Y'` | Code exists in CIS and can be enriched. |
| `insert_flag = 'Y'` | Code is not yet in the dim and will be inserted. |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- Freight flags (`frt_out_chg_to_cust_flag`, `frt_out_exp_flag`) are refreshed from MyDaaS on every run for all rows, including existing ones. Changes in the MyDaaS reference will propagate automatically.
- Expense codes not found in `ods_cis_corp_exp_codes` are never inserted — no placeholder row is created for unresolved codes.
- The candidate-set defaults (`'N'` flags) are immediately overridden by the MyDaaS join in the final INSERT; they exist only as structural placeholders in the intermediate view.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `ods_breport_mydaas_dw_frt_exp_codes.chg_to_deal_flag` in Vertica once MCP verification is completed for this document.

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
| **CPL Reporting** | Provides description and freight classification for every expense code, enabling P&L reports to separate freight expense lines from other expense categories. |
| **Data Engineers** | Controlled incremental dimension — only CIS-validated new codes are inserted; freight flags are refreshed from MyDaaS on every run. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_disty_brpt_extract_cpl_exp_code
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `dws_disty_brpt_extract_cpl_stage` | Source of distinct `exp_code` values | `dim_disty_brpt_extract_cpl_exp_code.sql:6` |
| `ods_cis_corp_exp_codes` | Reference lookup for description and validation | `dim_disty_brpt_extract_cpl_exp_code.sql:7,25` |
| `dim_disty_brpt_extract_cpl_exp_code` | Existing dim rows read and rewritten | `dim_disty_brpt_extract_cpl_exp_code.sql:9,16` |
| `ods_breport_mydaas_dw_frt_exp_codes` | Freight flag enrichment at INSERT | `dim_disty_brpt_extract_cpl_exp_code.sql:36` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| None identified in repository. | — |

### Operational detail (verified)

- Full table overwrite (`INSERT OVERWRITE`) — entire dimension is rewritten each run.
- Freight flags are re-evaluated for all rows on every run via the MyDaaS left join.

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs.

---

*Document generated from `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/cpl/data_service/cpl_extract/sql/dim_disty_brpt_extract_cpl_exp_code.sql`.*
