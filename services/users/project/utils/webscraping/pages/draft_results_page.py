from bs4 import BeautifulSoup

from project.utils.webscraping.locators.draft_results_locator import DraftResultsLocator
from project.utils.webscraping.parsers.draft_parser import DraftResultsParser


class DraftResultsPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def teams(self):
        return [DraftResultsParser(table).team for table in self.soup.select(DraftResultsLocator.RESULTS)]
