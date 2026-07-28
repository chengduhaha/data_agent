# Examples index — `starrocks_pos`

- artifact_type: examples-index
- artifact_id: rds/starrocks_pos/examples-index
- source: `typical examples index.txt`
- note: Catalog only — never converted to `.sql` or Knowledgebase `.md`.

## Catalog

```text
StarRocks POS typical examples index

Use these examples as implementation references when generating StarRocks POS SQL. Load the POS reference files first, then open the closest example only when the requested report matches the business pattern.

1. typical_pos_spa_rebate_btl_17797.txt
   Source: US/run/rds_17797_rtv.sp
   Use when the request needs StarRocks POS output with SPA rebate/BTL-style enrichment and tempdb output patterns.

2. typical_pos_ship_bo_inventory_tracking_7522.txt
   Source: CA/run/rds_7522_rtv.sp
   Use when the request links shipped POS/order activity with backorder, inventory, or tracking-style enrichment.

3. typical_pos_vendor_so_fallback_18529.txt
   Source: US/run/rds_18529_rtv.sp
   Use when the request needs vendor SO fallback logic, POS/order enrichment, and StarRocks-specific join or filter patterns.
```
