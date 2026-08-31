from __future__ import annotations

import math

import numpy as np
import pandas as pd


def compute_metrics(trades: pd.DataFrame, starting_balance: float) -> dict[str, float]:
    if trades.empty:
        return {"total_return": 0.0, "win_rate": 0.0, "max_drawdown": 0.0, "trades": 0}
    pnl = trades["pnl"]
    equity = starting_balance + pnl.cumsum()
    peak = equity.cummax()
    dd = ((equity - peak) / peak).min()
    returns = pnl / starting_balance
    sharpe = 0.0 if returns.std() == 0 else (returns.mean() / returns.std()) * math.sqrt(252)
    return {
        "total_return": float((equity.iloc[-1] - starting_balance) / starting_balance),
        "win_rate": float((pnl > 0).mean()),
        "max_drawdown": float(dd),
        "profit_factor": float(pnl[pnl > 0].sum() / abs(pnl[pnl < 0].sum())) if (pnl < 0).any() else np.inf,
        "sharpe": float(sharpe),
        "trades": int(len(trades)),
        "fees_paid": float(trades["fee"].sum()),
        "estimated_slippage": float(trades["slippage"].sum()),
    }
