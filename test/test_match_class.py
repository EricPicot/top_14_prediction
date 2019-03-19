import pytest
import unittest
from configurations.load_parameters import load_parameters
from data_preparation.scraping.scrap_seasons import Match
import requests
from bs4 import BeautifulSoup as b


PARAMETERS = load_parameters('configurations/debug_dataprep_parameters.yml')

# ---- Get the soup of the Test Day ----
day_http_request = requests.get(PARAMETERS['fixed_url'] + PARAMETERS['day_url_list'][0])
day_page = day_http_request.content
day_soup = b(day_page, 'html.parser')
day_container = day_soup.select('div.day-results-table')

# ---- Get one of the matches of the day ----
html_match_info = day_container[0].select('tr.info-line.after')[-1]

current_match = Match(html_match_info,
                      season_id=PARAMETERS['season_id'],
                      current_day=PARAMETERS['current_day'],
                      season_url=PARAMETERS['seasons_url_list'][0],
                      day_url=PARAMETERS['day_url_list'][0])

print(current_match.match_results.head())


class TestMatchClass(unittest.TestCase):

    def test_df_creation_rows(self):
        assert current_match.match_results.shape[0] == 1, \
            "DataFrame should load 1 row of data per match"

    def test_df_creation_cols(self):
        assert current_match.match_results.shape[1] == len(PARAMETERS['MATCHES_RESULTS_COLS']), \
            "The number of columns in the DataFrame does not match the required amount"

    def test_value(self):
        assert int(current_match.match_results['score_dom']) == 53, \
            "The recorded score does not match the expected value"

