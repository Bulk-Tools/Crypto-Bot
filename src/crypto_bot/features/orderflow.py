from __future__ import annotations

import pandas as pd


def add_orderflow_features(frame: pd.DataFrame, imbalance: float | None = None, spread: float | None = None) -> pd.DataFrame:
    df = frame.copy()
    df["orderbook_imbalance"] = imbalance if imbalance is not None else 0.0
    df["orderbook_spread"] = spread if spread is not None else 0.0
    return df
