from __future__ import annotations

import logging
from typing import Any

from .exchange import ExchangeConfig, build_exchange

logger = logging.getLogger(__name__)


class RestClient:
    def __init__(self, config: ExchangeConfig) -> None:
        self.exchange = build_exchange(config)

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 500) -> list[list[float]]:
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as exc:
            logger.error("OHLCV request failed for %s %s: %s", symbol, timeframe, exc)
            return []

    def fetch_ticker(self, symbol: str) -> dict[str, Any]:
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as exc:
            logger.error("Ticker request failed for %s: %s", symbol, exc)
            return {}

    def fetch_order_book(self, symbol: str, limit: int = 50) -> dict[str, Any]:
        try:
            return self.exchange.fetch_order_book(symbol, limit=limit)
        except Exception as exc:
            logger.error("Order book request failed for %s: %s", symbol, exc)
            return {}
