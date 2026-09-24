# Hoops Forecast — Frontend

React (Vite) frontend for the Hoop-Forecast NBA points predictor.

## Setup

```
npm install
cp .env.example .env      # set VITE_API_BASE_URL to your FastAPI backend
npm run dev
```

Build: `npm run build` → output in `dist/`.

## Structure

```
src/
  api/            axios client + typed request functions
  components/     reusable UI: Navbar, Footer, PlayerSearchForm,
                  PredictionCard, StatsTable, MetricBadge, Loader, ErrorBanner
  hooks/          usePrediction — fetch + localStorage history
  pages/          Home (predict), History, About
```

## Expected backend API (see backend prompt)

| Method | Path                          | Purpose                          |
|--------|-------------------------------|-----------------------------------|
| GET    | /api/health                   | liveness + model status          |
| GET    | /api/players?search=&limit=   | autocomplete                     |
| GET    | /api/players/{name}           | latest season stats for a player |
| GET    | /api/players/{name}/history   | full season history for a player |
| POST   | /api/predict                  | body `{player_name}` → prediction|
| GET    | /api/model/metrics            | MAE/MSE/RMSE/R², features         |

All responses are JSON. Build the backend to match this contract exactly —
the frontend is already wired against it.
