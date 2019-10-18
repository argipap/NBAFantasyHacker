# services/users/project/api/views/users.py
from flask import Blueprint, jsonify, render_template

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
