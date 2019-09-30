# services/users/project/api/views/players.py
from flask import Blueprint, jsonify

from project.api.models.player import Player
from project.utils.yahooAdapter import YahooFantasyAPI

players_blueprint = Blueprint('players', __name__, template_folder='./templates')


@players_blueprint.route('/kbinator/player/<player_id>/<year>', methods=['GET'])
def get_player_stats(player_id, year):
    api = YahooFantasyAPI()
    player_stats = api.get_player_stats(player_id, year)
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


@players_blueprint.route('/kbinator/players/<name>', methods=['GET'])
def get_player(name):
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
    api = YahooFantasyAPI()
    players_info_list = []
    for player_id in player_ids:
        player_info = api.get_player_info(player_id[0])
        players_info_list.append(player_info)
    return jsonify({
        'status': 'success',
        'players': players_info_list
    }), 200
