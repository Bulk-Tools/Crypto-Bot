from __future__ import annotations

from dataclasses import dataclass

from .fees import trading_fee
from .slippage import slippage_cost


@dataclass(slots=True)
class Fill:
    entry: float
    exit: float
    quantity: float
    fee: float
    slippage: float
    pnl: float


def simulate_fill(entry: float, exit_price: float, quantity: float, fee_bps: float, slippage_bps: float, side: str) -> Fill:
    notional_entry = entry * quantity
    notional_exit = exit_price * quantity
    fee = trading_fee(notional_entry, fee_bps) + trading_fee(notional_exit, fee_bps)
    slip = slippage_cost(notional_entry, slippage_bps) + slippage_cost(notional_exit, slippage_bps)
    gross = (exit_price - entry) * quantity if side == "LONG" else (entry - exit_price) * quantity
    pnl = gross - fee - slip
    return Fill(entry=entry, exit=exit_price, quantity=quantity, fee=fee, slippage=slip, pnl=pnl)
