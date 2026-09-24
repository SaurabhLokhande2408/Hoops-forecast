"""Thin FastAPI route handlers for the public API."""

from fastapi import APIRouter, HTTPException, Query, Request

from app.schemas.schemas import (
    HealthResponse,
    LatestPlayerResponse,
    ModelMetrics,
    PlayerHistoryResponse,
    PlayerSearchResponse,
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter()


def _not_found(request: str, suggestions: list[str]) -> HTTPException:
    """Build a consistent player-not-found response."""
    detail = {"message": f"Player '{request}' not found", "suggestions": suggestions}
    return HTTPException(status_code=404, detail=detail)


@router.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    """Return service and model readiness."""
    return HealthResponse(status="ok", model_loaded=request.app.state.model_service is not None,
                          rows_loaded=len(request.app.state.dataframe))


@router.get("/players", response_model=PlayerSearchResponse)
def search_players(
    request: Request,
    search: str = Query(min_length=2),
    limit: int = Query(default=8, ge=1, le=100),
) -> PlayerSearchResponse:
    """Search player names by case-insensitive substring."""
    return PlayerSearchResponse(results=request.app.state.player_service.search(search, limit))


@router.get("/players/{player_name}", response_model=LatestPlayerResponse)
def latest_player(player_name: str, request: Request) -> LatestPlayerResponse:
    """Return the most recent season row for a player."""
    service = request.app.state.player_service
    result = service.latest_stats(player_name)
    if result is None:
        raise _not_found(player_name, service.suggestions(player_name))
    canonical, stats = result
    return LatestPlayerResponse(player=canonical, latest_season=int(stats["season"]), stats=stats)


@router.get("/players/{player_name}/history", response_model=PlayerHistoryResponse)
def player_history(player_name: str, request: Request) -> PlayerHistoryResponse:
    """Return every available season for a player oldest first."""
    service = request.app.state.player_service
    result = service.history(player_name)
    if result is None:
        raise _not_found(player_name, service.suggestions(player_name))
    canonical, seasons = result
    return PlayerHistoryResponse(player=canonical, seasons=seasons)


@router.post("/predict", response_model=PredictionResponse)
def predict(request_body: PredictionRequest, request: Request) -> PredictionResponse:
    """Predict next-season points using the player's latest available season."""
    player_service = request.app.state.player_service
    found = player_service.find_player(request_body.player_name)
    if found is None:
        raise _not_found(request_body.player_name, player_service.suggestions(request_body.player_name))
    canonical, rows = found
    model_service = request.app.state.model_service
    predicted_pts, based_on_season = model_service.predict_for_player(rows)
    metric_values = {key: model_service.metrics[key] for key in ("mae", "mse", "rmse", "r2")}
    return PredictionResponse(player=canonical, season=based_on_season + 1,
                              based_on_season=based_on_season, predicted_pts=predicted_pts,
                              metrics=metric_values)


@router.get("/model/metrics", response_model=ModelMetrics)
def model_metrics(request: Request) -> ModelMetrics:
    """Return held-out metrics captured during offline training."""
    return ModelMetrics(**request.app.state.model_service.metrics)