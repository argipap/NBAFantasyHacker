# services/users/manage.py

import unittest
from flask.cli import FlaskGroup
from project import create_app, db
from project.utils.util import get_statistics, get_players, fetch_draft_results_archive, get_stat_modifiers
from project.models.statistic import Statistic
from project.views.players import Player
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
                    Statistic(
                        statistic_id=int(stat['stat']['stat_id']),
                        stat_short_name=stat['stat']['display_name'],
                        stat_full_name=stat['stat']['name'],
                        stat_modifier=modifier_value
                    )
                )
            else:
                continue
    db.session.commit()


@cli.command()
def seed_db_stat_modifiers():
    """Seeds the database."""
    modifiers = get_stat_modifiers()
    print(modifiers)
    # for stat in statistics:
    #     db.session.add(
    #         Statistic(
    #             statistic_id=int(stat['stat']['stat_id']),
    #             stat_short_name=stat['stat']['name'],
    #             stat_full_name=stat['stat']['display_name']
    #         )
    #     )
    # db.session.commit()


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# @cli.command()
# def test_stats():
#     api = YahooFantasyAPI()
#     result = Player.get_player_stats(3704, 2018)
#     print(result)


@cli.command()
def test_player_id():
    result = Player.get_player_id_by_full_name('Vince', 'Carter')
    print(result)


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
