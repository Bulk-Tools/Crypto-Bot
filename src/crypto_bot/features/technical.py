from __future__ import annotations

import pandas as pd


def add_trend_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    df["sma_20"] = df["close"].rolling(20).mean()
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()
    fast = df["close"].ewm(span=12, adjust=False).mean()
    slow = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = fast - slow
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    return df
