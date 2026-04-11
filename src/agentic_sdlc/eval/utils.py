"""Shared utilities for the eval package."""

from __future__ import annotations

from pathlib import Path


def rel(path: Path, root: Path) -> str:
    """Return path relative to root, falling back to str(path) if not under root."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
