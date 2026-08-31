from __future__ import annotations

from crypto_bot.strategies.models import StrategySignal


def normalize_score(signals: list[StrategySignal]) -> float:
    if not signals:
        return 0.0
    return max(0.0, min(100.0, sum(s.score for s in signals) / len(signals)))
