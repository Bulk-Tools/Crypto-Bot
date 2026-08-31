import pandas as pd

from crypto_bot.backtesting.engine import BacktestConfig, BacktestEngine


def test_backtest_runs_and_returns_metrics():
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=30, freq="h", tz="UTC"),
            "close": [100 + i for i in range(30)],
        }
    )
    engine = BacktestEngine(BacktestConfig(fee_bps=10, slippage_bps=5, hold_bars=3))
    trades, metrics = engine.run(frame)
    assert not trades.empty
    assert "total_return" in metrics
