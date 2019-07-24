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
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
# import xgboost


def add_old_info(group, cols, _range):
    for i in _range:
        tmp_new_cols = [col+"diff_t-"+str(4) for col in cols]
        group[tmp_new_cols] = group[cols] - group[cols].shift(i).fillna(0)
        
        
    return group

######## Variables-----------------------------------------
w = 2
path = '/home/m420726/workspace/rugby/top_14_prediction/'
classement_original = pd.read_csv(path+"data_classement.csv")
journees = pd.read_csv(path+"data_saison.csv")

print(journees.columns)
print(classement_original.columns)


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

