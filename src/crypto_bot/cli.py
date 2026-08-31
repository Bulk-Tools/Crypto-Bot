from __future__ import annotations

import argparse
import json
from pathlib import Path

from crypto_bot.backtesting.engine import BacktestConfig, BacktestEngine
from crypto_bot.data.derivatives import DerivativesProvider
from crypto_bot.data.exchange import ExchangeConfig
from crypto_bot.data.market_data import MarketDataProvider
from crypto_bot.data.orderbook import OrderBookProvider
from crypto_bot.data.rest_client import RestClient
from crypto_bot.features.cross_market import add_cross_market_features
from crypto_bot.features.derivatives import add_derivatives_features
from crypto_bot.features.momentum import add_momentum_indicators
from crypto_bot.features.orderflow import add_orderflow_features
from crypto_bot.features.structure import add_structure_features
from crypto_bot.features.technical import add_trend_indicators
from crypto_bot.features.volatility import add_volatility_indicators
from crypto_bot.features.volume import add_volume_indicators
from crypto_bot.monitoring.health import run_health_checks
from crypto_bot.monitoring.performance import write_report
from crypto_bot.paper.paper_broker import PaperBroker
from crypto_bot.risk.position_sizing import fixed_fractional_size
from crypto_bot.risk.risk_manager import RiskManager
from crypto_bot.risk.stops import atr_stop_distance_pct
from crypto_bot.signals.signal_engine import SignalEngine
from crypto_bot.storage.database import init_db
from crypto_bot.storage.parquet_store import ParquetStore
from crypto_bot.storage.sqlite_store import SQLiteStore
from crypto_bot.utils.config import load_yaml
from crypto_bot.utils.logging import setup_logging


def _load_settings() -> dict:
    return load_yaml("config/settings.yaml")


def _build_pipeline(symbol: str, timeframe: str):
    settings = _load_settings()
    exchange_cfg = settings.get("exchange", {})
    rest = RestClient(ExchangeConfig(exchange_cfg.get("id", "binance"), exchange_cfg.get("timeout_ms", 10000), exchange_cfg.get("rate_limit", True)))
    md = MarketDataProvider(rest)
    data = md.get_ohlcv(symbol, timeframe, settings.get("data", {}).get("history_limit", 500))
    frame = data.frame
    if frame.empty:
        raise RuntimeError(f"No data returned for {symbol} {timeframe}")

    frame = add_trend_indicators(frame)
    frame = add_momentum_indicators(frame)
    frame = add_volatility_indicators(frame)
    frame = add_volume_indicators(frame)
    frame = add_structure_features(frame)

    ob_raw = rest.fetch_order_book(symbol)
    ob = OrderBookProvider().to_features(ob_raw) if ob_raw else None
    frame = add_orderflow_features(frame, ob.imbalance if ob else None, ob.spread if ob else None)

    derivatives = DerivativesProvider(rest)
    frame = add_derivatives_features(frame, derivatives.get_funding_rate(symbol), derivatives.get_open_interest(symbol))
    frame = add_cross_market_features(frame)

    return settings, frame, data.quality


def cmd_health(_: argparse.Namespace) -> int:
    setup_logging()
    statuses = run_health_checks()
    for s in statuses:
        print(f"[{ 'OK' if s.ok else 'FAIL' }] {s.name}: {s.message}")
    return 0 if all(s.ok for s in statuses) else 1


def cmd_status(args: argparse.Namespace) -> int:
    return cmd_health(args)


def cmd_data(args: argparse.Namespace) -> int:
    setup_logging()
    settings, frame, quality = _build_pipeline(args.symbol, args.timeframe)
    if not quality.valid:
        print("Warning:", "; ".join(quality.warnings))
    init_db()
    sqlite_store = SQLiteStore()
    parquet_store = ParquetStore()
    n = sqlite_store.upsert_candles(args.symbol, args.timeframe, frame)
    out = parquet_store.save(args.symbol, args.timeframe, frame)
    print(f"Stored {n} candles in SQLite and wrote {out}")
    return 0


def cmd_signal(args: argparse.Namespace) -> int:
    setup_logging()
    settings, frame, quality = _build_pipeline(args.symbol, args.timeframe)
    if not quality.valid:
        print(f"{args.symbol} SIGNAL: NO_TRADE\nReason: data quality issue ({'; '.join(quality.warnings)})")
        return 0

    signal_cfg = settings.get("signal", {})
    engine = SignalEngine(signal_cfg.get("min_score", 60), signal_cfg.get("min_expected_value", 0.0))
    sig = engine.generate(args.symbol, args.timeframe, frame)
    print(f"{sig.symbol} SIGNAL\nDirection: {sig.direction}\nSignal Score: {sig.score:.1f}/100\nExpected Value: {sig.expected_value:.4f}\nMarket Regime: {sig.regime}\nReasons:")
    for reason in sig.reasons:
        print(f"- {reason}")
    return 0


def cmd_backtest(args: argparse.Namespace) -> int:
    settings, frame, _ = _build_pipeline(args.symbol, args.timeframe)
    costs = settings.get("costs", {})
    bt = BacktestEngine(BacktestConfig(costs.get("taker_fee_bps", 10), costs.get("slippage_bps", 3), hold_bars=args.hold_bars))
    trades, metrics = bt.run(frame, side=args.side)
    report = {"symbol": args.symbol, "timeframe": args.timeframe, "metrics": metrics}
    write_report(report)
    trades.to_csv("reports/latest_trades.csv", index=False)
    print(json.dumps(report, indent=2))
    return 0


def cmd_train(args: argparse.Namespace) -> int:
    from crypto_bot.ml.dataset import build_target
    from crypto_bot.ml.features import feature_matrix
    from crypto_bot.ml.model_registry import ModelRegistry
    from crypto_bot.ml.training import train_baseline

    settings, frame, _ = _build_pipeline(args.symbol, args.timeframe)
    frame = frame.dropna().reset_index(drop=True)
    y = build_target(frame)
    x = feature_matrix(frame)
    split = int(len(frame) * 0.7)
    x_train, x_test = x.iloc[:split], x.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    model, result = train_baseline(x_train, y_train, x_test, y_test)
    registry = ModelRegistry()
    model_id = f"model_v{len(registry.read_all()) + 1:03d}"
    registry.append({
        "model_id": model_id,
        "status": "candidate",
        "model_name": result.model_name,
        "training_samples": result.samples,
        "test_auc": result.auc,
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "features": list(x.columns),
    })
    print(f"Trained {result.model_name}, test_auc={result.auc:.4f}, saved as {model_id}")
    _ = model
    _ = settings
    return 0


def cmd_paper(args: argparse.Namespace) -> int:
    settings, frame, _ = _build_pipeline(args.symbol, args.timeframe)
    latest = frame.iloc[-1]
    risk_cfg = settings.get("risk", {})
    costs = settings.get("costs", {})
    atr = float(latest.get("atr_14", 0) or 0)
    price = float(latest["close"])
    stop_pct = atr_stop_distance_pct(
        atr,
        price,
        risk_cfg.get("atr_multiplier", 2.0),
        risk_cfg.get("min_stop_pct", 0.2),
        risk_cfg.get("max_stop_pct", 4.0),
    )
    qty = fixed_fractional_size(risk_cfg.get("equity", 10_000), risk_cfg.get("max_risk_per_trade_pct", 1.0), stop_pct, price)
    rm = RiskManager(
        risk_cfg.get("max_portfolio_exposure_pct", 60.0),
        risk_cfg.get("max_daily_loss_pct", 3.0),
        risk_cfg.get("max_consecutive_losses", 5),
        risk_cfg.get("emergency_stop", False),
    )
    decision = rm.validate(risk_cfg.get("equity", 10_000), 0, 0, 0)
    if not decision.accepted:
        print(f"NO_TRADE: {decision.reason}")
        return 0

    broker = PaperBroker(costs.get("taker_fee_bps", 10), costs.get("slippage_bps", 3))
    broker.open_position(args.symbol, "LONG", qty, price)
    fill = broker.close_position(args.symbol, price * 1.002)
    print(f"Paper trade done. qty={qty:.6f}, pnl={fill.pnl if fill else 0:.4f}")
    return 0


def cmd_init_db(_: argparse.Namespace) -> int:
    init_db()
    print("SQLite initialized at data/crypto_bot.db")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crypto bot CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ["data", "signal", "backtest", "train", "paper"]:
        p = sub.add_parser(command)
        p.add_argument("--symbol", default="BTC/USDT")
        p.add_argument("--timeframe", default="1h")
        if command == "backtest":
            p.add_argument("--side", default="LONG", choices=["LONG", "SHORT"])
            p.add_argument("--hold-bars", type=int, default=5)
    sub.add_parser("health")
    sub.add_parser("status")
    sub.add_parser("init-db")

    sub.choices["health"].set_defaults(func=cmd_health)
    sub.choices["status"].set_defaults(func=cmd_status)
    sub.choices["init-db"].set_defaults(func=cmd_init_db)
    sub.choices["data"].set_defaults(func=cmd_data)
    sub.choices["signal"].set_defaults(func=cmd_signal)
    sub.choices["backtest"].set_defaults(func=cmd_backtest)
    sub.choices["train"].set_defaults(func=cmd_train)
    sub.choices["paper"].set_defaults(func=cmd_paper)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
