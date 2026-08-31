from __future__ import annotations

import pandas as pd


DEFAULT_FEATURES = [
    "sma_20",
    "ema_20",
    "macd",
    "rsi_14",
    "atr_14",
    "rolling_vol_20",
    "volume_ratio",
    "orderbook_imbalance",
    "funding_rate",
]


def feature_matrix(frame: pd.DataFrame, feature_names: list[str] | None = None) -> pd.DataFrame:
    names = feature_names or DEFAULT_FEATURES
    existing = [n for n in names if n in frame.columns]
    return frame[existing].fillna(0.0)
