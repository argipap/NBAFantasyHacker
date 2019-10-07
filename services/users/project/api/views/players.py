# services/users/project/api/views/players.py
from flask import Blueprint, jsonify

from project.api.models.player import Player
from project.api.models.statistic import Statistic
from project.utils.yahooAdapter import YahooFantasyAPI

players_blueprint = Blueprint('players', __name__, template_folder='./templates')


@players_blueprint.route('/kbinator/player/<player_id>/<year>', methods=['GET'])
def get_player_stats(player_id, year):
    player_stats = {}
    data = get_player_info(player_id, year)
    for stat in data['fantasy_content']['league'][1]['players']['0']['player'][1]['player_stats']['stats']:
        stat_name = Statistic.get_stat_name_by_id(stat['stat']['stat_id'])
        player_stats[stat_name] = stat['stat']['value']
    return jsonify({
        'status': 'success',
        'player_stats': player_stats
    })


@players_blueprint.route('/kbinator/players', methods=['GET'])
def get_players():
    """Get all players"""
    response_object = {
        'status': 'success',
        'players': [player.to_json() for player in Player.query.all()]
    }
    return jsonify(response_object), 200


@players_blueprint.route('/kbinator/players/<name>/<year>', methods=['GET'])
def get_player(name, year):
    player_ids = Player.query.with_entities(
        Player.player_id
    ).filter(
        Player.first_name.ilike(f"%{name}%") | Player.last_name.ilike(f"%{name}%")
    ).all()
    if len(player_ids) == 0:
        return jsonify(
            {'status': 'fail',
             'message': 'Player not found'}
        ), 404
    players_info_list = []
    for player_id in player_ids:
        player_info = get_player_info(player_id[0], year)
        players_info_list.append(player_info)
    return jsonify({
        'status': 'success',
        'players': players_info_list
    }), 200


def get_player_info(player_id, year):
    api = YahooFantasyAPI()
    request_uri = f"{api.uri}/league/{api.league_key}/players;" \
        f"player_keys={api.game_key}.p.{player_id}/" \
        f"stats;type=season;season={year}?format={api.request_format}"
    player_info = api.yahoo_request(request_uri)
    return player_info
