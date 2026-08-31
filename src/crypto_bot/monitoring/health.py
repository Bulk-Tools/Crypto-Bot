from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from crypto_bot.storage.database import connect, init_db


@dataclass(slots=True)
class HealthStatus:
    name: str
    ok: bool
    message: str


def run_health_checks(db_path: str = "data/crypto_bot.db") -> list[HealthStatus]:
    statuses: list[HealthStatus] = []
    try:
        init_db(db_path)
        conn = connect(db_path)
        conn.execute("SELECT 1")
        conn.close()
        statuses.append(HealthStatus("database", True, "sqlite reachable"))
    except Exception as exc:
        statuses.append(HealthStatus("database", False, f"sqlite error: {exc}"))

    for folder in ["data/raw", "data/processed", "data/parquet", "logs", "reports"]:
        p = Path(folder)
        statuses.append(HealthStatus(folder, p.exists(), "present" if p.exists() else "missing"))
    return statuses
