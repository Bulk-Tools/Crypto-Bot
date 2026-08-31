from crypto_bot.risk.position_sizing import fixed_fractional_size
from crypto_bot.risk.risk_manager import RiskManager


def test_position_size_positive():
    qty = fixed_fractional_size(10_000, 1, 0.01, 100)
    assert qty > 0


def test_risk_manager_blocks_emergency_stop():
    rm = RiskManager(60, 3, 5, True)
    decision = rm.validate(10_000, 1000, 0, 0)
    assert not decision.accepted
