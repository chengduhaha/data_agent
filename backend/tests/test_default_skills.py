"""Default builtin skills (file-ops, web-research) are always on, not slash-invoked."""

from __future__ import annotations

from app.agent.extensions.default_skills import (
    DEFAULT_BUILTIN_SKILLS,
    default_skill_paths,
    is_default_builtin_skill,
)
from app.agent.factory import build_memory_paths


def test_default_builtin_skill_names() -> None:
    assert DEFAULT_BUILTIN_SKILLS == frozenset({"file-ops", "web-research"})
    assert is_default_builtin_skill("file-ops")
    assert not is_default_builtin_skill("ontology-query")


def test_default_skill_paths_in_memory() -> None:
    paths = build_memory_paths()
    for p in default_skill_paths():
        assert p in paths
