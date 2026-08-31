from __future__ import annotations


def fixed_fractional_size(equity: float, risk_pct: float, stop_distance_pct: float, price: float) -> float:
    if stop_distance_pct <= 0 or price <= 0:
        return 0.0
    risk_amount = equity * (risk_pct / 100)
    units = risk_amount / (price * stop_distance_pct)
    return max(units, 0.0)
