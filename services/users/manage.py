# services/users/manage.py

import unittest
import re
import json
from flask.cli import FlaskGroup
from project import create_app, db
from project.utils.yahooAdapter import YahooFantasyAPI
from project.api.models.player import Player
from project.api.models.statistic import Statistic

app = create_app()
cli = FlaskGroup(create_app=create_app)


def get_players():
    api = YahooFantasyAPI()
    player_list = []
    for start in range(0, 709, 25):
        players = api.get_players(start)
        for player in players:
            player_first_name = player['name']['first']
            player_last_name = player['name']['last']
            player_id = player['player_id']
            player_info = dict()
            player_info["player_id"] = player_id
            player_info["first_name"] = player_first_name
            player_info["last_name"] = player_last_name
            player_list.append(player_info)
    return player_list


def get_statistics():
    api = YahooFantasyAPI()
    statistics = api.get_league_stats(api.fetch_league_settings())
    return statistics


@cli.command()
def seed_db_players():
    """Seeds the database."""
    players = get_players()
    for player in players:
        db.session.add(
            Player(
               player_id=int(player["player_id"]),
               first_name=player["first_name"],
               last_name=player["last_name"]
            )
        )
    db.session.commit()


@cli.command()
def seed_db_stats():
    """Seeds the database."""
    statistics = get_statistics()
    for stat in statistics:
        print(stat['stat']['stat_id'], stat['stat']['name'], stat['stat']['display_name'])
        db.session.add(
            Statistic(
                statistic_id=int(stat['stat']['stat_id']),
                stat_short_name=stat['stat']['name'],
                stat_full_name=stat['stat']['display_name']
            )
        )
    db.session.commit()


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test_stats():
    api = YahooFantasyAPI()
    result = api.get_player_stats(3704, 2018)
    print(result)


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def test_league_id():
    api = YahooFantasyAPI()
    result = api.get_league_id('kantina', '2016')
    print(result)


if __name__ == '__main__':
    cli()
