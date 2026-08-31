import pandas as pd

from crypto_bot.storage.database import init_db
from crypto_bot.storage.sqlite_store import SQLiteStore


def test_sqlite_store_roundtrip(tmp_path):
    db_path = tmp_path / "test.db"
    init_db(db_path)
    store = SQLiteStore(db_path)
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=5, freq="h", tz="UTC"),
            "open": [1, 2, 3, 4, 5],
            "high": [2, 3, 4, 5, 6],
            "low": [0.5, 1.5, 2.5, 3.5, 4.5],
            "close": [1.5, 2.5, 3.5, 4.5, 5.5],
            "volume": [10, 11, 12, 13, 14],
        }
    )
    store.upsert_candles("BTC/USDT", "1h", frame)
    out = store.load_candles("BTC/USDT", "1h", 5)
    assert len(out) == 5
