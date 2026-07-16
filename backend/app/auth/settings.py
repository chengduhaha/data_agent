"""OAuth2/OIDC configuration from environment variables."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# data_agent/.env (repo root), not cwd-relative backend/.env
_REPO_ENV = Path(__file__).resolve().parents[3] / ".env"


class OAuth2Settings(BaseSettings):
    """OAuth2/OIDC + PKCE for data_agent Web UI login."""

    model_config = SettingsConfigDict(
        env_prefix="OAUTH2_",
        env_file=str(_REPO_ENV) if _REPO_ENV.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    enabled: bool = False
    client_id: str = ""
    authorize_url: str = ""
    token_url: str = ""
    userinfo_url: str = ""
    scopes: str = "openid profile email"
    redirect_uri: str = ""
    session_secret: str = ""
    button_label: str = "Log in with Microsoft Entra"
    cookie_secure: bool = False
    cookie_max_age_seconds: int = 604800
    idle_timeout_seconds: int = 86400
    frontend_origin: str = ""

    def is_configured(self) -> bool:
        return bool(
            self.enabled
            and self.client_id.strip()
            and self.authorize_url.strip()
            and self.token_url.strip()
            and self.userinfo_url.strip()
            and self.redirect_uri.strip()
            and self.session_secret.strip()
            and self.frontend_origin.strip()
        )


@lru_cache
def get_oauth_settings() -> OAuth2Settings:
    return OAuth2Settings()


def clear_oauth_settings_cache() -> None:
    clear = getattr(get_oauth_settings, "cache_clear", None)
    if callable(clear):
        clear()
