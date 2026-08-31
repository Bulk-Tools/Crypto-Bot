from __future__ import annotations

from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from .dataset import DEFAULT_N_JOBS, threading_backend


@dataclass(slots=True)
class TrainingResult:
    model_name: str
    auc: float
    samples: int


def train_baseline(x_train, y_train, x_test, y_test) -> tuple[object, TrainingResult]:
    models = {
        "logistic_regression": LogisticRegression(max_iter=500, n_jobs=DEFAULT_N_JOBS),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=DEFAULT_N_JOBS),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }
    best_model_name = "logistic_regression"
    best_model = models[best_model_name]
    best_auc = -1.0
    with threading_backend():
        for name, model in models.items():
            model.fit(x_train, y_train)
            probs = model.predict_proba(x_test)[:, 1]
            auc = roc_auc_score(y_test, probs) if len(set(y_test)) > 1 else 0.5
            if auc > best_auc:
                best_auc, best_model_name, best_model = auc, name, model
    return best_model, TrainingResult(best_model_name, float(best_auc), int(len(y_train)))
