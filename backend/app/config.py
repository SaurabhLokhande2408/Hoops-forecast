"""Application settings loaded from environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the FastAPI application."""

    dataset_path: Path = Path("Dataset/Player Per Game.csv")
    model_path: Path = Path("app/artifacts/model.joblib")
    metrics_path: Path = Path("app/artifacts/metrics.json")
    feature_columns_path: Path = Path("app/artifacts/feature_columns.json")
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def origins(self) -> list[str]:
        """Return configured CORS origins as a normalized list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def resolve_path(self, path: Path) -> Path:
        """Resolve a path relative to the backend directory when needed."""
        return path if path.is_absolute() else Path(__file__).resolve().parents[1] / path


settings = Settings()