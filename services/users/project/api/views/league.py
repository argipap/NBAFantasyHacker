# services/users/project/api/views/league.py
from flask import Blueprint, jsonify
from project.utils.yahooAdapter import YahooFantasyAPI

league_blueprint = Blueprint('league', __name__, template_folder='./templates')


@league_blueprint.route('/kbinator/league/settings', methods=['GET'])
def get_league_settings():
    api = YahooFantasyAPI()
    league_settings = api.fetch_league_settings()
    return jsonify({
        'status': 'success',
        'data': {
                    'settings': league_settings
                }
    })


@league_blueprint.route('/kbinator/league/standings', methods=['GET'])
def get_league_standings():
    api = YahooFantasyAPI()
    league_standings = api.fetch_league_standings()
    return jsonify({
        'status': 'success',
        'data': {
                    'settings': league_standings
                }
    })


@league_blueprint.route('/kbinator/league/draftresults/<year>', methods=['GET'])
def get_draft_results(year):
    api = YahooFantasyAPI()
    draft_results = api.fetch_draft_results(year)
    return jsonify({
        'status': 'success',
        'data': {
                    'draft_results': draft_results
                }
    })


@league_blueprint.route('/kbinator/league/<league_name>/<year>', methods=['GET'])
def get_league_id(league_name, year):
    api = YahooFantasyAPI()
    league_id = api.get_league_id(league_name, year)
    response_object = {
        'status': 'success',
        'league_id': league_id
    }
    return jsonify(response_object), 200
