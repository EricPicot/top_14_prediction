import pytest
import unittest
from configurations.load_parameters import load_parameters
from data_preparation.scraping.scrap_seasons import Match
import requests
from bs4 import BeautifulSoup as b


class TestDayClass(unittest.TestCase):

    def test_df_creation_rows(self):

        self.assertEqual(True, False)


