from yahoo_oauth import OAuth2
from project.api.models.statistic import Statistic
from project.utils.decorators import jsonify
import os
import xmltodict


class YahooFantasyAPI:
    def __init__(self):
        self.uri = 'https://fantasysports.yahooapis.com/fantasy/v2'
        self.players_uri = 'https://fantasysports.yahooapis.com/fantasy/v2/players'
        self.request_format = 'json'
        self._session = self.get_session()
        self.game_key = self.fetch_game_key('nba')
        self.league_key = f"{self.game_key}.l.30109"

    @jsonify
    def yahoo_request(self, uri):
        return self._session.get(uri).text

    def fetch_game_key(self, game):
        url = f"{self.uri}/game/{game}?format={self.request_format}"
        result = self.yahoo_request(url)
        key = result['fantasy_content']['game'][0]['game_key']
        return key

    def get_players(self, start):
        url = f"{self.uri}/league/{self.league_key}/players;start={start}"
        result = self._session.get(url).text
        json_data = xmltodict.parse(result)['fantasy_content']['league']['players']['player']
        return json_data

    @jsonify
    def fetch_league_settings(self):
        request_uri = f"{self.uri}/league/{self.league_key}/settings?format={self.request_format}"
        r = self._session.get(request_uri)
        return r.text

    def get_league_stats(self, settings):
        stats_list = settings['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']
        return stats_list

    def get_player_stat_value(self, player_statistics):
        for player_stat in player_statistics:
            if player_stat['stat_id'] == player_stat[0].text:
                return player_stat[1].text

    def get_stat_id(self, display_name, stat_list):
        for stat in stat_list:
            if stat['display_name'] == display_name:
                return stat['stat_id']
        return -1

    @staticmethod
    def get_session():
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'oauth2.json')
        oauth = OAuth2(None, None, from_file=filename)
        if not oauth.token_is_valid():
            oauth.refresh_access_token()
        return oauth.session


if __name__ == '__main__':
    api = YahooFantasyAPI()
    # standings = api.fetch_league_standings()
    # statistics = api.get_league_stats(api.fetch_league_settings())
#     points_stat_id = api.get_stat_id("REB", statistics)
#     player_info = api.fetch_player_info('2016')
#     player_stats = api.get_player_stats(player_info)
#     player_points = api.get_player_stat_value(player_stats, points_stat_id)
#     print("REB: %s" % player_points)
#     print("key: %s" % api.game_key)
