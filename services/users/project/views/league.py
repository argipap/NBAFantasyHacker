# services/users/project/api/views/league.py
from flask import Blueprint, jsonify

from project.utils.webscraping.pages.draft_results_page import DraftResultsPage
from project.utils.yahooAdapter import YahooFantasyAPI
from project.models.statistic import Statistic
import re
import json
import datetime

league_blueprint = Blueprint('league', __name__)


@league_blueprint.route('/league/settings', methods=['GET'])
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


@league_blueprint.route('/league/standings', methods=['GET'])
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


@league_blueprint.route('/league/draftresults/<year>', methods=['GET'])
def get_draft_results(year):
    api = YahooFantasyAPI()
    if str(datetime.datetime.now().year) == year:
        request_uri = f"{api.uri}/league/{api.league_key}/draftresults?format={api.request_format}"
        draft_results = api.yahoo_request(request_uri)['fantasy_content']['league'][1]['draft_results']
    else:
        league_id = get_league_id('kantina', year)
        draft_results_page = fetch_draft_results_archive(year, league_id)
        draft_results = DraftResultsPage(draft_results_page).teams
    return jsonify({
        'status': 'success',
        'data': {
                    'draft_results': draft_results
                }
    })


@league_blueprint.route('/league/<league_name>/<year>', methods=['GET'])
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


@league_blueprint.route('/league/stats', methods=['GET'])
def get_league_stats():
    return jsonify({
        'status': 'success',
        'data': {
                    'statistics': [statistic.to_json() for statistic in Statistic.query.all()]
                }
    }), 200


def fetch_draft_results_archive(year, league_id):
    api = YahooFantasyAPI()
    request_uri = f"https://basketball.fantasysports.yahoo.com/archive/nba/{year}/{league_id}/" \
        f"draftresults?drafttab=team"
    draft_results = api.get_session().get(request_uri).content
    return draft_results
