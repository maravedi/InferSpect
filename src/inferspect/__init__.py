"""InferSpect automation helpers exposed as a Python package."""

from __future__ import annotations

from importlib import metadata
from importlib.metadata import PackageNotFoundError

__all__ = ("get_package_version",)


def get_package_version() -> str:
    """Return the installed InferSpect distribution version."""
    try:
        return metadata.version("inferspect")
    except PackageNotFoundError as exc:
        raise RuntimeError(
            "InferSpect package metadata not found. Install via `poetry install`."
        ) from exc
