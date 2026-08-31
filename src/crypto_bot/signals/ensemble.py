from __future__ import annotations

from collections import Counter

from crypto_bot.strategies.models import StrategySignal


def vote_direction(signals: list[StrategySignal]) -> str:
    tradable = [s.direction for s in signals if s.direction in {"LONG", "SHORT"}]
    if not tradable:
        return "NO_TRADE"
    counts = Counter(tradable)
    if counts["LONG"] == counts["SHORT"]:
        return "NO_TRADE"
    return "LONG" if counts["LONG"] > counts["SHORT"] else "SHORT"
