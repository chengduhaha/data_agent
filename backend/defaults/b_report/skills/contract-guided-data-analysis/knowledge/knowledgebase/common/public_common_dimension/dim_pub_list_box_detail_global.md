# DIM: Global List Box Detail — All Servers (`dim_pub_list_box_detail`) [ods_gbl variant]

- artifact_type: etl_table
- artifact_id: dim_us.dim_pub_list_box_detail
- domain: common
- one_line_purpose: This job loads all global CIS list-box code records into `dim_pub_list_box_detail` without any country or CIS-server filter. It is intended for use in global reporting schemas (e.g., `ods_gbl`) where all enumeration codes across all countri...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_us.dim_pub_list_box_detail`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per list-box entry per CIS server (global, all servers).
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** none — full table overwrite. - resolved from pipeline (see L4)
- **Natural key:** `cisserver`, `list_box_code`, `code_value`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per list-box entry per CIS server (global, all servers).
- **Partition:** none — full table overwrite.
- **Natural key:** `cisserver`, `list_box_code`, `code_value`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_pub_list_box_detail` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_pub_list_box_detail` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_us.dim_pub_list_box_detail` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `none — full table overwrite.` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "common dim_pub_list_box_detail_global schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `ods_gbl.ods_cis_mygbl_global_list_box_detail` | Sole source |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code` (used only in target table name — no filtering applied) |


---

## L2 Declarative Knowledge

### Business purpose
This job loads all global CIS list-box code records into `dim_pub_list_box_detail` without any
country or CIS-server filter. It is intended for use in global reporting schemas (e.g., `ods_gbl`)
where all enumeration codes across all countries must be available for cross-country code
resolution and global dashboards.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Global BI / reporting** | Resolve code values from any country without needing to know which CIS server the code belongs to |
| **Data engineering** | Single unfiltered reference for all list-box codes, useful for building cross-country dashboards |

---

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** none — full table overwrite.
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.

### Metrics served
When exposing this table to the business, lead with:

1. **Global code resolution:** `cisserver`, `list_box_code`, `code_value`, `code_desc`
2. **Validity:** `activeflag`, `delete_datetime`

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Code:** `cisserver`, `list_box_code`, `code_value`

### Dimension columns

- `code_desc` — Human-readable label
- `activeflag` — Active status
- `sequence` — Display order
- `key1`, `ref1`, `ref2` — Auxiliary reference keys
- `entry_datetime`, `entry_id`, `delete_datetime`, `delete_id`, `update_datetime` — Audit fields
- `h_version` — History version
- `purgeflag`, `schedule_date` — Maintenance flags

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql` |

### Key filters and ETL business logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_list_box_detail`

**From:** `ods_gbl.ods_cis_mygbl_global_list_box_detail lbd`

**Filter:** None — all rows, all CIS servers.

**Pass-through columns:**
`cisserver`, `list_box_code`, `code_value`, `code_desc`, `activeflag`, `sequence`, `key1`,
`ref1`, `ref2`, `entry_datetime`, `entry_id`, `delete_datetime`, `delete_id`, `update_datetime`,
`h_version`, `purgeflag`, `schedule_date`

---

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_pub_list_box_detail
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code` (target schema only)
**Target table:** `dim_${country_code}.dim_pub_list_box_detail` — full table overwrite.

1. Read all rows from `ods_gbl.ods_cis_mygbl_global_list_box_detail` (no filter).
2. **INSERT OVERWRITE** all columns.

```mermaid
flowchart LR
  SRC[ods_gbl.ods_cis_mygbl_global_list_box_detail
ALL rows - no filter] --> INS[INSERT OVERWRITE
dim_pub_list_box_detail]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Global full copy** | Reads every row from `ods_gbl.ods_cis_mygbl_global_list_box_detail` and writes it to `dim_pub_list_box_detail` without any filtering |

**Parameters:** `country_code` (used only in target table name — no filtering applied)

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `ods_gbl.ods_cis_mygbl_global_list_box_detail` | Sole source — all list-box records, all CIS servers |

**Temporary tables (inside the job only):**
None — direct INSERT from source.

---

### Step-by-step logic
### Step 1 — Final `INSERT OVERWRITE` into `dim_pub_list_box_detail`

**From:** `ods_gbl.ods_cis_mygbl_global_list_box_detail lbd`

**Filter:** None — all rows, all CIS servers.

**Pass-through columns:**
`cisserver`, `list_box_code`, `code_value`, `code_desc`, `activeflag`, `sequence`, `key1`,
`ref1`, `ref2`, `entry_datetime`, `entry_id`, `delete_datetime`, `delete_id`, `update_datetime`,
`h_version`, `purgeflag`, `schedule_date`

---

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `activeflag` | Code is active |
| `purgeflag` | Code is marked for purge |

---

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM ods_gbl.ods_cis_mygbl_global_list_box_detail
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM ods_gbl.ods_cis_mygbl_global_list_box_detail
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM ods_gbl.ods_cis_mygbl_global_list_box_detail
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
- **No country filtering:** Unlike the country-scoped version, this script loads ALL servers. Loading this into a country-specific schema will overwrite the country-filtered data, so use only in global schemas.
- **Duplicate codes across servers:** Multiple rows with the same `list_box_code` + `code_value` but different `cisserver` are expected and valid.
- **Full refresh on every run.**

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `ods_gbl.ods_cis_mygbl_global_list_box_detail` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `ods_gbl.ods_cis_mygbl_global_list_box_detail` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `ods_gbl.ods_cis_mygbl_global_list_box_detail` in Vertica once MCP verification is completed for this document.

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
| **Global BI / reporting** | Resolve code values from any country without needing to know which CIS server the code belongs to |
| **Data engineering** | Single unfiltered reference for all list-box codes, useful for building cross-country dashboards |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_pub_list_box_detail
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_gbl.ods_cis_mygbl_global_list_box_detail` | All columns — no filter | `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql:20` |

### Downstream consumers (verified)

None identified in repository.

### Operational detail (verified)

- Full table overwrite: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql:1`

### Not documented in repository

- Schedule, owner, SLA — not in scripts or configs

### Related scripts (verified)

- `script/dim_pub_list_box_detail.sql` — Country-scoped version (INNER JOIN to `app_config`) — `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/`

---

*Document generated from `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/common/source/etl/flows/public_order_tools/ingest/public_common_dimension/script/ods_gbl/dim_pub_list_box_detail.sql`.*
