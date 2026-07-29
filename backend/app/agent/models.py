"""Multi-provider model registry + Synnex gateway catalog."""

from __future__ import annotations

import os
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.agent.gemini_openai_compat import GeminiThoughtSignatureChatOpenAI, _is_gemini_model
from app.agent.model_catalog import (
    apply_profile_to_model_config,
    get_catalog_meta,
    get_profile,
    list_profiles,
)
from app.agent.harness.config import load_harness_config
from app.store.schemas import ModelConfig, ProviderInfo, UserConfig

_meta = get_catalog_meta()
_synnex_models = [p.id for p in list_profiles()]

PROVIDERS: list[ProviderInfo] = [
    ProviderInfo(
        id=_meta.provider_id,
        name=_meta.provider_name,
        kind="openai_compatible",
        default_base_url="",
        models=_synnex_models,
        requires_api_key=True,
    ),
    ProviderInfo(
        id="openai",
        name="OpenAI",
        kind="native",
        models=["gpt-4.1", "gpt-4.1-mini", "gpt-4o", "o3-mini", "o4-mini"],
    ),
    ProviderInfo(
        id="anthropic",
        name="Anthropic",
        kind="native",
        models=["claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5", "claude-3-5-sonnet-latest"],
    ),
    ProviderInfo(
        id="google_genai",
        name="Google Gemini",
        kind="native",
        models=["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"],
    ),
    ProviderInfo(
        id="deepseek",
        name="DeepSeek",
        kind="native",
        models=["deepseek-chat", "deepseek-reasoner"],
        default_base_url="https://api.deepseek.com",
    ),
    ProviderInfo(
        id="qwen",
        name="Qwen (DashScope)",
        kind="openai_compatible",
        default_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        models=["qwen-max", "qwen-plus", "qwen-turbo", "qwen-long"],
    ),
    ProviderInfo(
        id="zhipu",
        name="Zhipu GLM",
        kind="openai_compatible",
        default_base_url="https://open.bigmodel.cn/api/paas/v4",
        models=["glm-4-plus", "glm-4-flash", "glm-4.5"],
    ),
    ProviderInfo(
        id="moonshot",
        name="Moonshot / Kimi",
        kind="openai_compatible",
        default_base_url="https://api.moonshot.cn/v1",
        models=["moonshot-v1-auto", "moonshot-v1-128k", "kimi-k2-0711-preview"],
    ),
    ProviderInfo(
        id="ollama",
        name="Ollama (local)",
        kind="openai_compatible",
        default_base_url="http://127.0.0.1:11434/v1",
        models=["llama3.2", "qwen2.5", "deepseek-r1"],
        requires_api_key=False,
    ),
    ProviderInfo(
        id="openai_compatible",
        name="Custom OpenAI-compatible",
        kind="openai_compatible",
        default_base_url="",
        models=[],
    ),
]

_PROVIDER_MAP = {p.id: p for p in PROVIDERS}
_NATIVE = {"openai", "anthropic", "google_genai", "deepseek"}
_SYNNEX = _meta.provider_id


def list_providers() -> list[ProviderInfo]:
    return PROVIDERS


def _resolve_api_key(cfg: ModelConfig) -> str | None:
    if cfg.api_key:
        return cfg.api_key
    # Catalog profile key (UAT)
    profile = get_profile(cfg.model) if cfg.provider == _SYNNEX or get_profile(cfg.model) else None
    if profile and profile.api_key:
        return profile.api_key
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google_genai": "GOOGLE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "qwen": "DASHSCOPE_API_KEY",
        "zhipu": "ZHIPU_API_KEY",
        "moonshot": "MOONSHOT_API_KEY",
        _SYNNEX: "SYNNEX_API_KEY",
    }
    env_name = env_map.get(cfg.provider)
    if env_name:
        return os.getenv(env_name)
    return os.getenv("OPENAI_API_KEY") or os.getenv("SYNNEX_API_KEY")


def _normalize_cfg(cfg: ModelConfig | dict[str, Any] | UserConfig) -> ModelConfig:
    if isinstance(cfg, UserConfig):
        model_cfg = cfg.model.model_copy(deep=True)
    elif isinstance(cfg, dict):
        model_cfg = ModelConfig.model_validate(cfg.get("model", cfg))
    else:
        model_cfg = cfg.model_copy(deep=True)
    apply_profile_to_model_config(model_cfg)
    return model_cfg


def _build_openai_compatible(model_cfg: ModelConfig) -> ChatOpenAI:
    """Build ChatOpenAI for OpenAI-compatible or Azure deployment URLs."""
    name = (model_cfg.model or "").strip()
    profile = get_profile(name) if model_cfg.provider == _SYNNEX or get_profile(name) else None

    base_url = (model_cfg.base_url or "").rstrip("/")
    if not base_url and profile:
        base_url = profile.api_base
    meta = _PROVIDER_MAP.get(model_cfg.provider)
    if not base_url and meta and meta.default_base_url:
        base_url = meta.default_base_url.rstrip("/")
    if not base_url:
        raise ValueError(f"Provider '{model_cfg.provider}' requires a base_url.")

    api_key = _resolve_api_key(model_cfg) or "x"
    temperature = model_cfg.temperature if model_cfg.temperature is not None else 0.0
    api_version = (model_cfg.api_version or "").strip() or (profile.api_version if profile else None)
    api_model = (model_cfg.api_model or "").strip() or (profile.api_model if profile else None) or name
    max_tokens = model_cfg.max_tokens
    if max_tokens is None and profile:
        max_tokens = profile.max_tokens

    kwargs: dict[str, Any] = {
        "model": api_model,
        "api_key": api_key,
        "base_url": base_url,
        "temperature": temperature,
        "streaming": True,
    }
    if api_version:
        kwargs["default_query"] = {"api-version": api_version}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    harness = load_harness_config()
    kwargs["max_retries"] = harness.llm_max_retries

    llm_cls = GeminiThoughtSignatureChatOpenAI if _is_gemini_model(name) else ChatOpenAI
    return llm_cls(**kwargs)


def build_model(cfg: ModelConfig | dict[str, Any] | UserConfig) -> BaseChatModel:
    """Build a chat model from user config. Synnex catalog models resolve automatically."""
    model_cfg = _normalize_cfg(cfg)

    provider = (model_cfg.provider or "").strip()
    name = (model_cfg.model or "").strip()
    if not provider or not name:
        raise ValueError(
            "No model configured. Select a model from the chat toolbar or ask an admin to configure one."
        )

    temperature = model_cfg.temperature if model_cfg.temperature is not None else 0.0
    api_key = _resolve_api_key(model_cfg)

    # Synnex / catalog-backed / openai-compatible Azure deployment URLs
    if provider == _SYNNEX or (provider == "openai_compatible" and get_profile(name)):
        return _build_openai_compatible(model_cfg)

    if provider in _NATIVE:
        kwargs: dict[str, Any] = {
            "temperature": temperature,
            "streaming": True,
        }
        if api_key:
            kwargs["api_key"] = api_key
        if provider == "deepseek" and model_cfg.base_url:
            kwargs["base_url"] = model_cfg.base_url
        try:
            return init_chat_model(f"{provider}:{name}", **kwargs)
        except Exception:
            if provider == "deepseek":
                return ChatOpenAI(
                    model=name,
                    api_key=api_key or "x",
                    base_url=model_cfg.base_url or "https://api.deepseek.com",
                    temperature=temperature,
                    streaming=True,
                )
            raise

    return _build_openai_compatible(model_cfg)
