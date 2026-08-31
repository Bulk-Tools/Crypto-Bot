from __future__ import annotations


def exposure_pct(open_notional: float, equity: float) -> float:
    if equity <= 0:
        return 100.0
    return (open_notional / equity) * 100
