"""Zip upload, validation, and publish helpers for standard skill packages."""

from __future__ import annotations

import io
import re
import shutil
import zipfile
from pathlib import Path

from fastapi import HTTPException

MAX_ZIP_BYTES = 100 * 1024 * 1024
_SAFE_NAME = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*$")


def _validate_member_name(name: str) -> None:
    if name.startswith("/") or ".." in Path(name).parts:
        raise HTTPException(status_code=400, detail=f"Unsafe zip path: {name}")


def _find_skill_md(root: Path) -> tuple[Path, str] | None:
    direct = root / "SKILL.md"
    if direct.exists():
        return direct, root.name
    for child in sorted(root.iterdir()):
        if child.is_dir():
            nested = child / "SKILL.md"
            if nested.exists():
                return nested, child.name
    return None


def extract_skill_zip(data: bytes, dest_parent: Path) -> tuple[Path, str]:
    """Extract zip to ``dest_parent/{name}/``; return (skill_dir, skill_name)."""
    if len(data) > MAX_ZIP_BYTES:
        raise HTTPException(status_code=413, detail="Zip exceeds 100MB limit")

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for info in zf.infolist():
            _validate_member_name(info.filename)

        tmp = dest_parent / "_zip_upload_tmp"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)

        zf.extractall(tmp)
        found = _find_skill_md(tmp)
        if not found:
            shutil.rmtree(tmp, ignore_errors=True)
            raise HTTPException(status_code=400, detail="Zip must contain SKILL.md at root or one subfolder")

        skill_md, skill_name = found
        if not _SAFE_NAME.match(skill_name):
            shutil.rmtree(tmp, ignore_errors=True)
            raise HTTPException(status_code=400, detail="Invalid skill directory name")

        skill_root_in_tmp = skill_md.parent
        final_dir = dest_parent / skill_name
        if final_dir.exists():
            shutil.rmtree(final_dir)
        shutil.move(str(skill_root_in_tmp), str(final_dir))

        # Clean leftover wrapper dir if zip had single top-level folder.
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)

        return final_dir, skill_name


def publish_skill_dir(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
