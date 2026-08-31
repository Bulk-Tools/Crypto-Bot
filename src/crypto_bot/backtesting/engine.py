from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

from crypto_bot.backtesting.execution_simulator import simulate_fill
from crypto_bot.backtesting.metrics import compute_metrics


@dataclass(slots=True)
class BacktestConfig:
    fee_bps: float
    slippage_bps: float
    hold_bars: int = 5


class BacktestEngine:
    def __init__(self, config: BacktestConfig) -> None:
        self.config = config

    def run(self, frame: pd.DataFrame, side: str = "LONG", quantity: float = 1.0, starting_balance: float = 10_000) -> tuple[pd.DataFrame, dict]:
        trades: list[dict] = []
        for idx in range(len(frame) - self.config.hold_bars):
            entry = float(frame.iloc[idx]["close"])
            exit_price = float(frame.iloc[idx + self.config.hold_bars]["close"])
            fill = simulate_fill(entry, exit_price, quantity, self.config.fee_bps, self.config.slippage_bps, side)
            trades.append(asdict(fill) | {"timestamp": frame.iloc[idx + self.config.hold_bars]["timestamp"]})
        trades_df = pd.DataFrame(trades)
        return trades_df, compute_metrics(trades_df, starting_balance)
