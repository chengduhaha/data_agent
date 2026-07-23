# Sales knowledgebase

Domain folder for ETL under `sales/`.

## Documented scripts (in repository)

| Source | Knowledgebase doc | Vertica query table |
|--------|-------------------|---------------------|
| `source/etl/sql/sales/data_service/brpt_patch/python/load_dm_disty_brpt_lost_sales_di.py` | [load_dm_disty_brpt_lost_sales_di.md](load_dm_disty_brpt_lost_sales_di.md) |
| `source/etl/sql/sales/data_service/brpt_patch/python/load_dm_disty_brpt_sales_tam_qf.py` | [load_dm_disty_brpt_sales_tam_qf.md](load_dm_disty_brpt_sales_tam_qf.md) |

## Not documented (SQL missing from repository)

Azkaban flows reference sales-territory scoring ODS scripts under `source/etl/flows/public_order_tools/ingest/ods_etl/script/`; those `.sql` files are not checked in. See **Dependencies** section in [load_dm_disty_brpt_lost_sales_di.md](load_dm_disty_brpt_lost_sales_di.md) for flow citations.
