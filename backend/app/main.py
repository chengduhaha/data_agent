"""FastAPI entrypoint for data_agent."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.factory import close_checkpointers
from app.agent.mcp_manager import mcp_manager
from app.api import auth, chat, config_routes, files, mcp, rules, skills, subagents, tools
from app.auth.settings import get_oauth_settings
from app.deps import require_web_auth, require_admin
from app.store.paths import DEFAULT_USER_ID, ensure_user_layout

_REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_REPO_ROOT / ".env")
_secrets = _REPO_ROOT / ".env.secrets"
if _secrets.exists():
    load_dotenv(_secrets)

from app.auth.settings import clear_oauth_settings_cache

clear_oauth_settings_cache()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data_agent")


def _cors_origins() -> list[str]:
    oauth = get_oauth_settings()
    if oauth.enabled and oauth.is_configured() and oauth.frontend_origin.strip():
        return [oauth.frontend_origin.rstrip("/")]

    raw = os.getenv("DATA_AGENT_CORS_ORIGINS", "")
    if raw.strip():
        return [o.strip().rstrip("/") for o in raw.split(",") if o.strip()]

    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://localhost:6641",
        "http://127.0.0.1:6641",
        "http://bigdatauatgpu3.synnex.org:6641",
    ]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    ensure_user_layout(DEFAULT_USER_ID)
    logger.info("data_agent ready (default user=%s)", DEFAULT_USER_ID)
    yield
    await mcp_manager.invalidate(DEFAULT_USER_ID)
    await close_checkpointers()


app = FastAPI(
    title="data_agent",
    description="Cursor-grade general-purpose web agent (FastAPI + deepagents)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

protected = [Depends(require_web_auth)]
admin_only = [Depends(require_web_auth), Depends(require_admin)]

app.include_router(chat.router, dependencies=protected)
app.include_router(skills.router, dependencies=protected)
app.include_router(config_routes.router, dependencies=admin_only)
app.include_router(mcp.router, dependencies=admin_only)
app.include_router(rules.router, dependencies=admin_only)
app.include_router(subagents.router, dependencies=admin_only)
app.include_router(tools.router, dependencies=admin_only)
app.include_router(files.router, dependencies=admin_only)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "data_agent"}


@app.get("/")
async def root():
    return {
        "service": "data_agent",
        "docs": "/docs",
        "health": "/health",
    }
