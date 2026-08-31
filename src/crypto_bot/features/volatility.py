from __future__ import annotations

import pandas as pd


def add_volatility_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - df["close"].shift()).abs(),
            (df["low"] - df["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    df["atr_14"] = tr.rolling(14).mean()
    rolling = df["close"].rolling(20)
    mean = rolling.mean()
    std = rolling.std()
    df["bb_upper"] = mean + 2 * std
    df["bb_lower"] = mean - 2 * std
    df["rolling_vol_20"] = df["close"].pct_change().rolling(20).std()
    return df
