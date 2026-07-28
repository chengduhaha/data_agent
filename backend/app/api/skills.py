"""Skills CRUD, zip upload, and platform publish routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.auth.models import AuthenticatedUser
from app.auth.roles import is_admin
from app.deps import get_current_user, require_admin
from app.store.io import (
    delete_user_skill,
    get_skill,
    install_user_skill_from_zip,
    list_skills,
    load_user_config,
    publish_user_skill_to_platform,
    save_user_skill,
)

router = APIRouter(prefix="/api/skills", tags=["skills"])


class SkillWrite(BaseModel):
    name: str
    content: str


@router.get("")
async def skills_list(
    include_disabled: bool = False,
    user: AuthenticatedUser = Depends(get_current_user),
):
    if include_disabled and not is_admin(user.workspace_slug):
        raise HTTPException(status_code=403, detail="Admin access required")
    user_id = user.workspace_slug
    cfg = await load_user_config(user_id)
    items = await list_skills(user_id, cfg)
    # Slash menu: hide disabled + default builtins. Settings uses include_disabled=true.
    if include_disabled:
        visible = items
    else:
        visible = [s for s in items if not s.disabled and not s.default_skill]
    return {"skills": [s.model_dump() for s in visible]}


@router.post("/upload")
async def skills_upload(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(require_admin),
):
    """Upload a skill.zip and install it as a personal skill (overwrite same name)."""
    user_id = user.workspace_slug
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()
    looks_like_zip = (
        filename.endswith(".zip")
        or "zip" in content_type
        or filename.endswith(".skill")
        or not filename  # some browsers omit name
    )
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty upload")
    # Windows may hide the .zip extension; accept ZIP local-file magic as fallback.
    if not looks_like_zip and not data.startswith(b"PK"):
        raise HTTPException(status_code=400, detail="Only .zip skill packages are supported")
    try:
        skill = await install_user_skill_from_zip(user_id, data)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001 — surface zip validation errors
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, "skill": skill.model_dump()}


@router.post("/{name}/publish")
async def skills_publish(name: str, user: AuthenticatedUser = Depends(require_admin)):
    """Publish a personal skill to the platform shared catalog (overwrite on name clash)."""
    user_id = user.workspace_slug
    try:
        result = await publish_user_skill_to_platform(user_id, name)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@router.get("/{name}")
async def skills_get(
    name: str,
    source: str = "user",
    user: AuthenticatedUser = Depends(get_current_user),
):
    if source not in ("builtin", "org", "user"):
        raise HTTPException(status_code=400, detail="Invalid source")
    skill = await get_skill(user.workspace_slug, name, source=source)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.model_dump()


@router.put("/{name}")
async def skills_put(
    name: str,
    body: SkillWrite,
    user: AuthenticatedUser = Depends(require_admin),
):
    skill = await save_user_skill(user.workspace_slug, body.name or name, body.content)
    return skill.model_dump()


@router.delete("/{name}")
async def skills_delete(name: str, user: AuthenticatedUser = Depends(require_admin)):
    ok = await delete_user_skill(user.workspace_slug, name)
    if not ok:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"ok": True}
