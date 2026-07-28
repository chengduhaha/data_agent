# DWD: Distributor Common Sales Detail Daily (`dw_${country_code}.dwd_disty_common_sales_detail_di`)

- artifact_type: etl_table
- artifact_id: dw_${country_code}.dwd_disty_common_sales_detail_di
- domain: order
- one_line_purpose: This job builds an enriched sales-line fact used by reporting and downstream sync jobs. It takes single-order sales lines and adds vendor, part, customer, location, and order-header context so downstream users can query one table instead of...
- layer_type: DWD
- source_kind: etl_sql
- evidence_source: source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql

---

## L1 Data Foundation

### Identity and physical mapping
- **Table:** `dw_${country_code}.dwd_disty_common_sales_detail_di`
- **Layer type:** DWD
- **Canonical / derived:** Derived / ETL-loaded (see L3)
- **Owner team:** not registered in metadata catalog

### Grain, scope, exclusions
- **Grain:** one row per shipped order line per date partition.
- **Scope:** See L2 business purpose / L3 filters
- **Partition:** `date_flag` (resolved from runtime date-window parameters; see **Resolved partition value**). - resolved from pipeline (see L4)
- **Natural key:** `order_type`, `order_no`, `order_line_no`.
- **Exclusions:** Not documented in repository

#### Grain detail (preserved)

- **Grain:** one row per shipped order line per date partition.
- **Partition:** `date_flag` (resolved from runtime date-window parameters; see **Resolved partition value**).
- **Natural key:** `order_type`, `order_no`, `order_line_no`.

---

### Cross-engine presence
| Engine | Present | Canonical FQN | Notes |
|--------|---------|---------------|-------|
| Hive | yes | `dw_${country_code}.dwd_disty_common_sales_detail_di` | ETL target / intermediate per evidence script |
| Vertica | pending | `dw_${country_code}.dwd_disty_common_sales_detail_di` | Confirm via hive2vertica flow evidence / MCP |

### Physical schema reference

Pointer block only - full column catalog lives in WKB L1 storage JSON.

| Field | Value |
|-------|-------|
| **Authoritative catalog** | WKB L1 storage seed (not duplicated in this file) |
| **entity_id** | `dw_${country_code}.dwd_disty_common_sales_detail_di` |
| **l1_catalog_seed** | `target/storage/wkb/snapshots/_snapshot_id_template/l1_catalog/{engine}_{schema}_{table}.json` |
| **column_count** | pending (run ddl_seed_writer) |
| **partition_keys** | `date_flag` |
| **ddl_source** | pending Bitbucket DDL / Vertica metadata ingest |
| **retrieval** | `python -m tools.wkb.indexing.run_query --query "order dwd_disty_common_sales_detail_di schema" --intent find_table_schema` |

### Lineage
| Object | Role |
|--------|------|
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | Main ETL source for line-level sales rows |
| `ods_${country_code}.ods_etl_order_exp_all` | Expense aggregate source |
| `dim_${country_code}.dim_pub_vendor_info` | Vendor enrichment |
| `dim_${country_code}.dim_pub_part_info` | Part/product enrichment |
| `dim_${country_code}.dim_pub_customer_info` | Customer enrichment |
| `ods_${country_code}.ods_cis_corp_from_ref_type` | Order ref type description |
| `ods_${country_code}.ods_cis_corp_history_header` | Header/ship-to/currency enrichment |
| `ods_${country_code}.ods_cis_corp_location_info` | Location enrichment |
| `ods_${country_code}.ods_etl_order_detail_date_all` | FX cost and FX price |
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | Base table for sync view DDL |
| `ods_us.ods_cis_corp_order_type` | View DDL lookup |
| `dim_us.dim_pub_part_info` | View DDL lookup |
| `dim_us.dim_pub_vpl_info` | View DDL lookup |
| `ods_us.ods_cis_corp_terms_file` | View DDL lookup |
| `ods_us.ods_cis_corp_history_detail` | View DDL lookup |

---

### Freshness and load path
| Item | Value |
|------|-------|
| Load pattern | See L3 end-to-end / INSERT pattern in evidence script |
| Schedule | Not documented in repository |
| Parameters | `country_code`, `start_date`, `end_date` |


---

## L2 Declarative Knowledge

### Business purpose
This job builds an enriched sales-line fact used by reporting and downstream sync jobs. It takes single-order sales lines and adds vendor, part, customer, location, and order-header context so downstream users can query one table instead of stitching many sources. It also computes net unit prices in domestic and foreign-currency contexts and publishes the result for Vertica and Snowflake sync flows.

---

### Audience and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Sales analytics** | Uses line-level price/quantity and customer hierarchy fields for revenue and mix analysis. |
| **Finance / FP&A** | Uses domestic and FX net price columns for margin and pricing views. |
| **Operations** | Uses ship-to, location, and order-reference attributes for fulfillment/channel analysis. |
| **Data consumers (BI / exports)** | Receives a single denormalized table that is also synced to Vertica and Snowflake. |

---

### Fact key resolution
- Natural key: `order_type`, `order_no`, `order_line_no`.
- FK / label-on attributes: see L3 dimension join patterns and step-by-step logic.
- Negative assertion: do not treat descriptive labels as grain keys unless listed under natural key.

### Time field semantics
- **date_flag / partition columns:** `date_flag` (resolved from runtime date-window parameters; see **Resolved partition value**).
- Primary reporting filter should use the partition column(s) documented in L1; resolve values via L4.



### Metrics served

| Category | Column | Logical metric | Business reading |
|----------|--------|----------------|------------------|
| Measures | — | — | No measure columns mapped for this table. |

### Metric serving map

**Formula authority:** [`source/contracts/order/metric-index.md`](../../source/contracts/order/metric-index.md)

N/A — no measure columns mapped for this table.

### etl_metrics

No governed logical metrics from `source/contracts/order/metric-index.md` are mapped on this table.

---

### Metric serving map
N/A - not a `*_comb_mtd` / multi-period wide serving table (or map not present in legacy doc).


### Data products and column groups (preserved)

### Identifiers and relationships

- **Order line:** `order_type`, `order_no`, `order_line_no`
- **Vendor:** `vend_no`, `vend_name`, `universal_vend_no`, `universal_vend_name`
- **Product:** `sku_no`, `part_no`, `mfg_partno`, `family`, `category`
- **Customer:** `cust_no`, `cust_name`, `master_cust_no`, `master_cust_name`

### Dimension columns (reporting-ready, pre-computed from source)

- `from_ref_type`, `from_ref_type_desc` — order channel/type code and description.
- `from_loc_no`, `loc_name` — source location and description.
- `ship_to_*` columns — standardized ship-to address attributes.
- `cust_terr`, `terms`, `company_no`, `order_entry_datetime`.

### Quantity, pricing, and cost building blocks

- `ship_qty`, `u_price`, `u_cost`.
- `base_cost` (from part dimension `po_cost`).
- `fx_u_cost`, `fx_u_price`, `fx_currency`.

### Core derived metrics

| Column | Formula | Business reading |
|--------|---------|-----------------|
| `net_u_price` | `a.u_price + a.u_sum_expense` | Domestic net unit price including unit expense component. |
| `fx_net_u_price` | `nvl(oda.foreign_price,0) + nvl(uue.usd_unit_exp,0)` | FX-side net unit price including aggregated line expense. |

---

### etl_metrics

#### `net_u_price`
- **Source:** [metric-index.md](../../source/contracts/order/metric-index.md#net_u_price)
- **Business definition:** Domestic net unit price including unit expense component.
```sql
a.u_price + a.u_sum_expense
```

#### `fx_net_u_price`
- **Source:** [metric-index.md](../../source/contracts/order/metric-index.md#fx_net_u_price)
- **Business definition:** FX-side net unit price including aggregated line expense.
```sql
nvl(oda.foreign_price,0) + nvl(uue.usd_unit_exp,0)
```

#### `usd_unit_exp`
- **Source:** [metric-index.md](../../source/contracts/order/metric-index.md#usd_unit_exp)
- **Business definition:** Total expense component per order line.
```sql
sum(usd_unit_exp)
```

#### `ods__country_code_ods_etl_order_detail_date_all_oda`
- **Source:** [metric-index.md](../../source/contracts/order/metric-index.md#ods__country_code_ods_etl_order_detail_date_all_oda)
- **Business definition:** Add FX cost/price.
```sql
a.order_no/type/line_no = oda.order_no/type/line_no
```

#### `temp_usd_unit_exp_uue`
- **Source:** [metric-index.md](../../source/contracts/order/metric-index.md#temp_usd_unit_exp_uue)
- **Business definition:** Add aggregated expense.
```sql
a.order_no/type/line_no = uue.order_no/type/line_no
```


---

## L3 Procedural Knowledge

### Query and routing rules
**Business filters:** Use partition / date keys from L1 grain for reporting scope.
**Technical predicates (load only):** See Key filters and step-by-step logic below.

### Dimension join patterns
| Dimension FQN | Join keys | Purpose | Evidence |
|---------------|-----------|---------|----------|
| See step-by-step / base tables | See L3 steps | Dimension enrichment | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql` |

### Key filters and ETL business logic
### Step 1 -- `temp_usd_unit_exp`

**Source:** `ods_${country_code}.ods_etl_order_exp_all`

**Filter (natural language):**
- No row-level filter in this step; all rows are grouped by order-line keys.

**What happens to columns:**
- Group by `order_type`, `order_no`, `order_line_no`.
- Aggregate `sum(usd_unit_exp)` into one value per order line.

**Derived columns in this step:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `usd_unit_exp` | `sum(usd_unit_exp)` | Total expense component per order line. |

---

### Step 2 -- Final `INSERT` into `dw_${country_code}.dwd_disty_common_sales_detail_di`

**From:** `dw_${country_code}.dwd_disty_sales_single_orders_di a`

**Filter (natural language):**
- `a.date_flag >= '${start_date}' and a.date_flag < '${end_date}'`
- `a.order_type > 0`
- `a.ship_qty <> 0`
- `terr_status = 'n'`

**Left joins on insert:**

| Join | Keys | Purpose |
|------|------|---------|
| `dim_${country_code}.dim_pub_vendor_info b` | `a.vend_no = b.vend_no` | Add vendor name. |
| `dim_${country_code}.dim_pub_part_info c` | `a.sku_no = c.sku_no` | Add product and cost attributes. |
| `dim_${country_code}.dim_pub_customer_info d` | `a.cust_no = d.cust_no` | Add customer and master customer names. |
| `ods_${country_code}.ods_cis_corp_from_ref_type frt` | `a.from_ref_type = frt.from_ref_type` | Add ref-type description. |
| `ods_${country_code}.ods_cis_corp_history_header h` | `a.order_no = h.order_no and a.order_type = h.order_type` ...

### Standard time-filter SQL
```sql
-- relative period filter using resolved partition value (see L4)
SELECT *
FROM dw_${country_code}.dwd_disty_common_sales_detail_di
WHERE /* partition predicate */ date_flag = '${partition_value}';
```

### End-to-end flow
**Runtime parameters:** `country_code`, `start_date`, `end_date`  
**Target table:** `dw_${country_code}.dwd_disty_common_sales_detail_di`, partitioned by **`date_flag`**.

1. Aggregate `ods_etl_order_exp_all` into `temp_usd_unit_exp` by order line.
2. Read `dwd_disty_sales_single_orders_di` for the runtime date window and business filters.
3. Left-join dimensions/lookups and FX detail tables.
4. Compute net price columns and write target partition.
5. Flow sync jobs read `dw_${country_code}.dwd_disty_common_sales_detail_di_view` and publish to Vertica/Snowflake.

```mermaid
flowchart LR
  subgraph src [Source tables]
    S1[dw_${country_code}.dwd_disty_sales_single_orders_di]
    S2[ods_${country_code}.ods_etl_order_exp_all]
    S3[dim_${country_code}.dim_pub_vendor_info]
    S4[dim_${country_code}.dim_pub_part_info]
    S5[dim_${country_code}.dim_pub_customer_info]
    S6[ods_${country_code}.ods_cis_corp_from_ref_type]
    S7[ods_${country_code}.ods_cis_corp_history_header]
    S8[ods_${country_code}.ods_cis_corp_location_info]
    S9[ods_${country_code}.ods_etl_order_detail_date_all]
  end
  S2 --> T0[temp_usd_unit_exp]
  S1 --> T1[enriched select]
  S3 --> T1
  S4 --> T1
  S5 --> T1
  S6 --> T1
  S7 --> T1
  S8 --> T1
  S9 --> T1
  T0 --> T1
  T1 --> T2[INSERT OVERWRITE dwd_disty_common_sales_detail_di]

  subgraph view [Permanent view for sync]
    V1[dwd_disty_common_sales_detail_di_view]
  end

  T2 --> V1
  S10[dw_us.dwd_disty_pub_dw_orders_extend_di] --> V1
  S11[ods_us.ods_cis_corp_order_type] --> V1
  S12[dim_us.dim_pub_part_info] --> V1
  S13[dim_us.dim_pub_vpl_info] --> V1
  S14[ods_us.ods_cis_corp_location_info] --> V1
  S15[ods_us.ods_cis_corp_terms_file] --> V1
  S16[ods_us.ods_cis_corp_history_header] --> V1
  S17[ods_us.ods_cis_corp_history_detail] --> V1
  V1 --> OUT[Vertica/Snowflake sync query source]
```

---


#### High-level stages (preserved)

| Stage | Business meaning |
|-------|-----------------|
| **Expense pre-aggregation** | Summarizes order-line expenses into one row per `(order_type, order_no, order_line_no)` for net price calculation. |
| **Sales-line filter** | Reads territory-normalized, non-zero-quantity lines inside the runtime date window. |
| **Dimension enrichment** | Joins vendor, part, customer, order header, location, and reference-type lookups. |
| **Price derivation and publish** | Computes net prices, writes partitioned Hive table, then flow-level sync jobs read from a permanent view for Vertica/Snowflake. |

**Parameters:** `country_code`, `start_date`, `end_date`

---


### Base tables register
| Object | Role in this job |
|--------|-----------------|
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | Primary sales-line source and partition/date filter driver. |
| `ods_${country_code}.ods_etl_order_exp_all` | Expense source used to build temp expense aggregate. |
| `dim_${country_code}.dim_pub_vendor_info` | Vendor-name enrichment. |
| `dim_${country_code}.dim_pub_part_info` | Part attributes and base cost enrichment. |
| `dim_${country_code}.dim_pub_customer_info` | Customer and master-customer enrichment. |
| `ods_${country_code}.ods_cis_corp_from_ref_type` | Order reference type description lookup. |
| `ods_${country_code}.ods_cis_corp_history_header` | Ship-to, currency, and order entry datetime enrichment. |
| `ods_${country_code}.ods_cis_corp_location_info` | Source location name lookup. |
| `ods_${country_code}.ods_etl_order_detail_date_all` | Foreign cost/price enrichment. |
| `dw_us.dwd_disty_common_sales_detail_di_view` | Permanent view (see DDL) used as sync source for downstream publish jobs. |

**Temporary tables (inside the job only):**  
`temp_usd_unit_exp` -> final `INSERT`

---

### Step-by-step logic
### Step 1 -- `temp_usd_unit_exp`

**Source:** `ods_${country_code}.ods_etl_order_exp_all`

**Filter (natural language):**
- No row-level filter in this step; all rows are grouped by order-line keys.

**What happens to columns:**
- Group by `order_type`, `order_no`, `order_line_no`.
- Aggregate `sum(usd_unit_exp)` into one value per order line.

**Derived columns in this step:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `usd_unit_exp` | `sum(usd_unit_exp)` | Total expense component per order line. |

---

### Step 2 -- Final `INSERT` into `dw_${country_code}.dwd_disty_common_sales_detail_di`

**From:** `dw_${country_code}.dwd_disty_sales_single_orders_di a`

**Filter (natural language):**
- `a.date_flag >= '${start_date}' and a.date_flag < '${end_date}'`
- `a.order_type > 0`
- `a.ship_qty <> 0`
- `terr_status = 'n'`

**Left joins on insert:**

| Join | Keys | Purpose |
|------|------|---------|
| `dim_${country_code}.dim_pub_vendor_info b` | `a.vend_no = b.vend_no` | Add vendor name. |
| `dim_${country_code}.dim_pub_part_info c` | `a.sku_no = c.sku_no` | Add product and cost attributes. |
| `dim_${country_code}.dim_pub_customer_info d` | `a.cust_no = d.cust_no` | Add customer and master customer names. |
| `ods_${country_code}.ods_cis_corp_from_ref_type frt` | `a.from_ref_type = frt.from_ref_type` | Add ref-type description. |
| `ods_${country_code}.ods_cis_corp_history_header h` | `a.order_no = h.order_no and a.order_type = h.order_type` | Add ship-to, currency, entry datetime. |
| `ods_${country_code}.ods_cis_corp_location_info loc` | `a.from_loc_no = loc.loc_no` | Add location name. |
| `ods_${country_code}.ods_etl_order_detail_date_all oda` | `a.order_no/type/line_no = oda.order_no/type/line_no` | Add FX cost/price. |
| `temp_usd_unit_exp uue` | `a.order_no/type/line_no = uue.order_no/type/line_no` | Add aggregated expense. |

**Derived columns computed at INSERT:**

| Column | Formula | Plain language |
|--------|---------|----------------|
| `net_u_price` | `a.u_price + a.u_sum_expense` | Net domestic unit price. |
| `fx_net_u_price` | `nvl(oda.foreign_price,0)+nvl(uue.usd_unit_exp,0)` | Net FX unit price plus expense. |
| `base_cost` | `c.po_cost` | Base part cost from part dimension. |
| `order_entry_datetime` | `h.entry_datetime` | Order-entry timestamp. |

### Step 2.1 -- view `dw_us.dwd_disty_common_sales_detail_di_view` pre-computation (for downstream sync)

**Source:** `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql`

**What happens in the view:**
- Reads `dw_us.dwd_disty_pub_dw_orders_extend_di` as the base row set.
- Joins `ods_us.ods_cis_corp_order_type`, `dim_us.dim_pub_part_info`, `dim_us.dim_pub_vpl_info`, `ods_us.ods_cis_corp_location_info`, `ods_us.ods_cis_corp_terms_file`, `ods_us.ods_cis_corp_history_header`, and `ods_us.ods_cis_corp_history_detail`.
- Derives reporting aliases and extended metrics such as `ext_unit_price`, `ext_net_price`, `opl_amt`, `ngm_amt`.
- Applies business filters `dw.order_type > 0` and `dw.ship_qty <> 0`.

---

### Relationship map (embedded)

| from_fqn | to_fqn | cardinality | join_keys | provenance |
|----------|--------|-------------|-----------|------------|
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `dim_${country_code}.dim_pub_vendor_info` | many:1 (LEFT) | `a.vend_no` = `b.vend_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:59`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `dim_${country_code}.dim_pub_part_info` | many:1 (LEFT) | `a.sku_no` = `c.sku_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:60`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `dim_${country_code}.dim_pub_customer_info` | many:1 (LEFT) | `a.cust_no` = `d.cust_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:61`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `ods_${country_code}.ods_cis_corp_from_ref_type` | many:1 (LEFT) | `a.from_ref_type` = `frt.from_ref_type` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:62`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `ods_${country_code}.ods_cis_corp_history_header` | many:1 (LEFT) | `a.order_no` = `h.order_no`; `a.order_type` = `h.order_type` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:63`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `ods_${country_code}.ods_cis_corp_location_info` | many:1 (LEFT) | `a.from_loc_no` = `loc.loc_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:64`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `ods_${country_code}.ods_etl_order_detail_date_all` | many:1 (LEFT) | `a.order_no` = `oda.order_no`; `a.order_type` = `oda.order_type`; `a.order_line_no` = `oda.order_line_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:65`) |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | `temp_usd_unit_exp` | many:1 (LEFT) | `a.order_no` = `uue.order_no`; `a.order_type` = `uue.order_type`; `a.order_line_no` = `uue.order_line_no` | etl_sql (`source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:69`) |

### Special logic (embedded)

Not documented in repository

### Column / field derivations (from ETL SQL)

| target_column | expression_sql | upstream_columns | upstream_tables | transform_kind | evidence |
|---------------|----------------|------------------|-----------------|----------------|----------|
| `vend_no` | `a.vend_no` | `vend_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:16` |
| `vend_name` | `b.vend_name` | `vend_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:17` |
| `universal_vend_no` | `c.universal_vend_no` | `universal_vend_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:18` |
| `universal_vend_name` | `c.universal_vend_name` | `universal_vend_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:19` |
| `sku_no` | `a.sku_no` | `sku_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:20` |
| `part_no` | `c.part_no` | `part_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:21` |
| `mfg_partno` | `c.mfg_partno` | `mfg_partno` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:22` |
| `weight` | `c.weight` | `weight` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:23` |
| `base_cost` | `c.po_cost` | `po_cost` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:24` |
| `family` | `c.family` | `family` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:25` |
| `category` | `c.category` | `category` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:26` |
| `cust_no` | `a.cust_no` | `cust_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:27` |
| `cust_name` | `d.cust_name` | `cust_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:28` |
| `master_cust_no` | `d.mcust_no` | `mcust_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:29` |
| `master_cust_name` | `d.mcust_name` | `mcust_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:30` |
| `ship_qty` | `a.ship_qty` | `ship_qty` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:31` |
| `u_price` | `a.u_price` | `u_price` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:32` |
| `u_cost` | `a.u_cost` | `u_cost` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:33` |
| `net_u_price` | `a.u_price+a.u_sum_expense` | `u_price`, `u_sum_expense` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | arithmetic | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:34` |
| `order_no` | `a.order_no` | `order_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:35` |
| `order_type` | `a.order_type` | `order_type` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:36` |
| `order_line_no` | `a.order_line_no` | `order_line_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:37` |
| `from_ref_type` | `a.from_ref_type` | `from_ref_type` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:38` |
| `from_ref_type_desc` | `frt.from_ref_type_desc` | `from_ref_type_desc` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:39` |
| `ship_to_name` | `h.ship_to_name` | `ship_to_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:40` |
| `ship_to_addr` | `h.ship_to_addr` | `ship_to_addr` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:41` |
| `ship_to_po_box` | `h.ship_to_po_box` | `ship_to_po_box` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:42` |
| `ship_to_city` | `h.ship_to_city` | `ship_to_city` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:43` |
| `ship_to_state` | `h.ship_to_state` | `ship_to_state` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:44` |
| `ship_to_country` | `h.ship_to_country` | `ship_to_country` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:45` |
| `ship_to_zip` | `h.ship_to_zip` | `ship_to_zip` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:46` |
| `from_loc_no` | `a.from_loc_no` | `from_loc_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:47` |
| `loc_name` | `loc.loc_name` | `loc_name` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:48` |
| `fx_currency` | `h.fx_currency` | `fx_currency` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:49` |
| `cust_terr` | `a.cust_terr` | `cust_terr` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:50` |
| `fx_u_cost` | `oda.foreign_cost` | `foreign_cost` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:51` |
| `fx_u_price` | `oda.foreign_price` | `foreign_price` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:52` |
| `fx_net_u_price` | `nvl(oda.foreign_price,0)+nvl(uue.usd_unit_exp,0)` | `foreign_price`, `usd_unit_exp` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | coalesce | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:53` |
| `terms` | `a.terms` | `terms` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:54` |
| `company_no` | `a.company_no` | `company_no` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:55` |
| `order_entry_datetime` | `h.entry_datetime` | `entry_datetime` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | rename | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:56` |
| `date_flag` | `a.date_flag` | `date_flag` | `dw_${country_code}.dwd_disty_sales_single_orders_di`, `dim_${country_code}.dim_pub_vendor_info`, `dim_${country_code}.dim_pub_part_info`, `dim_${country_code}.dim_pub_customer_info`, `ods_${country_code}.ods_cis_corp_from_ref_type`, `ods_${country_code}.ods_cis_corp_history_header`, `ods_${country_code}.ods_cis_corp_location_info`, `ods_${country_code}.ods_etl_order_detail_date_all`, `temp_usd_unit_exp` | passthrough | `source/etl/sql/order/public_order_scripts/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:57` |

### Sentinel and code values
| Value | Meaning |
|-------|---------|
| `terr_status = 'n'` | Keep territory-normalized records only. |
| `order_type > 0` | Exclude non-positive order types. |
| `ship_qty <> 0` | Exclude non-shipped lines. |
| `nvl(...,0)` in net price formulas | Prevent null arithmetic from dropping line-level metric values. |

---

---

## L4 Validation

### Resolved partition value
#### Resolved partition value

| Step | Source | How `date_flag` is determined |
|------|--------|-------------------------------|
| 1 | Flow bootstrap node | Flow runs `gen_date_parameter` node pointing to `gen_date_m_parameter.sql` to emit runtime date parameters (`start_date`, `end_date`) used by this job — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:41-45` |
| 2 | ETL job parameter wiring | Main job passes `${start_date}`/`${end_date}` into script execution — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:105-114` |
| 3 | ETL SQL filter | Script filters source rows with `a.date_flag >= '${start_date}' and a.date_flag < '${end_date}'` and writes partition `date_flag` — `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:15,73-74` |
| 4 | Vertica sync query | Flow sync reads the view with the same date window (`date_flag >= '${start_date}' and date_flag < '${end_date}'`) — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:124` |

**Plain language:** each run processes and publishes the partition range from runtime `start_date` (inclusive) to `end_date` (exclusive), then exposes that same range through the sync view.

---

### Data quality checks
- Prefer row-count-by-partition, metric sums, and grain duplicate checks (see Validation SQL).
- Additional checks from legacy caveats / operational notes when present.

### Validation SQL
```sql
-- 1) row count by partition
-- SELECT partition_col, COUNT(*) FROM dw_${country_code}.dwd_disty_common_sales_detail_di WHERE partition_col = '${partition_value}' GROUP BY 1;
-- 2) metric sum by dimension (top N) - replace metric/dim from L2
-- 3) grain duplicate check on natural keys
```


### Caveats for interpretation
- Main ETL writes `dw_${country_code}.dwd_disty_common_sales_detail_di`, but flow-level external sync uses `dwd_disty_common_sales_detail_di_view` as source.
- View DDL in repository is country-specific (`dw_us...`), while ETL and flows are parameterized by `${country_code}`.
- Partition bootstrap SQL file (`gen_date_m_parameter.sql`) is referenced in flow but missing from this repository snapshot, so internal expression details are not directly verifiable here.

---

### Conflicts and open questions
- Schedule, owner, SLA: Not documented in repository (unless preserved schedule evidence above).
- Vertica MCP verification: pending unless confirmed in L5.



---

## L5 Runtime View

### Query path and engine preference
| Role | Hive object | Vertica object | Sync mode | Evidence | MCP verified |
|------|-------------|----------------|-----------|----------|--------------|
| Query for reporting | `dw_${country_code}.dwd_disty_common_sales_detail_di_view` | `dw_${country_code}.dwd_disty_common_sales_detail_di` | `overwrite` | `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:115-125` | pending (not verified in this run) |
| Hive alternative | `dw_${country_code}.dwd_disty_common_sales_detail_di_view` | same as reporting table (flow sync source) | - | `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:124` | - |
| ETL internal | `dw_${country_code}.dwd_disty_common_sales_detail_di` | Not synced directly (sync reads view) | - | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:15` | - |

Business users should query `dw_${country_code}.dwd_disty_common_sales_detail_di` in Vertica after environment-specific verification is completed.

---

### Access constraints
- Country / company schema parameters may apply (`literal_country`, `company_no`, etc.).
- Hive-only staging objects are not reporting surfaces unless synced.

### Query risk profile
| Field | Value |
|-------|-------|
| requires_date_predicate | yes |
| scan_risk_tier | high |

---

## L6 Access and Consumption

### Primary consumers and use cases
| Audience | How they benefit |
|----------|-----------------|
| **Sales analytics** | Uses line-level price/quantity and customer hierarchy fields for revenue and mix analysis. |
| **Finance / FP&A** | Uses domestic and FX net price columns for margin and pricing views. |
| **Operations** | Uses ship-to, location, and order-reference attributes for fulfillment/channel analysis. |
| **Data consumers (BI / exports)** | Receives a single denormalized table that is also synced to Vertica and Snowflake. |

---

### Representative query patterns
```sql
-- certified / illustrative lookup - replace predicates from L1/L4
SELECT *
FROM dw_${country_code}.dwd_disty_common_sales_detail_di
WHERE date_flag = '${partition_value}'
LIMIT 100;
```

### Dependencies and notes
### Upstream objects (verified)

| Object | Usage | Evidence |
|--------|-------|----------|
| `ods_${country_code}.ods_etl_order_exp_all` | Builds `temp_usd_unit_exp` | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:1-13` |
| `dw_${country_code}.dwd_disty_sales_single_orders_di` | Main source and row filters | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:58,73-77` |
| `dim_${country_code}.dim_pub_vendor_info` | Vendor enrichment | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:59` |
| `dim_${country_code}.dim_pub_part_info` | Part enrichment and `base_cost` | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:60` |
| `dim_${country_code}.dim_pub_customer_info` | Customer/master customer enrichment | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:61` |
| `ods_${country_code}.ods_cis_corp_from_ref_type` | Reference type description | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:62` |
| `ods_${country_code}.ods_cis_corp_history_header` | Ship-to/currency/entry datetime | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:63` |
| `ods_${country_code}.ods_cis_corp_location_info` | Location name | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:64` |
| `ods_${country_code}.ods_etl_order_detail_date_all` | FX cost/price | `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:65-68` |
| `dw_us.dwd_disty_pub_dw_orders_extend_di` | Base table in sync view DDL | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:68` |
| `ods_us.ods_cis_corp_order_type` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:69` |
| `dim_us.dim_pub_part_info` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:70` |
| `dim_us.dim_pub_vpl_info` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:71` |
| `ods_us.ods_cis_corp_location_info` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:72` |
| `ods_us.ods_cis_corp_terms_file` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:73` |
| `ods_us.ods_cis_corp_history_header` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:74` |
| `ods_us.ods_cis_corp_history_detail` | Sync view DDL join | `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql:75-78` |

### Downstream consumers (verified)

| Object / script | Evidence |
|-----------------|----------|
| `hive2vertica-overwrite-dwd_disty_common_sales_detail_di` sync job | `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:115-125` |
| `hive2snowflake-dwd_disty_common_sales_detail_di` sync job | `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:126-141` |

### Operational detail (verified)

- ETL writes with `insert overwrite ... partition (date_flag)` — `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql:15`.
- Flow injects `query.parameter.start_date` and `query.parameter.end_date` for ETL runtime window — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:112-114`.
- Vertica sync window uses same `date_flag >= '${start_date}' and date_flag < '${end_date}'` filter over the view — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:124`.

### Not documented in repository

- `public_order_dw/script/gen_date_m_parameter.sql` referenced by flow bootstrap is not present in this repository snapshot, so direct parameter derivation SQL is unavailable — `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:44`.
- Schedule owner and SLA owner mapping for this specific table are not documented at script level.

### Related scripts (verified)

- `source/etl/views/order/dwd_disty_common_sales_detail_di_view.sql` -- downstream sync source view DDL -- `source/etl/flows/public_order_tools/ingest/public_order_dw/public_order_dw_us_m.flow:124`.

---

*Document generated from `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql`.*

#### Not documented in repository
- Owner, SLA (unless schedule evidence preserved above)
- Any dependency without `file:line` evidence in this document

---

*Document migrated to L1-L6 from legacy Knowledgebase content. Evidence: `source/etl/sql/order/source/etl/flows/public_order_tools/ingest/public_order_dw/script/dwd_disty_common_sales_detail_di.sql`.*
