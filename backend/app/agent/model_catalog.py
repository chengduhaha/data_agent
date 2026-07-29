"""Synnex AI Gateway model catalog (UAT presets).

Loads profiles from ``app/config/llm_catalog.json`` at runtime.
Keys are embedded for internal UAT — see README.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_CATALOG_PATH = Path(__file__).resolve().parent.parent / "config" / "llm_catalog.json"


@dataclass(frozen=True)
class ModelProfile:
    id: str
    display_name: str
    api_base: str
    provider_type: str  # openai | azure
    api_key: str
    api_version: str | None = None
    api_model: str | None = None
    temperature: float = 0.1
    max_tokens: int = 8192


@dataclass(frozen=True)
class CatalogMeta:
    provider_id: str
    provider_name: str
    provider_kind: str
    description: str
    default_model: str
    default_temperature: float
    default_max_tokens: int
    shared_api_key: str


_CATALOG_PATH = Path(__file__).resolve().parent.parent / "config" / "llm_catalog.json"
_cached_mtime: float | None = None
_cached_raw: dict[str, Any] | None = None


def _load_raw() -> dict[str, Any]:
    """Load catalog JSON; re-read when the file mtime changes."""
    global _cached_mtime, _cached_raw
    mtime = _CATALOG_PATH.stat().st_mtime
    if _cached_raw is not None and _cached_mtime == mtime:
        return _cached_raw
    with _CATALOG_PATH.open(encoding="utf-8") as f:
        _cached_raw = json.load(f)
    _cached_mtime = mtime
    return _cached_raw


def reload_catalog() -> None:
    """Force re-read of llm_catalog.json on next access."""
    global _cached_mtime, _cached_raw
    _cached_mtime = None
    _cached_raw = None


def get_catalog_meta() -> CatalogMeta:
    raw = _load_raw()
    provider = raw["provider"]
    defaults = raw["defaults"]
    return CatalogMeta(
        provider_id=provider["id"],
        provider_name=provider["name"],
        provider_kind=provider.get("kind", "openai_compatible"),
        description=provider.get("description", ""),
        default_model=defaults["default_model"],
        default_temperature=float(defaults.get("temperature", 0.1)),
        default_max_tokens=int(defaults.get("max_tokens", 8192)),
        shared_api_key=defaults["api_key"],
    )


def list_profiles() -> list[ModelProfile]:
    raw = _load_raw()
    meta = get_catalog_meta()
    out: list[ModelProfile] = []
    for m in raw["models"]:
        key = m.get("api_key") or meta.shared_api_key
        out.append(
            ModelProfile(
                id=m["id"],
                display_name=m.get("display_name") or m["id"],
                api_base=m["api_base"].rstrip("/"),
                provider_type=m.get("provider_type") or "openai",
                api_key=key,
                api_version=m.get("api_version") or None,
                api_model=m.get("api_model") or None,
                temperature=meta.default_temperature,
                max_tokens=meta.default_max_tokens,
            )
        )
    return out


def get_profile(model_id: str) -> ModelProfile | None:
    mid = (model_id or "").strip()
    if not mid:
        return None
    for p in list_profiles():
        if p.id == mid:
            return p
    return None


def catalog_as_api() -> dict[str, Any]:
    """Serialize catalog for frontend Settings UI."""
    meta = get_catalog_meta()
    return {
        "provider_id": meta.provider_id,
        "provider_name": meta.provider_name,
        "description": meta.description,
        "default_model": meta.default_model,
        "defaults": {
            "temperature": meta.default_temperature,
            "max_tokens": meta.default_max_tokens,
        },
        "models": [
            {
                "id": p.id,
                "display_name": p.display_name,
                "api_base": p.api_base,
                "provider_type": p.provider_type,
                "api_version": p.api_version,
                "api_model": p.api_model,
                "has_api_key": bool(p.api_key),
                "temperature": p.temperature,
                "max_tokens": p.max_tokens,
            }
            for p in list_profiles()
        ],
    }


def apply_profile_to_model_config(cfg: Any) -> Any:
    """Resolve ModelConfig from catalog when using the Synnex provider.

    For ``provider=synnex``, catalog is the source of truth for base_url /
    api_version / api_model (and api_key when empty) so switching models
    never leaves a stale Azure deployment URL.

    Mutates and returns the same ModelConfig instance.
    """
    provider = (getattr(cfg, "provider", None) or "").strip()
    model = (getattr(cfg, "model", None) or "").strip()
    meta = get_catalog_meta()

    # Never hijack native / third-party providers (e.g. openai + gpt-4o)
    if provider and provider not in (meta.provider_id, "openai_compatible", ""):
        return cfg

    profile = get_profile(model) if model else None
    if profile is None:
        if not provider and not model:
            profile = get_profile(meta.default_model)
        elif provider == meta.provider_id:
            profile = get_profile(meta.default_model)
        else:
            return cfg

    # Catalog model under empty / openai_compatible → promote to synnex
    if not provider or provider == "openai_compatible":
        cfg.provider = meta.provider_id
    if not cfg.model:
        cfg.model = profile.id

    # Always sync endpoint fields from the selected catalog profile
    cfg.base_url = profile.api_base
    cfg.api_version = profile.api_version or ""
    cfg.api_model = profile.api_model or ""
    # Catalog owns keys per model (shared UAT key)
    cfg.api_key = profile.api_key
    if getattr(cfg, "max_tokens", None) is None:
        cfg.max_tokens = profile.max_tokens
    else:
        cfg.max_tokens = cfg.max_tokens or profile.max_tokens
    if cfg.temperature is None or cfg.temperature == 0.0:
        cfg.temperature = profile.temperature
    return cfg
