from __future__ import annotations

import pandas as pd


def add_momentum_indicators(frame: pd.DataFrame) -> pd.DataFrame:
    df = frame.copy()
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean().replace(0, 1e-9)
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))
    df["roc_10"] = df["close"].pct_change(10)
    return df
