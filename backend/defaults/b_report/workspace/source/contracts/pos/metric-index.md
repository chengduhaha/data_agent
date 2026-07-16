# Metric Index Contract Header

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: POS
- domain: POS

# Metric Index — POS

## Purpose

- Metric-first routing index for the POS domain.
- **Canonical source for all POS metric formulas.** Table L2 sections list metric names and point here.

## Metric Registry

### extend_net_price

- aliases: extended net price, POS sales amount, net sales
- business_definition: Extended net selling price for a shipped POS order line — standard POS revenue metric.
- final_effective_formula_sql: `extend_net_price` (stored column on hub) OR `unit_net_price * ship_qty` when unit-level validation needed
- formula_verification_status: verified
- formula_component_breakdown:
  - component: unit_net_price × ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di
  - meaning: line extended net price
- refresh_pattern: daily by date_flag
- owner_team: Disty POS reporting
- status: active

### unit_net_price

- aliases: unit net price
- business_definition: Per-unit net selling price on POS line.
- final_effective_formula_sql: `unit_net_price`
- formula_verification_status: verified
- formula_component_breakdown:
  - component: unit_net_price
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di.unit_net_price
  - meaning: unit net price before extension
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### ship_qty

- aliases: shipped quantity, qty
- business_definition: Quantity shipped on POS order line.
- final_effective_formula_sql: `ship_qty`
- formula_verification_status: verified
- formula_component_breakdown:
  - component: ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di.ship_qty
  - meaning: shipped units
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### extend_base_cost

- aliases: extended base cost, extended cost
- business_definition: Extended base cost for POS line.
- final_effective_formula_sql: `extend_base_cost` OR `base_cost * ship_qty`
- formula_verification_status: verified
- formula_component_breakdown:
  - component: base_cost × ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di
  - meaning: extended base cost
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### base_cost

- aliases: unit base cost
- business_definition: Per-unit base cost on POS line.
- final_effective_formula_sql: `base_cost`
- formula_verification_status: verified
- formula_component_breakdown:
  - component: base_cost
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di.base_cost
  - meaning: unit base cost
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### net_sales_with_expense

- aliases: net price including SCM expense, expense-inclusive net sales
- business_definition: Net sales recalculated to include unit SCM expense in unit price before extension.
- final_effective_formula_sql: `(unit_price + COALESCE(unit_sum_exp, 0)) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - component: unit_price × ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di.unit_price, ship_qty
  - meaning: base extended price
  - component: unit_sum_exp × ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di.unit_sum_exp, ship_qty
  - meaning: SCM expense included in price
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### scm_usage_amt

- aliases: SCM usage, unit_sum_exp extended
- business_definition: Extended SCM expense usage on POS line.
- final_effective_formula_sql: `COALESCE(unit_sum_exp, 0) * ship_qty` OR `extend_sum_exp` when populated
- formula_verification_status: verified
- formula_component_breakdown:
  - component: unit_sum_exp × ship_qty
  - sign: +
  - source: dw_us.dwd_disty_common_pos_di
  - meaning: SCM expense dollars
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### rebate_amt

- aliases: rebate amount, SPA rebate
- business_definition: Rebate amount from SPA/SCM claim detail at order line.
- final_effective_formula_sql: `rebate_amt` from SPA detail after ROW_NUMBER/pre-agg at order-line grain
- formula_verification_status: partial
- formula_component_breakdown:
  - component: rebate_amt
  - sign: +
  - source: dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di or dw_us.dwd_disty_scm_shipped_order_spa_di
  - meaning: vendor rebate on line
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### approved_cost

- aliases: approved cost, vendor approved cost
- business_definition: Vendor-approved cost from SPA/SCM detail.
- final_effective_formula_sql: `approved_cost` from SPA detail (pre-aggregated to order-line grain)
- formula_verification_status: partial
- formula_component_breakdown:
  - component: approved_cost
  - sign: +
  - source: SPA/SCM detail tables
  - meaning: approved vendor cost for claim
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

### credit_adjustment

- aliases: order type 114 credit, price protection
- business_definition: Credit/price-protection order amounts — not standard shipment sales.
- final_effective_formula_sql: `CASE WHEN order_type = 114 THEN extend_net_price ELSE 0 END` (or zero-out per vendor CPO rules)
- formula_verification_status: verified
- formula_component_breakdown:
  - component: extend_net_price when order_type=114
  - sign: +/-
  - source: dw_us.dwd_disty_common_pos_di
  - meaning: credit/protection adjustment separate from standard sales
- refresh_pattern: daily
- owner_team: Disty POS reporting
- status: active

## Metric-to-Table Mapping

### extend_net_price

- base_table_dwd: dw_us.dwd_disty_common_pos_di
- serving_tables:
  - table_fqn: dw_us.dwd_disty_common_pos_di
  - layer: DWD
  - aggregation_grain: order_no + order_type + order_line_no
  - dimensions: cust, vendor, sku, vpl, territory, order attributes on hub
  - time_grain: date_flag (daily)
  - refresh_pattern: daily incremental
  - quality_level: governed hub

### net_sales_with_expense / scm_usage_amt

- base_table_dwd: dw_us.dwd_disty_common_pos_di
- serving_tables:
  - table_fqn: dw_us.dwd_disty_common_pos_di (unit_sum_exp on hub)
  - layer: DWD
  - aggregation_grain: order line
  - dimensions: same as hub
  - time_grain: date_flag
  - refresh_pattern: daily
  - quality_level: governed; SPA detail tables for claim-level breakdown

### rebate_amt / approved_cost

- base_table_dwd: dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di
- serving_tables:
  - table_fqn: dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di
  - layer: DWD
  - aggregation_grain: scm/spa record; must pre-aggregate to POS line
  - dimensions: exp_code, claim_type, scm_no, spa_no
  - time_grain: date_flag
  - refresh_pattern: daily
  - quality_level: one-to-many — pre-agg required

## Selection Rules

### extend_net_price

- use_table_when:
  - table_fqn: dw_us.dwd_disty_common_pos_di
  - conditions: standard POS sales export, vendor/customer POS reports, default revenue metric
- avoid_table_when:
  - conditions: report explicitly requires expense-inclusive net price — use net_sales_with_expense instead
- fallback_order:
  - preferred: extend_net_price on hub
  - fallback: recalculate unit_net_price * ship_qty for validation

### net_sales_with_expense

- use_table_when:
  - conditions: historical report pattern adds unit_sum_exp to unit_price; SPA/SCM usage reporting
- avoid_table_when:
  - conditions: standard POS sales — use extend_net_price
- fallback_order:
  - preferred: hub unit_price + unit_sum_exp formula
  - fallback: join SPA detail for exp_code-level breakdown

### rebate_amt / approved_cost

- use_table_when:
  - conditions: SPA/SCM claim detail reports (rds_5380-style)
- avoid_table_when:
  - conditions: standard POS line export without claim columns
- fallback_order:
  - preferred: dwd_pub_common_shipped_order_scm_spa_detail_di
  - fallback: dwd_disty_scm_shipped_order_spa_di

### credit_adjustment

- use_table_when:
  - conditions: price protection, trailing credit, order_type 114 reports
- avoid_table_when:
  - conditions: standard sales revenue — exclude order_type 114
- fallback_order:
  - preferred: filter or segregate order_type 114 on hub

## Consistency and Conflict

### extend_net_price vs net_sales_with_expense

- consistency_status: related but not identical
- conflict_summary: extend_net_price is stored hub metric; net_sales_with_expense adds unit_sum_exp to unit_price — values differ when unit_sum_exp non-zero
- decision_required: Confirm with report request which definition matches historical RDS script

### SPA detail one-to-many

- consistency_status: grain conflict if not pre-aggregated
- conflict_summary: Multiple SPA rows per POS line multiply hub rows on direct join
- decision_required: Always pre-aggregate SPA detail before joining to hub for line-grain reports
