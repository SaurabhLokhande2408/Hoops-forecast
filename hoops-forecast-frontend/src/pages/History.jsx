import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getLocalHistory } from "../hooks/usePrediction";

export default function History() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    setItems(getLocalHistory());
  }, []);

  return (
    <section className="page page--history">
      <h1>Your prediction history</h1>
      <p className="page__subtitle">Stored locally in this browser only.</p>

      {items.length === 0 ? (
        <p className="empty-state">
          No predictions yet. <Link to="/">Go predict one.</Link>
        </p>
      ) : (
        <ul className="history-list">
          {items.map((item) => (
            <li key={item.player + item.timestamp} className="history-list__item">
              <span className="history-list__player">{item.player}</span>
              <span>
                {Number(item.predicted_pts).toFixed(1)} pts — season {item.season}
              </span>
              <span className="history-list__time">
                {new Date(item.timestamp).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
