import sqlite3
import json
from flask import jsonify

db_path = "/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db"


def get_team_list(season):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    conn.row_factory = sqlite3.Row

    if season == None:
        c.execute("SELECT id, code, name FROM teams")
    else:
        c.execute(
            """SELECT DISTINCT t.id, t.code, t.name 
            FROM teams t
            JOIN playersTeams pt on t.id = pt.team_id 
            JOIN seasons s on s.id  = pt.season_id 
            WHERE s."year" = ?""",
            (season,),
        )
    teams = c.fetchall()

    conn.commit()
    conn.close()

    res = []
    for row in teams:
        team_data = {"id": row[0], "code": row[1], "name": row[2]}
        res.append(team_data)

    return json.dumps(res, indent=4)


def get_team_roster(season, team_code):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    conn.row_factory = sqlite3.Row

    c.execute(
        """SELECT p.code, p.first_name, p.last_name, p.yob
            FROM players p 
            JOIN playersTeams pt on p.id = pt.player_id 
            JOIN teams t on t.id = pt.team_id
            JOIN seasons s on s.id = pt.season_id 
            WHERE s."year" = ? and t.code = ?""",
        (season, team_code),
    )

    players = c.fetchall()

    conn.commit()
    conn.close()

    res = []
    for row in players:
        player_data = {
            "code": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "yob": row[3],
        }
        res.append(player_data)
    if not res:
        return json.dumps({"error 404": "Resource not found."})

    return json.dumps(res, indent=4)
