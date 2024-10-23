import sqlite3
import json
from flask import jsonify

db_path = '/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db'

# retrieves players list for a provided season
def retrieve_players(season):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''SELECT p.id, p.first_name, p.last_name, t.name
              FROM players p 
              JOIN playersTeams pt ON p.id = pt.player_id 
              JOIN teams t ON pt.team_id  = t.id 
              JOIN seasons s ON pt.season_id = s.id
              WHERE s."year" = ?''', (season,))
    players = c.fetchall()
    
    conn.commit()
    conn.close()

    p_list = [
        {
            'player_id': player[0],
            'first_name': player[1],
            'last_name': player[2],
            'team': player[3]
        }
        for player in players
    ]
    return json.dumps(p_list)