from __future__ import annotations

from contextlib import contextmanager

import pandas as pd
from joblib import parallel_backend


DEFAULT_N_JOBS = 1


@contextmanager
def threading_backend():
    with parallel_backend("threading"):
        yield


def build_target(frame: pd.DataFrame, up_pct: float = 0.01, down_pct: float = 0.01, horizon: int = 12) -> pd.Series:
    future_max = frame["high"].shift(-horizon).rolling(horizon).max()
    future_min = frame["low"].shift(-horizon).rolling(horizon).min()
    up_hit = (future_max / frame["close"] - 1) >= up_pct
    down_hit = (1 - future_min / frame["close"]) >= down_pct
    return (up_hit & ~down_hit).astype(int)
