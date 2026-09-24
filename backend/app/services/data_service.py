"""Dataset loading and cleaning."""

from pathlib import Path

import pandas as pd


ZERO_FILL_COLUMNS = [
    "x3p_per_game", "x3pa_per_game", "x3p_percent", "x2p_per_game",
    "x2pa_per_game", "x2p_percent", "e_fg_percent", "stl_per_game",
    "blk_per_game", "tov_per_game", "drb_per_game", "orb_per_game",
    "gs", "mp_per_game",
]
MEDIAN_FILL_COLUMNS = ["age", "fg_percent", "ft_percent", "trb_per_game", "pf_per_game"]


def load_and_clean_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load the player CSV and apply the project's established cleaning rules."""
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    dataframe = pd.read_csv(dataset_path, na_values=["NA"])
    cleaned = dataframe.copy()
    available_zero_columns = [column for column in ZERO_FILL_COLUMNS if column in cleaned]
    cleaned[available_zero_columns] = cleaned[available_zero_columns].fillna(0)
    available_median_columns = [column for column in MEDIAN_FILL_COLUMNS if column in cleaned]
    cleaned[available_median_columns] = cleaned[available_median_columns].fillna(
        cleaned[available_median_columns].median()
    )
    cleaned = cleaned.drop(columns=["lg", "player_id", "URL"], errors="ignore")
    cleaned["pos"] = cleaned["pos"].fillna("unknown")
    cleaned = cleaned.sort_values("g", ascending=False)
    cleaned = cleaned.groupby(["player", "season"], as_index=False).first()
    return cleaned.reset_index(drop=True)