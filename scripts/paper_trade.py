from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from crypto_bot.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["paper", "--symbol", "BTC/USDT", "--timeframe", "1h"]))
