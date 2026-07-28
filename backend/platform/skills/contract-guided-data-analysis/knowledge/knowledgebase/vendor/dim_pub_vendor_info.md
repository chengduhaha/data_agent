# dim_pub_vendor_info.sql

- artifact_type: etl_table
- artifact_id: dim_${country_code}.dim_pub_vendor_info
- domain: vendor
- one_line_purpose: This ETL builds a consolidated vendor dimension record by combining vendor master attributes with profile, cross-reference, currency, segment, and status details. The output is designed to support vendor master data consumption in analytics...
- layer_type: DIM
- source_kind: etl_sql
- evidence_source: source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dim_${country_code}.dim_pub_vendor_info`
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
| Hive | yes | `dim_${country_code}.dim_pub_vendor_info` | ETL target / intermediate per evidence script |
| Vertica | pending | `dim_${country_code}.dim_pub_vendor_info` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dim_${country_code}.dim_pub_vendor_info` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/vertica_dim_us_dim_pub_vendor_info.json` |
| **column_count** | 49 |
| **partition_keys** | `Not documented in repository` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "vendor dim_pub_vendor_info schema" --intent find_table_schema` |

### Lineage
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_profile` | source for profile-derived temp fields (`temp_corp_vendor_profile`) |
| 2 | `ods_${country_code}.ods_cis_corp_vendor_xref` | source for latest xref (`temp_vendor_xref`) and purchasing xref join |
| 3 | `ods_${country_code}.ods_cis_corp_v_vend_currency` | source for vendor currency (`temp_vend_currency`) |
| 4 | `ods_${country_code}.ods_cis_corp_vend_master_etc` | source for vendor extra attributes (`temp_vend_master_etc`) |
| 5 | `ods_${country_code}.ods_cis_corp_vend_master` | primary source/vendor grain base |
| 6 | `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | source for SMB image flag |
| 7 | `dim_${country_code}.dim_pub_list_box_detail` | lookup for diversity status description |
| 8 | `ods_${country_code}.ods_cis_corp_vendor_segment` | source for segment name |
| 9 | `ods_${country_code}.ods_cis_corp_v_vend_etc` | source for vendor terms |
| 10 | `dim_${country_code}.dim_pub_vendor_info` | target table (overwrite load) |

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | See source script / flow parameters |


---

## L2 Declarative Knowledge

### Business purpose
This ETL builds a consolidated vendor dimension record by combining vendor master attributes with profile, cross-reference, currency, segment, and status details. The output is designed to support vendor master data consumption in analytics and operational reporting.

It helps procurement, AP, supply chain, and master-data users analyze vendor hierarchy, purchasing-vendor linkage, diversity status, segment metadata, and key vendor control flags.

### Audience and use cases
| Audience | How they benefit |
|----------|------------------|
| **Domain consumers (vendor)** | Uses `dim_${country_code}.dim_pub_vendor_info` for operational and reporting workflows documented below. |

### Identifier search profile
- Primary lookup keys: see natural key under L1 Grain.
- Use latest snapshot / active flags when documented in L3 filters.

### Time field semantics
- **date_flag / partition columns:** Not documented in repository
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| P&L adjustment / measure | `vend_pay_frt_amt` | `vend_pay_frt_amt` | vend_pay_frt_amt at unspecified grain |

### Metric serving map

**Formula authority:** [`source/contracts/vendor/metric-index.md`](../../source/contracts/vendor/metric-index.md)

| Logical metric | Period scope | Physical column | Formula reference |
|----------------|--------------|-----------------|-------------------|
| `vend_pay_frt_amt` | unspecified | `vend_pay_frt_amt` | Not in metric-index.md |

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
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql` |

### Key filters and ETL business logic
### Sources and joins
- Builds four temporary views for profile rollups, latest xref per `(vend_no, xref_type)`, vendor currency, and vendor extra attributes before final insert (`dim_pub_vendor_info.sql:5`, `dim_pub_vendor_info.sql:40`, `dim_pub_vendor_info.sql:56`, `dim_pub_vendor_info.sql:64`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master` as the base table and left-joins profile/xref/currency/segment/detail tables to enrich vendor attributes (`dim_pub_vendor_info.sql:132` onward).
- Uses xref type `SRef` to derive master vendor linkage and xref type `DIVS` to derive diversity status (`dim_pub_vendor_info.sql:140`, `dim_pub_vendor_info.sql:168`).
- Joins list box detail on diversity code value and active `DIVS` entries to map descriptions (`dim_pub_vendor_info.sql:169-173`).

### Filters and business rules
- Profile temp view keeps specific profile types and active records for several attributes (`dim_pub_vendor_info.sql:15`, `dim_pub_vendor_info.sql:19`, `dim_pub_vendor_info.sql:22`, `dim_pub_vendor_info.sql:27`, `dim_pub_vendor_info.sql:31`, `dim_pub_vendor_info.sql:37`).
- Xref temp view keeps only active rows with `xref_type in ('SRef','DIVS')`, non-zero `xref_no`, then selects latest by `entry_datetime` via `row_number()` (`dim_pub_vendor_info.sql:49-54`).
- Consignment and purchasing joins require active profile/xref rows (`dim_pub_vendor_info.sql:147-154`).
- SMB image flag is based on active rows in the global SMB config source (`dim_pub_vendor_info.sql:160`).

### Grain and deduplication
- Final dataset grain is one row per `vm.vend_no` from vendor master, with left joins for optional attributes (`dim_pub_vendor_info.sql:79`, `dim_pub_vendor_info.sql:132-177`).
- Deduplication is explicit in `temp_vendor_xref` using `row_number()` partitioned by `vend_no, xref_type` and keeping `rn = 1` (`dim_pub_vendor_info.sql:49-54`).
- Profile/currency/etc temp views collapse multiple records per vendor with grouped `max(...)` expressions (`dim_pub_vendor_info.sql:8-38`, `dim_pub_vendor_info.sql:59-63`, `dim_pub_vendor_info.sql:66-73`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_flag` | Whether vendor is considered a master vendor reference | `Y` when latest `SRef` xref number equals the vendor number, else `N` |
| `master_vend_no` | Referenced master vendor number | Latest `SRef` xref number from xref temp view |
| `vend_consign_flag` | Whether vendor is marked as consignment vendor | Active `CSGN_VEND` profile value, default `N` when missing |
| `pur_vend_no` | Purchasing vendor number | Active `VEND_PURCH` xref number |
| `smb_vend_image_flag` | Whether vendor is in active SMB image config | `Y` when vendor appears in active SMB config list |
| `n_comp_brp_flag` | Indicator for N_COMP_BRP vendor profile presence | `1` when derived profile flag exists, else `0` |
| `diversity_status_desc` | Description of vendor diversity status | Lookup from `dim_pub_list_box_detail` for `DIVS` code |
| `etl_timestamp` | ETL load timestamp (Pacific time) | Current timestamp converted from UTC to `America/Los_Angeles` |

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dim_${country_code}.dim_pub_vendor_info
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
### Sources and joins
- Builds four temporary views for profile rollups, latest xref per `(vend_no, xref_type)`, vendor currency, and vendor extra attributes before final insert (`dim_pub_vendor_info.sql:5`, `dim_pub_vendor_info.sql:40`, `dim_pub_vendor_info.sql:56`, `dim_pub_vendor_info.sql:64`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master` as the base table and left-joins profile/xref/currency/segment/detail tables to enrich vendor attributes (`dim_pub_vendor_info.sql:132` onward).
- Uses xref type `SRef` to derive master vendor linkage and xref type `DIVS` to derive diversity status (`dim_pub_vendor_info.sql:140`, `dim_pub_vendor_info.sql:168`).
- Joins list box detail on diversity code value and active `DIVS` entries to map descriptions (`dim_pub_vendor_info.sql:169-173`).

### Filters and business rules
- Profile temp view keeps specific profile types and active records for several attributes (`dim_pub_vendor_info.sql:15`, `dim_pub_vendor_info.sql:19`, `dim_pub_vendor_info.sql:22`, `dim_pub_vendor_info.sql:27`, `dim_pub_vendor_info.sql:31`, `dim_pub_vendor_info.sql:37`).
- Xref temp view keeps only active rows with `xref_type in ('SRef','DIVS')`, non-zero `xref_no`, then selects latest by `entry_datetime` via `row_number()` (`dim_pub_vendor_info.sql:49-54`).
- Consignment and purchasing joins require active profile/xref rows (`dim_pub_vendor_info.sql:147-154`).
- SMB image flag is based on active rows in the global SMB config source (`dim_pub_vendor_info.sql:160`).

### Grain and deduplication
- Final dataset grain is one row per `vm.vend_no` from vendor master, with left joins for optional attributes (`dim_pub_vendor_info.sql:79`, `dim_pub_vendor_info.sql:132-177`).
- Deduplication is explicit in `temp_vendor_xref` using `row_number()` partitioned by `vend_no, xref_type` and keeping `rn = 1` (`dim_pub_vendor_info.sql:49-54`).
- Profile/currency/etc temp views collapse multiple records per vendor with grouped `max(...)` expressions (`dim_pub_vendor_info.sql:8-38`, `dim_pub_vendor_info.sql:59-63`, `dim_pub_vendor_info.sql:66-73`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_flag` | Whether vendor is considered a master vendor reference | `Y` when latest `SRef` xref number equals the vendor number, else `N` |
| `master_vend_no` | Referenced master vendor number | Latest `SRef` xref number from xref temp view |
| `vend_consign_flag` | Whether vendor is marked as consignment vendor | Active `CSGN_VEND` profile value, default `N` when missing |
| `pur_vend_no` | Purchasing vendor number | Active `VEND_PURCH` xref number |
| `smb_vend_image_flag` | Whether vendor is in active SMB image config | `Y` when vendor appears in active SMB config list |
| `n_comp_brp_flag` | Indicator for N_COMP_BRP vendor profile presence | `1` when derived profile flag exists, else `0` |
| `diversity_status_desc` | Description of vendor diversity status | Lookup from `dim_pub_list_box_detail` for `DIVS` code |
| `etl_timestamp` | ETL load timestamp (Pacific time) | Current timestamp converted from UTC to `America/Los_Angeles` |

```mermaid
flowchart LR
  SRC[upstream sources] --> JOB[dim_pub_vendor_info]
  JOB --> TGT[dim_${country_code}.dim_pub_vendor_info]
```



### Base tables register
| Step | Object | Role |
|------|--------|------|
| 1 | `ods_${country_code}.ods_cis_corp_vendor_profile` | source for profile-derived temp fields (`temp_corp_vendor_profile`) |
| 2 | `ods_${country_code}.ods_cis_corp_vendor_xref` | source for latest xref (`temp_vendor_xref`) and purchasing xref join |
| 3 | `ods_${country_code}.ods_cis_corp_v_vend_currency` | source for vendor currency (`temp_vend_currency`) |
| 4 | `ods_${country_code}.ods_cis_corp_vend_master_etc` | source for vendor extra attributes (`temp_vend_master_etc`) |
| 5 | `ods_${country_code}.ods_cis_corp_vend_master` | primary source/vendor grain base |
| 6 | `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | source for SMB image flag |
| 7 | `dim_${country_code}.dim_pub_list_box_detail` | lookup for diversity status description |
| 8 | `ods_${country_code}.ods_cis_corp_vendor_segment` | source for segment name |
| 9 | `ods_${country_code}.ods_cis_corp_v_vend_etc` | source for vendor terms |
| 10 | `dim_${country_code}.dim_pub_vendor_info` | target table (overwrite load) |

### Step-by-step logic
### Sources and joins
- Builds four temporary views for profile rollups, latest xref per `(vend_no, xref_type)`, vendor currency, and vendor extra attributes before final insert (`dim_pub_vendor_info.sql:5`, `dim_pub_vendor_info.sql:40`, `dim_pub_vendor_info.sql:56`, `dim_pub_vendor_info.sql:64`).
- Uses `ods_${country_code}.ods_cis_corp_vend_master` as the base table and left-joins profile/xref/currency/segment/detail tables to enrich vendor attributes (`dim_pub_vendor_info.sql:132` onward).
- Uses xref type `SRef` to derive master vendor linkage and xref type `DIVS` to derive diversity status (`dim_pub_vendor_info.sql:140`, `dim_pub_vendor_info.sql:168`).
- Joins list box detail on diversity code value and active `DIVS` entries to map descriptions (`dim_pub_vendor_info.sql:169-173`).

### Filters and business rules
- Profile temp view keeps specific profile types and active records for several attributes (`dim_pub_vendor_info.sql:15`, `dim_pub_vendor_info.sql:19`, `dim_pub_vendor_info.sql:22`, `dim_pub_vendor_info.sql:27`, `dim_pub_vendor_info.sql:31`, `dim_pub_vendor_info.sql:37`).
- Xref temp view keeps only active rows with `xref_type in ('SRef','DIVS')`, non-zero `xref_no`, then selects latest by `entry_datetime` via `row_number()` (`dim_pub_vendor_info.sql:49-54`).
- Consignment and purchasing joins require active profile/xref rows (`dim_pub_vendor_info.sql:147-154`).
- SMB image flag is based on active rows in the global SMB config source (`dim_pub_vendor_info.sql:160`).

### Grain and deduplication
- Final dataset grain is one row per `vm.vend_no` from vendor master, with left joins for optional attributes (`dim_pub_vendor_info.sql:79`, `dim_pub_vendor_info.sql:132-177`).
- Deduplication is explicit in `temp_vendor_xref` using `row_number()` partitioned by `vend_no, xref_type` and keeping `rn = 1` (`dim_pub_vendor_info.sql:49-54`).
- Profile/currency/etc temp views collapse multiple records per vendor with grouped `max(...)` expressions (`dim_pub_vendor_info.sql:8-38`, `dim_pub_vendor_info.sql:59-63`, `dim_pub_vendor_info.sql:66-73`).

### Key columns
| Column | Business meaning | How it is derived (plain language) |
|--------|------------------|-------------------------------------|
| `master_vend_flag` | Whether vendor is considered a master vendor reference | `Y` when latest `SRef` xref number equals the vendor number, else `N` |
| `master_vend_no` | Referenced master vendor number | Latest `SRef` xref number from xref temp view |
| `vend_consign_flag` | Whether vendor is marked as consignment vendor | Active `CSGN_VEND` profile value, default `N` when missing |
| `pur_vend_no` | Purchasing vendor number | Active `VEND_PURCH` xref number |
| `smb_vend_image_flag` | Whether vendor is in active SMB image config | `Y` when vendor appears in active SMB config list |
| `n_comp_brp_flag` | Indicator for N_COMP_BRP vendor profile presence | `1` when derived profile flag exists, else `0` |
| `diversity_status_desc` | Description of vendor diversity status | Lookup from `dim_pub_list_box_detail` for `DIVS` code |
| `etl_timestamp` | ETL load timestamp (Pacific time) | Current timestamp converted from UTC to `America/Los_Angeles` |

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_corp_vendor_profile` | many:1 | `vm.vend_no = vp.vend_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_vendor_xref` | many:1 | `vm.vend_no = vx.vend_no and vm.company_no = vx.company_no and vx.xref_type='SRef'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_vend_currency` | many:1 | `vm.vend_no = vc.vend_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `ods_${country_code}.ods_cis_corp_vendor_profile` | many:1 | `vm.vend_no = vp2.vend_no and vp2.profile_type = 'CSGN_VEND' and vp2.active='Y'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `ods_${country_code}.ods_cis_corp_vendor_xref` | many:1 | `vm.vend_no = vx2.vend_no and vm.company_no=vx2.company_no and vx2.xref_type = 'VEND_PURCH' and vx2.active = 'Y'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vendor_xref` | `ods_${country_code}.ods_cis_corp_vend_master` | many:1 | `vm2.vend_no = vx2.xref_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `temp_vendor_xref` | `ods_${country_code}.ods_cis_corp_vend_master` | many:1 | `vx.vend_no = vm3.vend_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_vend_master_etc` | many:1 | `vm.vend_no = vme.vend_no` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `temp_vendor_xref` | many:1 | `vm.vend_no = vx3.vend_no and vx3.xref_type='DIVS'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `temp_vendor_xref` | `dim_${country_code}.dim_pub_list_box_detail` | many:1 | `lbd.code_value = cast(vx3.xref_no as string) and lbd.list_box_code='DIVS' and activeflag='Y'` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `temp_vend_master_etc` | `ods_${country_code}.ods_cis_corp_vendor_segment` | many:1 | `vme.seg_code = vseg.seg_code` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |
| `ods_${country_code}.ods_cis_corp_vend_master` | `ods_${country_code}.ods_cis_corp_v_vend_etc` | many:1 | `vm.vend_no = vetc.vend_no ;` | etl_sql (source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:1) |

`source/ref/vendor/table relationship.txt`: Not documented in repository.

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `vm.vend_no` | `vend_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:79` |
| `vend_name` | `vm.vend_name` | `vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:80` |
| `primary_loc` | `vm.primary_loc` | `primary_loc` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:81` |
| `pay_to_loc` | `vm.pay_to_loc` | `pay_to_loc` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:82` |
| `purchase_loc` | `vm.purchase_loc` | `purchase_loc` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:83` |
| `entry_datetime` | `vm.entry_datetime` | `entry_datetime` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:84` |
| `entry_id` | `vm.entry_id` | `entry_id` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:85` |
| `discontinued` | `vm.discontinued` | `discontinued` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:86` |
| `restricted` | `vm.restricted` | `restricted` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:87` |
| `vend_type` | `vm.vend_type` | `vend_type` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:88` |
| `buyer_no` | `vm.buyer_no` | `buyer_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:89` |
| `rma_rep` | `vm.rma_rep` | `rma_rep` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:90` |
| `ap_clerk` | `vm.ap_clerk` | `ap_clerk` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:91` |
| `tolerance` | `vm.tolerance` | `tolerance` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:92` |
| `po_type` | `vm.po_type` | `po_type` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:93` |
| `vend_pay_frt` | `vm.vend_pay_frt` | `vend_pay_frt` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:94` |
| `fob` | `vm.fob` | `fob` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:95` |
| `stock_rotation` | `vm.stock_rotation` | `stock_rotation` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:96` |
| `restock_fee` | `vm.restock_fee` | `restock_fee` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:97` |
| `ship_method` | `vm.ship_method` | `ship_method` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:98` |
| `freight` | `vm.freight` | `freight` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:99` |
| `vend_category` | `vm.vend_category` | `vend_category` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:100` |
| `ap_hold_flag` | `vm.ap_hold_flag` | `ap_hold_flag` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:101` |
| `company_no` | `vm.company_no` | `company_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:102` |
| `universal_vend_no` | `vp.universal_vend_no` | `universal_vend_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:103` |
| `universal_vend_name` | `vp.universal_vend_name` | `universal_vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:104` |
| `master_vend_flag` | `case when vx.xref_no = vm.vend_no and vx.vend_no is not null then 'Y' else 'N' end` | `xref_no`, `vend_no`, `Y`, `N` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:72` |
| `master_vend_no` | `vx.xref_no` | `xref_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:106` |
| `vend_company` | `vp.vend_company` | `vend_company` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:110` |
| `vend_currency` | `vc.vend_currency` | `vend_currency` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:111` |
| `vend_segment` | `vp.vend_segment` | `vend_segment` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:112` |
| `pas_code` | `vp.pas_code` | `pas_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:113` |
| `etl_timestamp` | `from_utc_timestamp(current_timestamp(),'America/Los_Angeles')` | `from_utc_timestamp`, `current_timestamp`, `America`, `Los_Angeles` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | arithmetic | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:114` |
| `vend_consign_flag` | `nvl(vp2.profile_c,'N')` | `profile_c`, `N` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | coalesce | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:115` |
| `pur_vend_no` | `vx2.xref_no pur_vend_no` | `xref_no`, `pur_vend_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | partial | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:116` |
| `pur_vend_name` | `vm2.vend_name pur_vend_name` | `vend_name`, `pur_vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | partial | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:117` |
| `master_vend_name` | `vm3.vend_name` | `vend_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:118` |
| `smb_vend_image_flag` | `case when svic.vend_no is not null then 'Y' else 'N' end` | `vend_no`, `Y`, `N` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:119` |
| `n_comp_brp_flag` | `case when vp.n_comp_brp_flag is not null then 1 else 0 end` | `n_comp_brp_flag` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | case | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:120` |
| `vend_seg_code` | `vp.vend_seg_code` | `vend_seg_code` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:121` |
| `prefix` | `vme.prefix` | `prefix` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:68` |
| `diversity_status` | `vx3.xref_no` | `xref_no` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:123` |
| `diversity_status_desc` | `lbd.code_desc` | `code_desc` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:124` |
| `vend_seg_name` | `vseg.seg_name` | `seg_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | rename | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:125` |
| `cis_mk_name` | `vp.cis_mk_name` | `cis_mk_name` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:126` |
| `vend_rank` | `vp.vend_rank` | `vend_rank` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:127` |
| `vend_pay_frt_amt` | `vme.vend_pay_frt_amt` | `vend_pay_frt_amt` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:69` |
| `discont_pur` | `vme.discont_pur` | `discont_pur` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:70` |
| `vend_terms` | `vetc.vend_terms` | `vend_terms` | `ods_${country_code}.ods_cis_corp_vend_master`, `temp_corp_vendor_profile`, `temp_vendor_xref`, `temp_vend_currency`, `ods_${country_code}.ods_cis_corp_vendor_profile`, `ods_${country_code}.ods_cis_corp_vendor_xref`, `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config`, `temp_vend_master_etc`, `dim_${country_code}.dim_pub_list_box_detail`, `ods_${country_code}.ods_cis_corp_vendor_segment`, `ods_${country_code}.ods_cis_corp_v_vend_etc` | passthrough | `source/etl/sql/vendor/public_order_scripts/public_vendor_dimension/script/dim_pub_vendor_info.sql:130` |

### Sentinel and code values
None identified in repository

---

## L4 Validation

### Resolved partition value
| Step | Source | How partition / date scope is determined |
|------|--------|------------------------------------------|
| 1 | evidence script / flow | See parameters in L1 Freshness and L3 filters - `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql` |

**Plain language:** Partition and date scope follow Azkaban/bootstrap parameters documented in the source script and orchestrating flow; do not hardcode calendar literals.

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) Row count by partition
SELECT ${partition_col}, COUNT(*) AS row_cnt
FROM dim_${country_code}.dim_pub_vendor_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${partition_col};

-- 2) Metric sum by business dimension (top deltas)
SELECT ${dim_key}, SUM(${metric}) AS metric_sum
FROM dim_${country_code}.dim_pub_vendor_info
WHERE ${partition_col} = '${partition_value}'
GROUP BY ${dim_key}
ORDER BY ABS(SUM(${metric})) DESC
LIMIT 20;

-- 3) Grain duplicate check
SELECT ${grain_key_1}, ${grain_key_2}, ${grain_key_3}, ${partition_col}, COUNT(*) AS cnt
FROM dim_${country_code}.dim_pub_vendor_info
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
| **Query for reporting** | *See script lineage* | `dim_${country_code}.dim_pub_vendor_info` | *Verify from flow* | *Add flow file:line* | pending |
| **Hive alternative** | `*` | `dim_${country_code}.dim_pub_vendor_info` | - | *See dependencies* | - |
| **ETL internal** | staging/temp tables | *Not synced to Vertica* | - | *See step-by-step logic* | - |

Business users should query `dim_${country_code}.dim_pub_vendor_info` in Vertica once MCP verification is completed for this document.

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
| `ods_${country_code}.ods_cis_corp_vendor_profile` | Profile rollups + consignment flag enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:36`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:144-148` |
| `ods_${country_code}.ods_cis_corp_vendor_xref` | Latest SRef/DIVS xref + VEND_PURCH linkage | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:50-54`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:14

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dim_${country_code}.dim_pub_vendor_info
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)
| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_cis_corp_vendor_profile` | Profile rollups + consignment flag enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:36`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:144-148` |
| `ods_${country_code}.ods_cis_corp_vendor_xref` | Latest SRef/DIVS xref + VEND_PURCH linkage | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:50-54`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:149-154` |
| `ods_${country_code}.ods_cis_corp_v_vend_currency` | Vendor currency enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:61-62` |
| `ods_${country_code}.ods_cis_corp_vend_master_etc` | Segment/prefix/freight/discontinued purchase attributes | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:71-72`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:162-164` |
| `ods_${country_code}.ods_cis_corp_vend_master` | Base vendor grain + purchaser and master vendor names | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:132`, `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:155-159` |
| `ods_gbl.ods_daas_mygbldaas_smb_vend_image_config` | SMB image flag source | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:160` |
| `dim_${country_code}.dim_pub_list_box_detail` | Diversity status description lookup | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:169-173` |
| `ods_${country_code}.ods_cis_corp_vendor_segment` | Segment name lookup | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:174-175` |
| `ods_${country_code}.ods_cis_corp_v_vend_etc` | Vendor terms enrichment | `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:176-177` |

### Downstream consumers (verified)
| Object / script | Evidence |
|-----------------|----------|
| Not documented in repository | No downstream consumer reference is present in this script |

### Operational detail (verified)
- Load mode is full-table overwrite into `dim_${country_code}.dim_pub_vendor_info` via `insert overwrite` (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:76-77`).
- Runtime ETL timestamp is generated in Pacific timezone (`source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql:114`).
- Partition strategy is not specified in this script (no partition clause in the target write statement).

### Not documented in repository
- Owner
- Schedule / cadence
- SLA / alerting policy
- Explicit downstream report/job dependencies

### Related scripts (verified)
- Not documented in repository (no explicit related script path/name is referenced in this SQL).

---

---

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/vendor/source/etl/flows/public_order_tools/ingest/public_vendor_dimension/script/dim_pub_vendor_info.sql`.*
