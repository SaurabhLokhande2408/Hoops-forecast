import { useEffect, useRef, useState } from "react";
import { searchPlayers } from "../api/predictionApi";

export default function PlayerSearchForm({ onSubmit, loading }) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (query.trim().length < 2) {
      setSuggestions([]);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      try {
        const data = await searchPlayers(query.trim());
        setSuggestions(data.results || []);
      } catch {
        setSuggestions([]);
      }
    }, 300);
    return () => clearTimeout(debounceRef.current);
  }, [query]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setShowSuggestions(false);
    onSubmit(query.trim());
  };

  const pick = (name) => {
    setQuery(name);
    setShowSuggestions(false);
    onSubmit(name);
  };

  return (
    <form className="search-form" onSubmit={handleSubmit} autoComplete="off">
      <div className="search-form__field">
        <input
          type="text"
          value={query}
          placeholder="Enter player name, e.g. Stephen Curry"
          onChange={(e) => {
            setQuery(e.target.value);
            setShowSuggestions(true);
          }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {showSuggestions && suggestions.length > 0 && (
          <ul className="search-form__suggestions">
            {suggestions.map((s) => (
              <li key={s.player} onMouseDown={() => pick(s.player)}>
                <span>{s.player}</span>
                <span className="search-form__meta">
                  last: {s.last_season}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </form>
  );
}
