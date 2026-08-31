import pandas as pd

from crypto_bot.features.momentum import add_momentum_indicators
from crypto_bot.features.structure import add_structure_features
from crypto_bot.features.technical import add_trend_indicators
from crypto_bot.features.volatility import add_volatility_indicators
from crypto_bot.signals.signal_engine import SignalEngine


def test_signal_engine_runs():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=80, freq="h", tz="UTC"),
            "open": [100 + i * 0.2 for i in range(80)],
            "high": [100.5 + i * 0.2 for i in range(80)],
            "low": [99.5 + i * 0.2 for i in range(80)],
            "close": [100 + i * 0.2 for i in range(80)],
            "volume": [20 + (i % 5) for i in range(80)],
        }
    )
    for fn in [add_trend_indicators, add_momentum_indicators, add_volatility_indicators, add_structure_features]:
        df = fn(df)
    engine = SignalEngine(min_score=0, min_expected_value=-1)
    result = engine.generate("BTC/USDT", "1h", df)
    assert result.direction in {"LONG", "SHORT", "NO_TRADE"}
