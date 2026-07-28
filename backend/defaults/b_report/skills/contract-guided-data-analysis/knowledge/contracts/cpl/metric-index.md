# Metric Index - cpl

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: cpl

## Purpose

- Metric-first routing index for the cpl domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### refer_flag

- aliases:
- business_definition: `'Y'` when the customer is NOT in public customer info (unresolved).
- final_effective_formula_sql: `CASE WHEN dim_pub_customer_info_df.cust_no IS NOT NULL THEN 'N' ELSE 'Y' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### insert_flag

- aliases:
- business_definition: `'Y'` when the customer is NOT yet in the CPL dim (new).
- final_effective_formula_sql: `CASE WHEN dim_disty_brpt_extract_cpl_cust.cust_no IS NOT NULL THEN 'N' ELSE 'Y' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_terr

- aliases:
- business_definition: Territory set only for new customers; NULL for existing ones.
- final_effective_formula_sql: `CASE WHEN d.cust_no IS NULL THEN m.sales_terr END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_type

- aliases:
- business_definition: Type set only for new customers; NULL for existing ones.
- final_effective_formula_sql: `CASE WHEN d.cust_no IS NULL THEN m.cust_type END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### frt_out_chg_to_cust_flag

- aliases:
- business_definition: `'Y'` if MyDaaS marks this code as charged to the deal.
- final_effective_formula_sql: `CASE WHEN e.chg_to_deal_flag = 'Y' THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### frt_out_exp_flag

- aliases:
- business_definition: `'Y'` if MyDaaS marks this code as outbound freight.
- final_effective_formula_sql: `CASE WHEN e.frt_out_flag = 'Y' THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### payroll_flag

- aliases:
- business_definition: `'Y'` if MyDaaS marks this GL account as payroll-related.
- final_effective_formula_sql: `CASE WHEN s.payroll_flag = 'Y' THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cash_flag

- aliases:
- business_definition: Terms represent a cash-payment arrangement.
- final_effective_formula_sql: `CASE WHEN t.risk_cash_flag = 'Y' THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cod_flag

- aliases:
- business_definition: Terms represent a COD arrangement.
- final_effective_formula_sql: `CASE WHEN t.risk_cod_flag = 'Y' THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### other_flag

- aliases:
- business_definition: `'N'` only when the code is cash or COD but NOT flagged as a standard risk term; `'Y'` otherwise (standard credit or unclassified).
- final_effective_formula_sql: `CASE WHEN (risk_cash_flag='Y' OR risk_cod_flag='Y') AND risk_term_flag <> 'Y' THEN 'N' ELSE 'Y' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### inv_type

- aliases:
- business_definition: Inventory type from history; defaults to `1` when history row is absent.
- final_effective_formula_sql: `nvl(h.from_inv_type, 1)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### hist_terr

- aliases:
- business_definition: Territory from order history first; falls back to customer master territory.
- final_effective_formula_sql: `nvl(h.sales_terr, c.sales_terr)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_sales_disty

- aliases:
- business_definition: Distributor flooring sales.
- final_effective_formula_sql: `SUM(floor_sales_disty)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_sales_dealer

- aliases:
- business_definition: Dealer flooring sales.
- final_effective_formula_sql: `SUM(floor_sales_dealer)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_sales_vend

- aliases:
- business_definition: Vendor flooring sales.
- final_effective_formula_sql: `SUM(floor_sales_vend)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_chgs_disty

- aliases:
- business_definition: Distributor flooring charges.
- final_effective_formula_sql: `SUM(floor_chgs_disty)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_chgs_dealer

- aliases:
- business_definition: Dealer flooring charges.
- final_effective_formula_sql: `SUM(floor_chgs_dealer)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### floor_chgs_vend

- aliases:
- business_definition: Vendor flooring charges.
- final_effective_formula_sql: `SUM(floor_chgs_vend)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### terms_sales_cash

- aliases:
- business_definition: Cash-terms sales.
- final_effective_formula_sql: `SUM(terms_sales_cash)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### terms_sales_cod

- aliases:
- business_definition: COD-terms sales.
- final_effective_formula_sql: `SUM(terms_sales_cod)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### period_dayxnpmt

- aliases:
- business_definition: Days-times-non-payment metric for the period.
- final_effective_formula_sql: `SUM(period_dayxnpmt)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### period_pmt

- aliases:
- business_definition: Period payment total.
- final_effective_formula_sql: `SUM(period_pmt)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### period_disc_taken

- aliases:
- business_definition: Period discount taken total.
- final_effective_formula_sql: `SUM(period_disc_taken)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sales

- aliases:
- business_definition: Revenue at shipped quantity × unit price for the order.
- final_effective_formula_sql: `SUM(o.ship_qty * o.u_price)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### exp

- aliases:
- business_definition: Expense portion; NULL unit expense treated as zero.
- final_effective_formula_sql: `SUM(o.ship_qty * nvl(o.u_sum_expense, 0))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cost

- aliases:
- business_definition: Cost of goods at shipped quantity × unit cost.
- final_effective_formula_sql: `SUM(o.ship_qty * o.u_cost)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
