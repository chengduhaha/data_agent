"""Skills CRUD routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.deps import get_user_id
from app.store.io import delete_user_skill, get_skill, list_skills, load_user_config, save_user_skill

router = APIRouter(prefix="/api/skills", tags=["skills"])


class SkillWrite(BaseModel):
    name: str
    content: str


@router.get("")
async def skills_list(include_disabled: bool = False, user_id: str = Depends(get_user_id)):
    cfg = await load_user_config(user_id)
    items = await list_skills(user_id, cfg)
    # Slash menu hides disabled skills entirely; Settings passes include_disabled=true.
    visible = items if include_disabled else [s for s in items if not s.disabled]
    return {"skills": [s.model_dump() for s in visible]}


@router.get("/{name}")
async def skills_get(name: str, source: str = "user", user_id: str = Depends(get_user_id)):
    if source not in ("builtin", "org", "user"):
        raise HTTPException(status_code=400, detail="Invalid source")
    skill = await get_skill(user_id, name, source=source)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.model_dump()


@router.put("/{name}")
async def skills_put(name: str, body: SkillWrite, user_id: str = Depends(get_user_id)):
    skill = await save_user_skill(user_id, body.name or name, body.content)
    return skill.model_dump()


@router.delete("/{name}")
async def skills_delete(name: str, user_id: str = Depends(get_user_id)):
    ok = await delete_user_skill(user_id, name)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"ok": True}
