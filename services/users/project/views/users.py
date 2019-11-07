# services/users/project/api/views/users.py
from flask import Blueprint, jsonify, render_template, request

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@users_blueprint.route('/user/draftpicks', methods=['GET', 'POST'])
def draft_picks_calculator():
    if request.method == 'POST':
        rounds = int(request.form['rounds'])
        teams = int(request.form['teams'])
        turn = int(request.form['turn'])
        if rounds < 1 or teams < 1:
            return jsonify({
                'status': 'error',
                'message': 'Rounds or teams must be >1'
            })
        if turn == 0 or turn > teams:
            return jsonify({
                'status': 'error',
                'message': 'Turn cannot be zero or greater than the number of the teams'
            })
        results_list = calculate_pick_turns(rounds, teams, turn)
        return jsonify({
                'status': 'success',
                'message': results_list
            })
    return render_template("draftpicks.html")


def calculate_pick_turns(rounds, num_of_teams, draft_turn):
    results_list = []
    for round in range(1, rounds+1):
        if round % 2 == 1:
            result = num_of_teams * round - num_of_teams + draft_turn
        else:
            result = num_of_teams * round - draft_turn + 1
        results_list.append(result)
    return results_list
