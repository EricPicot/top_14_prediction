#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:07:34 2019

@author: ericpicot
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as b
import urllib as url #if you are using python3+ version, import urllib.request
import requests
from urllib.request import urlopen as uReq
import datetime

now = datetime.datetime.now()


print("résultats --------------------------------------------------------------------------")

#Loading old data (saison)
data_old = pd.read_csv("data_saison.csv")

#Saving old version
data_old.to_csv("data_saison"+now.strftime("%Y_%m_%d")+".csv")

know_journees = data_old["saison - journee"].drop_duplicates().tolist()
fixe = "https://www.lnr.fr/"
# acces aux pages des saisons
saison_wiki = [
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14524&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14523&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14522&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14519&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14520&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14521&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14528&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14529&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14530&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14534&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=14535&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=18505&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=21642&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=24725&day=all",
    "/rugby-top-14/calendrier-resultats-rugby-top-14?season=27591&day=all"
    ]

last_season = saison_wiki[-1]

requete = requests.get(fixe +last_season)
page = requete.content
soup = b(page, features="lxml")


journee_name = []
wiki_temp = []
saison = []
for i in (soup.findAll("section", {"class": "block block-lnr-custom block-lnr-custom-calendar-results-filter"})[0].
     findAll("span", {"class": "field-content"}))[15:]:
    
#   Only scrapping unknown journees
    if i.a["data-title"] not in know_journees:
        wiki_temp.append(i.a["href"])
        journee_name.append(i.a["data-title"])
        
    journee_n = 0
# Retrieving all information from unknown journees
for j in wiki_temp:
    requete = requests.get(fixe+j)
    page = requete.content
    soup = b(page,features="lxml")
    container = soup.findAll("div", {"class":"day-results-table"})

    journee = []
    for match in container[0].findAll("tr",{"class": 'info-line after'}):
        list_info = [i.text for i in (match.findAll("span",{"format-full"}))[:-1]]
        list_score = match.find("td",{"cell-score"}).text.strip().split("-")
        list_score.append((match.find("td",{"cell-bonus-a"}).text.strip("\n")))
        list_score.append((match.find("td",{"cell-bonus-b"}).text.strip("\n")))
        match_list = [journee_name[journee_n]] +list_info + list_score
        saison.append(match_list)

    for match in container[0].findAll("tr",{"class": 'info-line after table-hr'}):
        list_info = [i.text for i in (match.findAll("span",{"format-full"}))[:-1]]
        list_score = match.find("td",{"cell-score"}).text.strip().split("-")
        list_score.append((match.find("td",{"cell-bonus-a"}).text.strip("\n")))
        list_score.append((match.find("td",{"cell-bonus-b"}).text.strip("\n")))
        match_list = [journee_name[journee_n]] +list_info + list_score
        saison.append(match_list)
    journee_n +=1
    
cols = ["saison - journee", "date","equipe_d", "equipe_e", "score_d", "score_e", "bonus_d", "bonus_e"]
data = pd.DataFrame(saison,columns=cols)

print("Adding following journees:", data["saison - journee"].drop_duplicates().tolist(),"\n")

# Saving new saison data version
pd.concat([data_old, data], sort = True)[cols].to_csv("data_saison.csv")


##### Classement

print("classement --------------------------------------------------------------------------")

#  Loading old data version
data_old = pd.read_csv("data_classement.csv")

#  saving old version before changes
data_old.to_csv("data_classement"+now.strftime("%Y_%m_%d")+".csv")
know_journees = data_old["journee_nom"].drop_duplicates().tolist()

# Current version
cl = "https://www.lnr.fr/rugby-top-14/classement-rugby-top-14"
requete_class = requests.get(cl)
page_class = requete_class.content
soup_class = b(page_class, features="lxml")

wiki_temp_class = []
journee_name_class = []
classement = []

for i in soup_class.find("div", {"class": "tabs-content"}).findAll("a", {"class": "filter"})[10:]:
#     i.findAll("span", {"class": "field-content"})[15:]
    if i["data-title"] not in know_journees:
        wiki_temp_class.append(i["href"])
        journee_name_class.append(i["data-title"])
    
p=0
for k,j in enumerate(wiki_temp_class):
    requete = requests.get(fixe+j)
    page = requete.content
    soup_class = b(page, features="lxml")
    for x in range(14):
        try:
            team = []
            team.append(p)
            team.append(journee_name_class[k])

            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field views-field-field-ranking"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-points"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field views-field-field--quipe"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-nbmatchsplayed"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-won"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-draws"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-lost"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-bonus"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-pointsscored"})[x].text.strip())
            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-pointsconceded"})[x].text.strip())

            team.append(soup_class.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-diff"})[x].text.strip()[1:])


            classement.append(team)
        except:
            None
    p+=1
    
col_class = ["journee","journee_nom", "classement", "nb_pts","equipe","nb_matchs_joues","victoire","nul", "defaite", "bonus", "pts_marques","pts_pris","ga"]
data = pd.DataFrame(classement,columns = col_class)

print("Adding following journees:", data["journee_nom"].drop_duplicates().tolist(),"\n")

pd.concat([data_old, data], sort = True)[col_class].to_csv("classement_test.csv")

