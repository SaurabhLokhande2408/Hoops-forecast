"""Feature construction shared by training and inference."""

from dataclasses import dataclass

import pandas as pd
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "pts_per_game", "age_encoded", "fg_percent", "ft_percent", "x3p_percent",
    "mp_per_game", "ast_per_game", "trb_per_game", "g", "stl_per_game",
    "blk_per_game", "pos_C", "pos_PF", "pos_PG", "pos_SF", "pos_SG",
]
POSITION_COLUMNS = ["pos_C", "pos_PF", "pos_PG", "pos_SF", "pos_SG"]


@dataclass
class FeatureTransformer:
    """Fitted age scaler and position columns used by the model."""

    age_scaler: StandardScaler
    position_columns: list[str]


def build_features(
    dataframe: pd.DataFrame,
    transformer: FeatureTransformer | None = None,
) -> tuple[pd.DataFrame, FeatureTransformer]:
    """Build the shifted target and model features, fitting transforms when needed."""
    encoded = dataframe.sort_values(["player", "season"]).copy()
    encoded["next_season_pts"] = encoded.groupby("player")["pts_per_game"].shift(-1)
    encoded = encoded.dropna(subset=["next_season_pts"]).copy()
    encoded["next_season_pts"] = encoded["next_season_pts"].astype(float)
    encoded = pd.get_dummies(encoded, columns=["pos"], dtype=int)
    if transformer is None:
        transformer = FeatureTransformer(StandardScaler(), POSITION_COLUMNS.copy())
        transformer.age_scaler.fit(encoded[["age"]])
    encoded["age_encoded"] = transformer.age_scaler.transform(encoded[["age"]]).ravel()
    encoded = encoded.drop(columns=["age"])
    for column in transformer.position_columns:
        if column not in encoded:
            encoded[column] = 0
    return encoded, transformer


def transform_player_row(row: pd.DataFrame, transformer: FeatureTransformer) -> pd.DataFrame:
    """Transform one latest-season player row into the persisted model feature order."""
    transformed = pd.get_dummies(row.copy(), columns=["pos"], dtype=int)
    transformed["age_encoded"] = transformer.age_scaler.transform(transformed[["age"]]).ravel()
    transformed = transformed.drop(columns=["age"])
    for column in transformer.position_columns:
        if column not in transformed:
            transformed[column] = 0
    return transformed[FEATURE_COLUMNS]