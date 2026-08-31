from __future__ import annotations

from pathlib import Path

import pandas as pd

from .database import connect


class SQLiteStore:
    def __init__(self, db_path: str | Path = "data/crypto_bot.db") -> None:
        self.db_path = Path(db_path).expanduser().resolve()

    def upsert_candles(self, symbol: str, timeframe: str, frame: pd.DataFrame) -> int:
        if frame.empty:
            return 0
        conn = connect(self.db_path)
        rows = [
            (
                symbol,
                timeframe,
                row.timestamp.isoformat(),
                float(row.open),
                float(row.high),
                float(row.low),
                float(row.close),
                float(row.volume),
            )
            for row in frame.itertuples(index=False)
        ]
        with conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO candles
                (symbol, timeframe, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
        conn.close()
        return len(rows)

    def load_candles(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        conn = connect(self.db_path)
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM candles
            WHERE symbol = ? AND timeframe = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        frame = pd.read_sql_query(query, conn, params=[symbol, timeframe, limit])
        conn.close()
        if frame.empty:
            return frame
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        return frame.sort_values("timestamp").reset_index(drop=True)
