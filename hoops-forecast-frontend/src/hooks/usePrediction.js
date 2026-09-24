import { useState, useCallback } from "react";
import { predictNextSeason, getPlayerHistory } from "../api/predictionApi";

const HISTORY_KEY = "hoops_forecast_history";

function saveToLocalHistory(entry) {
  try {
    const existing = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    const next = [entry, ...existing.filter((e) => e.player !== entry.player)].slice(0, 20);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
  } catch {
    /* localStorage unavailable, ignore */
  }
}

export function getLocalHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

export default function usePrediction() {
  const [prediction, setPrediction] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runPrediction = useCallback(async (playerName) => {
    setLoading(true);
    setError(null);
    setPrediction(null);
    try {
      const [predictionData, historyData] = await Promise.all([
        predictNextSeason(playerName),
        getPlayerHistory(playerName).catch(() => ({ seasons: [] }))
      ]);
      setPrediction(predictionData);
      setSeasons(historyData.seasons || []);
      saveToLocalHistory({
        player: predictionData.player,
        season: predictionData.season,
        predicted_pts: predictionData.predicted_pts,
        timestamp: Date.now()
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { prediction, seasons, loading, error, runPrediction };
}
