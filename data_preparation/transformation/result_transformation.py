import pandas as pd
import numpy as np
import sys
sys.path.append( '../data_preparation/raw_data')

nom_standard = {'Oyonnax':'Oyonnax',
 'Racing 92':'Racing 92',
 'Montpellier':'Montpellier Herault Rugby',
 'Paris':'Stade Francais Paris',
 'Brive':'CA Brive',
 'CA Brive':'CA Brive',
 'Bordeaux-Bègles':'Union Bordeaux-Begles',
 'Toulon':'RC Toulon',
 'Agen':'SU Agen',
 'Lyon':"LOU Rugby",
 'Castres':"Castres Olympique",
 'Toulouse':"Stade Toulousain",
 'Clermont':"ASM Clermont",
 'La Rochelle':'Stade Rochelais',
 'Pau':'Section Paloise',
 'Perpignan':'USA Perpignan',
 'Grenoble':'FC Grenoble Rugby',
 'RC Toulon':'RC Toulon',
 'Castres Olympique':"Castres Olympique",
 'FC Grenoble Rugby':"FC Grenoble Rugby",
 'SU Agen':"Agen",
 'Union Bordeaux-Bègles':'Union Bordeaux-Begles',
 'ASM Clermont':"ASM Clermont",
 'Stade Toulousain':'Stade Toulousain',
 'LOU Rugby':"LOU Rugby",
 'Stade Français Paris':'Stade Francais Paris',
 'USA Perpignan':"USA Perpignan",
 'Section Paloise': "Section Paloise",
 'Stade Rochelais':"Stade Rochelais",
 'Montpellier Hérault Rugby':"Montpellier Herault Rugby",
 'Béziers':'Beziers',
 'Bayonne':"Aviron Bayonnais",
 "Aviron Bayonnais":"Aviron Bayonnais",
 'Auch':"Auch",
 'Biarritz':"Biarritz",
 'Bourgoin':'Bourguoin',
 'Narbonne':'Narbonne',
 'Montauban':'Montauban',
 'Albi':'Albi',
 'Dax':'Dax',
 'Mont-de-Marsan':'Mont-de-Marsan'}

class ResultTransformation():
    
    def __init__(self):

#         # ---- Initialize attributes ----
        self.result_df = None



    def set_result_df(self, df):

        # Raw Data saving file
        self.result_df  = df.copy()

        
    def transform(self):

        # self.result_df = pd.read_csv(self.raw_data_path, sep = "|")


        # Pour l'instant on tachera de predire la saison reguliere
        self.result_df = (self.result_df.loc[~self.result_df["season_day"].isin([
                                        "Match accession",
                                        'Barrages',
                                        'Matchs de barrage',
                                        'Demi Finales',
                                        'Demi-Finales',
                                        'Demi-finales',
                                        'Finale'])])
        self.result_df[["day_of_week", "day_of_month""month"]] = (self.result_df.date
                                                                                .str
                                                                                .split(" ")
                                                                      .apply(pd.Series))

        self.result_df["month"] = (self.result_df["month"].str.lower()
                                                         .str.replace("û", "u")
                                                         .str.replace("é", "e")
                                                         .str.replace("è", "e"))
        self.result_df["bonus_dom"] = self.result_df["bonus_dom"].fillna("0")
        self.result_df["bonus_ext"] = self.result_df["bonus_ext"].fillna("0")
        self.result_df["score_dom"] = self.result_df["score_dom"].astype(int)
        self.result_df["score_ext"] = self.result_df["score_ext"].astype(int)
        self.result_df["season_day"] = self.result_df["season_day"].astype(int) 

        self.result_df["label"] = self.result_df["score_dom"] > self.result_df["score_ext"]
        
        self.result_df["team_dom"] = self.result_df["team_dom"].apply(lambda x: nom_standard[x]) 
        self.result_df["team_ext"] = self.result_df["team_ext"].apply(lambda x: nom_standard[x]) 

#         self.result_df.to_csv(self.raw_transformed_data_path,
#                                     sep='|',
#                                     encoding='utf-8',
#                                     index=False)

#         print('Updated Raw Data exported to {}'.format(self.raw_transformed_data_path))

