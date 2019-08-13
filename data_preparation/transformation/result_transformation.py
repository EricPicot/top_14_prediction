import pandas as pd
import numpy as np
import sys
sys.path.append( '../data_preparation/raw_data')

class ResultTransformation():
    
    def __init__(self):

#         # ---- Initialize attributes ----
        self.result_df = None



    def set_result_df(self, df):

        # Raw Data saving file
        self.result_df  = df.copy()

        
    def transform(self):

#         self.result_df = pd.read_csv(self.raw_data_path, sep = "|")


        # Pour l'instant on tachera de prédire la saison reguliere
        self.result_df = self.result_df.loc[~self.result_df["season_day"].isin(["Match accession",
                                        'Barrages',
                                        'Matchs de barrage',
                                        'Demi Finales',
                                        'Demi-Finales',
                                        'Demi-finales',
                                        'Finale'])]
        self.result_df[["day_of_week","day_of_month","month"]] = self.result_df\
                                                                                        .date\
                                                                                        .str\
                                                                                        .split(" ")\
                                                                                        .apply(pd.Series)
        self.result_df["month"] = self.result_df["month"].str.lower().str.replace("û","u").str.replace("é","e").str.replace("è","e")
        self.result_df["bonus_dom"] = self.result_df["bonus_dom"].fillna("0")
        self.result_df["bonus_ext"] = self.result_df["bonus_ext"].fillna("0")
        self.result_df["score_dom"] =  self.result_df["score_dom"].astype(int) 
        self.result_df["score_ext"] =  self.result_df["score_ext"].astype(int) 
        self.result_df["season_day"] = self.result_df["season_day"].astype(int) 

        self.result_df["label"] = self.result_df["score_dom"]>self.result_df["score_ext"]

#         self.result_df.to_csv(self.raw_transformed_data_path,
#                                     sep='|',
#                                     encoding='utf-8',
#                                     index=False)

#         print('Updated Raw Data exported to {}'.format(self.raw_transformed_data_path))

