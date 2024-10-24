from flask import Blueprint, jsonify, Response

from fetchers.get_players import PlayerFetcher

db_path = "/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db"

player_fetch = PlayerFetcher(db_path)

players_bp = Blueprint("players_bp", __name__)


# GET: all players list from one season
@players_bp.route("/players/<int:season>", methods=["GET"])
def all_players_data(season):
    players_json = player_fetch.retrieve_all_players(season)
    players_json = player_fetch.retrieve_all_players(season)
    if players_json == [] or not players_json:
        return jsonify({"error": "Resource not found."}), 404
    return Response(players_json, mimetype="application/json charset=utf-8")


# GET: player carrer grouped by seasons
@players_bp.route("/player/<firstname>/<lastname>", methods=["GET"])
def single_player_data(firstname, lastname):
    player_json = player_fetch.retrieve_player(firstname, lastname)
    if player_json == [] or not player_json:
        return jsonify({"error": "Resource not found."}), 404
    return Response(player_json, mimetype="application/json charset=utf-8")
