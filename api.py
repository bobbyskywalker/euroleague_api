from flask import Flask, render_template, jsonify, request
from fetchers.get_players import retrieve_all_players, retrieve_player
from fetchers.get_teams import get_team_list, get_team_roster

app = Flask(__name__)


# GET: all players list from one season
@app.route("/players/<int:season>", methods=["GET"])
def all_players_data(season):
    players_json = retrieve_all_players(season)
    return players_json


# GET: player carrer grouped by seasons
@app.route("/player/<firstname>/<lastname>")
def single_player_data(firstname, lastname):
    player_json = retrieve_player(firstname, lastname)
    return player_json


# GET: all teams list
@app.route("/teams")
def team_list():
    teams_json = get_team_list(None)
    return teams_json


# GET: teams playing in a specific season
@app.route("/teams/<int:season>")
def teams_in_season(season):
    teams_json = get_team_list(season)
    return teams_json


# GET: team roster
@app.route("/teams/<team_code>/<season>")
def team_roster(team_code, season):
    roster_json = get_team_roster(season, team_code)
    return roster_json


if __name__ == "__main__":
    app.run(debug=True)
