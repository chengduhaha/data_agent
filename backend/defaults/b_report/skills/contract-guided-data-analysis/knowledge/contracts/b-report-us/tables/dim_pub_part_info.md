# dim_us.dim_pub_part_info

- contract_version: v2.0.0
- artifact_type: table
- artifact_id: dim_us.dim_pub_part_info
- domain: b-report-us
- one_line_purpose: US product/part master — resolve `sku_no` from part numbers and enrich VPL/vendor hierarchy

## L1 Data Foundation

### Identity and Physical Mapping

- Table: `dim_us.dim_pub_part_info`
- Layer: DIM
- Canonical/Derived: Canonical dimension reference
- Owner team: not registered in metadata catalog
- Verified in Hive: yes
- Verified in Vertica: yes
- Canonical FQN: `dim_us.dim_pub_part_info`

### Grain, Scope, Exclusions

- Grain: dimension key level (one row per business key)
- Scope: US disty B Report shipped-order P&L and performance metrics.
- Exclusions: Non-US schemas, backup/temp table variants (`_bkp`, `_temp`), and non-shipped-order scenarios.

### Cross-Engine Presence

- Hive: `dim_us.dim_pub_part_info` verified present.
- Vertica: `dim_us.dim_pub_part_info` verified present.
- Row count (Vertica, 2026-06-25): 12,173,527 rows; `sku_no` unique at grain.
- Label cardinality: `part_no` 12,167,803 distinct; `mfg_partno` 10,181,609 distinct (non-unique labels expected).
- Snapshot variant: `dim_pub_part_info_df` partitioned by `date_flag` for as-of product attributes in B Report serving ETL.

### Column Catalog (100% columns)

- documented_column_count: 147
- catalog_status: complete

| column_name | data_type | nullable | default_value | ordinal_position | column_comment | semantic_role | business_definition | value_pattern_or_domain | quality_flags | enriched_explanation | dimension_reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sku_no | int | engine metadata not exposed | — | 1 | Synnex unique ID for each product distributed | key | sku no | integer | not_null_expected|dim_fk_check_recommended | sku no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| part_no | varchar(200) | engine metadata not exposed | — | 2 | Synnex Manually created ID for products. Generally includes a 3 character prefix for the vendor, then a dash character, then the manufacturers part number. Due to column width limitations, the manufacturers part number may be altered.. | key | part no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | part no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| short_desc | varchar(225) | engine metadata not exposed | — | 3 | Description of the product. This description appears on order screens, packing list, and invoices.  the short version of the long_desc in part_master table. | dimension | short desc | categorical_or_expression_text | domain_value_check_recommended | short desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| long_desc | varchar(2500) | engine metadata not exposed | — | 4 | Long description. | dimension | long desc | categorical_or_expression_text | domain_value_check_recommended | long desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| abc_code | varchar(4) | engine metadata not exposed | — | 5 | ABC code | dimension | abc code | categorical_or_expression_text | domain_value_check_recommended | abc code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| prod_code | int | engine metadata not exposed | — | 6 | Known as PM code and defined in the prod_code table. Old grouping of SKUs for reporting purposes. Use VPC code (vpl_no) | dimension | prod code | integer | domain_value_check_recommended | prod code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| prod_type | varchar(2) | engine metadata not exposed | — | 7 | Product type. | dimension | prod type | categorical_or_expression_text | domain_value_check_recommended | prod type; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| weight | numeric(19,4) | engine metadata not exposed | — | 8 | Gross product weight includes packaging for a single unit. | measure | weight | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | weight; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| cu_height | numeric(19,4) | engine metadata not exposed | — | 9 | Unit height | measure | cu height | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cu height; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| cu_width | numeric(19,4) | engine metadata not exposed | — | 10 | Unit width | measure | cu width | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cu width; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| cu_length | numeric(19,4) | engine metadata not exposed | — | 11 | Unit length | measure | cu length | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | cu length; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ser_no_flag | varchar(2) | engine metadata not exposed | — | 12 | Some part has ser_no, but some has not,system must read the field | dimension | ser no flag | categorical_or_expression_text | domain_value_check_recommended | ser no flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| avail_to_sell | varchar(2) | engine metadata not exposed | — | 13 | If this part is available for sell. | dimension | avail to sell | categorical_or_expression_text | domain_value_check_recommended | avail to sell; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| active_status | varchar(2) | engine metadata not exposed | — | 14 | The status of a product. A = Active, D = Discontinued/Deactivated, I = Inactive. | dimension | active status | categorical_or_expression_text | domain_value_check_recommended | active status; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| po_cost | numeric(19,4) | engine metadata not exposed | — | 15 | Base cost | measure | po cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | po cost; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_no | int | engine metadata not exposed | — | 16 | Synnex unique ID for each vendor as defined in vend_master table | key | vend no | integer | not_null_expected|dim_fk_check_recommended | vend no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vendor_info.vend_no` |
| upc_code | varchar(80) | engine metadata not exposed | — | 17 | UPC code, universal product code | dimension | upc code | categorical_or_expression_text | domain_value_check_recommended | upc code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| sug_retail_price | numeric(19,4) | engine metadata not exposed | — | 18 | Suggested retail price. MSRP. | measure | sug retail price | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | sug retail price; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| mfg_partno | varchar(240) | engine metadata not exposed | — | 19 | Manufacture part# | dimension | mfg partno | categorical_or_expression_text | domain_value_check_recommended | mfg partno; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| master_flag | varchar(2) | engine metadata not exposed | — | 20 | Flag identifying if this is a master sku. | dimension | master flag | categorical_or_expression_text | domain_value_check_recommended | master flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| model | varchar(191) | engine metadata not exposed | — | 21 | Model of the part | dimension | model | categorical_or_expression_text | domain_value_check_recommended | model; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vpl_no | int | engine metadata not exposed | — | 22 | Unique ID for VPC (Vendor Product Code) as defined in the dw_vend_pl table. | key | vpl no | integer | not_null_expected|dim_fk_check_recommended | vpl no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vpl_info.vpl_no` |
| usage_type | varchar(4) | engine metadata not exposed | — | 23 | Usage type. | dimension | usage type | categorical_or_expression_text | domain_value_check_recommended | usage type; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| category_id | int | engine metadata not exposed | — | 24 | Category ID | key | category id | integer | not_null_expected|dim_fk_check_recommended | category id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| series_no | int | engine metadata not exposed | — | 25 | series no | key | series no | integer | not_null_expected|dim_fk_check_recommended | series no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| accept_rma | varchar(2) | engine metadata not exposed | — | 26 | If this part accepts RMA | dimension | accept rma | categorical_or_expression_text | domain_value_check_recommended | accept rma; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| group_id | int | engine metadata not exposed | — | 27 | ID number for SKUs to identify what product category a SKU has been assigned to as defined in the part_cat table. | key | group id | integer | not_null_expected|dim_fk_check_recommended | group id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| uni_group_id | int | engine metadata not exposed | — | 28 | if(ods_cis_dbo_part_prod_cat.group_id is null, ods_cis_dbo_part_master.group_id,  ods_cis_dbo_part_prod_cat.group_id) | key | uni group id | integer | not_null_expected|dim_fk_check_recommended | uni group id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| family_id | int | engine metadata not exposed | — | 29 | This is the top level and we attempt to keep these unique values to less than 20 | key | family id | integer | not_null_expected|dim_fk_check_recommended | family id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| family | varchar(160) | engine metadata not exposed | — | 30 | A category description for the level family of the category structure. | dimension | family | categorical_or_expression_text | domain_value_check_recommended | family; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| cat_id | int | engine metadata not exposed | — | 31 | This is the middle level and we attempt to keep the unique values for each top level to less than 12 | key | cat id | integer | not_null_expected|dim_fk_check_recommended | cat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| category | varchar(160) | engine metadata not exposed | — | 32 | A category description for the level category of the category structure. | dimension | category | categorical_or_expression_text | domain_value_check_recommended | category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| subcat_id | int | engine metadata not exposed | — | 33 | The lowest level which is optional. Provides more detailed breakdown of the middle level, if desired. Should keep the number of values for any one middle level to less than 10 values. | key | subcat id | integer | not_null_expected|dim_fk_check_recommended | subcat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| sub_category | varchar(160) | engine metadata not exposed | — | 34 | A category description for the level sub category of the category structure. | dimension | sub category | categorical_or_expression_text | domain_value_check_recommended | sub category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_family_id | int | engine metadata not exposed | — | 35 | This is the top level from tc tables | key | tc family id | integer | not_null_expected|dim_fk_check_recommended | tc family id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_family | varchar(160) | engine metadata not exposed | — | 36 | A category description for the level family of the category structure,  from tc tables | dimension | tc family | categorical_or_expression_text | domain_value_check_recommended | tc family; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_cat_id | int | engine metadata not exposed | — | 37 | This is the middle level  from tc tables | key | tc cat id | integer | not_null_expected|dim_fk_check_recommended | tc cat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_category | varchar(160) | engine metadata not exposed | — | 38 | A category description for the level category of the category structure,  from tc tables | dimension | tc category | categorical_or_expression_text | domain_value_check_recommended | tc category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_subcat_id | int | engine metadata not exposed | — | 39 | The lowest level which is optional. Provides more detailed breakdown of the middle level, if desired. Should keep the number of values for any one middle level to less than 10 values,  from tc tables | key | tc subcat id | integer | not_null_expected|dim_fk_check_recommended | tc subcat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_sub_category | varchar(160) | engine metadata not exposed | — | 40 | A category description for the level sub category of the category structure,  from tc tables | dimension | tc sub category | categorical_or_expression_text | domain_value_check_recommended | tc sub category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vpl_code | varchar(200) | engine metadata not exposed | — | 41 | the code for one vpl | dimension | vpl code | categorical_or_expression_text | domain_value_check_recommended | vpl code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vpl_desc | varchar(200) | engine metadata not exposed | — | 42 | description for the vpl | dimension | vpl desc | categorical_or_expression_text | domain_value_check_recommended | vpl desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_name | varchar(200) | engine metadata not exposed | — | 43 | Name of the vendor | dimension | vend name | categorical_or_expression_text | domain_value_check_recommended | vend name; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_currency | varchar(200) | engine metadata not exposed | — | 44 | vend_currency | dimension | vend currency | categorical_or_expression_text | domain_value_check_recommended | vend currency; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_segment | varchar(200) | engine metadata not exposed | — | 45 | segment of the vendor | dimension | vend segment | categorical_or_expression_text | domain_value_check_recommended | vend segment; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| alt_vpl_no | int | engine metadata not exposed | — | 46 | vpl no. from dw_vend_pl, associated by vpl no from part_master | key | alt vpl no | integer | not_null_expected|dim_fk_check_recommended | alt vpl no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vpl_info.vpl_no` |
| alt_vpl_code | varchar(200) | engine metadata not exposed | — | 47 | the code for one vpl | dimension | alt vpl code | categorical_or_expression_text | domain_value_check_recommended | alt vpl code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| alt_vpl_desc | varchar(200) | engine metadata not exposed | — | 48 | description for the vpl | dimension | alt vpl desc | categorical_or_expression_text | domain_value_check_recommended | alt vpl desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| universal_vend_no | int | engine metadata not exposed | — | 49 | Holds any integer data | key | universal vend no | integer | not_null_expected|dim_fk_check_recommended | universal vend no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vendor_info.universal_vend_no` |
| universal_vend_name | varchar(200) | engine metadata not exposed | — | 50 | Holds any character data | dimension | universal vend name | categorical_or_expression_text | domain_value_check_recommended | universal vend name; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pur_end_date | timestamp | engine metadata not exposed | — | 51 | Purchase comments effective date | dimension | pur end date | categorical_or_expression_text | domain_value_check_recommended | pur end date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| catalog_desc | varchar(510) | engine metadata not exposed | — | 52 | Catalog description | dimension | catalog desc | categorical_or_expression_text | domain_value_check_recommended | catalog desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ave_cost | numeric(19,4) | engine metadata not exposed | — | 53 | The product cost which sometimes include expenses for freight and import fees. This is the cost used for sales and is not necessarily the price we paid for the product | measure | ave cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | ave cost; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| std_cost | numeric(19,4) | engine metadata not exposed | — | 54 | Standard cost | measure | std cost | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | std cost; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| cost_meth | varchar(200) | engine metadata not exposed | — | 55 | Cost method. Not in use | dimension | cost meth | categorical_or_expression_text | domain_value_check_recommended | cost meth; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| entry_datetime | timestamp | engine metadata not exposed | — | 56 | Date record was inserted to table. NEVER update this column!! | dimension | entry datetime | categorical_or_expression_text | domain_value_check_recommended | entry datetime; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| entry_id | int | engine metadata not exposed | — | 57 | User ID of who inserted record into table. NEVER update this column!! | key | entry id | integer | not_null_expected|dim_fk_check_recommended | entry id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| entry_name | varchar(200) | engine metadata not exposed | — | 58 | The first name  and last name of the employee | dimension | entry name | categorical_or_expression_text | domain_value_check_recommended | entry name; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| production_flag | varchar(200) | engine metadata not exposed | — | 59 | If this part has to go to production line | dimension | production flag | categorical_or_expression_text | domain_value_check_recommended | production flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pur_comment | varchar(510) | engine metadata not exposed | — | 60 | Purchase comments | dimension | pur comment | categorical_or_expression_text | domain_value_check_recommended | pur comment; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| mar_comment | varchar(510) | engine metadata not exposed | — | 61 | Marketing comments | dimension | mar comment | categorical_or_expression_text | domain_value_check_recommended | mar comment; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| mar_end_date | timestamp | engine metadata not exposed | — | 62 | Marketing comments effective until | dimension | mar end date | categorical_or_expression_text | domain_value_check_recommended | mar end date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| shortage | varchar(200) | engine metadata not exposed | — | 63 | Allocated | dimension | shortage | categorical_or_expression_text | domain_value_check_recommended | shortage; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| fixed_price | numeric(19,4) | engine metadata not exposed | — | 64 | Fixed price of the part | measure | fixed price | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | fixed price; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| reorder_level | int | engine metadata not exposed | — | 65 | reorder_level | dimension | reorder level | integer | domain_value_check_recommended | reorder level; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| reorder_qty | int | engine metadata not exposed | — | 66 | reorder_qty | dimension | reorder qty | integer | domain_value_check_recommended | reorder qty; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| package_qty | int | engine metadata not exposed | — | 67 | when part is packed in warehouse | dimension | package qty | integer | domain_value_check_recommended | package qty; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| wgt_chk_date | timestamp | engine metadata not exposed | — | 68 | Weight check date | dimension | wgt chk date | categorical_or_expression_text | domain_value_check_recommended | wgt chk date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| mrp_date | timestamp | engine metadata not exposed | — | 69 | MRP date. Not in use | dimension | mrp date | categorical_or_expression_text | domain_value_check_recommended | mrp date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| security | varchar(200) | engine metadata not exposed | — | 70 | Security control | dimension | security | categorical_or_expression_text | domain_value_check_recommended | security; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| wms_profile | varchar(200) | engine metadata not exposed | — | 71 | wms_profile | dimension | wms profile | categorical_or_expression_text | domain_value_check_recommended | wms profile; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| lifecycle_status | varchar(200) | engine metadata not exposed | — | 72 | Lifecycle status | dimension | lifecycle status | categorical_or_expression_text | domain_value_check_recommended | lifecycle status; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| source_status | varchar(200) | engine metadata not exposed | — | 73 | The main states are  FS--FULL Stock LS--Limited Stock NS--Not stocked DS--Drop Ship Only ST--Stock Only | dimension | source status | categorical_or_expression_text | domain_value_check_recommended | source status; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| mult | int | engine metadata not exposed | — | 74 | If field != null, then do not allow PO to be entered in unless entered in multiples of field value | dimension | mult | integer | domain_value_check_recommended | mult; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| min_poqty | int | engine metadata not exposed | — | 75 | If field != null, then if user attempts to enter PO with qty < field value,do not allow PO to be entered with less than qty in this field | dimension | min poqty | integer | domain_value_check_recommended | min poqty; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| active_status_date | timestamp | engine metadata not exposed | — | 76 | Last date when the active status was changed | dimension | active status date | categorical_or_expression_text | domain_value_check_recommended | active status date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| last_pur_date | timestamp | engine metadata not exposed | — | 77 | Last sales date | dimension | last pur date | categorical_or_expression_text | domain_value_check_recommended | last pur date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| prod_lifecycle_code | varchar(200) | engine metadata not exposed | — | 78 | part lifecyle | dimension | prod lifecycle code | categorical_or_expression_text | domain_value_check_recommended | prod lifecycle code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| bundle_kit | varchar(200) | engine metadata not exposed | — | 79 | type of part is bundle/kit part | dimension | bundle kit | categorical_or_expression_text | domain_value_check_recommended | bundle kit; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_seg_code | varchar(200) | engine metadata not exposed | — | 80 | The code assigned to vendors and VPC codes. The key of this table.From vendor_profile,profile_type='SEG' | dimension | vend seg code | categorical_or_expression_text | domain_value_check_recommended | vend seg code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_family_id | int | engine metadata not exposed | — | 81 | This is the top level of ec type | key | ec family id | integer | not_null_expected|dim_fk_check_recommended | ec family id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_family | varchar(200) | engine metadata not exposed | — | 82 | A category description for the level ec type of the category structure | dimension | ec family | categorical_or_expression_text | domain_value_check_recommended | ec family; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_cat_id | int | engine metadata not exposed | — | 83 | This is the middle level id   from ec tables | key | ec cat id | integer | not_null_expected|dim_fk_check_recommended | ec cat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_category | varchar(200) | engine metadata not exposed | — | 84 | A category description for the level category of the category structure,  from ec tables | dimension | ec category | categorical_or_expression_text | domain_value_check_recommended | ec category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_subcat_id | int | engine metadata not exposed | — | 85 | The lowest level which is optional. Provides more detailed breakdown of the middle level, if desired. Should keep the number of values for any one middle level to less than 10 values,  from ec tables | key | ec subcat id | integer | not_null_expected|dim_fk_check_recommended | ec subcat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_sub_category | varchar(200) | engine metadata not exposed | — | 86 | A category description for the level sub category of the category structure,  from ec tables | dimension | ec sub category | categorical_or_expression_text | domain_value_check_recommended | ec sub category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_family_id | int | engine metadata not exposed | — | 87 | not used | key | brpt family id | integer | not_null_expected|dim_fk_check_recommended | brpt family id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_family | varchar(200) | engine metadata not exposed | — | 88 | A category description for the level family of the category structure,  from b report tables | dimension | brpt family | categorical_or_expression_text | domain_value_check_recommended | brpt family; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_cat_id | int | engine metadata not exposed | — | 89 | This is the middle level  from b report tables | key | brpt cat id | integer | not_null_expected|dim_fk_check_recommended | brpt cat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_category | varchar(200) | engine metadata not exposed | — | 90 | A category description for the level category of the category structure,  from b report tables | dimension | brpt category | categorical_or_expression_text | domain_value_check_recommended | brpt category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_subcat_id | int | engine metadata not exposed | — | 91 | The lowest level which is optional. Provides more detailed breakdown of the middle level, if desired. Should keep the number of values for any one middle level to less than 10 values,  from b report | key | brpt subcat id | integer | not_null_expected|dim_fk_check_recommended | brpt subcat id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| brpt_sub_category | varchar(200) | engine metadata not exposed | — | 92 | A category description for the level sub category of the category structure,  from b report tables | dimension | brpt sub category | categorical_or_expression_text | domain_value_check_recommended | brpt sub category; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| global_cat_type | varchar(200) | engine metadata not exposed | — | 93 | global type of category | dimension | global cat type | categorical_or_expression_text | domain_value_check_recommended | global cat type; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| categorizer | varchar(200) | engine metadata not exposed | — | 94 | The first name and last name of the employee | dimension | categorizer | categorical_or_expression_text | domain_value_check_recommended | categorizer; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| categorized_time | timestamp | engine metadata not exposed | — | 95 | entry date | dimension | categorized time | categorical_or_expression_text | domain_value_check_recommended | categorized time; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| modifier | varchar(200) | engine metadata not exposed | — | 96 | The first name and last name of the employee | dimension | modifier | categorical_or_expression_text | domain_value_check_recommended | modifier; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| last_modify_date | timestamp | engine metadata not exposed | — | 97 | Date last modified | dimension | last modify date | categorical_or_expression_text | domain_value_check_recommended | last modify date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| asc606 | varchar(200) | engine metadata not exposed | — | 98 | the new revenue recognition standard that affects all businesses that enter into contracts with customers to transfer goods or services.From sku_profile,profile_type='ASC606'and profile_cat = 'SKU' | dimension | asc606 | categorical_or_expression_text | domain_value_check_recommended | asc606; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| renewal_flag | varchar(200) | engine metadata not exposed | — | 99 | if the part can be renewed.From sku_profile,profile_type='ASC606'and profile_cat = 'SKU' | dimension | renewal flag | categorical_or_expression_text | domain_value_check_recommended | renewal flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| image_count | int | engine metadata not exposed | — | 100 | part image count | dimension | image count | integer | domain_value_check_recommended | image count; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| image_upload_date | timestamp | engine metadata not exposed | — | 101 | Date of when the record was inserted into this table | dimension | image upload date | categorical_or_expression_text | domain_value_check_recommended | image upload date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| fill_count | int | engine metadata not exposed | — | 102 | fill number of part_technotes | dimension | fill count | integer | domain_value_check_recommended | fill count; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| multiimage | varchar(200) | engine metadata not exposed | — | 103 | if the part has multiple images | dimension | multiimage | categorical_or_expression_text | domain_value_check_recommended | multiimage; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| msrp_flag | varchar(200) | engine metadata not exposed | — | 104 | if the part has sugguestion retail price.From sku_profile,profile_type='RETAIL $' | dimension | msrp flag | categorical_or_expression_text | domain_value_check_recommended | msrp flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| sku_map | varchar(200) | engine metadata not exposed | — | 105 | Categories of commodity prices, map is the lowest price a retailer can advertise the product for sale.From sli_profile,profile_type='MAP'and profile_cat='PRIC' | dimension | sku map | categorical_or_expression_text | domain_value_check_recommended | sku map; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| coo | varchar(200) | engine metadata not exposed | — | 106 | country of Origin.From sku_xref,xref_type='COO' | dimension | coo | categorical_or_expression_text | domain_value_check_recommended | coo; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_mkt_overview | varchar(32768) | engine metadata not exposed | — | 107 | marketing overview | dimension | tc mkt overview | categorical_or_expression_text | domain_value_check_recommended | tc mkt overview; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| ec_flag | varchar(200) | engine metadata not exposed | — | 108 | used to mark the row if EC defined to use | dimension | ec flag | categorical_or_expression_text | domain_value_check_recommended | ec flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| accessory_cnt | int | engine metadata not exposed | — | 109 | accessory number Calculation method: count(*)  from sku_xref and xref_type='ACCESSORY' | dimension | accessory cnt | integer | domain_value_check_recommended | accessory cnt; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| qc_status | varchar(200) | engine metadata not exposed | — | 110 | Content QC give a status to a part | dimension | qc status | categorical_or_expression_text | domain_value_check_recommended | qc status; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| qc_flag | varchar(200) | engine metadata not exposed | — | 111 | Content QC give a status to a part  such as  QC and UR | dimension | qc flag | categorical_or_expression_text | domain_value_check_recommended | qc flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| upc_flag | varchar(200) | engine metadata not exposed | — | 112 | if the part has Universal product Code,From sku_profile,profile_type ='UPC_CODE' | dimension | upc flag | categorical_or_expression_text | domain_value_check_recommended | upc flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| part_cust_no | varchar(200) | engine metadata not exposed | — | 113 | relevant customer number of this part.From sku_profile,profile_type ='CUST_SKU' | key | part cust no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | part cust no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| hwsw_comb | varchar(200) | engine metadata not exposed | — | 114 | hardware and software combined.From sku_profile,profile_type='HWSW-COMB'and profile_cat ='SKU' | dimension | hwsw comb | categorical_or_expression_text | domain_value_check_recommended | hwsw comb; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| etl_timestamp | timestamp | engine metadata not exposed | — | 115 | ETL datetime | technical | etl timestamp | timestamp | expression_parseable_check | etl timestamp; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_consign_flag | varchar(200) | engine metadata not exposed | — | 116 | to define if the vendor is consigment vendor,enum value is Y,N | dimension | vend consign flag | categorical_or_expression_text | domain_value_check_recommended | vend consign flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| part_consign_flag | varchar(2) | engine metadata not exposed | — | 117 | consignment flag of part,enum value is Y,N | dimension | part consign flag | categorical_or_expression_text | domain_value_check_recommended | part consign flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| vend_part_no | varchar(100) | engine metadata not exposed | — | 118 | vend part no | key | vend part no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | vend part no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| global_family_desc | varchar(78) | engine metadata not exposed | — | 119 | A category description for the level family of the category structure from CIS.global_pco_cat_id | dimension | global family desc | categorical_or_expression_text | domain_value_check_recommended | global family desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| global_cat_desc | varchar(80) | engine metadata not exposed | — | 120 | A category description for the level category of the category structure,  from CIS..global_pco_cat_id | dimension | global cat desc | categorical_or_expression_text | domain_value_check_recommended | global cat desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| global_sub_desc | varchar(80) | engine metadata not exposed | — | 121 | A category description for the level sub category of the category structure from CIS.global_pco_cat_id | dimension | global sub desc | categorical_or_expression_text | domain_value_check_recommended | global sub desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pcode | varchar(6) | engine metadata not exposed | — | 122 | Product category as defined by global financial team for financial reporting across all TD Synnex companies | dimension | pcode | categorical_or_expression_text | domain_value_check_recommended | pcode; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pcode_desc | varchar(54) | engine metadata not exposed | — | 123 | Description of the product category as defined by the global financial team | dimension | pcode desc | categorical_or_expression_text | domain_value_check_recommended | pcode desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| series_desc | varchar(116) | engine metadata not exposed | — | 124 | series description | dimension | series desc | categorical_or_expression_text | domain_value_check_recommended | series desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| std_whls_price | numeric(19,4) | engine metadata not exposed | — | 125 | Standard_whls price(limitStock) | measure | std whls price | decimal_currency_or_ratio | non_negative_expected|outlier_check_recommended | std whls price; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| jv_business | varchar(100) | engine metadata not exposed | — | 126 | joint venture. used to flag JV related SKUs and indicate whether it is large (=main) or small components | dimension | jv business | categorical_or_expression_text | domain_value_check_recommended | jv business; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| data_source | varchar(100) | engine metadata not exposed | — | 127 | Data source identifier either from CIS or HIS | dimension | data source | categorical_or_expression_text | domain_value_check_recommended | data source; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| uni_sku_no | varchar(100) | engine metadata not exposed | — | 128 | universal sku of sku# | key | uni sku no | categorical_or_expression_text | not_null_expected|dim_fk_check_recommended | uni sku no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| dg_code | varchar(100) | engine metadata not exposed | — | 129 | Dangerous goods code | dimension | dg code | categorical_or_expression_text | domain_value_check_recommended | dg code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| tc_fill_count | int | engine metadata not exposed | — | 130 | fill number of  tc_part_technotes_en | dimension | tc fill count | integer | domain_value_check_recommended | tc fill count; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| company_no | int | engine metadata not exposed | — | 131 | Comapny Number | key | company no | integer | not_null_expected|dim_fk_check_recommended | company no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| first_image_name | varchar(100) | engine metadata not exposed | — | 132 | Image Name | dimension | first image name | categorical_or_expression_text | domain_value_check_recommended | first image name; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| global_load_date | timestamp | engine metadata not exposed | — | 133 | indicates the time when a local sku_no was loaded from sybase to global database | dimension | global load date | categorical_or_expression_text | domain_value_check_recommended | global load date; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| fx_flag | varchar(100) | engine metadata not exposed | — | 134 | fx flag | dimension | fx flag | categorical_or_expression_text | domain_value_check_recommended | fx flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| forecast_cat | int | engine metadata not exposed | — | 135 | forecast_cat | dimension | forecast cat | integer | domain_value_check_recommended | forecast cat; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pp_code | varchar(136) | engine metadata not exposed | — | 136 | Data Value | dimension | pp code | categorical_or_expression_text | domain_value_check_recommended | pp code; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| pp_data_no | int | engine metadata not exposed | — | 137 | Data Number | key | pp data no | integer | not_null_expected|dim_fk_check_recommended | pp data no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| arr_flag | varchar(2) | engine metadata not exposed | — | 138 | This flag could be used to indicate whether a subscription or recurring billing model is in place for a specific service or product. Possible values are Y (Yes) or N (No) | measure | arr flag | categorical_or_expression_text | non_negative_expected|outlier_check_recommended | arr flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| arr_entry_id | int | engine metadata not exposed | — | 139 | This entry ID could be used to uniquely identify a specific subscription or customer agreement within the recurring revenue system | key | arr entry id | integer | not_null_expected|dim_fk_check_recommended | arr entry id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| xaas_flag | varchar(2) | engine metadata not exposed | — | 140 | This flag could be used to indicate whether a particular XaaS offering is active or enabled for a customer. Possible values are Y (Yes) or N (No) | dimension | xaas flag | categorical_or_expression_text | domain_value_check_recommended | xaas flag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| xaas_entry_id | int | engine metadata not exposed | — | 141 | This entry ID could be used to uniquely identify a specific resource or service instance within the XaaS environment | key | xaas entry id | integer | not_null_expected|dim_fk_check_recommended | xaas entry id; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| iqc_req | varchar(2) | engine metadata not exposed | — | 142 | Inbound Quality Control | dimension | iqc req | categorical_or_expression_text | domain_value_check_recommended | iqc req; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| comb_vend_no | int | engine metadata not exposed | — | 143 | Comb vendor number | key | comb vend no | integer | not_null_expected|dim_fk_check_recommended | comb vend no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vendor_info.vend_no` |
| alt_vend_no | int | engine metadata not exposed | — | 144 | Alt vendor number | key | alt vend no | integer | not_null_expected|dim_fk_check_recommended | alt vend no; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | `dim_us.dim_pub_vendor_info.vend_no` |
| item_type | varchar(100) | engine metadata not exposed | — | 145 | item type | dimension | item type | categorical_or_expression_text | domain_value_check_recommended | item type; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| item_type_desc | varchar(100) | engine metadata not exposed | — | 146 | item type description | dimension | item type desc | categorical_or_expression_text | domain_value_check_recommended | item type desc; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |
| asset_tag | varchar(10) | engine metadata not exposed | — | 147 | Asset tag | dimension | asset tag | categorical_or_expression_text | domain_value_check_recommended | asset tag; Product/part master attribute on `dim_us.dim_pub_part_info`; join on `sku_no` for part and VPL context. | — |

### Lineage

- lineage_degree: 2
- upstream_n_hops:
  - table_fqn: `ods_us.ods_etl_part_master_all`
    hop: 1
    relation_type: source_sync
    via_job_or_view: `public_part_dimension_us.dim_pub_part_info`
  - table_fqn: `ods_us.ods_cis_corp_vend_master`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: vendor name / company enrichment
  - table_fqn: `ods_us.ods_cis_corp_tc_part_cat` (and TC category mapping tables)
    hop: 1
    relation_type: enrich_join
    via_job_or_view: TC family/category hierarchy columns
- downstream_n_hops:
  - table_fqn: `dw_us.dws_disty_brpt_pl_extend_1d`
    hop: 1
    relation_type: enrich_join
    via_job_or_view: `dim_pub_part_info_df` as-of join for `part_no`, `vpl_no`, descriptions
  - table_fqn: `dw_us.dws_disty_brpt_part_1d`
    hop: 1
    relation_type: read_aggregate
    via_job_or_view: product-level serving mart
  - table_fqn: `dw_us.dws_disty_brpt_vpl_1d`
    hop: 2
    relation_type: read_aggregate
    via_job_or_view: aggregated from part / pl_extend chain
- lineage_last_verified_at: 2026-06-24
- lineage_confidence: high (pub_dw part dimension SQL + B Report joins)


### Column Lineage and Derivation

- `sku_no`: primary product key from part master ODS.
- `part_no`, `short_desc`, `mfg_partno`, physical attributes: pass-through from `ods_etl_part_master_all`.
- `vpl_no`, `vpl_code`, `alt_vpl_no`: VPL assignment and alternate-VPL logic from part/VPL enrichment joins.
- `vend_no`, `vend_name`, segment fields: joined from vendor master reference.
- TC hierarchy columns (`tc_family`, `tc_category`, etc.): derived via CIS group → TC category mapping chain in `dim_pub_part_info.sql`.


### Freshness and Load Path

- Producer flow: `public_part_dimension_us` job `dim_pub_part_info` (and `dim_pub_part_info_df` for date-keyed snapshots).
- Vertica sync via pub part dimension hive2vertica jobs.
- Expected completion window: 02:00-05:00 PT (large part master).
- Freshness confidence: medium.


## L2 Declarative Knowledge

### Business Definitions

- Domain: US product/part master for SKU-level enrichment in B Report and pub analytics.
- Trust tier: governed reference.
- Grain: one row per `sku_no`.
- Primary B Report usage: resolve `sku_no` to `part_no`, descriptions, VPL/vendor hierarchy; serving ETL often uses `dim_pub_part_info_df` for as-of `date_flag` joins.



### Dimension Keys and Lookup Reference

- Primary key: `sku_no` (int) — one row per SKU.
- Outbound FKs: `vend_no` → `dim_us.dim_pub_vendor_info`; `vpl_no` → `dim_us.dim_pub_vpl_info`.
- Denormalized vendor/VPL labels (`vend_name`, `vpl_code`, `vpl_desc`) are convenience copies; prefer canonical dims for cross-table consistency checks.

### Dimension Lookup / Join Reference

- `vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_part_info.vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `vpl_no` → `dim_us.dim_pub_vpl_info.vpl_no` | join: `dim_pub_part_info.vpl_no = dim_pub_vpl_info.vpl_no` | lookup labels: `vpl_code`, `vpl_desc` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `alt_vpl_no` → `dim_us.dim_pub_vpl_info.vpl_no` | join: `dim_pub_part_info.alt_vpl_no = dim_pub_vpl_info.vpl_no` | lookup labels: `vpl_code`, `vpl_desc` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `universal_vend_no` → `dim_us.dim_pub_vendor_info.universal_vend_no` | join: `dim_pub_part_info.universal_vend_no = dim_pub_vendor_info.universal_vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `comb_vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_part_info.comb_vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)
- `alt_vend_no` → `dim_us.dim_pub_vendor_info.vend_no` | join: `dim_pub_part_info.alt_vend_no = dim_pub_vendor_info.vend_no` | lookup labels: `vend_name`, `master_vend_name`, `vend_segment` | cardinality: many:1 | confidence: high (KB-wide ref index)


### Identifier Search Profile

- searchable_identifier_columns:
  - column: `part_no`
    data_type: varchar
    match_mode: exact then contains_like (`ILIKE '%token%'`)
  - column: `mfg_partno`
    data_type: varchar
    match_mode: exact then contains_like (`ILIKE '%token%'`)
  - column: `upc_code`
    data_type: varchar
    match_mode: exact
  - column: `vend_part_no`
    data_type: varchar
    match_mode: exact then contains_like
- non_searchable_key_columns: `sku_no`, `prod_code`, `vpl_no`, `vend_no`, `category_id` — alphanumeric user tokens must not be compared to these integer keys
- user_facing_aliases: `mfg_part_no`, `mfr_part_no`, `manufacturer part` → `mfg_partno`; `part`, `sku label` → search `part_no` and `mfg_partno`
- resolution_flow: user alphanumeric token → exact/`ILIKE` on `part_no` and `mfg_partno` → obtain `sku_no` → join facts/serving on `fact.sku_no = dim.sku_no`

### Column Profiling (key vs label)

| column_name | distinct_count | total_rows | uniqueness | safe_for_group_by | notes |
| --- | --- | --- | --- | --- | --- |
| sku_no | 12173527 | 12173527 | unique | yes | primary join key |
| part_no | 12167803 | 12173527 | non_unique | no | search/filter; ~5.7k duplicate part_no values |
| mfg_partno | 10181609 | 12173527 | non_unique | no | manufacturer part search |
| vpl_no | — | 12173527 | — | filter_ok | FK to `dim_pub_vpl_info` |

### Time Field Semantics

- Base table is current-state part master; B Report serving uses `dim_pub_part_info_df` partitioned by `date_flag` for as-of product attributes.
- Do not join base `dim_pub_part_info` for historical month-close analysis when `_df` snapshot is required by the target mart.

### Metrics Served

- Dimension attributes only; no fact metrics stored on this table


## L3 Procedural Knowledge

### Query and Routing Rules

- Use when resolving user-supplied part numbers or manufacturer part strings to `sku_no`.
- For metric questions scoped by part label, prefer `dw_us.dws_disty_brpt_part_mtd` when denormalized `part_no`/`mfg_partno` suffice; otherwise resolve here then join serving/fact on `sku_no`.
- Exact match on `part_no` / `mfg_partno` first; if zero rows, retry `ILIKE '%token%'` on the same columns before concluding no match.
- Facts carry `sku_no` (int) only; they do **not** have `part_no` or `mfg_partno` — filter user label tokens via this dimension or denormalized serving slice.
- Do not mix `1d`/`wtd`/`mtd`/`comb_mtd` grains in one aggregation step.

### Dimension Join Patterns

- Primary key: `sku_no`
- Fact join: `fact.sku_no = dim_pub_part_info.sku_no`
- VPL enrichment: `dim_pub_part_info.vpl_no = dim_pub_vpl_info.vpl_no`
- Vendor enrichment: `dim_pub_part_info.vend_no = dim_pub_vendor_info.vend_no`
- As-of join (serving ETL): `dim_pub_part_info_df` on `sku_no` AND `date_flag` when historical product attributes matter
- High-risk pitfalls: matching user text to `sku_no`; duplicate `part_no` labels mapping to multiple `sku_no` — always aggregate at `sku_no` after resolution

### Key Filters and ETL Business Logic

- Dimension load filters inactive/discontinued masters per CIS source rules; do not re-apply shipped-order filters (`dim_pub_order_type`) when querying this table directly.
- For B Report metric questions, apply shipped-order scope on the fact/serving table, then join this dimension for labels.
- Technical ETL predicates (partition sync, `date_flag` load guards on `*_df` snapshots) are not business filters on the base dimension.

### Standard Time-Filter SQL (3 snippets)

Time-filter snippets below apply to **fact/serving tables** joined to this dimension for metric questions. This dimension has no `date_flag`; use `*_df` snapshot variants when as-of attributes are required.

1) Natural month (month-end snapshot)

1) Natural month (month-end snapshot)

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: scalar_lookup
table_fqn: dim_us.dim_pub_part_info
grain: date_flag_month_end
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_flag, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= '2026-01-01'
  AND date_flag <  '2026-02-01'
GROUP BY date_flag
ORDER BY date_flag;
```

2) Fiscal month / fiscal quarter

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_pub_part_info
grain: fiscal_month
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT f.fyear, f.month, SUM(t.ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi t
JOIN dim_us.dim_pub_date f
  ON t.date_flag = f.date_flag
WHERE f.fyear = 2026
GROUP BY f.fyear, f.month;
```

3) Recent N-month trend without double counting

<!-- sql-artifact
snippet_type: time_filter_pattern
intent: trend
table_fqn: dim_us.dim_pub_part_info
grain: month_start
anti_use: do not copy as ranking/breakdown SQL; borrow date filter only
-->
```sql
SELECT date_trunc('MM', date_flag) AS month_start, SUM(ngm_amt) AS ngm_amt
FROM dw_us.dwd_disty_brpt_orders_pl_etl_mi
WHERE date_flag >= add_months(current_date, -6)
GROUP BY date_trunc('MM', date_flag)
ORDER BY month_start;
```

### Metric Selection Guidance

- Use this table for dashboard and period-comparison queries when dimensions match.
- Use DWD base for formula debugging, order_type adjustments, and transaction-level audit.
- Canonical metric formulas and routing: see `metric-index.md`.

## L4 Validation

### Data Quality Checks

- Verify row count stability day-over-day; expect slow growth as new customers/vendors/parts onboard.
- Monitor duplicate-key risk on business keys (`cust_no`, `vend_no`, `sku_no`, `vpl_no`) — each should be unique at stated grain.
- For label columns used in user search (`*_name`, `part_no`, `vpl_code`), spot-check null rate and trim/whitespace anomalies.
- When joining to facts, validate match rate on integer FK columns; unmatched keys often indicate inactive master or cross-company scope mismatch.

### Metric Recompute Spot-Checks

- Not applicable — dimension tables carry no fact metrics. Validate attribute lookups by joining a sample of fact keys and comparing label coverage.

### Conflicts and Open Questions

- No active conflicts on dimension grain or key semantics as of 2026-06-25.

## L5 Runtime View

### Query Path and Engine Preference

- Primary: Vertica `dw_us`/`dm_us` for BI dashboards (fresher on detail facts).
- Fallback: Hive for reconciliation or when Vertica unavailable.
- Metadata: domain table docs and `metric-index.md` for routing.

### Access Constraints

- Standard `dw_us`/`dm_us`/`dim_us` role-based access applies.
- No table-specific ACL exceptions documented.

## L6 Access and Consumption

### Primary Consumers and Use Cases

- Consumers: B Report `pl_extend` pre-load, part/VPL serving marts, semantic layer part lookup.
- Use cases: resolve part numbers to `sku_no`, enrich product hierarchy (TC/EC/BRPT categories), vendor/VPL context on order lines.

### Representative Query Patterns

<!-- sql-artifact
snippet_type: routing_certified
intent: metric_lookup
table_fqn: dim_us.dim_pub_part_info
grain: part_label_resolution
golden_ref: b-report-us#part-enn-525-revenue-margin
verified_at: 2026-06-25
verified_engine: vertica
verified_shape: part_scope CTE resolves sku_no from part_no/mfg_partno
anti_use: dimension lookup step only; aggregate metrics on dws_disty_brpt_part_mtd
-->
```sql
SELECT sku_no, part_no, mfg_partno, short_desc, vpl_no, vend_no
FROM dim_us.dim_pub_part_info
WHERE part_no = 'ENN-525'
   OR mfg_partno = 'ENN-525'
   OR part_no ILIKE '%ENN-525%'
   OR mfg_partno ILIKE '%ENN-525%'
LIMIT 20;
```

See `golden-questions.md` entry `part-enn-525-revenue-margin` for the full certified metric query using this resolution pattern.
