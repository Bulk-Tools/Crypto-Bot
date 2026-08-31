from __future__ import annotations

from typing import Any

from .rest_client import RestClient


class DerivativesProvider:
    """Best-effort derivatives features from free endpoints when available."""

    def __init__(self, rest_client: RestClient) -> None:
        self.rest_client = rest_client

    def get_funding_rate(self, symbol: str) -> float | None:
        exchange = self.rest_client.exchange
        if hasattr(exchange, "fetch_funding_rate"):
            try:
                data: dict[str, Any] = exchange.fetch_funding_rate(symbol)
                return float(data.get("fundingRate")) if data.get("fundingRate") is not None else None
            except Exception:
                return None
        return None

    def get_open_interest(self, symbol: str) -> float | None:
        exchange = self.rest_client.exchange
        if hasattr(exchange, "fetch_open_interest"):
            try:
                data: dict[str, Any] = exchange.fetch_open_interest(symbol)
                return float(data.get("openInterestAmount")) if data.get("openInterestAmount") is not None else None
            except Exception:
                return None
        return None
