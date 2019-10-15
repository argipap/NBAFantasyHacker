# services/users/project/tests/test_users.py
import unittest

from project.models.player import Player
from project.tests.base import BaseTestCase
from project.utils.util import add_player


class TestPlayerService(BaseTestCase):

    def test_player_id(self):
        add_player(1, "Argi", "Pap")
        result = Player.get_player_id_by_full_name("Argi", "Pap")
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
