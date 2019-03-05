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
soup = b(page)


journee_name = []
wiki_temp = []
saison = []
for i in (soup.findAll("section", {"class": "block block-lnr-custom block-lnr-custom-calendar-results-filter"})[0].
     findAll("span", {"class": "field-content"}))[15:]:
    
    wiki_temp.append(i.a["href"])
    journee_name.append(i.a["data-title"])
    journee_n = 0
for j in wiki_temp:
    requete = requests.get(fixe+j)
    page = requete.content
    soup = b(page)
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
data.to_csv("data_saison_test_last.csv")


