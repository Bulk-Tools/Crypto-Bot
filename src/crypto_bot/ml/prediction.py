from __future__ import annotations

from .dataset import threading_backend


def predict_probability(model: object, x_row) -> float:
    if hasattr(model, "predict_proba"):
        with threading_backend():
            return float(model.predict_proba(x_row)[0, 1])
    return 0.5
