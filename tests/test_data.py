import pandas as pd

from crypto_bot.data.validators import validate_ohlcv


def test_validate_ohlcv_detects_negative_price():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=3, freq="h", tz="UTC"),
            "open": [1, -1, 1],
            "high": [1, 1, 1],
            "low": [1, 1, 1],
            "close": [1, 1, 1],
            "volume": [1, 1, 1],
        }
    )
    report = validate_ohlcv(df)
    assert not report.valid
