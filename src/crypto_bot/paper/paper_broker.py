from __future__ import annotations

from dataclasses import dataclass

from crypto_bot.backtesting.execution_simulator import Fill, simulate_fill


@dataclass(slots=True)
class PaperPosition:
    symbol: str
    side: str
    quantity: float
    entry: float


class PaperBroker:
    def __init__(self, fee_bps: float, slippage_bps: float) -> None:
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps
        self.positions: dict[str, PaperPosition] = {}

    def open_position(self, symbol: str, side: str, quantity: float, price: float) -> None:
        self.positions[symbol] = PaperPosition(symbol, side, quantity, price)

    def close_position(self, symbol: str, price: float) -> Fill | None:
        position = self.positions.pop(symbol, None)
        if not position:
            return None
        return simulate_fill(position.entry, price, position.quantity, self.fee_bps, self.slippage_bps, position.side)
