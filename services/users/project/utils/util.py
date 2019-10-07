from project import db
from project.api.models.player import Player
from project.utils.yahooAdapter import YahooFantasyAPI


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


def add_player(p_id, first_name, last_name):
    """Adds a Player to the database."""
    db.session.add(
        Player(
            player_id=p_id,
            first_name=first_name,
            last_name=last_name
        )
    )
    db.session.commit()


def fetch_draft_results_archive(year, league_id):
    api = YahooFantasyAPI()
    request_uri = f"https://basketball.fantasysports.yahoo.com/archive/nba/{year}/{league_id}/" \
        f"draftresults?drafttab=team"
    draft_results = api.get_session().get(request_uri).content
    return draft_results
