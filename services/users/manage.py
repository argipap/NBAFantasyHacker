# services/users/manage.py

import unittest
import click
import time

from flask.cli import FlaskGroup
from project import create_app, db
from project.utils.util import get_statistics, get_players, fetch_draft_results_archive, get_stat_modifiers
from project.models.statistics import StatisticCategory, Statistic
from project.models.player import Player, PlayerFanPoints
from project.views.players import get_player_stats, stats_to_fapoints_archive
from project.utils.webscraping.pages.draft_results_page import DraftResultsPage

app = create_app()
cli = FlaskGroup(create_app=create_app)


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
    statistics, modifiers = get_statistics()
    print(statistics)
    print(modifiers)
    for stat in statistics:
        for modifier in modifiers:
            if stat['stat']['stat_id'] == modifier['stat']['stat_id']:
                modifier_value = modifier['stat']['value']
                db.session.add(
                    StatisticCategory(
                        category_id=int(stat['stat']['stat_id']),
                        stat_short_name=stat['stat']['display_name'],
                        stat_full_name=stat['stat']['name'],
                        stat_modifier=modifier_value
                    )
                )
            else:
                continue
    db.session.commit()


@cli.command()
@click.option('--year')
def seed_db_player_stats(year):
    """Seeds the database."""
    year = int(year)
    players = Player.query.all()
    for player in players:
        statistics = get_player_stats(player.player_id, year).json
        if statistics['status'] == 'error':
            continue
        else:
            for stat_key, stat_value in statistics['player_stats'].items():
                if stat_value == '-':
                    stat_value = 0
                db.session.add(
                    Statistic(
                        statistic_id=StatisticCategory.get_stat_id_by_name(stat_key),
                        player_id=player.player_id,
                        value=round(float(stat_value), 2),
                        year=year)
                )
            db.session.commit()
            # sleep for 2 seconds in order not to get error from yahoo
            time.sleep(2)


@cli.command()
@click.option('--year')
def seed_db_fanpoints(year):
    players = Player.query.all()
    for player in players:
        player_statistics = Statistic.get_statistics_by_player_id(player.player_id, year)
        fanpoints = stats_to_fapoints_archive(player_statistics)
        # print(player.player_id, player.last_name, fanpoints)
        db.session.add(PlayerFanPoints(player_id=player.player_id, total=fanpoints))
        db.session.commit()


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

#
# @cli.command()
# def test_league_id():
#     api = YahooFantasyAPI()
#     result = api.get_league_id('kantina', '2016')
#     print(result)
#
#
@cli.command()
def test_new():
    year = '2017'
    league_id = 6370
    page = fetch_draft_results_archive(year, league_id)
    print(DraftResultsPage(page).teams)


# @cli.command()
# def test_fan():
#     print(get_player_fanpoints(3704, '2018'))


if __name__ == '__main__':
    cli()
