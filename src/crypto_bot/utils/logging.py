from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from .config import load_yaml


def setup_logging(config_path: str | Path = "config/logging.yaml") -> None:
    path = Path(config_path)
    if path.exists():
        logging.config.dictConfig(load_yaml(path))
    else:
        logging.basicConfig(level=logging.INFO)
