"""Shared test setup for generated model artifacts."""

import pytest

from app.config import settings
from app.services.data_service import load_and_clean_dataset
from app.services.model_service import train_and_save


@pytest.fixture(scope="session", autouse=True)
def ensure_model_artifacts() -> None:
    """Train local test artifacts when a checkout has not trained yet."""
    model_path = settings.resolve_path(settings.model_path)
    metrics_path = settings.resolve_path(settings.metrics_path)
    feature_columns_path = settings.resolve_path(settings.feature_columns_path)
    if not model_path.exists() or not metrics_path.exists() or not feature_columns_path.exists():
        dataframe = load_and_clean_dataset(settings.resolve_path(settings.dataset_path))
        train_and_save(dataframe, model_path, metrics_path, feature_columns_path)