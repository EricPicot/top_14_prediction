import pandas as pd
import numpy as np
import sys


class RankingTransformation():
    
    def __init__(self):
        
        self.ranking_df = None

        # ---- Initialize attributes ----        
        

        
    def set_ranking_df(self, df):
        
        self.ranking_df = df
        
    def transform(self):
    
#         self.ranking_df = pd.read_csv(self.raw_data_path, sep = "|")
        self.ranking_df = self.ranking_df.rename(columns={"season": "season_id",
                                               "day" : "season_day",
                                               "bonus":"nb_bonus"})
        #self.ranking_df["equipe"] = self.ranking_df["equipe"].str.split("\n").apply(lambda x: x[0]).str.strip()
        self.ranking_df = self.ranking_df[~self.ranking_df["season_day"].isin(['Barrages','Matchs de barrage','Demi Finales','Match accession','Demi-Finales','Demi-finales','Finale'])]

        self.ranking_df["season_day+1"] = self.ranking_df["season_day"].astype(int)+1
        self.ranking_df["equipe"] = self.ranking_df["equipe"].str.replace("è","e").str.replace("é","e").str.replace("ç","c").str.replace("Brive", "CA Brive")
        self.ranking_df["equipe"] = self.ranking_df["equipe"].str.split("\n").apply(lambda x: x[0]).str.strip()

#         self.ranking_df.to_csv(self.raw_transformed_data_path,
#                                             sep='|',
#                                             encoding='utf-8',
#                                             index=False)

#         print('Updated Raw Data exported to {}'.format(self.raw_transformed_data_path))


# r = RankingTransformation()
# df = pd.read_csv("../raw_data/ranking_results.csv", sep = "|")
# r.set_ranking_df(df)
# r.transform()
        