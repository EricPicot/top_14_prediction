import pandas as pd
import numpy as np
import sys


class ResultsTransformation():
    
    def __init__(self):

        # ---- Initialize attributes ----
        # Raw Data saving file
        self.raw_data_path = 'raw_data/matches_results.csv'
        self.raw_transformed_data_path =  '../raw_data/matches_transformed_results.csv'
        self.matches_result_df = pd.read_csv(self.raw_data_path, sep = "|")


        # Pour l'instant on tachera de prédire la saison reguliere
        self.matches_result_df = self.matches_result_df[~self.matches_result_df["season_day"].isin(["Match accession",
                                        'Barrages',
                                        'Matchs de barrage',
                                        'Demi Finales',
                                        'Demi-Finales',
                                        'Demi-finales',
                                        'Finale'])]
        self.matches_result_df[["day_of_week","day_of_month","month"]] = self.matches_result_df.date.str.split(" ").apply(pd.Series)
        self.matches_result_df["month"] = self.matches_result_df["month"].str.lower().str.replace("û","u").str.replace("é","e").str.replace("è","e")
        self.matches_result_df["bonus_dom"] = self.matches_result_df["bonus_dom"].fillna("0")
        self.matches_result_df["bonus_ext"] = self.matches_result_df["bonus_ext"].fillna("0")
        self.matches_result_df["score_dom"] =  self.matches_result_df["score_dom"].astype(int) 
        self.matches_result_df["score_ext"] =  self.matches_result_df["score_ext"].astype(int) 
        self.matches_result_df["season_day"] = self.matches_result_df["season_day"].astype(int) 

        self.matches_result_df["label"] = self.matches_result_df["score_dom"]>self.matches_result_df["score_ext"]

#         self.matches_result_df.to_csv(self.raw_transformed_data_path,
#                                     sep='|',
#                                     encoding='utf-8',
#                                     index=False)

#         print('Updated Raw Data exported to {}'.format(self.raw_transformed_data_path))
