# Crypto Bot (Research + Signal + Backtest + Paper Trading)

## What this bot does
This project is a modular cryptocurrency research platform that can:
- download market data from free exchange APIs
- validate and store data in SQLite and Parquet
- compute technical/structure/volatility/volume features
- run baseline strategies and a weighted signal engine
- estimate expected value and block weak trades
- run realistic backtests with fees/slippage
- simulate paper trades (no real money)
- run health checks and write reports

## What this bot does NOT guarantee
- No guaranteed profits
- No guaranteed prediction accuracy
- Historical results do not guarantee future results
- Backtests and paper trading can differ from live markets

## Safety defaults
- `live_trading_enabled: false` by default
- No withdrawal logic
- No hard-coded API secrets
- `.env` is ignored by Git
- `NO_TRADE` is returned on bad conditions (stale/invalid data, high volatility, or failed risk checks)

## Architecture
`Data -> Validation -> Storage -> Features -> Strategies -> Signal Engine -> Risk -> Backtest/Paper -> Monitoring`

## Repository tree
- `config/` runtime settings, symbols, logging
- `src/crypto_bot/` core modules
- `scripts/` simple executable commands
- `tests/` unit tests
- `docs/` detailed user docs
- `data/`, `models/`, `reports/`, `logs/` runtime artifacts

## Installation
```bash
git clone <repo-url>
cd Crypto-Bot
bash scripts/setup.sh
source .venv/bin/activate
```

## Termux setup notes
In Termux, install base tools first:
```bash
pkg update && pkg upgrade
pkg install python git
```
Then run the installation steps above.

## GitHub + Termux workflow
```bash
git pull
# edit files
pytest
git add .
git commit -m "description"
git push
```
After code changes, restart any running Python process.

## Configuration
Main file: `config/settings.yaml`
Editable settings include:
- symbols/timeframes
- exchange id
- fees/slippage assumptions
- risk limits
- signal thresholds
- polling intervals
- paper/live mode
- telegram toggle

Secrets go only in `.env` (from `.env.example`):
- `EXCHANGE_API_KEY`
- `EXCHANGE_API_SECRET`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Simple commands
```bash
python scripts/health_check.py
python scripts/download_data.py
python scripts/backtest.py
python scripts/train_model.py
python scripts/paper_trade.py
python main.py signal --symbol BTC/USDT --timeframe 1h
python -m crypto_bot --help
```

## Backtesting
The backtester includes fees and slippage and writes:
- `reports/latest_report.json`
- `reports/latest_trades.csv`

## Machine learning
The ML pipeline:
- builds a configurable forward-looking binary target
- uses chronological splits
- compares Logistic Regression, Random Forest, and Gradient Boosting
- stores metadata in `models/registry.json`

## Paper trading
Paper mode simulates order fills and PnL from market prices only. It never uses real funds.

## Telegram
Optional and disabled by default. If enabled, token/chat id are read from `.env`.

## Data sources (free-first)
- Public exchange market data via CCXT (default Binance)
- Optional derivatives metrics where exchange endpoints are available
- Optional on-chain/sentiment/cross-market interfaces with safe fallback when unavailable

## Testing
```bash
pytest
```

## Security warnings
- Never commit `.env`
- Use API keys with no withdrawal permissions
- Limit API permissions and rotate keys
- Keep `live_trading_enabled: false` until strict validation is completed

## Limitations
- Free APIs may have rate limits/missing endpoints
- Optional modules (on-chain/sentiment/macro) are fallback interfaces unless a free source is integrated
- No guarantee of profitability

## Detailed docs
See:
- `docs/INSTALLATION.md`
- `docs/CONFIGURATION.md`
- `docs/DATA_SOURCES.md`
- `docs/STRATEGIES.md`
- `docs/BACKTESTING.md`
- `docs/MACHINE_LEARNING.md`
- `docs/RISK_MANAGEMENT.md`
- `docs/PAPER_TRADING.md`
- `docs/TROUBLESHOOTING.md`
