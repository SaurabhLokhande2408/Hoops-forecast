import os
from sklearn.model_selection import train_test_split

def data_training_func(df_encoded, verbose=True):
    """Split encoded features and target into reproducible train/test sets."""

    X = df_encoded[
        [
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
    ]

    y = df_encoded['next_season_pts']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if verbose:
        print("\n------------Training X ---------------")
        print(X_train)
        print("\n------------Training y ---------------")
        print(y_train)
        print("\n------------Test X ---------------")
        print(X_test)
        print("\n------------Test y ---------------")
        print(y_test)

    return X_train, X_test, y_train, y_test
