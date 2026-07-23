# Domains

## b_report（主域）

| 文件 | 版本 | 说明 |
|------|------|------|
| `b_report/ontology/objects.yaml` | 1.0.44 | 对象定义，hub = ShippedOrderLine |
| `b_report/ontology/relations.yaml` | 1.0.44 | JOIN 关系 |
| `b_report/ontology/metrics.yaml` | 1.0.44 | NET_SALES、NGM 等 |
| `b_report/domain.yaml` | — | Vertica + run_query_safely |

## 更新本体

```bash
SRC=bigdata-onto-agent/ontology_agent/backend/app/domains/b_report/ontology/versions
VER=1.0.44   # 换成最新版本目录名
cp $SRC/$VER/{objects,relations,metrics,main}.yaml domains/b_report/ontology/
```

## 新增域

复制 `_template/`，修改 `domain.yaml` 和 `ontology/`。
