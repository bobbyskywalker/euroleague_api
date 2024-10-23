from flask import Flask, render_template, jsonify, request
from get_players import retrieve_all_players, retrieve_player

app = Flask(__name__)

# GET: all players list from one season
@app.route("/players/<int:season>", methods = ['GET'])
def all_players_data(season):
    players_json = retrieve_all_players(season)
    return players_json

# GET: player carrer grouped by seasons
@app.route("/player/<firstname>/<lastname>")
def single_player_data(firstname, lastname):
    player_json = retrieve_player(firstname, lastname)
    return player_json

if __name__ == '__main__':
    app.run(debug=True)