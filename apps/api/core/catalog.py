from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = ROOT / "packages" / "catalog" / "algorithms.json"
PYTHON_PATH = ROOT / "algorithms" / "python" / "cp_algorithms.py"
CPP_PATH = ROOT / "algorithms" / "cpp" / "include" / "cp_algorithms.hpp"


@lru_cache
def algorithms() -> list[dict[str, Any]]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def algorithm_by_slug(slug: str) -> dict[str, Any] | None:
    return next((item for item in algorithms() if item["slug"] == slug), None)


@lru_cache
def code_sources() -> dict[str, str]:
    return {
        "python": PYTHON_PATH.read_text(encoding="utf-8"),
        "cpp": CPP_PATH.read_text(encoding="utf-8"),
    }
