from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StrategySignal:
    name: str
    direction: str
    score: float
    reason: str
    entry_condition: str
    invalidation_condition: str
