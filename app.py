from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})

@app.post('/api/score-word')
def validate_word():
    """View Function score_word:
    Is called via ajax in the browser.
    The body of the request should include game_id, word
    {'game_id':game_id,'word':'word'}

    score_word will call below methods:
    If method resolves false values:
    1.) is_word_not_a_dup() => {result: "word-dup"}
    2.) is_word_in_word_list() => {result: "not-word"}
    3.) check_word_on_board() => {result: "not-on-board"}

    If all methods resolve true: {result: "ok"}
    """

    game_id = request.json.get('game_id')
    word = request.json.get('word')
    game = games[game_id]

    if not game.is_word_not_a_dup(word):
        return jsonify({"result": "word-dup"})

    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})

    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})


    # await axios.post("/api/score-word", { /* your data goes here... */ } )