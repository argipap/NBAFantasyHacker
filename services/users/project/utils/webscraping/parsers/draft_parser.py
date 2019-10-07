from project.utils.webscraping.locators.draft_results_locator import DraftResultsLocator
from project.utils.webscraping.parsers.player_parser import PlayerParser


class DraftResultsParser:
    def __init__(self, parent):
        self.parent = parent

    @property
    def team(self):
        return {self.parent.select_one(DraftResultsLocator.TEAM).text: self.players}

    @property
    def players(self):
        return PlayerParser(self.parent).players
