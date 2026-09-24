"""Request and response models for the Hoop Forecast API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HealthResponse(BaseModel):
    """Health and model readiness response."""

    status: str
    model_loaded: bool
    rows_loaded: int


class PlayerSearchResult(BaseModel):
    """One autocomplete result."""

    player: str
    seasons_played: int
    last_season: int


class PlayerSearchResponse(BaseModel):
    """Autocomplete response."""

    results: list[PlayerSearchResult]


class SeasonStats(BaseModel):
    """Player statistics for one season."""

    model_config = ConfigDict(extra="ignore")
    season: int
    age: int | float
    pos: str
    g: int | float
    mp_per_game: float
    pts_per_game: float
    ast_per_game: float
    trb_per_game: float
    stl_per_game: float
    blk_per_game: float
    fg_percent: float
    x3p_percent: float
    ft_percent: float


class LatestPlayerResponse(BaseModel):
    """Latest season response."""

    player: str
    latest_season: int
    stats: SeasonStats


class PlayerHistoryResponse(BaseModel):
    """Full player history response."""

    player: str
    seasons: list[SeasonStats]


class PredictionRequest(BaseModel):
    """Prediction request body."""

    player_name: str = Field(min_length=2)

    @field_validator("player_name")
    @classmethod
    def strip_player_name(cls, value: str) -> str:
        """Normalize whitespace and reject names that become too short."""
        value = value.strip()
        if len(value) < 2:
            raise ValueError("player_name must contain at least 2 characters")
        return value


class ModelMetrics(BaseModel):
    """Held-out model metrics and training metadata."""

    mae: float
    mse: float
    rmse: float
    r2: float
    trained_on_rows: int
    features: list[str]


class PredictionResponse(BaseModel):
    """Prediction response."""

    player: str
    season: int
    based_on_season: int
    predicted_pts: float
    metrics: dict[str, Any]