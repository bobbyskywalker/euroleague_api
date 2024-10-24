from flask import Blueprint, jsonify, Response

from fetchers.get_teams import TeamFetcher

db_path = "/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db"

team_fetch = TeamFetcher(db_path)

teams_bp = Blueprint("teams_bp", __name__)


@teams_bp.route("/teams", methods=["GET"])
def team_list():
    teams_json = team_fetch.get_team_list(None)
    if teams_json == [] or not teams_json:
        return jsonify({"error": "Resource not found."}), 404
    return Response(teams_json, mimetype="application/json charset=utf-8")


# GET: teams playing in a specific season
@teams_bp.route("/teams/<int:season>", methods=["GET"])
def teams_in_season(season):
    teams_json = team_fetch.get_team_list(season)
    if teams_json == [] or not teams_json:
        return jsonify({"error": "Resource not found."}), 404
    return Response(teams_json, mimetype="application/json charset=utf-8")


# GET: team roster
@teams_bp.route("/teams/<team_code>/<season>", methods=["GET"])
def team_roster(team_code, season):
    roster_json = team_fetch.get_team_roster(season, team_code)
    if roster_json == [] or not roster_json:
        return jsonify({"error": "Resource not found."}), 404
    return Response(roster_json, mimetype="application/json charset=utf-8")
