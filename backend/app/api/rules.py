"""Rules (AGENTS.md) routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.deps import get_user_id
from app.store.io import load_rules, save_rules

router = APIRouter(prefix="/api/rules", tags=["rules"])


class RulesBody(BaseModel):
    content: str


@router.get("")
async def get_rules(user_id: str = Depends(get_user_id)):
    content = await load_rules(user_id)
    return {"content": content}


@router.put("")
async def put_rules(body: RulesBody, user_id: str = Depends(get_user_id)):
    content = await save_rules(user_id, body.content)
    return {"content": content}
