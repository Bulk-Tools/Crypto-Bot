from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class MarketDataProviderInterface(ABC):
    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 500):
        raise NotImplementedError


class OrderBookProviderInterface(ABC):
    @abstractmethod
    def to_features(self, order_book: dict):
        raise NotImplementedError


class DerivativesProviderInterface(ABC):
    @abstractmethod
    def get_funding_rate(self, symbol: str) -> float | None:
        raise NotImplementedError


class OnChainProviderInterface(ABC):
    def get_metrics(self, symbol: str) -> dict[str, float | None]:
        return {"active_addresses": None, "fees": None}


class MacroProviderInterface(ABC):
    def get_snapshot(self) -> dict[str, float | None]:
        return {"dxy": None, "sp500": None}


class SentimentProviderInterface(ABC):
    def get_score(self, symbol: str) -> float | None:
        return None


class DisabledOptionalProvider:
    """Safe fallback for optional data sources with no free reliable feed configured."""

    def get_metrics(self, symbol: str) -> dict[str, float | None]:
        return {"symbol": symbol, "status": "unavailable"}

    def get_snapshot(self) -> dict[str, float | None]:
        return {"status": "unavailable"}

    def get_score(self, symbol: str) -> float | None:
        return None
