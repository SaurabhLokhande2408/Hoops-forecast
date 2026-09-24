import os
from sklearn.linear_model import LinearRegression
from Data_preprocessing.check_up import check_up_func
from Data_preprocessing.encoding_scaling import encoding_scaling_func
from Ml_training.input_output import data_training_func

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


df_copy = check_up_func()
df_encoded = encoding_scaling_func(df_copy)
X_train, X_test, y_train, y_test = data_training_func(df_encoded)
#branch
model = LinearRegression()
model.fit(X_train, y_train)

player_name = input('Enter player name to predict next season points (or press Enter to skip): ').strip()
if player_name:
    matches = df_encoded[df_encoded['player'].str.lower() == player_name.lower()]
    if matches.empty:
        print(f"Player '{player_name}' not found in the dataset.")
    else:
        latest = matches.sort_values('season', ascending=False).iloc[0]
        features = latest[FEATURE_COLUMNS].values.reshape(1, -1)
        prediction = model.predict(features)[0]
        print(f"Prediction for {latest['player']} in season {int(latest['season']) + 1}: {prediction:.1f} pts per game")

from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np

y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2:", r2_score(y_test, y_pred))