from __future__ import annotations

from pathlib import Path

import pandas as pd


class ParquetStore:
    def __init__(self, base_dir: str | Path = "data/parquet") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, symbol: str, timeframe: str, frame: pd.DataFrame) -> Path:
        out = self.base_dir / f"{symbol.replace('/', '_')}_{timeframe}.parquet"
        frame.to_parquet(out, index=False)
        return out

    def load(self, symbol: str, timeframe: str) -> pd.DataFrame:
        target = self.base_dir / f"{symbol.replace('/', '_')}_{timeframe}.parquet"
        if not target.exists():
            return pd.DataFrame()
        return pd.read_parquet(target)
