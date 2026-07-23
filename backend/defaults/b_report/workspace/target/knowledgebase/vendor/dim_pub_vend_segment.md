# dim_pub_vend_segment.sql

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vendor_segment
- domain: vendor
- one_line_purpose: This ETL builds a vendor segment dimension by combining vendor master data, latest master-vendor cross-reference, marketing profile values, and segment hierarchy attributes. It produces a unified segment view for reporting and classificatio...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vendor_segment`
- **Layer type:** DIM
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** Not documented in repository
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** Not documented in repository - resolved from pipeline (see L4)
- **Natural key:** Not documented in repository
- **Exclusions:** Not documented in repository


### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dim_${country_code}.dim_pub_vendor_segment` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_${country_code}.dim_pub_vendor_segment` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_vendor_segment` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_vendor_segment.json` |
| **column_count** | 17 |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vend_segment schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_xref` | source for latest active `SRef` xref |
| 2 | `ods_${country_code}.ods_cis_corp_vend_master` | base vendor source + master vendor name |
| 3 | `ods_${country_code}.ods_cis_corp_vendor_profile` | MKNAME, SEG, and VEND_CAT profile attributes |
| 4 | `ods_${country_code}.ods_cis_corp_vendor_segment` | segment hierarchy lookup |
| 5 | `dim_${country_code}.dim_pub_vendor_segment` | target table (overwrite load) |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This ETL builds a vendor segment dimension by combining vendor master data, latest master-vendor cross-reference, marketing profile values, and segment hierarchy attributes. It produces a unified segment view for reporting and classification.

It helps procurement and category management teams analyze vendor segmentation, class/type structure, and master-vendor mapping.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (vendor)** | Uses `dim_${country_code}.dim_pub_vendor_segment` for operational and reporting workflows documented below. |

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/vendor/metric-index.md`](../../source/contracts/vendor/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/vendor/metric-index.md` are mapped on this table.

---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql` |

### Key filters and ETL business logic
### Sources and joins
- Creates `temp_vendor_xref` from active `SRef` xref records and keeps the latest per vendor by `entry_datetime` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:1-14`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master v` as base and joins xref, master vendor table, and profile/segment tables to enrich output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27-47`).

### Filters and business rules
- Xref temp view filters to `xref_type = 'SRef'`, `active = 'Y'`, and `xref_no <> 0` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:11-13`).
- MK name/rank values are from profile type `MKNAME`, category `CAT`, active only (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:35-37`).
- Catalog code prefers active `VEND_CAT` (`profile_cat='SEG'`) profile_i when present; otherwise falls back to segment table catalog_code (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:41-45`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:26`).

### Grain and deduplication
- Final grain is one row per vendor from `v` with optional enrichment columns (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:17`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27`).
- Deduplication of master xref is explicit with `row_number()` in temp view and `rn = 1` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:14`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_no` | Mapped master vendor number | Latest active `SRef` xref for vendor |
| `master_vend_name` | Master vendor name | Vendor name from vend_master for `master_vend_no` |
| `mk_name` | Marketing name attribute | Active MKNAME profile value for master vendor |
| `rank` | Vendor rank from marketing profile | Active MKNAME profile_i value |
| `catalog_code` | Catalog classification code | Uses `VEND_CAT` profile_i when available, else segment table default |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_${country_code}.dim_pub_vendor_segment
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
- Creates `temp_vendor_xref` from active `SRef` xref records and keeps the latest per vendor by `entry_datetime` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:1-14`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master v` as base and joins xref, master vendor table, and profile/segment tables to enrich output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27-47`).

### Filters and business rules
- Xref temp view filters to `xref_type = 'SRef'`, `active = 'Y'`, and `xref_no <> 0` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:11-13`).
- MK name/rank values are from profile type `MKNAME`, category `CAT`, active only (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:35-37`).
- Catalog code prefers active `VEND_CAT` (`profile_cat='SEG'`) profile_i when present; otherwise falls back to segment table catalog_code (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:41-45`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:26`).

### Grain and deduplication
- Final grain is one row per vendor from `v` with optional enrichment columns (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:17`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27`).
- Deduplication of master xref is explicit with `row_number()` in temp view and `rn = 1` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:14`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_no` | Mapped master vendor number | Latest active `SRef` xref for vendor |
| `master_vend_name` | Master vendor name | Vendor name from vend_master for `master_vend_no` |
| `mk_name` | Marketing name attribute | Active MKNAME profile value for master vendor |
| `rank` | Vendor rank from marketing profile | Active MKNAME profile_i value |
| `catalog_code` | Catalog classification code | Uses `VEND_CAT` profile_i when available, else segment table default |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[dim_pub_vend_segment]
  JOB --> TGT[dim_${country_code}.dim_pub_vendor_segment]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_xref` | source for latest active `SRef` xref |
| 2 | `ods_${country_code}.ods_cis_corp_vend_master` | base vendor source + master vendor name |
| 3 | `ods_${country_code}.ods_cis_corp_vendor_profile` | MKNAME, SEG, and VEND_CAT profile attributes |
| 4 | `ods_${country_code}.ods_cis_corp_vendor_segment` | segment hierarchy lookup |
| 5 | `dim_${country_code}.dim_pub_vendor_segment` | target table (overwrite load) |

### Step-by-step logic
### Sources and joins
- Creates `temp_vendor_xref` from active `SRef` xref records and keeps the latest per vendor by `entry_datetime` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:1-14`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master v` as base and joins xref, master vendor table, and profile/segment tables to enrich output (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27-47`).

### Filters and business rules
- Xref temp view filters to `xref_type = 'SRef'`, `active = 'Y'`, and `xref_no <> 0` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:11-13`).
- MK name/rank values are from profile type `MKNAME`, category `CAT`, active only (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:35-37`).
- Catalog code prefers active `VEND_CAT` (`profile_cat='SEG'`) profile_i when present; otherwise falls back to segment table catalog_code (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:41-45`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:26`).

### Grain and deduplication
- Final grain is one row per vendor from `v` with optional enrichment columns (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:17`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27`).
- Deduplication of master xref is explicit with `row_number()` in temp view and `rn = 1` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:9`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:14`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_no` | Mapped master vendor number | Latest active `SRef` xref for vendor |
| `master_vend_name` | Master vendor name | Vendor name from vend_master for `master_vend_no` |
| `mk_name` | Marketing name attribute | Active MKNAME profile value for master vendor |
| `rank` | Vendor rank from marketing profile | Active MKNAME profile_i value |
| `catalog_code` | Catalog classification code | Uses `VEND_CAT` profile_i when available, else segment table default |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_vendor_xref` | many:1 | `v.vend_no = x.vend_no and v.company_no=x.company_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |
| `temp_vendor_xref` | `ods_${country_code}.ods_cis_corp_vend_master` | many:1 | `x.xref_no = mv.vend_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |
| `temp_vendor_xref` | `ods_${country_code}.ods_cis_corp_vendor_profile` | many:1 | `x.xref_no = p.vend_no and p.profile_type = 'MKNAME' and p.profile_cat = 'CAT' and p.active = 'Y'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `ods_${country_code}.ods_cis_corp_vendor_profile` | many:1 | `v.vend_no = p1.vend_no and p1.profile_type = 'SEG'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `ods_${country_code}.ods_cis_corp_vendor_profile` | many:1 | `v.vend_no = p2.vend_no and p2.profile_type = 'VEND_CAT' and p2.profile_cat = 'SEG' and p2.active = 'Y'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |
| `ods_${country_code}.ods_cis_corp_vendor_profile` | `ods_${country_code}.ods_cis_corp_vendor_segment` | many:1 | `cast(p1.profile_c as varchar(3)) = vs.seg_code` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:1) |

`source/ref/vendor/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `v.vend_no` | `vend_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:17` |
| `discontinued` | `v.discontinued` | `discontinued` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:18` |
| `vend_name` | `v.vend_name` | `vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:19` |
| `master_vend_no` | `x.xref_no` | `xref_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:13` |
| `master_vend_name` | `mv.vend_name` | `vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:21` |
| `mk_name` | `p.profile_c` | `profile_c` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:22` |
| `rank` | `p.profile_i` | `profile_i` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:23` |
| `seg_code` | `seg_code` | `seg_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:24` |
| `seg_name` | `seg_name` | `seg_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `class_code` | `class_code` | `class_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `class_name` | `class_name` | `class_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `type_code` | `type_code` | `type_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `type_name` | `type_name` | `type_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `edi_flag` | `edi_flag` | `edi_flag` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `ece_flag` | `ece_flag` | `ece_flag` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:25` |
| `report_seq` | `report_seq` | `report_seq` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:26` |
| `catalog_code` | `if(p2.profile_i is null,catalog_code, p2.profile_i)` | `profile_i`, `catalog_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_vendor_xref`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_segment` | udf | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vend_segment.sql:26` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_vendor_segment
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_vendor_segment
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_vendor_segment
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}
HAVING COUNT(*) > 1;
```

Replace placeholders from this file's Grain and keys / Data you can fetch sections, and use the resolved partition value from run scope.

### Caveats for interpretation
None identified in repository

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_vendor_segment` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_vendor_segment` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_vendor_segment` in Vertica once MCP verification is completed for this document.

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
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_vendor_xref` | Latest `SRef` mapping derivation | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:10-13` |
| `ods_${country_code}.ods_cis_corp_vend_master` | Base vendor + master vendor name lookup | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:31-32` |
| `ods_${country_code}.ods_cis_corp_vendor_profile` | MKNAME, SEG, and VEND_CAT profile joins | `source/etl/sql/vendor/source/etl/flows/publ

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_${country_code}.dim_pub_vendor_segment
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_vendor_xref` | Latest `SRef` mapping derivation | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:10-13` |
| `ods_${country_code}.ods_cis_corp_vend_master` | Base vendor + master vendor name lookup | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:27`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:31-32` |
| `ods_${country_code}.ods_cis_corp_vendor_profile` | MKNAME, SEG, and VEND_CAT profile joins | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:33-45` |
| `ods_${country_code}.ods_cis_corp_vendor_segment` | Segment hierarchy lookup | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:46-47` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| `dim_${country_code}.dim_pub_vendor_segment_df` | Reads this table directly | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:4` |

### Operational detail (verified)
- Full overwrite load into `dim_${country_code}.dim_pub_vendor_segment` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql:16`).
- Partition strategy is not specified in this script.

### Not documented in repository
- Owner
- Schedule / cadence
- SLA / alerting
- Execution orchestration details

### Related scripts (verified)
- `dim_pub_vend_segment_df.sql` - downstream partitioned copy step from this output - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment_df.sql:4`.

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vend_segment.sql`.*
