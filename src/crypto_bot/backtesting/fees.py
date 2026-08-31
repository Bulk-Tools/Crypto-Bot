from __future__ import annotations


def trading_fee(notional: float, fee_bps: float) -> float:
    return notional * (fee_bps / 10_000)
