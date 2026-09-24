import client from "./client";

/** GET /api/health -> { status, model_loaded, rows_loaded } */
export const getHealth = () => client.get("/health").then((r) => r.data);

/** GET /api/players?search=<query>&limit=<n> -> { results: [{ player, seasons_played, last_season }] } */
export const searchPlayers = (search, limit = 8) =>
  client.get("/players", { params: { search, limit } }).then((r) => r.data);

/** GET /api/players/{player_name} -> { player, latest_season, stats: {...} } */
export const getPlayerLatestStats = (playerName) =>
  client.get(`/players/${encodeURIComponent(playerName)}`).then((r) => r.data);

/** GET /api/players/{player_name}/history -> { player, seasons: [{season, pts_per_game, ...}] } */
export const getPlayerHistory = (playerName) =>
  client.get(`/players/${encodeURIComponent(playerName)}/history`).then((r) => r.data);

/** POST /api/predict  body: { player_name } -> { player, season, predicted_pts, based_on_season, metrics: {mae,mse,rmse,r2} } */
export const predictNextSeason = (playerName) =>
  client.post("/predict", { player_name: playerName }).then((r) => r.data);

/** GET /api/model/metrics -> { mae, mse, rmse, r2, trained_on_rows, features: [...] } */
export const getModelMetrics = () => client.get("/model/metrics").then((r) => r.data);
