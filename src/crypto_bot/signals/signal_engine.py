from __future__ import annotations

from dataclasses import dataclass

from crypto_bot.regime.detector import detect_regime
from crypto_bot.signals.ensemble import vote_direction
from crypto_bot.signals.scoring import normalize_score
from crypto_bot.strategies import breakout, mean_reversion, momentum, trend


@dataclass(slots=True)
class FinalSignal:
    symbol: str
    timeframe: str
    direction: str
    score: float
    expected_value: float
    regime: str
    reasons: list[str]


class SignalEngine:
    def __init__(self, min_score: float, min_expected_value: float) -> None:
        self.min_score = min_score
        self.min_expected_value = min_expected_value

    def generate(self, symbol: str, timeframe: str, frame) -> FinalSignal:
        signals = [
            trend.evaluate(frame),
            breakout.evaluate(frame),
            momentum.evaluate(frame),
            mean_reversion.evaluate(frame),
        ]
        score = normalize_score(signals)
        direction = vote_direction(signals)
        regime = detect_regime(frame)
        expected_value = self._estimate_ev(frame, direction)
        if score < self.min_score or expected_value < self.min_expected_value or direction == "NO_TRADE" or regime == "ABNORMAL_HIGH_VOL":
            direction = "NO_TRADE"
        reasons = [s.reason for s in signals]
        if regime == "ABNORMAL_HIGH_VOL":
            reasons.append("abnormal volatility protection")
        return FinalSignal(symbol, timeframe, direction, score, expected_value, regime, reasons)

    @staticmethod
    def _estimate_ev(frame, direction: str) -> float:
        returns = frame["close"].pct_change().dropna()
        if returns.empty or direction == "NO_TRADE":
            return 0.0
        win = returns[returns > 0].mean() if not returns[returns > 0].empty else 0.0
        loss = -returns[returns < 0].mean() if not returns[returns < 0].empty else 0.0
        p_win = float((returns > 0).mean())
        p_loss = 1 - p_win
        return float(p_win * win - p_loss * loss)
