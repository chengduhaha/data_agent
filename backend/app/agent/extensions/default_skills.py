"""Built-in skills that are always on and not slash-invoked."""

from __future__ import annotations

# Guidance-only builtins: tools already exist; no `/skill` entry in chat menu.
DEFAULT_BUILTIN_SKILLS: frozenset[str] = frozenset({"file-ops", "web-research"})


def is_default_builtin_skill(name: str) -> bool:
    return name in DEFAULT_BUILTIN_SKILLS


def default_skill_paths() -> list[str]:
    return [f"/skills/builtin/{name}/SKILL.md" for name in sorted(DEFAULT_BUILTIN_SKILLS)]
