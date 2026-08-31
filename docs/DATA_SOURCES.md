# Data Sources

- Market/OHLCV/orderbook: exchange public API via CCXT (default Binance)
- Derivatives: optional `fetch_funding_rate` and `fetch_open_interest` if exchange supports them
- Cross-market, on-chain, sentiment: optional interfaces with safe fallback when unavailable

No paid API is required for core operation.
