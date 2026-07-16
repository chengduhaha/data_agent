# Graph Report - .  (2026-07-16)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 797 nodes · 1494 edges · 57 communities (41 shown, 16 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 212 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51

## God Nodes (most connected - your core abstractions)
1. `ensure_user_layout()` - 29 edges
2. `create_user_agent()` - 23 edges
3. `OAuth2Settings` - 17 edges
4. `AuthenticatedUser` - 16 edges
5. `compilerOptions` - 16 edges
6. `McpConfig` - 14 edges
7. `apiGet()` - 14 edges
8. `McpManager` - 13 edges
9. `build_model()` - 13 edges
10. `auth_callback()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `list_profiles()`  [INFERRED]
  scripts/test_synnex_models.py → backend/app/agent/model_catalog.py
- `test_model_catalog_never_exposes_api_key()` --calls--> `catalog_as_api()`  [INFERRED]
  backend/tests/test_productization.py → backend/app/agent/model_catalog.py
- `test_one()` --calls--> `build_model()`  [INFERRED]
  scripts/test_synnex_models.py → backend/app/agent/models.py
- `get_config()` --calls--> `load_user_config()`  [INFERRED]
  backend/app/api/config_routes.py → backend/app/store/io.py
- `_cors_origins()` --calls--> `get_oauth_settings()`  [INFERRED]
  backend/app/main.py → backend/app/auth/settings.py

## Import Cycles
- None detected.

## Communities (57 total, 16 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (78): build_backend(), Composite filesystem: personal workspace + shared org resources., delete_path(), FileWrite, list_files(), BaseModel, Path, Workspace file browser API. (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (49): McpManager, Any, BaseTool, Per-user MCP client manager using langchain-mcp-adapters., Hide Vertica metadata/discovery tools when a Vertica MCP server is enabled., Cache MultiServerMCPClient instances per user and expose tools., get_mcp(), mcp_tools() (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (38): AgentMiddleware, _float_env(), HarnessConfig, _int_env(), load_harness_config(), Harness configuration (env-driven execution controls)., recursion_limit(), get_harness_context() (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (41): AsyncSqliteSaver, get_builtin_tools(), _html_to_text(), _parse_ddg_html(), Any, Built-in tools beyond deepagents filesystem/shell suite., Fetch a URL and return cleaned text content (HTML tags stripped when possible)., Search the web via DuckDuckGo HTML results (no API key required).      Args: (+33 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (35): apply_profile_to_model_config(), catalog_as_api(), CatalogMeta, get_catalog_meta(), get_profile(), list_profiles(), _load_raw(), ModelProfile (+27 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (34): autoprefixer, dependencies, next, react, react-dom, react-markdown, remark-gfm, devDependencies (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (29): list_providers(), chat_resume(), chat_stream(), delete_thread(), get_thread(), Any, Chat streaming, resume (HITL), and thread management., Resume after a HITL interrupt with approve/reject decisions. (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (26): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (22): Candidate, CandidateSet, LayerHit, RetrievalResult, _add_undirected_neighbor(), build_indexes(), _candidate_id(), _flatten_text() (+14 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (19): Entry, AuthProvider(), apiUpload(), apiUrl(), AuthRequiredError, ChatMessage, ContinuePromptPayload, fetchOpts (+11 more)

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (14): ChatWindow(), threadTitlePreview(), uid(), ContinuePanel(), ContinuePromptPayload, HitlPanel(), Thread, ThreadSidebar() (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (17): _cache_tool_calls(), clear_tool_call_cache(), GeminiThoughtSignatureChatOpenAI, _has_thought_signature(), _is_gemini_model(), _lookup_tool_call(), _merge_tool_call_extras(), _patch_outbound_messages() (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.23
Nodes (13): AccountSettingsPage(), AuthGate(), LoginPage(), LoginPageShell(), UserMenu(), AuthContext, AuthContextType, useAuth() (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.19
Nodes (13): components, MarkdownRenderer(), MessageBubble(), extractQuery(), format(), isVerticaQueryTool(), ToolCallCard(), SubagentEvent (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (14): list_threads(), List chat threads for the current user's workspace., list_user_threads(), Any, Thread listing: merge per-user threads_meta with LangGraph checkpointer., List chat threads for sidebar — meta is primary, checkpointer enriches., _thread_row(), MonkeyPatch (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (11): _enabled_oauth_settings(), _patch_oauth_enabled(), MonkeyPatch, OAuth2/OIDC + PKCE + session unit tests., Ensure tests start from disabled OAuth unless explicitly patched., _reset_oauth_cache(), test_auth_bootstrap_unauthenticated_when_oauth_enabled(), test_auth_logout_clears_session_cookie() (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.16
Nodes (10): close_checkpointers(), get_rules(), put_rules(), BaseModel, Rules (AGENTS.md) routes., RulesBody, _cors_origins(), lifespan() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.32
Nodes (13): _extract_query_from_input(), _is_vertica_query_tool(), _message_text(), _preview_tool_input(), Any, Map LangGraph astream_events(v2) to typed SSE payloads., Truncate tool input for SSE, but preserve full SQL for Vertica query tools., Yield SSE strings from agent.astream_events(version='v2'). (+5 more)

### Community 18 - "Community 18"
Cohesion: 0.30
Nodes (12): auth_bootstrap(), auth_config(), auth_me(), AuthBootstrapResponse, AuthConfigResponse, AuthUserResponse, BaseModel, OAuth2/OIDC + PKCE authentication routes (BFF). (+4 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (12): auth_logout(), clear_oauth_settings_cache(), get_oauth_settings(), OAuth2/OIDC configuration from environment variables., get_current_user(), get_session_user(), get_user_id(), _oauth_enabled() (+4 more)

### Community 20 - "Community 20"
Cohesion: 0.25
Nodes (12): fold_checkpoint_messages(), _message_text(), Any, Fold LangGraph checkpoint messages into UI-friendly chat turns., Collapse LangGraph turns into user/assistant bubbles for the chat UI.      Inter, _role_of(), _tool_calls_of(), Tests for folding LangGraph checkpoint messages into chat UI turns. (+4 more)

### Community 21 - "Community 21"
Cohesion: 0.14
Nodes (6): OrgServer, Server, SubAgent, Tool, apiSend(), deleteThread()

### Community 22 - "Community 22"
Cohesion: 0.27
Nodes (11): Config, ModelSettingsPage(), Provider, ModelSwitcher(), Props, apiGet(), applyCatalogModel(), catalogLabel() (+3 more)

### Community 23 - "Community 23"
Cohesion: 0.29
Nodes (12): auth_callback(), delete_cookie_params(), dumps_flow(), dumps_session(), loads_flow(), loads_session(), Any, Signed cookie sessions for OAuth flow state and user sessions. (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.23
Nodes (10): build_authorize_url(), exchange_authorization_code(), fetch_userinfo(), OAuthClientError, Any, OAuth2/OIDC HTTP client (authorization code + PKCE, no client_secret)., OAuth2Settings, OAuth2/OIDC + PKCE for data_agent Web UI login. (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.24
Nodes (10): auth_login(), _require_oauth_config(), code_challenge_s256(), generate_code_verifier(), generate_oauth_state(), PKCE helpers (RFC 7636, S256)., URL-safe verifier, 43–128 chars per RFC 7636., test_oauth_state_unique() (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.20
Nodes (10): parse_oidc_userinfo(), ParsedUserinfo, Any, Parse company login-portal OIDC userinfo into normalized identity fields., Normalize userinfo from login-portal.      Expected shape:       {"globalUserId", Filesystem-safe per-user workspace directory name., workspace_slug(), test_parse_oidc_userinfo_company_portal() (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.38
Nodes (8): ChatInput(), SkillSlashMenu(), expandSkillMessage(), filterSlashSkills(), parseSlashSkillQuery(), skillVirtualPath(), SlashSkill, sourceLabel()

### Community 28 - "Community 28"
Cohesion: 0.40
Nodes (10): adapt_paths(), build_skill_md(), extract_mdc_body(), main(), merge_vertica_rule(), Path, sync_runtime(), sync_skill() (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.40
Nodes (9): main(), _norm(), _parse_sse(), Any, run_question(), RunResult, score_q1(), score_q2() (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.25
Nodes (6): fraunces, metadata, plex, sora, AppShell(), NAV

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (3): ACCOUNT_LINK, AGENT_LINKS, SettingsNav()

### Community 32 - "Community 32"
Cohesion: 0.60
Nodes (3): POST(), POST(), proxySse()

### Community 34 - "Community 34"
Cohesion: 0.70
Nodes (4): clearSessionActivity(), readLastActivity(), touchSessionActivity(), useIdleLogout()

### Community 36 - "Community 36"
Cohesion: 0.67
Nodes (3): NVM_DIR, start_daemon.sh script, stop_pid_file()

## Knowledge Gaps
- **76 isolated node(s):** `sora`, `fraunces`, `plex`, `metadata`, `Entry` (+71 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_user_agent()` connect `Community 3` to `Community 0`, `Community 2`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `ensure_user_layout()` connect `Community 0` to `Community 1`, `Community 3`, `Community 16`, `Community 19`, `Community 23`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `auth_callback()` connect `Community 23` to `Community 0`, `Community 18`, `Community 24`, `Community 25`, `Community 26`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `ensure_user_layout()` (e.g. with `build_backend()` and `create_user_agent()`) actually correct?**
  _`ensure_user_layout()` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `create_user_agent()` (e.g. with `get_builtin_tools()` and `load_harness_config()`) actually correct?**
  _`create_user_agent()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `OAuth2Settings` (e.g. with `AuthBootstrapResponse` and `AuthConfigResponse`) actually correct?**
  _`OAuth2Settings` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `AuthenticatedUser` (e.g. with `AuthBootstrapResponse` and `AuthConfigResponse`) actually correct?**
  _`AuthenticatedUser` has 5 INFERRED edges - model-reasoned connections that need verification._