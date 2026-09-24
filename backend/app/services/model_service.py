"""Model training, persistence, and prediction."""

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.services.feature_service import FEATURE_COLUMNS, FeatureTransformer, build_features, transform_player_row


class ModelService:
    """Loaded linear regression model and its persisted metadata."""

    def __init__(self, model_path: Path, metrics_path: Path, feature_columns_path: Path) -> None:
        """Load model artifacts and metrics into memory."""
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found at {model_path}. Run `python -m app.ml.train` first."
            )
        bundle = joblib.load(model_path)
        self.model: LinearRegression = bundle["model"]
        self.transformer: FeatureTransformer = bundle["transformer"]
        self.metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        self.feature_columns = json.loads(feature_columns_path.read_text(encoding="utf-8"))

    def predict_for_player(self, rows: pd.DataFrame) -> tuple[float, int]:
        """Predict next-season points from a player's latest cleaned season row."""
        latest = rows.sort_values("season", ascending=False).head(1)
        features = transform_player_row(latest, self.transformer)
        prediction = float(self.model.predict(features[FEATURE_COLUMNS])[0])
        return prediction, int(latest.iloc[0]["season"])


def train_and_save(dataframe: pd.DataFrame, model_path: Path, metrics_path: Path, feature_columns_path: Path) -> dict[str, Any]:
    """Train the linear regression model and persist all inference artifacts."""
    encoded, transformer = build_features(dataframe)
    x_values = encoded[FEATURE_COLUMNS]
    target = encoded["next_season_pts"]
    x_train, x_test, y_train, y_test = train_test_split(x_values, target, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, predictions)),
        "mse": float(mean_squared_error(y_test, predictions)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": float(r2_score(y_test, predictions)),
        "trained_on_rows": int(len(dataframe)),
        "features": FEATURE_COLUMNS,
    }
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "transformer": transformer}, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    feature_columns_path.write_text(json.dumps(FEATURE_COLUMNS, indent=2), encoding="utf-8")
    return metrics