from __future__ import annotations

import pandas as pd

from .models import StrategySignal


def evaluate(frame: pd.DataFrame) -> StrategySignal:
    latest = frame.iloc[-1]
    if latest.get("ema_20", 0) > latest.get("sma_20", 0):
        return StrategySignal("trend_v001", "LONG", 70, "EMA above SMA", "trend continuation", "EMA crosses below SMA")
    if latest.get("ema_20", 0) < latest.get("sma_20", 0):
        return StrategySignal("trend_v001", "SHORT", 70, "EMA below SMA", "trend continuation", "EMA crosses above SMA")
    return StrategySignal("trend_v001", "NO_TRADE", 45, "trend unclear", "n/a", "n/a")
