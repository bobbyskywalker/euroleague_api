from fastapi import APIRouter, HTTPException
import sqlite3

from inserts.team_class import Team
from routers.db_connect import get_db_conn

team_insert = APIRouter()
db_path = "../euroleague.db"

@team_insert.post("/team/add", response_model=Team)
async def insert_team(team: Team):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO teams (code, name) VALUES (?, ?)''', (team.code, team.name))
        conn.commit()
    return team
