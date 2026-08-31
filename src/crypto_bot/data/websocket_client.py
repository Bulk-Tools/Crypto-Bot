from __future__ import annotations

import logging
from collections.abc import Iterator

logger = logging.getLogger(__name__)


class WebSocketClient:
    """Safe placeholder for public websocket feeds.

    Termux compatibility varies by exchange websocket dependencies, so this
    client exposes a minimal iterable interface and degrades safely.
    """

    def stream(self, symbol: str, channel: str) -> Iterator[dict]:
        logger.warning("WebSocket stream not configured for %s %s; using REST fallback", symbol, channel)
        if False:
            yield {}
        return
