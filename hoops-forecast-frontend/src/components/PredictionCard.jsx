import MetricBadge from "./MetricBadge";

export default function PredictionCard({ prediction }) {
  if (!prediction) return null;
  const { player, season, predicted_pts, based_on_season, metrics } = prediction;

  return (
    <div className="prediction-card">
      <div className="prediction-card__header">
        <h2>{player}</h2>
        <span className="prediction-card__season">
          Projected for season {season}
        </span>
      </div>

      <div className="prediction-card__main">
        <span className="prediction-card__pts">
          {Number(predicted_pts).toFixed(1)}
        </span>
        <span className="prediction-card__unit">pts / game</span>
      </div>

      <p className="prediction-card__basis">
        Based on {player}'s {based_on_season} season stats.
      </p>

      {metrics && (
        <div className="prediction-card__metrics">
          <MetricBadge label="MAE" value={metrics.mae?.toFixed(2)} />
          <MetricBadge label="RMSE" value={metrics.rmse?.toFixed(2)} />
          <MetricBadge label="R²" value={metrics.r2?.toFixed(2)} />
        </div>
      )}
    </div>
  );
}
