"""Parse company login-portal OIDC userinfo into normalized identity fields."""
from __future__ import annotations

import re
from typing import Any, Dict, Optional, TypedDict


class ParsedUserinfo(TypedDict):
    sub: str
    email: Optional[str]
    cis_login_id: Optional[str]
    global_user_id: Optional[str]
    display_name: Optional[str]


def parse_oidc_userinfo(userinfo: Dict[str, Any]) -> ParsedUserinfo:
    """Normalize userinfo from login-portal.

    Expected shape:
      {"globalUserId": 1338086, "cisLoginId": "jic", "email": "...", "sub": "..."}
    """
    sub = str(userinfo.get("sub") or "").strip()
    email_raw = userinfo.get("email")
    email = str(email_raw).strip() if email_raw is not None and str(email_raw).strip() else None

    cis_raw = userinfo.get("cisLoginId")
    cis_login_id = str(cis_raw).strip() if cis_raw is not None and str(cis_raw).strip() else None

    global_raw = userinfo.get("globalUserId")
    global_user_id = (
        str(global_raw).strip()
        if global_raw is not None and str(global_raw).strip()
        else None
    )

    legacy_name = userinfo.get("name") or userinfo.get("preferred_username")
    display_name = (
        str(legacy_name).strip()
        if legacy_name is not None and str(legacy_name).strip()
        else None
    )
    if not display_name:
        display_name = cis_login_id or email

    return ParsedUserinfo(
        sub=sub,
        email=email,
        cis_login_id=cis_login_id,
        global_user_id=global_user_id,
        display_name=display_name,
    )


def workspace_slug(cis_login_id: str | None, sub: str) -> str:
    """Filesystem-safe per-user workspace directory name."""
    raw = (cis_login_id or sub or "").strip()
    slug = re.sub(r"[^\w\-.@]", "_", raw)
    slug = slug.strip("._") or "user"
    if len(slug) > 64:
        slug = slug[:64]
    return slug
