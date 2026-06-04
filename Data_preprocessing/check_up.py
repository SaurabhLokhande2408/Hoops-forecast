import pandas as pd
def check_up_func():
    
    data=pd.read_csv("D:\\Programs\\BACKEND\\PROJECTS_SCRATCH\\NBA\\Dataset\\Player Per Game.csv")
    df=pd.DataFrame(data)
   # print(df.head(20))
    #print("\n---------Isnull values in the dataset---------\n")
   # print(df.isnull().sum())
    #df.info()

    df_copy=df.copy()

    df_copy[['x3p_per_game', 'x3pa_per_game', 'x3p_percent', 'x2p_per_game', 'x2pa_per_game', 'x2p_percent', 'e_fg_percent', 'stl_per_game', 'blk_per_game', 'tov_per_game', 'drb_per_game', 'orb_per_game', 'gs', 'mp_per_game']] = df_copy[['x3p_per_game', 'x3pa_per_game', 'x3p_percent', 'x2p_per_game', 'x2pa_per_game', 'x2p_percent', 'e_fg_percent', 'stl_per_game', 'blk_per_game', 'tov_per_game', 'drb_per_game', 'orb_per_game', 'gs', 'mp_per_game']].fillna(0)
    #print("\n---------Isnull values in the dataset after filling with 0---------\n")
   # print(df_copy.isnull().sum())



    df_copy[["age", "fg_percent", "ft_percent", "trb_per_game", "pf_per_game"]] = df_copy[["age", "fg_percent", "ft_percent", "trb_per_game", "pf_per_game"]].fillna(df_copy[["age", "fg_percent", "ft_percent", "trb_per_game", "pf_per_game"]].median())
    df_copy = df_copy.drop(columns=["lg", "player_id", "URL"], errors='ignore')

    df_copy['pos']=df_copy['pos'].fillna("unknown")

    # keep only the TOT row for each player-season by sorting on games played first
    df_copy = df_copy.sort_values("g", ascending=False)
    df_copy = df_copy.groupby(["player", "season"]).first().reset_index()

   # print("\n---------Isnull values in the dataset after filling with median and dropping columns---------\n")
   # print(df_copy.isnull().sum())
   # print(df_copy.head(20))
   # if you still have the original df
    print(df.columns.tolist())

    return df_copy