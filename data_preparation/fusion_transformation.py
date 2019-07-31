import pandas as pd
import numpy as np
import sys
from transformation.matches_result_transformation import ResultsTransformation
from transformation.ranking_transformation import RankingTransformation

data= ResultsTransformation().matches_result_df
classement = RankingTransformation().ranking_df
for which in ["_dom","_ext"]:
    data = data.merge(right = classement,
                    right_on = ["season_id","season_day+1",'equipe'],
                    left_on = ["season_id","season_day","team"+which],
                    how = "inner").drop(["equipe",'day_url_y', 'season_day_y',"season_day+1"], axis=1)
    
    data = data.rename(columns = {'season_day_x':"season_day",
                             'day_url_x': "day_url"})
    
    for x in ['classement', 'nb_pts', 'nb_matchs_joues', 'victoire', 'nul', 'defaite',
       'nb_bonus', 'pts_marques', 'pts_pris', 'ga']:
        data = data.rename(columns = {x:x+which})
        
# print(data.columns)
# Ratio de victoires
data["win_ratio_dom"] = data["victoire_dom"]/data["nb_matchs_joues_dom"]
data["win_ratio_ext"] = data["victoire_ext"]/data["nb_matchs_joues_ext"]

# Ratio de bonus
data["bonus_ratio_dom"] = data["nb_bonus_dom"]/data["nb_matchs_joues_dom"]
data["bonus_ratio_ext"] = data["nb_bonus_ext"]/data["nb_matchs_joues_ext"]

# Average goal average
data["aga_dom"] = data["ga_dom"]/data["nb_matchs_joues_dom"]
data["aga_ext"] = data["ga_ext"]/data["nb_matchs_joues_ext"]

data = pd.get_dummies(data,columns=['day_of_week'])
data = data.dropna(how = "any")

data.to_csv("raw_data/transformed_data_class.csv", sep = "|")
print("data transformed and saved !")