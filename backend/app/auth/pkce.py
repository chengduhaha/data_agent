"""PKCE helpers (RFC 7636, S256)."""
from __future__ import annotations

import base64
import hashlib
import secrets


def generate_code_verifier(length: int = 64) -> str:
    """URL-safe verifier, 43–128 chars per RFC 7636."""
    if length < 43 or length > 128:
        raise ValueError("code_verifier length must be between 43 and 128")
    return secrets.token_urlsafe(length)[:length]


def code_challenge_s256(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def generate_oauth_state() -> str:
    return secrets.token_urlsafe(32)
