# services/users/project/api/views/league.py
from flask import Blueprint, jsonify
from project.utils.yahooAdapter import YahooFantasyAPI
import re
import json
import datetime

league_blueprint = Blueprint('league', __name__, template_folder='./templates')


@league_blueprint.route('/kbinator/league/settings', methods=['GET'])
def get_league_settings():
    api = YahooFantasyAPI()
    request_uri = f"{api.uri}/league/{api.league_key}/settings?format={api.request_format}"
    league_settings = api.yahoo_request(request_uri)
    return jsonify({
        'status': 'success',
        'data': {
                    'settings': league_settings
                }
    })


@league_blueprint.route('/kbinator/league/standings', methods=['GET'])
def get_league_standings():
    api = YahooFantasyAPI()
    request_uri = f"{api.uri}/league/{api.league_key}/standings?format={api.request_format}"
    league_standings = api.yahoo_request(request_uri)
    return jsonify({
        'status': 'success',
        'data': {
                    'settings': league_standings
                }
    })


@league_blueprint.route('/kbinator/league/draftresults/<year>', methods=['GET'])
def get_draft_results(year):
    api = YahooFantasyAPI()
    # draft_results = api.fetch_draft_results(year)
    if str(datetime.datetime.now().year) == year:
        request_uri = f"{api.uri}/league/{api.league_key}/draftresults?format={api.request_format}"
        draft_results = api.yahoo_request(request_uri)
    else:
        league_id = get_league_id('kantina', year)
        draft_results = get_draft_results_archive(league_id, year)
        return draft_results
    return jsonify({
        'status': 'success',
        'data': {
                    'draft_results': draft_results
                }
    })


@league_blueprint.route('/kbinator/league/<league_name>/<year>', methods=['GET'])
def get_league_id(league_name, year):
    api = YahooFantasyAPI()
    r = api.get_session().get(
        f"https://basketball.fantasysports.yahoo.com/league/{league_name}/{year}"
    )
    result = r.text
    pattern = re.compile(
        r"""YSF.Fantasy.League = {\n\s{4}"id":\s'\d+',\n\s{4}"uri":\s"\/archive\/nba\/\d{4}\/\d+",\n}""")
    reg_match = pattern.findall(result)[0]
    data = reg_match.replace("YSF.Fantasy.League = {", "{") \
        .replace("'", "\"").replace("\n", "") \
        .replace(",}", "}")
    league_json_data = json.loads(data)
    league_id = league_json_data['id']
    # response_object = {
    #     'status': 'success',
    #     'league_id': league_id
    # }
    return league_id


def get_league_stats(settings):
    stats_list = settings['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']
    return stats_list


def get_draft_results_archive(league_id, year):
    api = YahooFantasyAPI()
    request_uri = f"https://basketball.fantasysports.yahoo.com/archive/nba/{year}/{league_id}/draftresults"
    draft_results = api.get_session().get(request_uri)
    return draft_results
