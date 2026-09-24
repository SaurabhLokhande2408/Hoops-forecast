import PlayerSearchForm from "../components/PlayerSearchForm";
import PredictionCard from "../components/PredictionCard";
import StatsTable from "../components/StatsTable";
import Loader from "../components/Loader";
import ErrorBanner from "../components/ErrorBanner";
import usePrediction from "../hooks/usePrediction";

export default function Home() {
  const { prediction, seasons, loading, error, runPrediction } = usePrediction();

  return (
    <section className="page page--home">
      <div className="hero">
        <h1>
          Predict next season's <span className="hero__accent">points per game</span>
        </h1>
        <p>
          Type any NBA player's name. Our Linear Regression model, trained on
          33,000+ player-seasons since 1947, projects their scoring next season.
        </p>
        <PlayerSearchForm onSubmit={runPrediction} loading={loading} />
      </div>

      {loading && <Loader label="Crunching stats..." />}
      <ErrorBanner message={error} onRetry={() => prediction && runPrediction(prediction.player)} />

      {prediction && !loading && (
        <div className="results">
          <PredictionCard prediction={prediction} />
          {seasons.length > 0 && (
            <div className="results__history">
              <h3>Season history</h3>
              <StatsTable rows={seasons} />
            </div>
          )}
        </div>
      )}
    </section>
  );
}
