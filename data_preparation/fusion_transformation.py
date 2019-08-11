import pandas as pd
import numpy as np
import sys
from transformation.matches_result_transformation import ResultsTransformation
from transformation.ranking_transformation import RankingTransformation

class FusionTransformation(ResultsTransformation, RankingTransformation):
    
    def __init__(self):
        self.data = ResultsTransformation().matches_result_df
        self.classement = RankingTransformation().ranking_df
        for which in ["_dom","_ext"]:
            self.data = self.data.merge(right = self.classement,
                            right_on = ["season_id","season_day+1",'equipe'],
                            left_on = ["season_id","season_day","team"+which],
                            how = "inner").drop(["equipe",'day_url_y', 'season_day_y',"season_day+1"], axis=1)

            self.data = self.data.rename(columns = {'season_day_x':"season_day",
                                     'day_url_x': "day_url"})

            for x in ['classement', 'nb_pts', 'nb_matchs_joues', 'victoire', 'nul', 'defaite',
               'nb_bonus', 'pts_marques', 'pts_pris', 'ga']:
                self.data = self.data.rename(columns = {x:x+which})

        print(self.data.columns)
#         self.data["win_ratio_dom"] = self.data["victoire_dom"]/self.data["nb_matchs_joues_dom"]
#         self.data["win_ratio_ext"] = self.data["victoire_ext"]/self.data["nb_matchs_joues_ext"]

#         # Ratio de bonus
#         self.data["bonus_ratio_dom"] = self.data["nb_bonus_dom"]/self.data["nb_matchs_joues_dom"]
#         self.data["bonus_ratio_ext"] = self.data["nb_bonus_ext"]/self.data["nb_matchs_joues_ext"]

#         # Average goal average
#         self.data["aga_dom"] = self.data["ga_dom"]/self.data["nb_matchs_joues_dom"]
#         self.data["aga_ext"] = self.data["ga_ext"]/self.data["nb_matchs_joues_ext"]
#         self.data = pd.get_dummies(self.data,columns=['day_of_week'])
#         self.data = self.data.dropna(how = "any")

        self.data.to_csv("raw_data/transformed_self.data_class.csv", sep = "|")
# print(a.data)
        print("self.data transformed and saved !")
    
FusionTransformation()

