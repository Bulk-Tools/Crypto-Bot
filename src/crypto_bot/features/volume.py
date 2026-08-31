from __future__ import annotations

import numpy as np
import pandas as pd


def add_volume_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df["volume_sma_20"] = df["volume"].rolling(20).mean()
    df["volume_ratio"] = df["volume"] / df["volume_sma_20"].replace(0, np.nan)
    direction = np.sign(df["close"].diff().fillna(0))
    df["obv"] = (direction * df["volume"]).cumsum()
    cumulative_vp = (df["close"] * df["volume"]).cumsum()
    cumulative_vol = df["volume"].cumsum().replace(0, np.nan)
    df["vwap"] = cumulative_vp / cumulative_vol
    return df
