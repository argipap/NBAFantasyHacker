from project.utils.yahooAdapter import api


class League:
    def __init__(self):
        self.settings = League.get_settings()
        self.statistics = League.get_league_stats(self.settings)
        self.teams = []
        self.transactions = []
        self.users = []

    @classmethod
    def get_league_stats(cls, settings):
        stats_list = settings['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']
        return stats_list

    @classmethod
    def get_settings(cls):
        return api.fetch_league_settings()
