# Metric Index - order

- contract_version: v2.0.0
- artifact_type: metric-index
- artifact_id: order

## Purpose

- Metric-first routing index for the order domain.
- **Authoritative source** for metric formulas; Knowledgebase L2 copies formulas from here.

## Metric Registry


### pl_flag

- aliases:
- business_definition: `'Y'` for sales order types that are explicitly configured as P&L types in the PL code table, or for order type 1 which is always P&L eligible. All others get `'N'`.
- final_effective_formula_sql: `CASE WHEN a.sales = 'Y' AND (a.order_type = b.icode OR a.order_type = 1) THEN 'Y' ELSE 'N' END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### extend_exp

- aliases:
- business_definition: Total expenses/surcharges on the line.
- final_effective_formula_sql: `ship_qty * nvl(u_sum_expense, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### unit_net_price

- aliases:
- business_definition: Effective net unit price including expenses.
- final_effective_formula_sql: `u_price + nvl(u_sum_expense, 0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### extend_net_price

- aliases:
- business_definition: Total net revenue for the line.
- final_effective_formula_sql: `ship_qty * (u_price + nvl(u_sum_expense, 0))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### gm_amt

- aliases:
- business_definition: Gross margin amount using sales cost with unit cost fallback.
- final_effective_formula_sql: `(u_price − nvl(sales_cost, u_cost)) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### extend_base_cost_shipment

- aliases:
- business_definition: `coalesce(base_cost, 0) × ship_qty`
- final_effective_formula_sql: `coalesce(vpo_cost, 0) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### extend_base_cost_vpo

- aliases:
- business_definition: `coalesce(vpo_cost, 0) × ship_qty`
- final_effective_formula_sql: `coalesce(base_cost, 0) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### extra_u_exp

- aliases:
- business_definition: Placeholder — not populated from source in this version.
- final_effective_formula_sql: `CAST(NULL AS DECIMAL(19,4))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### net_sales

- aliases:
- business_definition: Revenue including summarized unit expenses.
- final_effective_formula_sql: `ship_qty * (u_price + u_sum_expense)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### net_cost

- aliases:
- business_definition: Cost including summarized unit expenses.
- final_effective_formula_sql: `ship_qty * (u_cost + u_sum_expense)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### tgm_amt

- aliases:
- business_definition: **Extended total gross margin** — all major PL components added to GM.
- final_effective_formula_sql: `gm_amt + btl + trans_btl + one_time_btl + hbtl + scm_profit_adj + btl_backout + pdt + inv_reserve + mof + marketing + frt_out_load + frt_out_exp + frt_ob_recovery + frt_ib_recovery + cust_pmt_disc + cust_rebate + cvr_rm + ap_adj + others + mfg_oh`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cogs

- aliases:
- business_definition: Cost of goods sold.
- final_effective_formula_sql: `nvl(sales_cost, u_cost) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### fx_cost

- aliases:
- business_definition: FX/sales-cost delta component.
- final_effective_formula_sql: `(nvl(sales_cost, u_cost) − u_cost) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### gv_user_type

- aliases:
- business_definition: GV history overrides source value; else keep source.
- final_effective_formula_sql: `nvl(hg.gv_user_type, twop.gv_user_type_old)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### ori_seg_code

- aliases:
- business_definition: Original segment: prefers SKU–PM preferred match, then fallback, then BRPT value. Pre-validation segment before VSEG check.
- final_effective_formula_sql: `coalesce(dsp.seg_code, dsp2.seg_code, twop.dim_seg_code)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cust_finance_ngm

- aliases:
- business_definition: Customer finance scaled by NGM CFNR rate.
- final_effective_formula_sql: `cust_finance * (p.mcode / nvl(nullif(p.icode2, 0), 1))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cr_risk_cterm_ngm

- aliases:
- business_definition: Credit risk scaled by NGM CRCR rate.
- final_effective_formula_sql: `cr_risk_cterm * (q.mcode / nvl(nullif(q.icode2, 0), 1))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sales_rep

- aliases:
- business_definition: If the order's entry user maps to a sales rep record, use their rep number; otherwise keep 0.
- final_effective_formula_sql: `CASE WHEN sr.user_id IS NOT NULL THEN sr.srep_no ELSE t1.sales_rep END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### u_sum_expense

- aliases:
- business_definition: Total DP per-unit expense on this order line.
- final_effective_formula_sql: `SUM(oe.unit_exp)` grouped by `order_type, order_no, order_line_no`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### division

- aliases:
- business_definition: Product codes in the 800–899 range map to division 1; all others keep their value (0 from temp1).
- final_effective_formula_sql: `CASE WHEN prod_code BETWEEN 800 AND 899 THEN 1 ELSE temp4.division END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### pm_code

- aliases:
- business_definition: If a VPL-part record exists for this vendor+SKU, use the `vpl_no` as the PM/VPL code; otherwise keep 0.
- final_effective_formula_sql: `CASE WHEN v.vend_no IS NOT NULL AND v.sku_no IS NOT NULL THEN v.vpl_no ELSE temp4.pm_code END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### date_flag

- aliases:
- business_definition: Converts the string date_flag from temp5 to a proper date type for partitioning.
- final_effective_formula_sql: `CAST(date_flag AS DATE)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### grid_price

- aliases:
- business_definition: Average new/contract cost for the line across the group.
- final_effective_formula_sql: `AVG(B.claim_new_cost)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### rebate

- aliases:
- business_definition: Total raw expense rebate amount on the line (0 when no expense).
- final_effective_formula_sql: `SUM(CASE WHEN he.unit_exp IS NULL THEN 0 ELSE he.unit_exp END)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### automatic_adjustment

- aliases:
- business_definition: SPA-weighted rebate/adjustment amount per line.
- final_effective_formula_sql: `Complex CASE — see detail below`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### etl_timestamp

- aliases:
- business_definition: ETL run time (Pacific).
- final_effective_formula_sql: `from_utc_timestamp(current_timestamp(), 'America/Los_Angeles')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sc_spa_keep_cpspa_profile_f

- aliases:
- business_definition: SPA rule keep % wins (higher).
- final_effective_formula_sql: `SC.spa_keep * HP.profile_f / 100`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### net_u_price

- aliases:
- business_definition: Domestic net unit price including unit expense component.
- final_effective_formula_sql: `a.u_price + a.u_sum_expense`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### fx_net_u_price

- aliases:
- business_definition: FX-side net unit price including aggregated line expense.
- final_effective_formula_sql: `nvl(oda.foreign_price,0) + nvl(uue.usd_unit_exp,0)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### usd_unit_exp

- aliases:
- business_definition: Total expense component per order line.
- final_effective_formula_sql: `sum(usd_unit_exp)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### total_sales

- aliases:
- business_definition: Net revenue for the line.
- final_effective_formula_sql: `ship_qty * (u_price + u_sum_expense)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### gm_rate

- aliases:
- business_definition: Gross margin % (0 if u_price is 0).
- final_effective_formula_sql: `((u_price − nvl(sales_cost, u_cost)) / nullif(u_price,0)) * 100`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### fx_net_price

- aliases:
- business_definition: FX net revenue for the line.
- final_effective_formula_sql: `(nvl(fx_u_price,0) + nvl(fx_u_expense,0)) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### exclude_rebate_flag

- aliases:
- business_definition: 'Y' if EX_REBATE profile is active.
- final_effective_formula_sql: `nvl(order_profile.exclude_rebate_flag, 'N')`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### vendor_appr_ref_no

- aliases:
- business_definition: Vendor approval reference — only populated for PM claim type 37.
- final_effective_formula_sql: `CASE WHEN claim_type = 37 THEN pri_approv_ref_no ELSE NULL END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### synnex_po_no

- aliases:
- business_definition: Internal Synnex PO number for drop-ship type-1 orders.
- final_effective_formula_sql: `CASE WHEN order_type=1 AND from_loc_no=98 AND from_inv_type IN(100,200) THEN int_ref_no ELSE NULL END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### cpo_no

- aliases:
- business_definition: CPO number: resolved from source SO for CM orders, otherwise the order's own ext_ref.
- final_effective_formula_sql: `CASE WHEN order_type IN(1,14) AND int_ref_type=1 THEN cn.cpo_no ELSE h.ext_ref END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### lol_reseller_no

- aliases:
- business_definition: LOL (line-of-line) reseller — only for agency/LOL sales models.
- final_effective_formula_sql: `CASE WHEN sales_model IN(1,3) THEN reseller_cust_no ELSE NULL END`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### big_deal_no

- aliases:
- business_definition: Big deal number: soldto field first, SPA_REF_NO profile fallback.
- final_effective_formula_sql: `nvl(s.big_deal_no, tpb.profile_c)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### sold_to_street_address

- aliases:
- business_definition: Street address for the sold-to location.
- final_effective_formula_sql: `max(concat(address1a, address1b))` per xref`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### tgm

- aliases:
- business_definition: Total Gross Margin — GM plus all major P&L adjustments plus FX/sales-cost delta.
- final_effective_formula_sql: `(u_price − nvl(sales_cost, u_cost)) * ship_qty + btl + one_time_btl + hbtl + scm_profit_adj + btl_backout + pdt + inv_reserve + mof + marketing + frt_out_load + frt_out_exp + frt_ob_recovery + frt_ib_recovery + cust_pmt_disc + cust_rebate + cvr_rm + margin_share + ap_adj + (nvl(sales_cost, u_cost) − u_cost) * ship_qty`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### ship_qty

- aliases:
- business_definition: Total units shipped.
- final_effective_formula_sql: `SUM(ship_qty)`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### nsales

- aliases:
- business_definition: Net sales — unit price plus expenses times quantity.
- final_effective_formula_sql: `SUM(ship_qty * (u_price + u_sum_expense))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### ncogs

- aliases:
- business_definition: Net cost of goods sold — unit cost plus expenses times quantity.
- final_effective_formula_sql: `SUM(ship_qty * (u_cost + u_sum_expense))`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### gm

- aliases:
- business_definition: Gross margin percentage for the order, signed, capped to avoid divide-by-zero distortion.
- final_effective_formula_sql: `sign(gross_margin_amt) * min(abs(gm% * 100), 99.99)` — signed, capped at ±99.99`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active

### oplgm

- aliases:
- business_definition: Operating profit margin % (or total order count in the summary rows).
- final_effective_formula_sql: `For low-OPLGM rows: signed OPLGM% (< 2), capped at ±99.99. For total-count rows: `COUNT(DISTINCT order_no)`.`
- formula_verification_status: partial
- formula_component_breakdown:
  - (append-only enricher entry; refine components in a follow-up if needed)
- refresh_pattern: not registered in metadata catalog
- owner_team: not registered in metadata catalog
- status: active
