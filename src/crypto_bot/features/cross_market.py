from __future__ import annotations

import pandas as pd


def add_cross_market_features(frame: pd.DataFrame, btc_dominance: float | None = None, eth_btc: float | None = None) -> pd.DataFrame:
    df = frame.copy()
    df["btc_dominance"] = btc_dominance
    df["eth_btc_ratio"] = eth_btc
    return df
