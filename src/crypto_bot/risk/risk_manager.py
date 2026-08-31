from __future__ import annotations

from dataclasses import dataclass

from .portfolio import exposure_pct


@dataclass(slots=True)
class RiskDecision:
    accepted: bool
    reason: str


class RiskManager:
    def __init__(
        self,
        max_portfolio_exposure_pct: float,
        max_daily_loss_pct: float,
        max_consecutive_losses: int,
        emergency_stop: bool,
    ) -> None:
        self.max_portfolio_exposure_pct = max_portfolio_exposure_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_consecutive_losses = max_consecutive_losses
        self.emergency_stop = emergency_stop

    def validate(self, equity: float, open_notional: float, daily_loss_pct: float, consecutive_losses: int) -> RiskDecision:
        if self.emergency_stop:
            return RiskDecision(False, "emergency stop enabled")
        if exposure_pct(open_notional, equity) > self.max_portfolio_exposure_pct:
            return RiskDecision(False, "portfolio exposure exceeds max")
        if daily_loss_pct > self.max_daily_loss_pct:
            return RiskDecision(False, "daily loss limit exceeded")
        if consecutive_losses >= self.max_consecutive_losses:
            return RiskDecision(False, "max consecutive losses reached")
        return RiskDecision(True, "accepted")
