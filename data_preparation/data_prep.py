# from ..configurations import load_parameters
# from configurations import load_parameters
from configurations.load_parameters import load_parameters

from data_preparation.scraping.scraping_main import Scraping
import sys
import pandas as pd


class DataPrep:

    def __init__(self,
                 dataprep_parameters_path='configurations/dataprep_parameters.yml'):

        # ---- Load Parameters ----
        self.dataprep_parameters = load_parameters(dataprep_parameters_path)
        print('Configuration Parameters loaded')

        # ---- Initialize attributes ----
        # Scraping DataFrames
        self.scraping_dict = {}

        # Transformed Data
        self.transformed_data = pd.DataFrame()

        # Prediction Data
        self.to_predict_data = pd.DataFrame()

        # Loading information
        self.loaded_to_csv = False

    def scrap(self, debug):
        print('Launch scraping of data')
        # Get scrapings performed by Scraping object as a dictionary
        self.scraping_dict = Scraping(self.dataprep_parameters, debug).scraping_dict

        return None

    def transform(self, debug):

        # Get 'transformed_df' attribute of TransformDB object
        # self.transformed_data = TransformDB(..., )

        return None

    def load(self, debug):

        # control DataFrame shape before loading
        if self.transformed_data.shape[0] == 0:
            raise Exception('Tried to load DataFrame with 0 line')

        if self.transformed_data.shape[1] == 0:
            raise Exception('Tried to load DataFrame with 0 column')

        # Load 'self.transformed_data' to .csv file
        self.transformed_data.to_csv(
            'data_preparation/transformed_data/transformed_data.csv',
            sep='|',
            encoding='utf-8',
            index=False
        )

        self.loaded_to_csv = True
        print('Data loaded at {}'.format('data_preparation/transformed_data/transformed_data.csv'))

        return None


def main_data_prep(dataprep_parameters_path='configurations/dataprep_parameters.yml', debug=False):

    print('Entering {}'.format(__name__))
    # ---- Create instance of DataPrep Class ----
    data_prep = DataPrep(dataprep_parameters_path)

    data_prep.scrap(debug)

    # data_prep.transform(debug)

    data_prep.load(debug)

    return None



