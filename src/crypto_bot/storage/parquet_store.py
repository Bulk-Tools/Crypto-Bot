from __future__ import annotations

from pathlib import Path

import pandas as pd

from .sqlite_store import SQLiteStore

try:
    import pyarrow  # noqa: F401

    HAS_PYARROW = True
except ImportError:
    HAS_PYARROW = False

try:
    import fastparquet  # noqa: F401

    HAS_FASTPARQUET = True
except ImportError:
    HAS_FASTPARQUET = False


class ParquetStore:
    def __init__(
        self,
        base_dir: str | Path = "data/parquet",
        fallback_dir: str | Path = "data/processed",
        sqlite_db_path: str | Path = "data/crypto_bot.db",
    ) -> None:
        self.base_dir = Path(base_dir).expanduser().resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.fallback_dir = Path(fallback_dir).expanduser().resolve()
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        self.sqlite_store = SQLiteStore(sqlite_db_path)
        self._has_parquet_engine = HAS_PYARROW or HAS_FASTPARQUET

    def _base_filename(self, symbol: str, timeframe: str) -> str:
        return f"{symbol.replace('/', '_')}_{timeframe}"

    def _csv_path(self, symbol: str, timeframe: str) -> Path:
        return self.fallback_dir / f"{self._base_filename(symbol, timeframe)}.csv.gz"

    def _parquet_path(self, symbol: str, timeframe: str) -> Path:
        return self.base_dir / f"{self._base_filename(symbol, timeframe)}.parquet"

    def save(self, symbol: str, timeframe: str, frame: pd.DataFrame) -> Path:
        parquet_path = self._parquet_path(symbol, timeframe)
        if self._has_parquet_engine:
            frame.to_parquet(parquet_path, index=False)
            return parquet_path

        self.sqlite_store.upsert_candles(symbol, timeframe, frame)
        csv_path = self._csv_path(symbol, timeframe)
        frame.to_csv(csv_path, index=False, compression="gzip")
        return csv_path

    def load(self, symbol: str, timeframe: str) -> pd.DataFrame:
        parquet_path = self._parquet_path(symbol, timeframe)
        if self._has_parquet_engine and parquet_path.exists():
            return pd.read_parquet(parquet_path)

        csv_path = self._csv_path(symbol, timeframe)
        if csv_path.exists():
            return pd.read_csv(csv_path, parse_dates=["timestamp"])

        return self.sqlite_store.load_candles(symbol, timeframe, limit=10_000)
