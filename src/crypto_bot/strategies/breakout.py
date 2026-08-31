from __future__ import annotations

import pandas as pd

from .models import StrategySignal


def evaluate(frame: pd.DataFrame) -> StrategySignal:
    latest = frame.iloc[-1]
    if bool(latest.get("breakout_up", False)):
        return StrategySignal("breakout_v001", "LONG", 75, "upside breakout", "close above range high", "breakout failure")
    if bool(latest.get("breakout_down", False)):
        return StrategySignal("breakout_v001", "SHORT", 75, "downside breakout", "close below range low", "breakout failure")
    return StrategySignal("breakout_v001", "NO_TRADE", 40, "no breakout", "n/a", "n/a")
