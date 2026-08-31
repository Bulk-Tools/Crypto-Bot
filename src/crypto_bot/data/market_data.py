from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .rest_client import RestClient
from .validators import DataQualityReport, validate_ohlcv


@dataclass(slots=True)
class MarketDataResult:
    frame: pd.DataFrame
    quality: DataQualityReport


class MarketDataProvider:
    def __init__(self, rest_client: RestClient) -> None:
        self.rest_client = rest_client

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 500) -> MarketDataResult:
        raw = self.rest_client.fetch_ohlcv(symbol, timeframe, limit)
        frame = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        if not frame.empty:
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
        quality = validate_ohlcv(frame) if not frame.empty else DataQualityReport(False, ["empty dataset"])
        return MarketDataResult(frame=frame, quality=quality)
