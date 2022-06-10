import string
from unittest import TestCase

from boggle import BoggleGame

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!--*Marker tag* Boggle Home Page, used for testing purposes-->', html)


    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")

        game_info = response.get_json()
        game_id = game_info['gameId']
        game_board = game_info['board']

        self.assertIn('gameId',game_info.keys())
        self.assertIsInstance(game_id, str)
        self.assertIn('board',game_info.keys())
        self.assertIsInstance(game_board, list)

        for lst in game_board:
            self.assertIsInstance(lst, list)

        # game[id] is an in the games dicitonary
        # Assert the value in-
        # -the dictionary is an instance of a game

        self.assertIn(game_id,games)
        self.assertIsInstance(games[game_id],BoggleGame)


        #breakpoint()
        # write a test for this route
