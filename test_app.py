import string
from unittest import TestCase

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

        self.assertIn('gameId',game_info.keys())
        self.assertIsInstance(game_info['gameId'], str)
        self.assertIn('board',game_info.keys())
        self.assertIsInstance(game_info['board'], list)

        for lst in game_info['board']:
            self.assertIsInstance(lst, list)

        #breakpoint()
        # write a test for this route
