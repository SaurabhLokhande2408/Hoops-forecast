import os
import sys
from sklearn.linear_model import LinearRegression

# Ensure the project root is on sys.path when running this file directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from ML_training.input_output import data_training_func
from Data_preprocessing.check_up import check_up_func
from Data_preprocessing.encoding_scaling import encoding_scaling_func

FEATURE_COLUMNS = [
    'pts_per_game',
    'age_encoded',
    'fg_percent',
    'ft_percent',
    'x3p_percent',
    'mp_per_game',
    'ast_per_game',
    'trb_per_game',
    'g',
    'stl_per_game',
    'blk_per_game',
    'pos_C',
    'pos_PF',
    'pos_PG',
    'pos_SF',
    'pos_SG'
]


def build_and_train_model():
    df_copy = check_up_func()
    df_encoded = encoding_scaling_func(df_copy)
    X_train, X_test, y_train, y_test = data_training_func(df_encoded=df_encoded)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, df_encoded


def predict_next_season_points(model, df_encoded, player_name: str):
    player_name = player_name.strip().lower()
    matches = df_encoded[df_encoded['player'].str.lower() == player_name]

    if matches.empty:
        raise ValueError(f"Player '{player_name}' not found in encoded dataset.")

    latest = matches.sort_values('season', ascending=False).iloc[0]
    features = latest[FEATURE_COLUMNS].values.reshape(1, -1)
    prediction = model.predict(features)[0]
    return latest['player'], int(latest['season']) + 1, float(prediction)


if __name__ == '__main__':
    model, df_encoded = build_and_train_model()
    player_name = input('Enter player name to predict next season points: ')
    try:
        player, next_season, predicted_pts = predict_next_season_points(model, df_encoded, player_name)
        print(f"Prediction for {player} in season {next_season}: {predicted_pts:.1f} pts per game")
    except ValueError as error:
        print(error)
