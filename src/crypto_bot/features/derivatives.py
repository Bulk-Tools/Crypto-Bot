from __future__ import annotations

import pandas as pd


def add_derivatives_features(frame: pd.DataFrame, funding_rate: float | None, open_interest: float | None) -> pd.DataFrame:
    df = frame.copy()
    df["funding_rate"] = funding_rate
    df["open_interest"] = open_interest
    return df
