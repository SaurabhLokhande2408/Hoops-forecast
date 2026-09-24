# Hoop Forecast Backend

FastAPI backend for the NBA points-per-game forecast frontend. The backend reads the existing `Dataset/Player Per Game.csv` file and never modifies it.

## Setup

From this directory, create an environment and install dependencies:

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` when paths or CORS origins need changing. Paths are relative to `backend/` unless absolute.

Train the model once before starting the API:

```bash
python -m app.ml.train
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`; interactive docs are at `/docs`.

## Routes

All API routes use the `/api` prefix.

### Health

```bash
curl http://localhost:8000/api/health
```

### Search players

```bash
curl "http://localhost:8000/api/players?search=cur&limit=8"
```

The search is a case-insensitive substring search. The query must contain at least two characters.

### Latest player stats

```bash
curl "http://localhost:8000/api/players/Stephen%20Curry"
```

### Player history

```bash
curl "http://localhost:8000/api/players/Stephen%20Curry/history"
```

### Predict next-season points

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Stephen Curry"}'
```

The prediction uses the player's latest available season and returns the held-out training metrics saved with the model.

### Model metrics

```bash
curl http://localhost:8000/api/model/metrics
```

## Tests

After training the artifacts, run:

```bash
pytest
```

The generated files under `app/artifacts/` are local model outputs and should be regenerated with `python -m app.ml.train` when the dataset changes.