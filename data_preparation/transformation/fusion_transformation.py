import pandas as pd
import numpy as np
import sys

from result_transformation import ResultTransformation
from ranking_transformation import RankingTransformation


def merging_data(ranking_df, result_df):
    data = result_df
    for which in ["_dom","_ext"]:
        data = data.merge(right = ranking_df,
                            left_on = ["season_id","season_day","team"+which],
                            right_on = ["season_id","season_day+1",'equipe'],
                            how = "inner").drop(["equipe",'day_url_y', 'season_day_y',"season_day+1"], axis=1)

        data = data.rename(columns = {'season_day_x':"season_day",
                                     'day_url_x': "day_url"})

        for x in ['classement', 'nb_pts', 'nb_matchs_joues', 'victoire', 'nul', 'defaite',
               'nb_bonus', 'pts_marques', 'pts_pris', 'ga']:
            data = data.rename(columns = {x:x+which})

    data["win_ratio_dom"] = data["victoire_dom"]/data["nb_matchs_joues_dom"]
    data["win_ratio_ext"] = data["victoire_ext"]/data["nb_matchs_joues_ext"]

        # Ratio de bonus
    data["bonus_ratio_dom"] = data["nb_bonus_dom"]/data["nb_matchs_joues_dom"]
    data["bonus_ratio_ext"] = data["nb_bonus_ext"]/data["nb_matchs_joues_ext"]

        # Average goal average
    data["aga_dom"] = data["ga_dom"]/data["nb_matchs_joues_dom"]
    data["aga_ext"] = data["ga_ext"]/data["nb_matchs_joues_ext"]
    data = pd.get_dummies(data,columns=['day_of_week'])
    data = data.fillna(0)

    return data
    
    
    
    
    
# ranking_df = pd.read_csv( '../raw_data/ranking_results.csv', sep = "|")
# Ranking = RankingTransformation()
# Ranking.set_ranking_df(ranking_df)
# Ranking.transform()


# results_df = pd.read_csv( '../raw_data/matches_results.csv', sep = "|")
# Results = ResultsTransformation()
# Results.set_result_df(results_df)
# Results.transform()

# # print(Results.result_df.columns)

# Merged = merging_data(Ranking.ranking_df, Results.result_df)

