import pandas as pd

from crypto_bot.features.momentum import add_momentum_indicators
from crypto_bot.features.technical import add_trend_indicators


def test_indicators_add_columns():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=50, freq="h", tz="UTC"),
            "open": [100 + i for i in range(50)],
            "high": [101 + i for i in range(50)],
            "low": [99 + i for i in range(50)],
            "close": [100 + i for i in range(50)],
            "volume": [10 for _ in range(50)],
        }
    )
    df = add_trend_indicators(df)
    df = add_momentum_indicators(df)
    assert "ema_20" in df.columns
    assert "rsi_14" in df.columns
