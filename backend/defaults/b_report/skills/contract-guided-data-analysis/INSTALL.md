# Installing contract-guided-data-analysis

Portable skill package built from `bigdata_wiki_llm_1`. Contains **skill instructions + bundled knowledge** (~20MB).

## Package layout

```
contract-guided-data-analysis/
├── SKILL.md
├── INSTALL.md
├── pack.yaml
├── scripts/
│   ├── wkb_query.py
│   ├── wkb_index_builder.py
│   └── wkb/
├── references/
├── knowledge/
│   ├── contracts/
│   ├── ref/
│   ├── knowledgebase/
│   └── storage/wkb/
└── assets/
```

## Build from wiki (maintainers)

This skill package is **self-contained**: `SKILL.md`, `pack.yaml`, `INSTALL.md`, `references/`, and `assets/` are hand-authored and canonical **in this folder** — there is no parallel `.cursor/rules/` copy to maintain for analysis policy. `tools/build_skill_package.py` only (a) refreshes bundled `knowledge/` from the wiki's `source/`/`target/` trees and (b) zips this folder as-is; it does not regenerate or overwrite `references/`, `SKILL.md`, `pack.yaml`, or `INSTALL.md`.

```bash
cd bigdata_wiki_llm_1
python tools/build_skill_package.py
# → refreshes contract-guided-data-analysis/knowledge/ and scripts/wkb/
# → contract-guided-data-analysis.zip
```

## Install into Cursor

```bash
unzip contract-guided-data-analysis.zip -d ~/.cursor/skills/
# or project-local:
unzip contract-guided-data-analysis.zip -d your-repo/.cursor/skills/
```

Add Vertica MCP (see `references/mcp-setup.md`). Invoke with `@contract-guided-data-analysis` or let the agent auto-discover via description.

## Install into Claude Code

```bash
unzip contract-guided-data-analysis.zip -d ~/.claude/skills/
```

Configure Vertica MCP per Claude Code docs. Skill triggers on KPI / B Report / POS metric questions.

## Install into Codex / custom agents

1. Unzip to the agent's skill/plugin directory
2. Point the agent at `SKILL.md` as the skill entry
3. Mount `knowledge/` read-only; run WKB scripts from skill root
4. Register Vertica MCP with `run_query_safely`

## data_agent org pack (legacy sync)

`data_agent/scripts/sync_wiki_to_data_agent.py` still syncs from wiki directly.
To consume this package instead, point sync at `contract-guided-data-analysis/knowledge/`
and `references/` or replace `backend/defaults/b_report/skills/contract-guided-data-analysis/`.

## Updating knowledge

1. Edit contracts/knowledgebase in `bigdata_wiki_llm_1`
2. Rebuild WKB indexes in wiki if snapshots changed
3. Run `python tools/build_skill_package.py`
4. Redistribute zip to agents

## Optional output directory

By default analysis files go to `output/` under the skill root.
Agents that only support chat output can skip file writes — follow `SKILL.md` synthesis section only.
