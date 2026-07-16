"""Workspace file browser API."""

from __future__ import annotations

import shutil
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.deps import get_user_id
from app.store.io import resolve_workspace_path
from app.store.paths import ensure_user_layout, files_dir
from app.store.schemas import FileEntry

router = APIRouter(prefix="/api/files", tags=["files"])


class FileWrite(BaseModel):
    path: str
    content: str


@router.get("")
async def list_files(path: str = "", user_id: str = Depends(get_user_id)):
    ensure_user_layout(user_id)
    try:
        target = resolve_workspace_path(user_id, path or ".")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not target.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    if target.is_file():
        return {
            "entries": [
                FileEntry(
                    name=target.name,
                    path=_rel(user_id, target),
                    is_dir=False,
                    size=target.stat().st_size,
                ).model_dump()
            ]
        }
    entries: list[FileEntry] = []
    for child in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if child.name == ".gitkeep":
            continue
        entries.append(
            FileEntry(
                name=child.name,
                path=_rel(user_id, child),
                is_dir=child.is_dir(),
                size=None if child.is_dir() else child.stat().st_size,
            )
        )
    return {"path": _rel(user_id, target) if target != files_dir(user_id).resolve() else "", "entries": [e.model_dump() for e in entries]}


@router.get("/content")
async def read_file(path: str, user_id: str = Depends(get_user_id)):
    try:
        target = resolve_workspace_path(user_id, path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    async with aiofiles.open(target, encoding="utf-8", errors="replace") as f:
        content = await f.read()
    return {"path": _rel(user_id, target), "content": content}


@router.put("/content")
async def write_file(body: FileWrite, user_id: str = Depends(get_user_id)):
    try:
        target = resolve_workspace_path(user_id, body.path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(target, "w", encoding="utf-8") as f:
        await f.write(body.content)
    return {"path": _rel(user_id, target), "ok": True}


@router.delete("")
async def delete_path(path: str, user_id: str = Depends(get_user_id)):
    try:
        target = resolve_workspace_path(user_id, path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    root = files_dir(user_id).resolve()
    if target == root:
        raise HTTPException(status_code=400, detail="Cannot delete workspace root")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()
    return {"ok": True}


@router.post("/upload")
async def upload_file(
    path: str = "",
    file: UploadFile = File(...),
    user_id: str = Depends(get_user_id),
):
    rel = f"{path.rstrip('/')}/{file.filename}" if path else (file.filename or "upload.bin")
    try:
        target = resolve_workspace_path(user_id, rel)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    data = await file.read()
    async with aiofiles.open(target, "wb") as f:
        await f.write(data)
    return {"path": _rel(user_id, target), "size": len(data)}


def _rel(user_id: str, path: Path) -> str:
    root = files_dir(user_id).resolve()
    try:
        return str(path.resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        return path.name
