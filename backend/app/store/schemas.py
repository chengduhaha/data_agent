"""Pydantic schemas for user configuration and API payloads."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    provider: str = ""
    model: str = ""
    api_key: str = ""
    base_url: str = ""
    temperature: float = 0.0
    api_version: str = ""
    api_model: str = ""
    max_tokens: int | None = None


class PermissionRule(BaseModel):
    operations: list[Literal["read", "write"]] = Field(default_factory=lambda: ["read", "write"])
    paths: list[str] = Field(default_factory=lambda: ["/**"])
    mode: Literal["allow", "deny", "interrupt"] = "allow"


class UserConfig(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    system_prompt: str = (
        "You are a helpful, careful general-purpose agent. "
        "Prefer using skills, tools, and the workspace under /workspace/."
    )
    approve_writes: bool = True
    approve_execute: bool = True
    enabled_tools: dict[str, bool] = Field(
        default_factory=lambda: {"web_fetch": True, "web_search": True}
    )
    permissions: list[PermissionRule] = Field(default_factory=list)


class McpServerConfig(BaseModel):
    transport: Literal["stdio", "streamable_http", "sse"] = "stdio"
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    url: str | None = None
    headers: dict[str, str] = Field(default_factory=dict)
    enabled: bool = True


class McpConfig(BaseModel):
    mcpServers: dict[str, McpServerConfig] = Field(default_factory=dict)


class SubAgentSpec(BaseModel):
    name: str
    description: str
    system_prompt: str
    tools: list[str] = Field(default_factory=list)
    model: str | None = None
    skills: list[str] = Field(default_factory=list)


class SubAgentsConfig(BaseModel):
    subagents: list[SubAgentSpec] = Field(default_factory=list)


class ChatStreamRequest(BaseModel):
    message: str = ""
    thread_id: str | None = None
    title: str | None = None  # UI display title (e.g. before skill expansion)
    continue_run: bool = False
    extended_run: bool = False


class ChatResumeRequest(BaseModel):
    thread_id: str
    decisions: list[dict[str, Any]] = Field(default_factory=list)


class ProviderInfo(BaseModel):
    id: str
    name: str
    kind: Literal["native", "openai_compatible"]
    default_base_url: str | None = None
    models: list[str] = Field(default_factory=list)
    requires_api_key: bool = True


class SkillInfo(BaseModel):
    name: str
    description: str = ""
    source: Literal["builtin", "org", "user"]
    path: str
    content: str | None = None
    editable: bool = False


class FileEntry(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: int | None = None


class ToolInfo(BaseModel):
    name: str
    description: str
    source: Literal["builtin", "mcp", "deepagents"]
    enabled: bool = True
