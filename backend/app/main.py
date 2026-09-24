"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.routes import router
from app.config import settings
from app.services.data_service import load_and_clean_dataset
from app.services.model_service import ModelService
from app.services.player_service import PlayerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the dataset and model exactly once for the application lifetime."""
    dataframe = load_and_clean_dataset(settings.resolve_path(settings.dataset_path))
    model_service = ModelService(
        settings.resolve_path(settings.model_path),
        settings.resolve_path(settings.metrics_path),
        settings.resolve_path(settings.feature_columns_path),
    )
    app.state.dataframe = dataframe
    app.state.player_service = PlayerService(dataframe)
    app.state.model_service = model_service
    yield


app = FastAPI(title="Hoop Forecast API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect the API root to interactive documentation."""
    return RedirectResponse(url="/docs")