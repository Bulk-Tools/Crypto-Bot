from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class OrderBookFeatures:
    spread: float
    bid_volume: float
    ask_volume: float
    imbalance: float


class OrderBookProvider:
    def to_features(self, order_book: dict) -> OrderBookFeatures | None:
        bids = order_book.get("bids") or []
        asks = order_book.get("asks") or []
        if not bids or not asks:
            return None
        best_bid, best_ask = bids[0][0], asks[0][0]
        bid_volume = sum(level[1] for level in bids[:10])
        ask_volume = sum(level[1] for level in asks[:10])
        denom = max(bid_volume + ask_volume, 1e-9)
        return OrderBookFeatures(
            spread=max(best_ask - best_bid, 0.0),
            bid_volume=bid_volume,
            ask_volume=ask_volume,
            imbalance=(bid_volume - ask_volume) / denom,
        )
