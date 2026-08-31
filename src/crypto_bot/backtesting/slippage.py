from __future__ import annotations


def slippage_cost(notional: float, slippage_bps: float) -> float:
    return notional * (slippage_bps / 10_000)
