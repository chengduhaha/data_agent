# RDS domain knowledge

- artifact_type: domain-knowledge
- artifact_id: rds
- source: RDS_Workspace/shared/business_term_aliases*.txt

Shared business-term aliases for RDS report SQL packs (POS, CPO, VPO, Inventory, Open_SO_BO, and related domains).

## Source: `business_term_aliases.txt`

```text
# =============================================================================
# AI RDS DEVELOPER — Shared Business Term Aliases
# =============================================================================
# Single mapping source for POS, CPO, VPO, Inventory, Open_SO_BO.
# Format spec: RDS_Workspace/shared/business_term_aliases_format.txt
# =============================================================================

# -----------------------------------------------------------------------------
# SECTION A — Business concepts
# CANONICAL | ALIASES | BUSINESS_MEANING
# -----------------------------------------------------------------------------

cust_po_no | cust_po_no, customer po, customer po#, cust po, cpo, cpo no, customer po number, partner po, reseller po, ext_ref | Customer purchase order number on sales/CPO/shipment context. cust_po_no and cpo_no are the same business field; physical column name varies by table.
cpo_id | cpo id, cpo_id | Internal CPO identifier (header key), not the same as customer PO text.
open_cpo | open cpo, open cpo report, open quote, open quote report, open quote/cpo, web quote | Active open customer purchase order / quote lines not converted to orders. Open Quote Report and Open CPO Report are the same report scope; do not split by QUOTESHEET vs other statuses unless a historical example explicitly does.
cpo_line_no | cpo line, cpo line no, cpo_line_no, cpo line seq | CPO line sequence number.
bill_to_cust_no | customer number, customer no, cust no, reseller number, bill to cust no, bill to customer | Bill-to / reseller customer number.
bill_to_cust_name | customer name, cust name, reseller name, bill to cust name | Bill-to / reseller customer name.
sold_to_cust_no | sold to cust no, sold to customer, sold to cust number | Sold-to customer number when distinct from bill-to.
sold_to_cust_name | sold to cust name, sold to customer name, sold to name | Sold-to customer name.
sku_no | sku, sku no, item number, synnex sku | Synnex SKU identifier.
part_no | part no, synnex part, snx part | Synnex internal part number.
vend_part_no | vend part no, vendor part no, vendor part number, mfg part no, manufacturer part number, mfg part# | Vendor/manufacturer part number; often stored as mfg_partno.
vend_no | vendor number, vendor no, vend no | Vendor number.
vend_name | vendor name, vend name | Vendor name.
ship_date | ship date, shipment date, distributor invoice date | Shipment/invoice display date.
date_flag | pos date, business date, ship date filter, reporting date | Primary date column for period filters on fact tables.
ship_qty | ship qty, shipped qty, quantity shipped, qty | Shipped quantity.
base_cost | base cost, po cost, unit base cost | Unit base cost.
extend_base_cost | extended base cost, ext base cost, extend base cost | Extended base cost (unit base cost × quantity when not stored).
unit_exp | unit exp, unit_exp, u_sum_expense, unit_sum_expense, scm unit exp, unit expense | Per-unit SCM/expense/rebate adjustment.
extend_exp | extend exp, extended exp, extend_exp, extended expense | Extended SCM/expense amount.
unit_cost | unit cost, net cost, u_cost | Unit net cost.
extend_net_price | net sales, sales amount, revenue, extended net price, extend net price | Extended net sales/price.
ncogs | ncogs, net cogs, net_cogs, NCOGs, net cog | Net COGS; usually includes unit cost and unit expense on shipment lines.
eu_company_name | eu company name, eu name, end user name, end customer name, company name, EU name | End-user / EU company name.
sales_terr | sales terr, cust terr, terr no, territory number | Sales territory number.
terr_name | territory name, terr name, sales terr name | Sales territory name.
order_no | order no, order#, invoice number, distributor invoice number, tds sales order | Order or invoice number.
order_type | order type | Order type code.
order_line_no | order line, line no, line#, order line no | Order line number.
synnex_po_no | synnex po, synnex po no, synnex_po, tds po, vpo no | Synnex/TDSynex PO reference on sales flow.
mso_no | mso no, mso#, mso number | MSO reference number.

# -----------------------------------------------------------------------------
# SECTION B — Physical column bindings
# DOMAIN | ENGINE | CANONICAL | PHYSICAL | SOURCE_TABLE | OUTPUT_RULE | NOTES
# -----------------------------------------------------------------------------

# --- POS Vertica (driving: dwd_disty_common_pos_di) ---
POS | Vertica | cust_po_no | cpo_no | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED | Use pos.cpo_no directly. Same as cust_po_no. Do not join history ext_ref unless example requires fallback and cpo_no is null.
POS | Vertica | bill_to_cust_no | bill_to_cust_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | bill_to_cust_name | bill_to_cust_name | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | sold_to_cust_no | sold_to_cust_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | sold_to_cust_name | sold_to_cust_name | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | sku_no | sku_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | part_no | part_no | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | vend_part_no | mfg_partno | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED | Prefer pos.mfg_partno; enrich from dim_xx.dim_pub_part_info only when example does.
POS | Vertica | vend_no | vend_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | vend_name | vend_name | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | ship_date | ship_date | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED | Display date; filter period on date_flag.
POS | Vertica | date_flag | date_flag | dw_xx.dwd_disty_common_pos_di | PHYSICAL | Primary POS period filter.
POS | Vertica | ship_qty | ship_qty | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | base_cost | base_cost | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | extend_base_cost | extend_base_cost | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED | Else EXPR: COALESCE(base_cost,0) * ship_qty.
POS | Vertica | unit_exp | unit_sum_exp | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | extend_exp | EXPR: ship_qty * COALESCE(unit_sum_exp, 0) | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | unit_cost | unit_cost | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | extend_net_price | extend_net_price | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | ncogs | EXPR: ship_qty * (COALESCE(unit_cost, 0) + COALESCE(unit_sum_exp, 0)) | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | eu_company_name | eu_company_name | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED | Prefer POS base before EU custom tables.
POS | Vertica | sales_terr | sales_terr | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | terr_name | terr_name | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | order_no | order_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | order_type | order_type | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | order_line_no | order_line_no | dw_xx.dwd_disty_common_pos_di | CANONICAL |
POS | Vertica | synnex_po_no | synnex_po_no | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |
POS | Vertica | mso_no | mso_no | dw_xx.dwd_disty_common_pos_di | USE_REQUESTED |

# --- POS StarRocks (driving tables vary; common orders extend) ---
POS | StarRocks | cust_po_no | cust_po_no | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED | cust_po_no and cpo_no are same business value; mockup may label output as cpo_no.
POS | StarRocks | cust_po_no | cpo_no | dw_xx.dwd_disty_common_dw_orders_pl_extend_di | USE_REQUESTED | When driving table is orders_pl extend.
POS | StarRocks | bill_to_cust_no | cust_no | dw_xx.dwd_disty_pub_dw_orders_extend_di | CANONICAL | Map to bill_to output label when mockup requires.
POS | StarRocks | bill_to_cust_name | cust_name | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | sku_no | sku_no | dw_xx.dwd_disty_pub_dw_orders_extend_di | CANONICAL |
POS | StarRocks | vend_part_no | mfg_partno | dim_xx.dim_pub_part_info | USE_REQUESTED | Usually via part dim join.
POS | StarRocks | ship_date | ship_date | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | date_flag | date_flag | dw_xx.dwd_disty_pub_dw_orders_extend_di | PHYSICAL |
POS | StarRocks | ship_qty | ship_qty | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | unit_exp | unit_sum_expense | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | extend_exp | EXPR: ship_qty * COALESCE(unit_sum_expense, 0) | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | base_cost | base_cost | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |
POS | StarRocks | ncogs | EXPR: ship_qty * (COALESCE(u_cost, 0) + COALESCE(unit_sum_expense, 0)) | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED | Confirm cost column on chosen driving table.
POS | StarRocks | eu_company_name | eu_company_name | dw_xx.dwd_disty_pub_dw_orders_extend_di | USE_REQUESTED |

# --- CPO Vertica ---
CPO | Vertica | cust_po_no | cpo_no | dm_xx.dm_disty_sales_open_cpo | USE_REQUESTED | Open CPO lines; same business field as cust_po_no.
CPO | Vertica | cust_po_no | cpo_no | dm_xx.dm_disty_sales_close_cpo_di | USE_REQUESTED | Closed/historical CPO lines.
CPO | Vertica | cpo_id | cpo_id | dm_xx.dm_disty_sales_open_cpo | CANONICAL |
CPO | Vertica | cpo_line_no | cpo_line_no | dm_xx.dm_disty_sales_open_cpo | CANONICAL |
CPO | Vertica | sku_no | cpo_sku_no | dm_xx.dm_disty_sales_open_cpo | CANONICAL | CPO line SKU; confirm grain in CPO examples.
CPO | Vertica | vend_no | vend_no | dm_xx.dm_disty_sales_open_cpo | CANONICAL |
CPO | Vertica | bill_to_cust_no | cust_no | dm_xx.dm_disty_sales_open_cpo | CANONICAL | CPO customer number context.

# --- CPO StarRocks ---
CPO | StarRocks | cust_po_no | cpo_no | ods_xx.ods_cis_corp_cpo_header_rt | USE_REQUESTED | Open CPO header; join to detail for lines.
CPO | StarRocks | cust_po_no | cpo_no | ods_xx.ods_cis_corp_history_cpo_header_rt | USE_REQUESTED | History/closed CPO header.
CPO | StarRocks | cpo_id | cpo_id | ods_xx.ods_cis_corp_cpo_header_rt | CANONICAL |
CPO | StarRocks | cpo_line_no | cpo_line_no | ods_xx.ods_cis_corp_cpo_detail_rt | CANONICAL |

# --- Open_SO_BO Vertica ---
Open_SO_BO | Vertica | cust_po_no | cpo_no | dw_xx.dwd_disty_sales_open_order_detail | USE_REQUESTED | Open order line customer PO.
Open_SO_BO | Vertica | cust_po_no | ext_ref | dw_xx.dwd_pub_common_order_header_extend | USE_REQUESTED | Order header customer PO when line cpo_no not used.
Open_SO_BO | Vertica | eu_company_name | eu_company_name | dw_xx.dwd_disty_sales_open_order_detail | USE_REQUESTED |
Open_SO_BO | Vertica | ship_qty | open_qty | dw_xx.dwd_disty_sales_open_order_detail | USE_REQUESTED | Open qty context; confirm grain in Open_SO_BO examples.

# --- Shared dimensions (any domain) ---
Shared | ALL | vend_part_no | mfg_partno | dim_xx.dim_pub_part_info | USE_REQUESTED | Product enrichment join on sku_no.
Shared | ALL | vend_no | vend_no | dim_xx.dim_pub_part_info | CANONICAL | Product vendor from part dim.
Shared | ALL | vend_name | vend_name | dim_xx.dim_pub_vendor_info | USE_REQUESTED | Join on vend_no.
Shared | ALL | bill_to_cust_name | cust_name | dim_xx.dim_pub_customer_info | USE_REQUESTED | Join on cust_no when fact table lacks name.
Shared | ALL | terr_name | terr_name | dim_xx.dim_pub_sales_hierarchy_primary_role_by_terr_view | USE_REQUESTED | Join on sales_terr when fact lacks terr_name.
```

## Source: `business_term_aliases_format.txt`

```text
# Business Term Aliases — File Format (AI RDS DEVELOPER)
#
# Single shared mapping file (all domains):
#   RDS_Workspace/shared/business_term_aliases.txt
#
# Optional domain-only exceptions (rare):
#   RDS_Workspace/<Engine>/<Domain>/Reference/business_term_overrides.txt
#
# When agents must read it
# - After the selected domain's table list.txt.
# - Before table relationship.txt, special_logic.txt, and SQL generation.
# - All domain skills (POS, CPO, VPO, Inventory, Open_SO_BO) use the same file.
#
# =============================================================================
# SECTION A — Business concepts (domain/engine neutral)
# =============================================================================
# One row per business concept. Synonyms only; no physical table here.
#
# CANONICAL | ALIASES | BUSINESS_MEANING
#
# CANONICAL        Standard internal name (snake_case).
# ALIASES          Comma-separated user/mockup/historical labels (case-insensitive).
# BUSINESS_MEANING Short definition and equivalence notes (e.g. cust_po_no = cpo_no).
#
# =============================================================================
# SECTION B — Physical column bindings
# =============================================================================
# Maps CANONICAL concepts to physical columns per domain and engine.
#
# DOMAIN | ENGINE | CANONICAL | PHYSICAL | SOURCE_TABLE | OUTPUT_RULE | NOTES
#
# DOMAIN       POS | CPO | VPO | Inventory | Open_SO_BO | Shared
# ENGINE       Vertica | StarRocks | ALL
# CANONICAL    Must match a Section A concept.
# PHYSICAL     Column on SOURCE_TABLE, or EXPR:<sql expression>.
# SOURCE_TABLE Use xx region placeholder (dw_xx, dim_xx, dm_xx, ods_xx).
# OUTPUT_RULE  USE_REQUESTED | CANONICAL | PHYSICAL
# NOTES        Join/fallback/calculation; when to prefer driving table vs enrich.
#
# =============================================================================
# Agent matching rules
# =============================================================================
#
# 1. Normalize user labels: lowercase, trim, treat _ and space as equivalent.
# 2. Match user label to Section A ALIASES → get CANONICAL.
# 3. Filter Section B by current DOMAIN (from business skill) and ENGINE.
# 4. If multiple Section B rows match, prefer the driving table for that domain.
# 5. Do not join another table when PHYSICAL is already on the driving table.
# 6. Use domain overrides file only when present and documented.
# 7. If no Section B row exists, fall back to domain reference + examples; ask if unclear.
#
```
