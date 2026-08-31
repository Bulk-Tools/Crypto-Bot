from __future__ import annotations

from dataclasses import dataclass

import ccxt


@dataclass(slots=True)
class ExchangeConfig:
    exchange_id: str = "binance"
    timeout_ms: int = 10000
    rate_limit: bool = True


def build_exchange(config: ExchangeConfig) -> ccxt.Exchange:
    exchange_cls = getattr(ccxt, config.exchange_id)
    return exchange_cls({"timeout": config.timeout_ms, "enableRateLimit": config.rate_limit})
