# Metric Index - b-report-us

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: b-report-us

## Purpose

- Metric-first routing index for the b-report-us domain.
- **Authoritative source** for metric formulas; table files carry serving summaries only.

## Metric Registry

### net_sales

- aliases: revenue, nsales, sales_total, net sales
- business_definition: Shipped quantity times unit price plus per-unit sum expense (net of returns scope per order_type filter).
- final_effective_formula_sql: `nvl(ship_qty,0) * (nvl(u_price,0) + nvl(u_sum_expense,0))`
- formula_verification_status: verified
- formula_component_breakdown:
  - ship_qty: shipped quantity at order-line grain
  - u_price: unit price
  - u_sum_expense: per-unit expense add-on
- refresh_pattern: disty_b_report_daily_us → dwd_disty_brpt_orders_pl_etl_mi; propagated to DWS/DM daily
- owner_team: not registered in metadata catalog
- status: active

### gross_sales

- aliases: gross revenue
- business_definition: Shipped quantity times unit price without sum expense.
- final_effective_formula_sql: `nvl(ship_qty,0) * nvl(u_price,0)`
- formula_verification_status: verified
- formula_component_breakdown:
  - ship_qty: shipped quantity
  - u_price: unit price
- refresh_pattern: same as net_sales base load
- owner_team: not registered in metadata catalog
- status: active

### gm_amt

- aliases: gm, gross margin
- business_definition: Core line gross margin before BTL/PDT and full NGM adjustment chain.
- final_effective_formula_sql: `(nvl(u_price,0) - nvl(if(sales_cost is null, u_cost, sales_cost), 0)) * nvl(ship_qty,0)`
- formula_verification_status: verified
- formula_component_breakdown:
  - unit margin spread: u_price minus effective unit cost (sales_cost or u_cost)
  - ship_qty: shipped quantity multiplier
- refresh_pattern: computed in total_ngm_normal chain before BTL add-backs
- owner_team: not registered in metadata catalog
- status: active

### tgm_amt

- aliases: tgm
- business_definition: Gross margin with core BTL/PDT and related trade-term add-backs (pre-full NGM overhead chain).
- final_effective_formula_sql: `gm_amt + nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0) + nvl(BTL_BACKOUT,0) + nvl(PDT,0)` (aggregated at serving grain)
- formula_verification_status: partial
- formula_component_breakdown:
  - gm_amt: core line margin
  - BTL family: trade term adjustments
  - PDT: promotional/discount terms
- refresh_pattern: DWS/DM aggregation from DWD columns
- owner_team: not registered in metadata catalog
- status: active

### ngm_amt

- aliases: ngm, negative ngm, net gross margin, margin
- business_definition: Net Gross Margin — final P&L profitability metric for PM/executive use after full adjustment chain.
- final_effective_formula_sql: |
    ( (nvl(u_price,0)-nvl(if(sales_cost is null,u_cost,sales_cost),0))*nvl(ship_qty,0)
      + nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0)
      + nvl(BTL_BACKOUT,0) + nvl(PDT,0) + nvl(AP_FINANCE,0) + nvl(SCM_COST,0) + nvl(SCM_RISK,0)
      + nvl(INV_COST,0) + nvl(INV_RESERVE,0) + nvl(INFRASTRUCTURE,0) + nvl(MARKETING,0)
      + nvl(FRT_OUT_LOAD,0) + nvl(FRT_OUT_EXP,0) + nvl(FRT_OB_RECOVERY,0) + nvl(FRT_IB_RECOVERY,0)
      + nvl(WHOH_PACK,0) + nvl(CSGN_EDI_FEE,0) + nvl(CUST_FINANCE,0) * nvl(c.NGM_CFN_RATE,1)
      + nvl(AR_FIN_RECOVERY,0) + nvl(CR_RISK_CTERM,0) * nvl(c.NGM_CRCT_RATE,1)
      + nvl(CUST_PMT_DISC,0) + nvl(CUST_REBATE,0) + nvl(CVR_RM,0) + nvl(DIRECT_CREDIT,0)
      + nvl(FLR_SYNNEX,0) + nvl(RMA,0) + nvl(MOF,0) + nvl(MARGIN_SHARE,0) + nvl(AP_ADJ,0)
      + nvl(CORPORATE,0) + nvl(HC_PM,0) + nvl(HC_BD,0) + nvl(HC_SALES,0) + nvl(ORDER_OVERHEAD,0)
      + nvl(OTHERS,0) + nvl(MFG_OH,0) + nvl(SFS,0) )
- formula_verification_status: verified
- formula_component_breakdown:
  - core margin spread: price minus cost times quantity
  - BTL/SCM/operations: trade and supply-chain adjustments
  - finance/risk weighted: CUST_FINANCE*NGM_CFN_RATE, CR_RISK_CTERM*NGM_CRCT_RATE
  - overhead and logistics: freight, warehouse, corporate allocations
- refresh_pattern: disty_b_report_daily_us (total_ngm_normal → normal_order_adj → total_ngm_adjust) → DWD → DWS/DM
- recompute_validation: date_flag=2026-06-09, row_cnt=117868, mismatch_cnt=0, max_abs_diff=0.0001
- owner_team: not registered in metadata catalog
- status: active

### oplgm_amt

- aliases: opl, order_pl
- business_definition: Order Profit and Loss for sales commission logic.
- final_effective_formula_sql: |
    ( (nvl(u_price,0)-nvl(if(sales_cost is null,u_cost,sales_cost),0))*nvl(ship_qty,0)
      + nvl(BTL_BACKOUT,0) + nvl(BTL_SALES,0) + nvl(TRANS_BTL_SALES,0)
      + nvl(PDT,0) + nvl(CUST_PMT_DISC,0) + nvl(CUST_REBATE,0) + nvl(CVR_RM,0)
      + nvl(FRT_OUT_LOAD,0) + nvl(FRT_OUT_EXP,0) + nvl(FRT_OB_RECOVERY,0)
      + nvl(MOF,0) + nvl(CUST_FINANCE_SALES,0) * nvl(c.CPL_CFN_RATE,1)
      + nvl(AR_FIN_RECOVERY,0) + nvl(CR_RISK_CTERM,0) * nvl(c.CPL_CRCT_RATE,1)
      + nvl(FLR_SYNNEX,0) + nvl(DIRECT_CREDIT,0) + nvl(WHOH_PACK,0) + nvl(RMA,0)
      + nvl(ORDER_OVERHEAD,0) + nvl(CSGN_EDI_FEE,0) + nvl(FRT_IB_RECOVERY,0)
      + nvl(OTHERS_SALES,0) + nvl(SFS,0)
      + (nvl(u_price,0)+nvl(u_sum_expense,0))*nvl(ship_qty,0) * nvl(c.CPL_COOP_RATE,0) )
- formula_verification_status: verified
- formula_component_breakdown:
  - core line margin spread
  - sales-side BTL/PDT and customer-program adjustments
  - rate-weighted finance/risk/coop terms (CPL_*_RATE from ods_cis_corp_pl_code)
- refresh_pattern: same daily US flow chain as ngm_amt
- recompute_validation: date_flag=2026-06-09, mismatch_cnt=0
- owner_team: not registered in metadata catalog
- status: active

### oplgm_plus_amt

- aliases: opl_plus
- business_definition: Extended OPL metric including additional direct cost/expense components beyond base OPL.
- final_effective_formula_sql: derived from oplgm_amt chain with additional OPL+ components (see oplgm_plus_amt_calcproc column on DWD)
- formula_verification_status: partial
- formula_component_breakdown:
  - base oplgm_amt components
  - additional OPL+ adjustments per ETL calcproc
- refresh_pattern: propagated from DWD through DWS/DM aggregations
- owner_team: not registered in metadata catalog
- status: active

### total_btl

- aliases: btl_total
- business_definition: Aggregate of Below-The-Line trade term adjustment components (BTL, TRANS_BTL, ONE_TIME_BTL, HBTL, etc.).
- final_effective_formula_sql: `nvl(BTL,0) + nvl(TRANS_BTL,0) + nvl(ONE_TIME_BTL,0) + nvl(HBTL,0) + nvl(SCM_PROFIT_ADJ,0) + nvl(BTL_BACKOUT,0)` (component set varies by report module)
- formula_verification_status: partial
- formula_component_breakdown:
  - BTL family columns on order-line fact
- refresh_pattern: DWD column passthrough → summed at DWS/DM grain
- owner_team: not registered in metadata catalog
- status: active

## Metric-to-Table Mapping

### net_sales / gross_sales / gm_amt / tgm_amt / ngm_amt / oplgm_amt / total_btl

- base_table_dwd: dw_us.dwd_disty_brpt_orders_pl_etl_mi
- serving_tables:
  - table_fqn: dw_us.dws_disty_brpt_*_{1d,wtd,mtd,comb_mtd}
  - layer: DWS
  - aggregation_grain: matches suffix (daily / wtd / mtd / comb monthly)
  - dimensions: slice-specific (cust, vend, vpl, part, cross, bd, etc.)
  - time_grain: 1d / wtd / mtd / comb_mtd
  - refresh_pattern: disty_b_report_daily_us family after DWD refresh
  - quality_level: governed
  - table_fqn: dm_us.dm_disty_brpt_*_{1d,wtd,mtd,comb_mtd}
  - layer: DM
  - aggregation_grain: role-specific (pm, buyer, sales, bd_rep)
  - dimensions: pm_id, buyer_id, sales hierarchy, bd_rep, etc.
  - refresh_pattern: role-specific loading flows (brpt_product_loading, brpt_customer_loading, BD flows)
  - quality_level: governed

## Selection Rules

### net_sales

- use_table_when:
  - Matching DWS/DM slice table covers required dimensions and time suffix
  - Dashboard trend or period comparison at served grain
- avoid_table_when:
  - Order_type adjustment debugging or transaction-level audit needed
  - Required dimension not present on serving table
- fallback_order:
  - preferred: dimension-matched `*_mtd` or `*_comb_mtd` serving table
  - fallback: dw_us.dwd_disty_brpt_orders_pl_etl_mi
- dimension_slice_routing:
  - when: question scopes by pm_id / PM id
  - preferred_table_fqn: dm_us.dm_disty_brpt_pm_mtd
  - avoid_table_fqn: dw_us.dws_disty_brpt_*_comb_mtd unless multi-period comb columns explicitly needed
  - time_pattern: natural month via dim_us.dim_pub_date; month-end snapshot for mtd/comb_mtd
  - when: question scopes by customer, master customer, territory, or sales hierarchy
  - preferred_table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line detail required
  - time_pattern: month-end `date_flag` snapshot; master filter via `mcust_name`; sub-customer breakdown key `cust_no` (display `cust_name`); see golden `cdw-sub-customer-ranking`
  - when: question scopes by sales territory name, terr group/sub-group, or `sales_terr` / `cust_terr` integer
  - preferred_table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required
  - time_pattern: month-end `date_flag` snapshot or latest open month via `dim_us.dim_pub_date`
  - filter_note: Phase-1 on `dim_us.dim_pub_sales_territory` (`terr_name`, `group_desc`, `sub_group_desc`); join serving on `cust_terr` = `sales_terr`; `terr_name` often denormalized on cust_mtd; extended dimensions → `dw_us.dws_disty_brpt_pl_extend_mtd`
  - when: question scopes by vendor, vend_no, vend_name, or manufacturer brand
  - preferred_table_fqn: dw_us.dws_disty_brpt_vend_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required
  - time_pattern: month-end `date_flag` via `dim_us.dim_pub_date`
  - filter_note: Phase-1 on `dim_us.dim_pub_vendor_info` (`vend_name`, `master_vend_name`, `universal_vend_name`); roll up `master_vend_no` / `universal_vend_name` when brand-family scope; **GROUP BY `vend_no`** for ranking; use `vend_name` as display only; see golden `jan-vendor-top5-ranking`
  - when: question scopes by part, product, sku label, part_no, or manufacturer part number
  - preferred_table_fqn: dw_us.dws_disty_brpt_part_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required; never filter DWD by `part_no` (column absent)
  - time_pattern: month-end `date_flag` snapshot or latest-month window via `dim_us.dim_pub_date`; filter `part_no` / `mfg_partno` (varchar) not `sku_no` with alphanumeric tokens
  - filter_note: resolve user token on `dim_us.dim_pub_part_info` when needed; exact match then `ILIKE` fallback; see golden `part-enn-525-revenue-margin`
  - when: question scopes by vpl, vpl code, product line, vpc, vpc group, or vendor product code label
  - preferred_table_fqn: dw_us.dws_disty_brpt_vpl_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required; never join dim_pub_vpl_hierarchy_info for VPL label lookup; never filter by vpl_id or vpl_name
  - time_pattern: latest open month via `latest_period` CTE on serving table when user omits year; month-end `date_flag` snapshot when month explicit
  - filter_note: Phase-1 on `dim_us.dim_pub_vpl_info` (`vpl_code`, `vpl_desc`, `vpc_group_desc`); exact match then `ILIKE` fallback; join serving on `vpl_no` or filter `vpc_group_desc` when group scope confirmed

### ngm_amt

- use_table_when: same as net_sales; prefer pre-aggregated when grain matches
- avoid_table_when: need full formula decomposition at order-line grain
- fallback_order: serving table → dw_us.dwd_disty_brpt_orders_pl_etl_mi
- dimension_slice_routing:
  - when: question scopes by customer, master customer, territory, or sales hierarchy
  - preferred_table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - avoid_table_fqn: dm_us.dm_disty_brpt_pm_mtd (PM slice) unless PM dimension explicitly required
  - time_pattern: month-end `date_flag` snapshot for closed-month MTD totals; filter master via `mcust_name`
  - when: question scopes by sales territory name, terr group/sub-group, or `sales_terr` / `cust_terr` integer
  - preferred_table_fqn: dw_us.dws_disty_brpt_cust_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required
  - time_pattern: month-end `date_flag` snapshot; Phase-1 dim validation on `dim_us.dim_pub_sales_territory` before aggregation
  - filter_note: join serving on `cust_terr` = `sales_terr`; extended dimensions → `dw_us.dws_disty_brpt_pl_extend_mtd`
  - when: question scopes by vendor, vend_no, vend_name, or manufacturer brand
  - preferred_table_fqn: dw_us.dws_disty_brpt_vend_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required
  - time_pattern: month-end `date_flag` via `dim_us.dim_pub_date`
  - filter_note: Phase-1 on `dim_us.dim_pub_vendor_info`; roll up `master_vend_no` / `universal_vend_name` when brand-family scope; **GROUP BY `vend_no`** for ranking; see golden `jan-vendor-top5-ranking`
  - when: question scopes by part, product, sku label, part_no, or manufacturer part number
  - preferred_table_fqn: dw_us.dws_disty_brpt_part_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required
  - time_pattern: month-end `date_flag` snapshot or latest open month; varchar filters on `part_no` / `mfg_partno`
  - filter_note: join `dim_us.dim_pub_part_info` to resolve label when fact or serving row lacks denormalized columns
  - when: question scopes by vpl, vpl code, product line, vpc, vpc group, or vendor product code label
  - preferred_table_fqn: dw_us.dws_disty_brpt_vpl_mtd
  - avoid_table_fqn: dw_us.dwd_disty_brpt_orders_pl_etl_mi unless order-line audit required; never use dim_pub_vpl_hierarchy_info for VPL label filters
  - time_pattern: latest open month or month-end `date_flag` snapshot; Phase-1 dim validation before fact aggregation
  - filter_note: resolve labels on `dim_us.dim_pub_vpl_info`; join serving on `vpl_no`; see golden `vpc-scanners-revenue-margin`

### oplgm_amt

- use_table_when: commission or sales OPL analysis at served grain
- avoid_table_when: cross-country parity audit (US chain verified; CA/BR/WCLA not fully reconciled)
- fallback_order: serving table → dw_us.dwd_disty_brpt_orders_pl_etl_mi

## Consistency and Conflict

### profitability_bundle

- consistency_status: Unknown
- conflict_summary: Multiple serving tables can answer the same metric at different slices; official module precedence not fully documented in metadata.
- decision_required: Confirm table priority by report module when siblings overlap.
