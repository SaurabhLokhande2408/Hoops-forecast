"""Player search and season lookup operations."""

import difflib

import pandas as pd


STATS_COLUMNS = [
    "season", "age", "pos", "g", "mp_per_game", "pts_per_game", "ast_per_game",
    "trb_per_game", "stl_per_game", "blk_per_game", "fg_percent", "x3p_percent",
    "ft_percent",
]


class PlayerService:
    """Read-only player operations over the cleaned dataset."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Store the cleaned dataframe used by all player requests."""
        self.dataframe = dataframe

    def find_player(self, player_name: str) -> tuple[str, pd.DataFrame] | None:
        """Return the canonical name and rows for an exact case-insensitive match."""
        normalized = player_name.strip().casefold()
        matches = self.dataframe[self.dataframe["player"].str.casefold() == normalized]
        if matches.empty:
            return None
        canonical = str(matches.iloc[0]["player"])
        return canonical, matches.sort_values("season")

    def suggestions(self, player_name: str) -> list[str]:
        """Return close canonical name suggestions for an unsuccessful exact lookup."""
        names = self.dataframe["player"].drop_duplicates().tolist()
        return difflib.get_close_matches(player_name, names, n=3, cutoff=0.45)

    def search(self, query: str, limit: int) -> list[dict[str, int | str]]:
        """Return deduplicated substring matches ordered by latest season."""
        matches = self.dataframe[self.dataframe["player"].str.contains(query, case=False, regex=False)]
        results = (
            matches.groupby("player", as_index=False)
            .agg(seasons_played=("season", "nunique"), last_season=("season", "max"))
            .sort_values(["last_season", "player"], ascending=[False, True])
            .head(limit)
        )
        return results.to_dict("records")

    def latest_stats(self, player_name: str) -> tuple[str, dict[str, object]] | None:
        """Return the latest season stats for an exact player match."""
        found = self.find_player(player_name)
        if found is None:
            return None
        canonical, rows = found
        row = rows.iloc[-1]
        return canonical, {column: row[column] for column in STATS_COLUMNS}

    def history(self, player_name: str) -> tuple[str, list[dict[str, object]]] | None:
        """Return all season stats oldest first for an exact player match."""
        found = self.find_player(player_name)
        if found is None:
            return None
        canonical, rows = found
        return canonical, [{column: row[column] for column in STATS_COLUMNS} for _, row in rows.iterrows()]