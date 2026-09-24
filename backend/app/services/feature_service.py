"""Feature construction shared by training and inference."""

from dataclasses import dataclass

import pandas as pd
from sklearn.preprocessing import StandardScaler

from Data_preprocessing.encoding_scaling import encoding_scaling_func
from ML_prediction.ml_model import FEATURE_COLUMNS


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
    if transformer is None:
        transformer = FeatureTransformer(StandardScaler(), POSITION_COLUMNS.copy())
    encoded = encoding_scaling_func(encoded, age_scaler=transformer.age_scaler)
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