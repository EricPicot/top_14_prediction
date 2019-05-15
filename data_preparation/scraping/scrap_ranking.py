from bs4 import BeautifulSoup as b
import requests
import pandas as pd
import os

RANKING_COLS = ["season","day_url","day",
                "classement",
                "nb_pts",
                "equipe",
                "nb_matchs_joues",
                "victoire",
                "nul",
                "defaite",
                "bonus",
                "pts_marques",
                "pts_pris",
                "ga"]
class ScrapRanking:
    
    """
    Class used as base to scrap ranking day after day data from LNR website.
    Construction:
    @input :
        - fixed_url_path :
        - seasons_url_list
        - debug

    The default file (usage recommended) is "scrapping_parameters.yml".
    The scraping is performed successively on the pages reachable with the PATHS defined
    in the "saison_wiki" field of the configuration file.

    The 'debug' parameter launches the scraping on the last PATH only

    The scraped data is loaded in the '.results' attribute
    """
    def __init__(self, fixed_url, seasons_ranking_list, debug):

        # ---- Initialize attributes ----
        # Raw Data saving file
        self.raw_data_path = 'data_preparation/raw_data/ranking_results.csv'

        # Fixed URL identifier: "https://www.lnr.fr/rugby-top-14/classement-rugby-top-14"
        self.fixed_url = fixed_url

        # List of seasons scraped
        if debug:
            # Debug test case :
            # We keep only the last season
            self.seasons_url_list = [seasons_ranking_list[-1]]
        else:
            self.seasons_url_list = seasons_ranking_list

        print('The ranking scraping will be performed over {} season(s)'
              .format(len(self.seasons_url_list))
              )

        # Results DataFrame
        if os.path.exists(self.raw_data_path):
            self.ranking_results = pd.read_csv(self.raw_data_path,
                                               sep='|',
                                               header=0,
                                               index_col=False)

        else:
            self.ranking_results = pd.DataFrame(columns=RANKING_COLS)

        # ---- Perform Scraping ----
        # For each season :
        for season_url in self.seasons_url_list:

            # First we have to check if there is already a "Finale" day in the DataFrame
            # In which case, it is not useful to scrap the page

            if (self.ranking_results.loc[(self.ranking_results['season'] == season_url) &
                                         (self.ranking_results['day'].astype('str') == 'Finale')].shape[0] == 0) \
                    or self.ranking_results.shape[0] == 0:
                # Then the season has not already been entirely loaded (or not loaded at all):
                # We have to access the URL for this season

                # Create an instance of the Season class using the corresponding url
                # For each season, the data are loaded in the .season_results attribute as a DataFrame
                current_season = Season(self.fixed_url, season_url, self.ranking_results)

                # Get the new DataFrame with the additional data
                self.ranking_results = self.ranking_results.append(current_season.season_results)

                # In case we add lines which are already in the dataframe,
                # we keep only the last occurrence (ie. the latest update)
                self.ranking_results.drop_duplicates(inplace=True,
                                                     subset=['season', 'day', 'equipe'],
                                                     keep='last'
                                                     )
                print('Season {} saved in DataFrame'.format(current_season.season_id))
                del current_season

            else:
                # The whole season has already been loaded,
                # there is no need to reload the URL
                pass

        # ---- Export new Data File ----
        self.ranking_results.to_csv(self.raw_data_path,
                                    sep='|',
                                    encoding='utf-8',
                                    index=False)

        print('Updated Raw Data exported to {}'.format(self.raw_data_path))


        
        
class Season:
    """
    Class corresponding to the data extracted from the URL of a single season
    The scraping is performed successively on the days of the season,
    through the  pages reachable with the URL defined in the scraped season html files.
    """
    def __init__(self, fixed_url, season_url, season_results_df):

        # ---- Initialize attributes ----
        self.season_url = season_url
        self.season_id = None
        self.days = []
        self.season_results = pd.DataFrame(columns=RANKING_COLS)
        self.fixed_url = fixed_url
        self.complete_season_url = self.fixed_url + season_url
        self.already_loaded_days = season_results_df['day_url'].unique()

        if len(self.already_loaded_days) == 0:
            self.last_day_loaded = None
        else:
            self.last_day_loaded = self.already_loaded_days[-1]
        # ---- Scrap data from current season ----
        # Access the current season data, using current season's url
        season_http_request = requests.get(self.complete_season_url)
        season_page = season_http_request.content
        self.season_soup = b(season_page, 'html.parser')

#         # Get the urls to the different Days of the current season (stored in a dictionary)
#         # and the identification of the current season.
        self.season_id, self.days = self.get_days_url()

        for day in self.days:
            # We will not scrap data for the days already loaded
            # The last day can have been loaded while all the matches were not already played
            # thus we reload the last day
            if (self.days[day] not in self.already_loaded_days) \
                    or (self.days[day] == self.last_day_loaded):

                # Scrap the data for this day
                current_day = Day(self.fixed_url,
                                  self.season_id,
                                  self.season_url,
                                  self.days[day],
                                  day)


                self.season_results = self.season_results.append(current_day.day_ranking)

                self.season_results.drop_duplicates(inplace=True,
                                                    subset=['season', 'day', 'equipe'],
                                                    keep='last'
                                                    )
                

                del current_day

            else:
                pass

    def get_days_url(self):
        season_id = None
        days = {}
        days_num = []

# #         Following gives a list of:
# [<a class="filter" data-title="TOP 14 2018-2019 - 1ère journée"
# href="/rugby-top-14/classement-rugby-top-14?season=27591&amp;day=27537" 
# title="TOP 14 2018-2019 - 1ère journée">
#   1ère journée</a>,
        html_calendar_filters = self.season_soup.find("div", {"class": "tabs-content"})\
                                                .findAll("a", {"class": "filter"})[10:]

        for day_filter in html_calendar_filters:
            # Remove general raw_data ('all' days in the season)

            if "all" not in day_filter['href']:

                day_url_temp = day_filter['href']
                day_temp = day_filter['data-title'].split(' - ')[-1].split('è')[0]

                days[day_temp] = day_url_temp
                days_num.append
                if season_id is None:
                    # Populate season information
                    season_id = day_filter['data-title'].split(' - ')[0].split()[-1]

        return season_id, days
    

class Day:
    

    def __init__(self, fixed_url,season_id, season_url, day_url, day):
#         self.season_url = season_url
        self.day_url = day_url
        self.complete_day_url = fixed_url + day_url
        self.season_id = season_id
        self.season_url = season_url
        self.current_day = day
        self.day_ranking = pd.DataFrame(columns=RANKING_COLS)

        # Access the current day raw_data, using current day url
        day_http_request = requests.get(self.complete_day_url)
        day_page = day_http_request.content
        self.day_soup = b(day_page, features="lxml")
#         there are 14 teams
        for team in range(14):
            current_team = Team(  self.season_id,
                                  self.current_day,
                                  self.season_url,
                                  self.day_url,
                                  self.day_soup,team=team)

            self.day_ranking = self.day_ranking.append(current_team.team_attributes_list)

            del current_team
        self.day_ranking.drop_duplicates(inplace=True,
                                         subset=['season', 'day', 'equipe'],
                                         keep='last'
                                         )

class Team:
    def __init__(self, season_id, current_day,
                 season_url, day_url, day_soup, team):

        self.season_url = season_url
        self.day_url = day_url
        self.day_soup = day_soup
        self.season_id = season_id
        self.current_day = current_day

        x = team
        self.classement = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field views-field-field-ranking"})[team].text.strip()
        self.nb_pts = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-points"})[team].text.strip()
        self.team = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field views-field-field--quipe"})[team].text.strip()
        self.nb_matchs_joues = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-nbmatchsplayed"})[team].text.strip()            
        self.victoire = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-won"})[team].text.strip()
        self.nul = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-draws"})[team].text.strip()
        self.defaite = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-lost"})[team].text.strip()
        self.bonus = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-bonus"})[team].text.strip()
        self.pts_marques = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-pointsscored"})[team].text.strip()
        self.pts_pris = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-pointsconceded"})[team].text.strip()
        self.ga = self.day_soup.find("div", {"class": "scroll-wrapper"}).findAll("td", {"class": "views-field-field-diff"})[team].text.strip()[1:]
        
        self.team_attributes_list = [[
            self.season_id,
            self.day_url,
            self.current_day,
            self.classement,
            self.nb_pts,
            self.team,
            self.nb_matchs_joues,
            self.victoire,
            self.nul,
            self.defaite,
            self.bonus,
            self.pts_marques,
            self.pts_pris,
            self.ga
        ]]

        self.team_attributes_list = pd.DataFrame(self.team_attributes_list, columns=RANKING_COLS)
