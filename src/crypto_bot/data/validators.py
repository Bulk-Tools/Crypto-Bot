from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class DataQualityReport:
    valid: bool
    warnings: list[str]


def validate_ohlcv(df: pd.DataFrame) -> DataQualityReport:
    warnings: list[str] = []
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        return DataQualityReport(valid=False, warnings=[f"missing columns: {missing_cols}"])

    if df["timestamp"].duplicated().any():
        warnings.append("duplicate timestamps detected")
    if not df["timestamp"].is_monotonic_increasing:
        warnings.append("timestamps are out of order")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        warnings.append("non-positive price detected")
    if (df["volume"] < 0).any():
        warnings.append("negative volume detected")
    if ((df["high"] < df["low"]) | (df["high"] < df["open"]) | (df["high"] < df["close"]) | (df["low"] > df["open"]) | (df["low"] > df["close"])).any():
        warnings.append("impossible OHLC candle values detected")
    return DataQualityReport(valid=len(warnings) == 0, warnings=warnings)
