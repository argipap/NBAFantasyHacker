from yahoo_oauth import OAuth2
from project.utils.decorators import jsonify
import os
import xmltodict

from project.utils.errors import AccessDeniedException


class YahooFantasyAPI:
    def __init__(self):
        self.uri = 'https://fantasysports.yahooapis.com/fantasy/v2'
        self.players_uri = 'https://fantasysports.yahooapis.com/fantasy/v2/players'
        self.request_format = 'json'
        self._session = self.get_session()
        self.game_key = '395'  # self.fetch_game_key('nba')
        self.league_key = f"{self.game_key}.l.30109"

    @jsonify
    def yahoo_request(self, uri):
        response = self._session.get(uri)
        if str(response.status_code) == '999':
            raise AccessDeniedException(f"http status code: {response.status_code}. Throttling error!")
        return response.text

    def fetch_game_key(self, game):
        url = f"{self.uri}/game/{game}?format={self.request_format}"
        result = self.yahoo_request(url)
        print(f"result: {result}")
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

    @staticmethod
    def get_league_stats(settings):
        stats_list = settings['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']
        stats_modifiers = settings['fantasy_content']['league'][1]['settings'][0]['stat_modifiers']['stats']
        return stats_list, stats_modifiers

    @staticmethod
    def get_league_stat_modifiers(settings):
        stats_list = settings['fantasy_content']['league'][1]['settings'][0]['stat_modifiers']['stats']
        return stats_list

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
    # for i in range(700):
    #     player_id = 6042
    #     year = 2018
    #     request_uri = f"{api.uri}/league/{api.league_key}/players;" \
    #         f"player_keys={api.game_key}.p.{player_id}/" \
    #         f"stats;type=season;season={year}?format={api.request_format}"
    #     player_info = api.yahoo_request(request_uri)
    #     print(player_info)

    # standings = api.fetch_league_standings()
    # statistics = api.get_league_stats(api.fetch_league_settings())
#     points_stat_id = api.get_stat_id("REB", statistics)
#     player_info = api.fetch_player_info('2016')
#     player_stats = api.get_player_stats(player_info)
#     player_points = api.get_player_stat_value(player_stats, points_stat_id)
#     print("REB: %s" % player_points)
#     print("key: %s" % api.game_key)
