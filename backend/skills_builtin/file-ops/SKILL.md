---
name: file-ops
description: Best practices for reading, writing, editing, and organizing files in the /workspace/ directory.
license: MIT
---

# File Operations Skill

## When to Use
- Creating or editing files in the user workspace
- Exploring project structure
- Refactoring or organizing content on disk

## Guidelines
1. Prefer paths under `/workspace/` for durable user artifacts.
2. Use `ls`, `glob`, and `grep` before making large edits so you understand context.
3. Prefer `edit_file` for surgical changes; use `write_file` for new files or full rewrites.
4. Keep changes minimal and reversible.
5. After writes, briefly confirm what changed.

## Safety
- Avoid deleting important files unless the user explicitly asks.
- Shell `execute` may require human approval — explain the command first.
