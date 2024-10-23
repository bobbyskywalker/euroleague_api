import sqlite3
import json
from flask import jsonify

db_path = "/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db"


# retrieves players list for a provided season
def retrieve_all_players(season):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(
        """SELECT p.id, p.first_name, p.last_name, t.name
              FROM players p 
              JOIN playersTeams pt ON p.id = pt.player_id 
              JOIN teams t ON pt.team_id  = t.id 
              JOIN seasons s ON pt.season_id = s.id
              WHERE s."year" = ?""",
        (season,),
    )
    players = c.fetchall()

    conn.commit()
    conn.close()

    p_list = [
        {
            "player_id": player[0],
            "first_name": player[1],
            "last_name": player[2],
            "team": player[3],
        }
        for player in players
    ]
    if not p_list:
        return json.dumps({"error 404": "Resource not found."})
    return json.dumps(p_list, indent=4)


def model_player_json(player_carrer):
    seasons_data = {}
    for row in player_carrer:
        year = row["year"]
        player_data = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "yob": row["yob"],
            "team_name": row["team_name"],
            "points_scored": row["points_scored"],
            "two_pointers_made": row["two_pointers_made"],
            "two_pointers_attempted": row["two_pointers_attempted"],
            "three_pointers_made": row["three_pointers_made"],
            "three_pointers_attempted": row["three_pointers_attempted"],
            "free_throws_made": row["free_throws_made"],
            "free_throws_attempted": row["free_throws_attempted"],
            "offensive_rebounds": row["offensive_rebounds"],
            "defensive_rebounds": row["defensive_rebounds"],
            "assists": row["assists"],
            "steals": row["steals"],
            "turnovers": row["turnovers"],
            "blocks": row["blocks"],
            "fouls": row["fouls"],
        }
        if year not in seasons_data:
            seasons_data[year] = []
        seasons_data[year].append(player_data)

    res_json = json.dumps(seasons_data, indent=1)
    return res_json


def retrieve_player(first_name, last_name):
    conn = sqlite3.connect(db_path)
    # ret rows as dicts
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        """SELECT p.id, p.first_name, p.last_name, p.yob, t.name AS team_name, s.year, 
                    st.points_scored, st.two_pointers_made, st.two_pointers_attempted, 
                    st.three_pointers_made, st.three_pointers_attempted, 
                    st.free_throws_made, st.free_throws_attempted, 
                    st.offensive_rebounds, st.defensive_rebounds, 
                    st.assists, st.steals, st.turnovers, st.blocks, st.fouls 
            FROM players p 
            JOIN playersTeams pt ON p.id = pt.player_id
            JOIN stats st ON pt.id = st.player_team_id 
            JOIN teams t ON pt.team_id  = t.id 
            JOIN seasons s ON pt.season_id = s.id
            WHERE p.first_name = ? AND p.last_name = ?""",
        (first_name, last_name),
    )
    player_career = c.fetchall()
    if not player_career:
        return json.dumps({"error 404": "Player not found."})
    res = model_player_json(player_career)
    return res
