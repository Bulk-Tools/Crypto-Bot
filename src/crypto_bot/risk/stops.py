from __future__ import annotations


def atr_stop_distance_pct(atr: float, price: float, multiplier: float, min_stop_pct: float, max_stop_pct: float) -> float:
    if price <= 0:
        return min_stop_pct / 100
    raw = (atr * multiplier / price) * 100
    bounded = min(max(raw, min_stop_pct), max_stop_pct)
    return bounded / 100
