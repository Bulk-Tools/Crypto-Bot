from __future__ import annotations

import pandas as pd


def add_structure_features(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df["swing_high"] = df["high"][(df["high"] > df["high"].shift(1)) & (df["high"] > df["high"].shift(-1))]
    df["swing_low"] = df["low"][(df["low"] < df["low"].shift(1)) & (df["low"] < df["low"].shift(-1))]
    df["breakout_up"] = df["close"] > df["high"].rolling(20).max().shift(1)
    df["breakout_down"] = df["close"] < df["low"].rolling(20).min().shift(1)
    return df
