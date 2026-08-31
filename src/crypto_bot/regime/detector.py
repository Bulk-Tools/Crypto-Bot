from __future__ import annotations

import pandas as pd


def detect_regime(frame: pd.DataFrame) -> str:
    latest = frame.iloc[-1]
    vol = float(latest.get("rolling_vol_20", 0) or 0)
    ema = float(latest.get("ema_20", latest["close"]))
    sma = float(latest.get("sma_20", latest["close"]))

    if vol > 0.05:
        return "ABNORMAL_HIGH_VOL"
    if ema > sma * 1.002:
        return "WEAK_BULLISH_TREND"
    if ema < sma * 0.998:
        return "WEAK_BEARISH_TREND"
    return "RANGING"
