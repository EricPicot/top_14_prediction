from bs4 import BeautifulSoup as b
import requests
import pandas as pd
import os


MATCHES_RESULTS_COLS = [
    'season_url',
    'day_url',
    "season_id",
    "season_day",
    "date",
    "team_dom",
    "team_ext",
    "score_dom",
    "score_ext",
    "bonus_dom",
    "bonus_ext"
]


class ScrapSeasons:
    """
    Class used as base to scrap matches data from LNR website.
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
    def __init__(self, fixed_url, seasons_url_list, debug):

        # ---- Initialize attributes ----
        # Raw Data saving file
        self.raw_data_path = 'data_preparation/raw_data/matches_results.csv'

        # Fixed URL identifier
        self.fixed_url = fixed_url

        # List of seasons scraped
        if debug:
            # Debug test case :
            # We keep only the last season
            self.seasons_url_list = [seasons_url_list[-1]]
        else:
            self.seasons_url_list = seasons_url_list

        print('The scraping will be performed over {} season(s)'
              .format(len(self.seasons_url_list))
              )

        # Results DataFrame
        if os.path.exists(self.raw_data_path):
            self.matches_results = pd.read_csv(self.raw_data_path,
                                               sep='|',
                                               header=0,
                                               index_col=False)

        else:
            self.matches_results = pd.DataFrame(columns=MATCHES_RESULTS_COLS)

        # ---- Perform Scraping ----
        # For each season :
        for season_url in self.seasons_url_list:

            # First we have to check if there is already a "Finale" day in the DataFrame
            # In which case, it is not useful to scrap the page

            if (self.matches_results.loc[(self.matches_results['season_url'] == season_url) &
                                         (self.matches_results['season_day'].astype('str') == 'Finale')].shape[0] == 0) \
                    or self.matches_results.shape[0] == 0:
                # Then the season has not already been entirely loaded (or not loaded at all):
                # We have to access the URL for this season

                # Create an instance of the Season class using the corresponding url
                # For each season, the data are loaded in the .season_results attribute as a DataFrame
                current_season = Season(self.fixed_url, season_url, self.matches_results)

                # Get the new DataFrame with the additional data
                self.matches_results = self.matches_results.append(current_season.season_results)

                # In case we add lines which are already in the dataframe,
                # we keep only the last occurrence (ie. the latest update)
                self.matches_results.drop_duplicates(inplace=True,
                                                     subset=['season_id', 'season_day', 'team_dom'],
                                                     keep='last'
                                                     )
                print('Season {} saved in DataFrame'.format(current_season.season_id))
                del current_season

            else:
                # The whole season has already been loaded,
                # there is no need to reload the URL
                pass

        # ---- Export new Data File ----
        self.matches_results.to_csv(self.raw_data_path,
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
    def __init__(self, fixed_url, season_url, matches_results_df):

        # ---- Initialize attributes ----
        self.season_url = season_url
        self.season_id = None
        self.days = []
        self.season_results = pd.DataFrame(columns=MATCHES_RESULTS_COLS)
        self.fixed_url = fixed_url
        self.complete_season_url = self.fixed_url + season_url
        self.already_loaded_days = matches_results_df['day_url'].unique()

        if len(self.already_loaded_days) == 0:
            self.last_day_loaded = None
        else:
            self.last_day_loaded = self.already_loaded_days[-1]

        # ---- Scrap data from current season ----
        # Access the current season data, using current season's url
        season_http_request = requests.get(self.complete_season_url)
        season_page = season_http_request.content
        self.season_soup = b(season_page, 'html.parser')

        # Get the urls to the different Days of the current season (stored in a dictionary)
        # and the identification of the current season.
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
                                  day,
                                  self.season_url,
                                  self.days[day])

                self.season_results = self.season_results.append(current_day.day_results)

                self.season_results.drop_duplicates(inplace=True,
                                                    subset=['season_id', 'season_day', 'team_dom'],
                                                    keep='last'
                                                    )
                del current_day

            else:
                pass

    def get_days_url(self):
        season_id = None
        days = {}

        html_calendar_filters = self.season_soup.select(
            'section.block.block-lnr-custom.block-lnr-custom-calendar-results-filter'
        )[0]
        html_field_content = html_calendar_filters.select(
            'span.field-content'
        )

        for day_filter in html_field_content:
            # Remove general raw_data ('all' days in the season)
            if "all" not in day_filter.a['href']:

                day_url_temp = day_filter.a['href']
                day_temp = day_filter.a['data-title'].split(' - ')[-1].split('è')[0]

                days[day_temp] = day_url_temp

                if season_id is None:
                    # Populate season information
                    season_id = day_filter.a['data-title'].split(' - ')[0].split()[-1]

        return season_id, days


class Day:
    def __init__(self, fixed_url, season_id, current_day, season_url, day_url):
        self.season_url = season_url
        self.day_url = day_url
        self.complete_day_url = fixed_url + day_url
        self.season_id = season_id
        self.current_day = current_day
        self.day_results = pd.DataFrame(columns=MATCHES_RESULTS_COLS)

        # Access the current day raw_data, using current day url
        day_http_request = requests.get(self.complete_day_url)
        day_page = day_http_request.content
        day_soup = b(day_page, 'html.parser')
        day_container = day_soup.select('div.day-results-table')

        for html_match_info in day_container[0].select('tr.info-line.after'):
            current_match = Match(html_match_info,
                                  self.season_id,
                                  self.current_day,
                                  self.season_url,
                                  self.day_url)

            self.day_results = self.day_results.append(current_match.match_results)

            del current_match

        self.day_results.drop_duplicates(inplace=True,
                                         subset=['season_id', 'season_day', 'team_dom'],
                                         keep='last'
                                         )


class Match:
    def __init__(self, html_match_info, season_id, current_day,
                 season_url, day_url):

        self.season_url = season_url
        self.day_url = day_url
        self.match = html_match_info
        self.match_results = []
        self.season_id = season_id
        self.current_day = current_day
        self.date = (self.match.select("span.format-full"))[0].text
        self.team_dom = (self.match.select("span.format-full"))[1].text
        self.team_ext = (self.match.select("span.format-full"))[2].text
        self.score_dom = self.match.select("td.cell-score")[0].text.strip().split("-")[0]
        self.score_ext = self.match.select("td.cell-score")[0].text.strip().split("-")[1]
        self.bonus_dom = self.match.select("td.cell-bonus-a")[0].text.strip("\n")
        self.bonus_ext = self.match.select("td.cell-bonus-b")[0].text.strip("\n")

        self.match_results_list = [[
            self.season_url,
            self.day_url,
            self.season_id,
            self.current_day,
            self.date,
            self.team_dom,
            self.team_ext,
            self.score_dom,
            self.score_ext,
            self.bonus_dom,
            self.bonus_ext
        ]]

        self.match_results = pd.DataFrame(self.match_results_list, columns=MATCHES_RESULTS_COLS)

