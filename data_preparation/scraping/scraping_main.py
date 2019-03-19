from data_preparation.scraping.scrap_ranking import ScrapRanking
from data_preparation.scraping.scrap_seasons import ScrapSeasons


class Scraping:

    def __init__(self, dataprep_parameters, debug):

        self.dataprep_parameters = dataprep_parameters
        self.scraping_dict = dict()

        # Get 'result' attribute of ScrapSeason object
        self.scraping_dict['scrap_seasons'] = ScrapSeasons(self.dataprep_parameters['fixed_url'],
                                                           self.dataprep_parameters['seasons_url_list'],
                                                           debug).matches_results

        # Get 'ranking_history' attribute of ScrapRanking object
        # self.scraping_dict['scrap_ranking'] = ScrapRanking(..., debug).ranking_history

        # ---- Next Scraping TBD ----
        #
        #

