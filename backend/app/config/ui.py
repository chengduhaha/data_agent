"""UI branding settings from environment (.env)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ENV = Path(__file__).resolve().parents[3] / ".env"


class UiSettings(BaseSettings):
    """Public UI branding (header subtitle under the main title)."""

    model_config = SettingsConfigDict(
        env_prefix="DATA_AGENT_",
        env_file=str(_REPO_ENV) if _REPO_ENV.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Shown as a small line under "Data Agent" in the chat header (empty = hidden).
    title_suffix: str = ""


@lru_cache
def get_ui_settings() -> UiSettings:
    return UiSettings()


def clear_ui_settings_cache() -> None:
    clear = getattr(get_ui_settings, "cache_clear", None)
    if callable(clear):
        clear()
