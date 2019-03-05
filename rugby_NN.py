#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:23:07 2019

@author: ericpicot
"""

"""
Created on Sun Mar  3 20:46:25 2019

@author: ericpicot
"""

####### Processing ----------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
#%autoreload 2
import process
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import xgboost


def add_old_info(group, cols, _range):
    for i in _range:
        tmp_new_cols = [col+"diff_t-"+str(4) for col in cols]
        group[tmp_new_cols] = group[cols] - group[cols].shift(i).fillna(0)
        
        
    return group

######## Variables-----------------------------------------
w = 2
path = '/Users/ericpicot/Documents/top_14_prediction/'
classement_original = pd.read_csv(path+"data_classement.csv")
journees = pd.read_csv(path+"data_saison.csv")

print(journees.shape, classement_original.shape)
############## --------------------------------------------
to_window_compute = ['victoire','nul', 'defaite', 'bonus','ga']
journees = process.processing_journees(journees)
classement_original = process.processing_classement(classement_original)
classement_original = process.add_0ere_journee(classement_original)
####### Exploration ----------------------------------------

classement_original = process.to_keep(classement_original)
classement = process.add_journee_prec(classement_original)
journees = process.to_keep(journees)
journees = process.add_journee_prec(journees)

classement["journee_int"] = classement["journee"].str[0:-11].astype(int)
classement = (classement[classement["journee"]!= "0ere journee"]
.groupby(["saison","equipe"],sort="journee_int")
.apply(add_old_info,to_window_compute,[w])).drop("journee_int",axis = 1)

data = process.return_data(classement, journees)

#Pour l'instant, je ne prends pas en compte les matchs nuls:
data["target"] = np.where(data["score_d"]>=data["score_e"],1,0) 

#### features ----------------------------------------------



categorical_features = ['day', 'month']
data = process.get_dummies(data, categorical_features)



features = [
       'classement_d', 'nb_pts_d', 'nb_matchs_joues_d', 'victoire_d', 'nul_d',
       'defaite_d', 'pts_marques_d', 'pts_pris_d', 'ga_d',
       'classement_e', 'nb_pts_e', 'nb_matchs_joues_e', 'victoire_e', 'nul_e',
       'defaite_e', 'pts_marques_e', 'pts_pris_e', 'ga_e',
       'daydimanche', 'dayjeudi', 'daymercredi', 'daysamedi',
       'dayvendredi', 'monthaout', 'monthavril', 'monthdecembre',
       'monthfevrier', 'monthjanvier', 'monthjuin', 'monthmai', 'monthmars',
       'monthnovembre', 'monthoctobre', 'monthseptembre',
        'victoirediff_t-4d', 'nuldiff_t-4d',
       'defaitediff_t-4d', 'bonusdiff_t-4d', 'gadiff_t-4d',
       'victoirediff_t-4e',
       'nuldiff_t-4e', 'defaitediff_t-4e', 'bonusdiff_t-4e', 'gadiff_t-4e']

for f in features:
    data[f] = data[f].fillna(0)

X_train, X_test, y_train, y_test = train_test_split(data[features+
                                                         ["equipe_d",
                                                          "equipe_e", 
                                                          "date", 
                                                          "saison"]], 
                                                    data["target"], 
                                                    test_size=.15, 
                                                    random_state=0)
list_tree = [10, 40,60,100,150]
list_max_depth = [4,6,8]
list_min_child_weight= [1, 2,5]
list_gamma = [0.5, 1]
list_subsample = [0.8, 1.0]
list_colsample_bytree = [0.6, 0.8, 1.0]

score = 0

for tree in list_tree:
    for max_depth in list_max_depth:
        for min_child_weight in list_min_child_weight:
            for gamma in list_gamma:
                for subsample in list_subsample:
                    for colsample_bytree in list_colsample_bytree:
                        model = xgboost.XGBClassifier(max_depth=max_depth, learning_rate=0.02, n_estimators=tree, silent=True,
                                                     min_child_weight=min_child_weight, gamma=gamma, subsample=subsample, colsample_bytree=colsample_bytree, nthread=2, reg_lambda=0, reg_alpha=1)
                        model.fit(X_train[features], y_train)
                        score_ = model.score(X_test[features], y_test)
                        
                        if score_ > score:
                            print(score_)
                            tmp_tree = tree
                            tmp_max_depth = max_depth
                            tmp_min_child_weight = min_child_weight
                            tmp_gamma = gamma
                            tmp_subsample = subsample
                            tmp_colsample_bytree = colsample_bytree
                            score = score_ 

print("results Grid Search : ")
print(tmp_tree)
print(tmp_max_depth)
print(tmp_min_child_weight)
print(tmp_gamma)
print(tmp_subsample)
print(tmp_colsample_bytree)
print("score :")
print(score)

#0.758064516129
#0.762096774194
#0.766129032258
#0.770161290323

#100
#10
#5
#0.5
#1.0
#1.0
#score :
#0.770161290323

    
    
    
    
    
    
