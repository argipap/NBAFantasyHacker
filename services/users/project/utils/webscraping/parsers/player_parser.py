import re
from project.utils.webscraping.locators.draft_results_locator import DraftResultsLocator


class PlayerParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def players(self):
        return [PlayerParser.player_data(player) for player in self.parent.select(DraftResultsLocator.TEAMS_PLAYERS)]

    @classmethod
    def player_data(cls, player):
        players_url = player.find(DraftResultsLocator.PLAYER_URL['tag'],
                                  href=re.compile(r'[/]([a-z]|[A-Z])\w+')
                                  ).attrs[DraftResultsLocator.PLAYER_URL['attr']]
        return {
            'player_name': player.select_one(DraftResultsLocator.PLAYER_NAME).text,
            'player_team': player.select_one(DraftResultsLocator.PLAYER_TEAM).text,
            'player_url': players_url,
            'player_id': players_url.split("https://sports.yahoo.com/nba/players/")[1],
            'player_pick': player.select_one(DraftResultsLocator.PLAYER_PICK).text,
            'player_pick_round': player.select_one(DraftResultsLocator.PLAYER_ROUND).text.replace('.', '')
        }
