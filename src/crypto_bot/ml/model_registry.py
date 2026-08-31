from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ModelRegistry:
    def __init__(self, path: str | Path = "models/registry.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, metadata: dict[str, Any]) -> None:
        rows = self.read_all()
        rows.append(metadata)
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))
