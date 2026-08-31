from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id

    def send(self, message: str) -> bool:
        if not self.token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            res = requests.post(url, json={"chat_id": self.chat_id, "text": message}, timeout=10)
            return res.status_code == 200
        except requests.RequestException as exc:
            logger.error("Telegram send failed: %s", exc)
            return False
