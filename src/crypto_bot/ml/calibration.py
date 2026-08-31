from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import brier_score_loss


@dataclass(slots=True)
class CalibrationReport:
    brier_score: float
    reliability_gap: float


def evaluate_calibration(y_true, y_prob) -> CalibrationReport:
    brier = float(brier_score_loss(y_true, y_prob))
    bins = np.linspace(0, 1, 6)
    gaps: list[float] = []
    for i in range(len(bins) - 1):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i + 1])
        if mask.sum() > 0:
            gaps.append(abs(y_true[mask].mean() - y_prob[mask].mean()))
    return CalibrationReport(brier_score=brier, reliability_gap=float(np.mean(gaps) if gaps else 0.0))
