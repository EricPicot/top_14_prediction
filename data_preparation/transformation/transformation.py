import pandas as pd
import numpy as np
import sys

mr = pd.read_csv("../raw_data/matches_results.csv", sep = "|")

# Pour l'instant on tachera de prédire la saison reguliere
mr = mr[~mr["season_day"].isin(["Match accession",
                                'Barrages',
                                'Matchs de barrage',
                                'Demi Finales',
                                'Demi-Finales',
                                'Demi-finales',
                                'Finale'])]
mr[["day_of_week","day_of_month","month"]] = mr.date.str.split(" ").apply(pd.Series)
mr["month"] = mr["month"].str.lower().str.replace("û","u").str.replace("é","e").str.replace("è","e")
mr["bonus_dom"] = mr["bonus_dom"].fillna("0")
mr["bonus_ext"] = mr["bonus_ext"].fillna("0")
mr["score_dom"] =  mr["score_dom"].astype(int) 
mr["score_ext"] =  mr["score_ext"].astype(int) 
mr["season_day"] = mr["season_day"].astype(int) 

mr["label"] = mr["score_dom"]>mr["score_ext"]




classement = pd.read_csv("../raw_data/ranking_results.csv", sep = "|")
classement = classement.rename(columns={"season": "season_id",
                                       "day" : "season_day",
                                       "bonus":"nb_bonus"})
classement = classement[~classement["season_day"].isin(['Barrages','Matchs de barrage','Demi Finales','Match accession','Demi-Finales','Demi-finales','Finale'])]

classement["season_day+1"] = classement["season_day"].astype(int)+1
data= mr
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

data.to_csv("../raw_data/transformed_data.csv", sep = "|")
print("data transformed and saved !")