import { useEffect, useState } from "react";
import MetricBadge from "../components/MetricBadge";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";
import { getModelMetrics } from "../api/predictionApi";

export default function About() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getModelMetrics()
      .then(setMetrics)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="page page--about">
      <h1>About Hoop-Forecast</h1>
      <p>
        A Linear Regression model trained on 33,000+ NBA player-seasons
        (1947–2026), sourced from Basketball Reference. Given a player's
        current-season stats, it projects next season's points per game.
      </p>

      {loading && <Loader label="Loading model metrics..." />}
      <ErrorBanner message={error} />

      {metrics && (
        <>
          <div className="about__metrics">
            <MetricBadge label="MAE" value={metrics.mae?.toFixed(2)} />
            <MetricBadge label="MSE" value={metrics.mse?.toFixed(2)} />
            <MetricBadge label="RMSE" value={metrics.rmse?.toFixed(2)} />
            <MetricBadge label="R²" value={metrics.r2?.toFixed(2)} />
          </div>
          <p className="about__rows">
            Trained on {metrics.trained_on_rows?.toLocaleString()} rows.
          </p>
          {metrics.features && (
            <div className="about__features">
              <h3>Features used</h3>
              <ul>
                {metrics.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </section>
  );
}
