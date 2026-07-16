# Contract-guided data analysis bundle (committed defaults)

Source-of-truth for seeding the **contract-guided-data-analysis** skill into data_agent (domains: `b-report-us`, `pos`).

## Layout

```text
skills/contract-guided-data-analysis/   # adapted skill (chat-only, /workspace paths)
workspace/                              # becomes /workspace at seed time
  source/contracts/{b-report-us,pos}/
  source/ref/{b-report-us,pos}/
  target/knowledgebase/{b-report-us,pos}/
  target/storage/wkb/snapshots/...      # l1_catalog metadata (per domain)
  tools/wkb/indexing/                   # stdlib TF-IDF retrieval
fragments/
  config.patch.json                     # approve_execute=false; generic system_prompt
  AGENTS.section.md                     # skill-triggered guardrails (not global identity)
  contract-data-analysis-vertica.md     # read when using the skill (not always-injected)
  mcp.example.json                      # PLACEHOLDER secrets only
```

## Harness parity with Cursor

| Dimension | Cursor | data_agent (runtime mount) |
|-----------|--------|----------------------------|
| Trigger unit | `contract-guided-data-analysis` skill | Same skill at `/skills/org/` |
| Domain scope | `b-report-us` + `pos` | Same at `/knowledge/org/` |
| Vertica rule | Conditional (when using skill) | `/rules/org/contract-data-analysis-vertica.md` |
| Identity | General agent | Personal `workspace/{id}/rules/AGENTS.md` + org fragments |
| Trigger | Skill description + rule | Skill metadata + merged rules |

## Secrets

Real Vertica credentials live in untracked `data_agent/.env.secrets` (see project root). Org MCP is injected server-side — never copied into per-user `mcp.json`.

## Verify bundle

From `data_agent/`:

```bash
./scripts/seed_b_report.sh
```

This **verifies** the bundle layout and optional `.env.secrets` — it does **not** copy into per-user workspaces. All users share this bundle read-only at runtime via `factory.py` mounts.

## Notes

- Wiki repo `bigdata_wiki_llm_1` was a one-time vendor source; runtime does not depend on it.
- `backend/app/agent/factory.py` mounts org skills/knowledge/rules and merges personal `/rules/AGENTS.md` into memory.
