# Golden Questions Contract Header

- contract_version: v2.0.0
- artifact_type: golden-questions
- artifact_id: POS
- domain: POS

# Golden Questions — POS

## Q1: SPA/SCM claim detail at order-line grain

**Question:** How do I produce a POS report with SPA/SCM expense codes, claim types, rebate, and approved cost at order-line grain for a vendor?

**Answer:** Start from `dw_us.dwd_disty_common_pos_di` with standard filters (`order_line_type <> 'Comp'`, date range on `date_flag`). LEFT JOIN `dw_us.dwd_pub_common_shipped_order_scm_spa_detail_di` (or `dw_us.dwd_disty_scm_shipped_order_spa_di`) on `order_no`, `order_type`, `order_line_no`. Pre-aggregate SPA rows with `ROW_NUMBER() OVER (PARTITION BY order_no, order_type, order_line_no ORDER BY scm_no)` or pivot first/second SPA values — do not direct-join without grain control. Metrics: see `metric-index.md` (`rebate_amt`, `approved_cost`, `scm_usage_amt`).

## Q2: RMA and original sales order tracing

**Question:** For return orders, how do I find the original SO number and RMA number?

**Answer:** From `dw_us.dwd_disty_common_pos_di`, use `int_ref_type` and `int_ref_no`: type 1 indicates original SO reference, type 9 indicates RMA reference. Use CASE logic to expose `original_so_no` and `rma_no` separately. Filter by customer and order types as needed (e.g. order_type IN (14,16) for returns).

## Q3: Serial authorization on POS export

**Question:** How do I include serial numbers on a POS vendor export?

**Answer:** Hub column `serial_no` may contain delimiter-separated values (replace `*` with `,` for display). For line-level serial detail, join `dw_us.dwd_disty_common_order_serial_no_di` on order keys — aggregate with LISTAGG if report grain stays order-line. Use serial-level grain only when one row per serial is required.

## Q4: Sales credit / price protection (order_type 114)

**Question:** How do I report price protection or trailing credit separately from normal sales?

**Answer:** `order_type = 114` represents credit/protection behavior — exclude from standard POS revenue. For dedicated credit reports, include order_type 114 and apply vendor-specific zero-out rules on net amounts when required. See `metric-index.md` → `credit_adjustment`.

## Q5: Backorder / shipping multisheet POS report

**Question:** How do I combine POS shipment data with backorder or open-order context?

**Answer:** Join `dw_us.dwd_disty_brpt_bo_detail_df` or open order tables (`dw_us.dwd_disty_sales_open_order_detail`) to hub on `order_no`, `order_type`, `order_line_no` when comparing shipped POS to BO/open lines. Preserve POS grain with LEFT JOIN from hub.

## Q6: Basic vendor-filtered POS monthly export

**Question:** How do I export last month's POS shipments for a specific vendor?

**Answer:**

```sql
SELECT order_no, order_type, order_line_no, date_flag, sku_no, part_no,
       ship_qty, extend_net_price, vend_no, vend_name, bill_to_cust_name
FROM dw_us.dwd_disty_common_pos_di
WHERE date_flag >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -1))
  AND date_flag < DATE_TRUNC('month', CURRENT_DATE)
  AND order_line_type <> 'Comp'
  AND order_type <> 114
  AND vend_no = :vend_no
ORDER BY date_flag;
```

Metrics: `extend_net_price`, `ship_qty` per `metric-index.md`.
