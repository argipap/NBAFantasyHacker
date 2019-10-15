# services/users/project/api/views/game.py
from flask import Blueprint, jsonify
from project.utils.yahooAdapter import YahooFantasyAPI

games_blueprint = Blueprint('games', __name__, template_folder='./templates')


@games_blueprint.route('/kbinator/game/<game_name>', methods=['GET'])
def get_game_id(game_name):
    api = YahooFantasyAPI()
    game_key = api.fetch_game_key(game_name)
    return jsonify({
        'status': 'success',
        'data': {
                    'game': game_name,
                    'game_key': game_key
                }
    })
