# Data Agent

Cursor-grade general-purpose web agent: chat with a deep agent that has MCP, Skills, Rules, Subagents, Tools, filesystem/shell ops, and human-in-the-loop approvals — configured per user in the browser.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + [deepagents](https://github.com/langchain-ai/deepagents) (LangGraph) |
| Frontend | Next.js App Router, TypeScript, Tailwind |
| Shared org bundle | `backend/defaults/b_report/` (skills, knowledge, rules — read-only at runtime) |
| Per-user data | `workspace/{userid}/` (config, personal MCP, skills, rules, files, threads) |

## Quick start

```bash
cd data_agent
./scripts/setup.sh    # venv, pip, Node (nvm), npm install, default workspace
./scripts/seed_b_report.sh   # verify org bundle + .env.secrets (no per-user copy)
./scripts/service.sh start              # API :8000 + UI :6641 (background)
# or: ./scripts/dev.sh                  # same stack, foreground + --reload
```

Then open [http://127.0.0.1:6641](http://127.0.0.1:6641). SSO users land in `workspace/{cisLoginId}/`. With `OAUTH2_ENABLED=false`, the default workspace is `local`.

### Migrate legacy `backend/app/users/`

If upgrading from an older layout:

```bash
./scripts/migrate_workspace.sh
```

## Core vs Org Pack

Data Agent is split into two layers so the platform stays usable without any
enterprise content installed:

| Layer | What it is | Assumes org content? |
|-------|-----------|----------------------|
| **Agent Core** | `backend/app/agent/`, `backend/app/store/`, `backend/app/api/`, the harness middleware chain, streaming/SSE protocol, and the chat UI shell | **No.** Core never hardcodes `wkb_query`, Vertica, or `contract-guided-data-analysis`. |
| **Org Pack** (extension) | `backend/defaults/b_report/` — skills, a WKB knowledge index, rule fragments, and an MCP server manifest | Optional. Swappable via `DATA_AGENT_ORG_BUNDLE`; can be empty. |

**How the two connect** — `backend/app/agent/extensions/` (`CapabilityRegistry`):
every extra tool, MCP server, rule fragment, or harness budget a skill needs is
declared in that skill's own `SKILL.md` frontmatter (see
[`extensions/manifest.py`](backend/app/agent/extensions/manifest.py)):

```yaml
---
name: contract-guided-data-analysis
extensions:
  rules: [/rules/org/AGENTS.contract-skill.md]
  tools: [wkb_query]
  mcp: [gateway-vertica-prod]
harness:
  phases: [research, execute, synthesize]
  tool_budgets: { run_query_safely: 12, wkb_query: 8 }
  require_synthesis: true
---
```

`factory.py` calls `CapabilityRegistry.resolve(...)` and only instantiates
`wkb_query` (or connects `gateway-vertica-prod`) when a non-disabled skill
actually asks for it — with **zero org bundle** (`DATA_AGENT_ORG_BUNDLE=`
unset/empty, or the skill disabled via Settings), the agent runs with builtin
tools + any user-added MCP servers only.

**Swapping org packs**: set `DATA_AGENT_ORG_BUNDLE=<name>` and drop a
`backend/defaults/<name>/` directory with the same shape as `b_report/`
(`skills/`, `workspace/`, `fragments/`, `extensions/*.yaml`, and an optional
top-level `pack.manifest.yaml` describing the bundle). See
[`backend/defaults/b_report/pack.manifest.yaml`](backend/defaults/b_report/pack.manifest.yaml)
for a worked example, and
[`backend/defaults/b_report/extensions/vertica_mcp.yaml`](backend/defaults/b_report/extensions/vertica_mcp.yaml)
for the generic `${ENV_VAR}` MCP server template consumed by
[`app/org/mcp.py`](backend/app/org/mcp.py).

**User-level overrides** (`UserConfig`, editable from Settings):

| Field | Effect |
|-------|--------|
| `disabled_skills` | Hides a skill from the slash menu and excludes its `extensions.tools`/`extensions.mcp` from the agent. |
| `disabled_mcp_servers` | Excludes an MCP server (including org-managed ones) at agent-build time. |
| `feature_flags` | e.g. `show_sql_appendix`, `extended_run_default`. |

Debug endpoint: `GET /api/capabilities` returns exactly what was resolved for
the current user (tools, MCP servers, rule fragments, harness budgets).

## Storage model

```
data_agent/
  backend/
    skills_builtin/           # platform built-in skills (read-only)
    defaults/b_report/        # organization shared bundle (read-only), a.k.a. "Org Pack"
      pack.manifest.yaml      # bundle metadata (skills, extensions, required env)
      skills/
      workspace/              # org knowledge (mounted as /knowledge/org/)
      fragments/              # org rules (mounted as /rules/org/)
      extensions/             # MCP server manifests (e.g. vertica_mcp.yaml)
    app/config/llm_catalog.json
  workspace/
    {userid}/                 # personal isolated workspace
      config.json
      mcp.json                # personal MCP only (org MCP injected server-side)
      skills/                 # personal skills (CRUD)
      rules/AGENTS.md         # personal memory
      files/                  # personal /workspace/
      threads.sqlite
      threads_meta.json       # chat titles
```

**Shared vs personal**

| Resource | Scope | Agent paths |
|----------|-------|-------------|
| Built-in skills | All users | `/skills/builtin/` |
| Org skills (e.g. contract-guided) | All users, read-only | `/skills/org/` |
| Org knowledge (WKB, contracts) | All users, read-only | `/knowledge/org/` |
| Org rules fragments | All users, read-only | `/rules/org/` |
| Org Vertica MCP | Injected from `.env.secrets` | server-side only |
| Personal skills / rules / files / chats | Per `workspace/{userid}/` | `/skills/user/`, `/rules/AGENTS.md`, `/workspace/` |

## SSO login (platform-wide)

Web UI authentication uses **OAuth2/OIDC + PKCE** through the company **login-portal** (Microsoft Entra ID).

| Mode | Config | Behavior |
|------|--------|----------|
| **Default** | `OAUTH2_ENABLED=true` | Login required; each user gets `workspace/{cisLoginId}/` |
| **Local bypass** | `OAUTH2_ENABLED=false` | Anonymous dev user (`workspace/local/`) |

Register redirect URI on OAuth client `bigdata-ontology-agent`:

`http://bigdatauatgpu3.synnex.org:6641/api/auth/callback`

See `.env.example` for all `OAUTH2_*` variables.

## Architecture

```
Browser (Next.js + SSO cookie)
  ▼
FastAPI
  ▼
create_deep_agent(...)
  ├─ skills: builtin → org → user (last wins)
  ├─ memory: /rules/org/* + /rules/AGENTS.md
  ├─ MCP: org (server-side) + personal mcp.json
  ├─ CompositeBackend: /workspace/, /skills/*, /knowledge/org/, /rules/*
  └─ AsyncSqliteSaver → workspace/{id}/threads.sqlite
```

## API surface

- Auth: `/api/auth/*`
- Chat: `/api/chat/stream`, `/api/chat/resume`, `/api/chat/threads`
- Settings: `/api/config`, `/api/mcp`, `/api/skills`, `/api/rules`, `/api/files`, …
- Capabilities (debug/UI): `/api/capabilities` — tools/MCP/rules/harness actually resolved for the current user

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Security notes

- **Org MCP secrets** live in `.env.secrets` and are never returned to the browser.
- **Model catalog keys** are applied server-side; `GET /api/model-catalog` does not expose `api_key`.
- **Personal MCP** responses redact sensitive header/env values; masked PUTs preserve server-side secrets.
- Shell `execute` runs on the host inside the user's `files/` directory — not a container sandbox.

## Project layout

```
data_agent/
  backend/app/
  backend/defaults/b_report/
  backend/skills_builtin/
  workspace/                # per-user runtime (gitignored except structure)
  frontend/
  scripts/
    migrate_workspace.sh
    seed_b_report.sh        # verify org bundle (no copy)
  .env.example
  .env.secrets              # org MCP credentials (gitignored)
```
