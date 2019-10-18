# services/users/project/api/views/players.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for

from project.models.player import Player
from project.models.statistic import Statistic
from project.utils.yahooAdapter import YahooFantasyAPI

players_blueprint = Blueprint('players', __name__)


@players_blueprint.route('/players', methods=['GET'])
def get_players():
    """Get all players"""
    # response_object = {
    #     'status': 'success',
    #     'players': [player.to_json() for player in Player.query.all()]
    # }
    players_list = [player.to_json() for player in Player.query.all()]
    return render_template('players/index.html', players=players_list)
    # return jsonify(response_object), 200


@players_blueprint.route('/player/stats/<player_id>/<year>', methods=['GET'])
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


@players_blueprint.route('/player/fanpoints/<player_id>/<year>', methods=['GET'])
def get_player_fanpoints(player_id, year):
    data = get_player_stats(player_id, year).get_json()
    fan_points = 0
    for modifier_name, modifier_value in data['player_stats'].items():
        if modifier_value == "-":
            continue
        fan_points = fan_points + (float(modifier_value) * float(Statistic.get_stat_modifier_by_name(modifier_name)))
    return jsonify({
        'status': 'success',
        'fanpoints': fan_points
    })


@players_blueprint.route('/players/<name>', methods=['GET'])
def get_player_id(name):
    players = Player.query.filter(Player.first_name.ilike(f"%{name}%") | Player.last_name.ilike(f"%{name}%")).all()
    if len(players) == 0:
        return jsonify(
            {'status': 'fail',
             'message': 'Player not found'}
        ), 404
    players_list = []
    for player in players:
        players_list.append(player.to_json())
    return jsonify({
        'status': 'success',
        'players': players_list
    }), 200


@players_blueprint.route('/fanpoints/calculator', methods=['GET', 'POST'])
def calculate_fanpoints():
    if request.method == 'POST':
        fan_points = 0
        for modifier_name, modifier_value in request.form.items():
            fan_points = fan_points + (float(modifier_value) * float(Statistic.get_stat_modifier_by_name(modifier_name)))
        return str(fan_points)

    return render_template("fanpoints/calculator.html")


def get_player_info(player_id, year):
    api = YahooFantasyAPI()
    request_uri = f"{api.uri}/league/{api.league_key}/players;" \
        f"player_keys={api.game_key}.p.{player_id}/" \
        f"stats;type=season;season={year}?format={api.request_format}"
    player_info = api.yahoo_request(request_uri)
    return player_info
