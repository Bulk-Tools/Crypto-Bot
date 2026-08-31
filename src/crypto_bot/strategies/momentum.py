from __future__ import annotations

import pandas as pd

from .models import StrategySignal


def evaluate(frame: pd.DataFrame) -> StrategySignal:
    latest = frame.iloc[-1]
    rsi = float(latest.get("rsi_14", 50))
    if rsi > 60:
        return StrategySignal("momentum_v001", "LONG", min(90, 50 + (rsi - 50)), "RSI bullish", "RSI above 60", "RSI below 50")
    if rsi < 40:
        return StrategySignal("momentum_v001", "SHORT", min(90, 50 + (50 - rsi)), "RSI bearish", "RSI below 40", "RSI above 50")
    return StrategySignal("momentum_v001", "NO_TRADE", 45, "RSI neutral", "n/a", "n/a")
