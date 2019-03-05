#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:44:14 2019

@author: ericpicot
"""

import pandas as pd
import numpy as np

def processing_journees(journees):
    
    journees[["day","day_number","month"]] = journees["date"].str.lower()\
                                                    .str.replace("û","u")\
                                                    .str.replace("é","e")\
                                                    .str.split(" ")\
                                                    .apply(pd.Series)
                                                    
                                                    
    journees[["saison","journee"]] = journees['saison - journee'].str.replace("é","e")\
                                                                .str.replace("è","e")\
                                                                .str.split(" - ")\
                                                                .apply(pd.Series)
                                                                
    return journees.drop('saison - journee', axis = 1)

def processing_classement(classement):
    
    classement[["saison","journee"]] = classement['journee_nom'].str.replace("é","e")\
                                                                .str.replace("è","e")\
                                                                .str.split(" - ")\
                                                                .apply(pd.Series)
    return classement.drop("journee_nom", axis = 1).drop("Unnamed: 0", axis = 1)
    
def add_0ere_journee(classement):
    to_add = []
    for saison in classement["saison"].drop_duplicates():
        
        
        
        equipe = classement["equipe"][classement["saison"]== "TOP 14 2018-2019"].drop_duplicates().tolist()
        for e in equipe:
            to_add.append(["0ere journee",0,0,e,0,0,0,0,0,0,0,0,saison])
    return pd.concat([classement, pd.DataFrame(to_add, columns=classement.columns)])

journee_to_keep = [
        "0ere journee",
        '1ere journee',
         '2eme journee',
         '3eme journee',
         '4eme journee',
         '5eme journee',
         '6eme journee',
         '7eme journee',
         '8eme journee',
         '9eme journee',
         '10eme journee',
         '11eme journee',
         '12eme journee',
         '13eme journee',
         '14eme journee',
         '15eme journee',
         '16eme journee',
         '17eme journee',
         '18eme journee',
         '19eme journee',
         '20eme journee',
         '21eme journee',
         '22eme journee',
         '23eme journee',
         '24eme journee',
         '25eme journee',
         '26eme journee',
 ]

saison_to_keep = ['TOP 14 Orange 2009-2010',
 'TOP 14 Orange 2010-2011',
 'TOP 14 Orange 2011-2012',
 'TOP 14 2012-2013',
 'TOP 14 2013-2014',
 'TOP 14 2014-2015',
 'TOP 14 2015-2016',
 'TOP 14 2016-2017',
 'TOP 14 2017-2018',
 'TOP 14 2018-2019']

def to_keep(data):
    return data[data["journee"].isin(journee_to_keep)&
                        data["saison"].isin(saison_to_keep)]
    
def add_journee_prec(classement):
    classement["journee_prec"] = classement["journee"]
    for i,j in enumerate(journee_to_keep[1:]):
        
        classement["journee_prec"] = classement.apply(lambda row: journee_to_keep[i] if row["journee"]== j else row["journee_prec"], axis =1)
    return classement
def return_data(classement, journees):
    
    data = journees.merge(classement[["saison","journee",'classement', 'nb_pts',
                                      "equipe", 'nb_matchs_joues',
           'victoire', 'nul', 'defaite', 'bonus', 'pts_marques', 'pts_pris', 'ga',
           'victoirediff_t-4',
       'nuldiff_t-4', 'defaitediff_t-4', 'bonusdiff_t-4', 'gadiff_t-4']],
                    right_on = ["journee","saison","equipe"],
                    left_on = ["journee_prec","saison","equipe_d"], how = "inner")
    data = (data.drop("journee_y",axis = 1)
                .drop("equipe", axis = 1)
                .drop("Unnamed: 0", axis = 1))
    
    data.columns = ["date",'equipe_d', 'equipe_e', 'score_d', 'score_e', 'bonus_d', 'bonus_e',
           'day', 'day_number', 'month', 'saison', 'journee', "journee_prec",'classement_d',
           'nb_pts_d', 'nb_matchs_joues_d', 'victoire_d', 'nul_d', 'defaite_d',
           'bonus_d_history', 'pts_marques_d', 'pts_pris_d', 'ga_d',
           'victoirediff_t-4d',
       'nuldiff_t-4d', 'defaitediff_t-4d', 'bonusdiff_t-4d', 'gadiff_t-4d']
    
    data = data.merge(classement[["saison","journee",'classement', 'nb_pts',
                                      "equipe", 'nb_matchs_joues',
           'victoire', 'nul', 'defaite', 'bonus', 'pts_marques', 'pts_pris', 'ga',
           'victoirediff_t-4',
       'nuldiff_t-4', 'defaitediff_t-4', 'bonusdiff_t-4', 'gadiff_t-4']],
                    right_on = ["journee","saison","equipe"],
                    left_on = ["journee_prec","saison","equipe_e"], how = "inner")
    data = (data.drop("journee_y",axis = 1)
                .drop("equipe", axis = 1))
    data.columns = ['date', 'equipe_d', 'equipe_e', 'score_d', 'score_e', 'bonus_d',
       'bonus_e', 'day', 'day_number', 'month', 'saison', 'journee_x',
       'journee_prec', 'classement_d', 'nb_pts_d', 'nb_matchs_joues_d',
       'victoire_d', 'nul_d', 'defaite_d', 'bonus_d_history', 'pts_marques_d',
       'pts_pris_d', 'ga_d', 'victoirediff_t-4d', 'nuldiff_t-4d',
       'defaitediff_t-4d', 'bonusdiff_t-4d', 'gadiff_t-4d', 'classement_e',
       'nb_pts_e', 'nb_matchs_joues_e', 'victoire_e', 'nul_e', 'defaite_e', 'bonus_e',
       'pts_marques_e', 'pts_pris_e', 'ga_e', 'victoirediff_t-4e',
       'nuldiff_t-4e', 'defaitediff_t-4e', 'bonusdiff_t-4e', 'gadiff_t-4e']
    return data

def get_dummies(df, cols):
    
    for col in cols:
        df[col] = df[col].fillna(0)
        temp = pd.get_dummies(df[col])
        df[[col+str(t) for t in temp.columns]] = temp
    return df

def find_game_feature(df,features, equipe_d, equipe_e, date,saison):
    return df[(df["equipe_d"] == equipe_d)&
       (df["equipe_e"] == equipe_e)&
       (df["date"] == date)&
       (df["saison"] == saison) 
    ][features]
        
        
    
           
           