from yahoo_oauth import OAuth2
from project.api.models.statistic import Statistic
from project.utils.decorators import jsonify
import xml.etree.ElementTree as ET
import os
import xmltodict
import re
import json
import datetime


class YahooFantasyAPI:
    def __init__(self):
        self.uri = 'https://fantasysports.yahooapis.com/fantasy/v2'
        self.players_uri = 'https://fantasysports.yahooapis.com/fantasy/v2/players'
        self._session = self.get_session()
        self.game_key = self.fetch_game_key('nba')
        self.league_key = f"{self.game_key}.l.30109"
        self.request_format = 'json'

    def fetch_game_key(self, game):
        r = self._session.get(
            f"{self.uri}/game/{game}"
        )
        root = ET.fromstring(r.text)
        key = root[0][1]
        return key.text

    def get_league_id(self, league, year):
        r = self._session.get(
            f"https://basketball.fantasysports.yahoo.com/league/{league}/{year}"
        )
        result = r.text
        pattern = re.compile(
            r"""YSF.Fantasy.League = {\n\s{4}"id":\s'\d+',\n\s{4}"uri":\s"\/archive\/nba\/\d{4}\/\d+",\n}""")
        reg_match = pattern.findall(result)[0]
        data = reg_match.replace("YSF.Fantasy.League = {", "{")\
            .replace("'", "\"").replace("\n", "")\
            .replace(",}", "}")
        league_json_data = json.loads(data)
        league_id = league_json_data['id']
        return league_id

    @jsonify
    def fetch_league_settings(self):
        request_uri = f"{self.uri}/league/{self.league_key}/settings?format={self.request_format}"
        r = self._session.get(request_uri)
        return r.text

    @jsonify
    def fetch_league_standings(self):
        request_uri = f"{self.uri}/league/{self.league_key}/standings?format={self.request_format}"
        r = self._session.get(request_uri)
        return r.text

    @jsonify
    def fetch_draft_results(self, year):
        if str(datetime.datetime.now().year) == year:
            request_uri = f"{self.uri}/league/{self.league_key}/draftresults?format={self.request_format}"
            result = self._session.get(request_uri).text
        else:
            result = '3'
        return result

    def fetch_draft_results_archive(self, league_id, year):
        request_uri = f"https://basketball.fantasysports.yahoo.com/archive/nba/{year}/{league_id}/draftresults"
        r = self._session.get(request_uri)
        return r.text

    @jsonify
    def get_player_info(self, player_id, year):
        request_uri = f"{self.uri}/league/{self.league_key}/players;player_keys={self.game_key}.p.{player_id}/stats;type=season;season={year}?format={self.request_format}"
        r = self._session.get(
            #f"{self.uri}/league/{self.league_key}/players;player_keys={self.game_key}.p.{player_id}/stats"
            request_uri
        )
        # json_data = xmltodict.parse(r.text)['fantasy_content']['league']['players']['player']
        json_data = r.text
        return json_data

    def get_player_stats(self, player_id, year):
        result_dictionary = {}
        data = self.get_player_info(player_id, year)
        for stat in data['fantasy_content']['league'][1]['players']['0']['player'][1]['player_stats']['stats']:
            stat_name = Statistic.get_stat_name_by_id(stat['stat']['stat_id'])
            result_dictionary[stat_name] = stat['stat']['value']
        return result_dictionary

    def get_players(self, start):
        r = self._session.get(
            f"{self.uri}/league/{self.league_key}/players;start={start}"
        )
        json_data = xmltodict.parse(r.text)['fantasy_content']['league']['players']['player']
        return json_data

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
    standings = api.fetch_league_standings()
    # statistics = api.get_league_stats(api.fetch_league_settings())
#     points_stat_id = api.get_stat_id("REB", statistics)
#     player_info = api.fetch_player_info('2016')
#     player_stats = api.get_player_stats(player_info)
#     player_points = api.get_player_stat_value(player_stats, points_stat_id)
#     print("REB: %s" % player_points)
#     print("key: %s" % api.game_key)
