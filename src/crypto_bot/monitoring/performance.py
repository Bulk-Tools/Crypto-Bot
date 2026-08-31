from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_report(report: dict[str, Any], path: str = "reports/latest_report.json") -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
