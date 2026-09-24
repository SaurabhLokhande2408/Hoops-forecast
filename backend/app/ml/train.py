"""Train and persist the Hoop Forecast model."""

from app.config import settings
from app.services.data_service import load_and_clean_dataset
from app.services.model_service import train_and_save


def main() -> None:
    """Load the configured dataset and write model artifacts."""
    dataframe = load_and_clean_dataset(settings.resolve_path(settings.dataset_path))
    metrics = train_and_save(
        dataframe,
        settings.resolve_path(settings.model_path),
        settings.resolve_path(settings.metrics_path),
        settings.resolve_path(settings.feature_columns_path),
    )
    print(f"Trained on {metrics['trained_on_rows']} rows; R2={metrics['r2']:.4f}")


if __name__ == "__main__":
    main()