from sklearn.preprocessing import StandardScaler
import pandas as pd

def encoding_scaling_func(df_copy):

    # Add target label for next season points per game
    df_copy = df_copy.sort_values(['player', 'season'])
    df_copy['next_season_pts'] = df_copy.groupby('player')['pts_per_game'].shift(-1)
    # Drop rows without a next season label
    df_copy = df_copy.dropna(subset=['next_season_pts'])
    df_copy['next_season_pts'] = df_copy['next_season_pts'].astype(float)

    # Encode pos column
    df_copy = pd.get_dummies(
        df_copy,
        columns=['pos'],
        dtype=int
    )

    # Scale age column
    s_s = StandardScaler()

    df_copy['age_encoded'] = s_s.fit_transform(df_copy[['age']])

    # Drop original age column
    df_copy = df_copy.drop(columns=['age'])

    # Final dataframe
    df_encoded = df_copy

    return df_encoded