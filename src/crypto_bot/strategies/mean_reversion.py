from __future__ import annotations

import pandas as pd

from .models import StrategySignal


def evaluate(frame: pd.DataFrame) -> StrategySignal:
    latest = frame.iloc[-1]
    close = float(latest["close"])
    upper = latest.get("bb_upper")
    lower = latest.get("bb_lower")
    if upper is not None and close > float(upper):
        return StrategySignal("mean_reversion_v001", "SHORT", 65, "close above upper band", "reversion setup", "trend acceleration")
    if lower is not None and close < float(lower):
        return StrategySignal("mean_reversion_v001", "LONG", 65, "close below lower band", "reversion setup", "trend acceleration")
    return StrategySignal("mean_reversion_v001", "NO_TRADE", 43, "inside bands", "n/a", "n/a")
