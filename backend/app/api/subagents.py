"""Subagents configuration routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import get_user_id
from app.store.io import load_subagents_config, save_subagents_config
from app.store.schemas import SubAgentsConfig

router = APIRouter(prefix="/api/subagents", tags=["subagents"])


@router.get("")
async def get_subagents(user_id: str = Depends(get_user_id)):
    cfg = await load_subagents_config(user_id)
    return cfg.model_dump()


@router.put("")
async def put_subagents(body: SubAgentsConfig, user_id: str = Depends(get_user_id)):
    saved = await save_subagents_config(user_id, body)
    return saved.model_dump()
