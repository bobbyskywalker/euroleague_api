import sqlite3

from app.dal.utils import get_db_conn, get_th_base64
from app.models.team_model import TeamView
from app.models.team_roster_model import TeamRoster

# the object fetches teams data from db and returns it in a predefined model format
class TeamFetcher:
    def __init__(self) -> None:
        pass

    # season parameter is optional- makes func generic both for
    # all-time list and specific season lists
    def get_team_list(self, season):
        with get_db_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            if season == None:
                c.execute("SELECT id, code, name, img_name FROM teams")
            else:
                c.execute(
                    """SELECT DISTINCT t.id, t.code, t.name, t.img_name
                    FROM teams t
                    JOIN playersTeams pt on t.id = pt.team_id 
                    JOIN seasons s on s.id  = pt.season_id 
                    WHERE s."year" = ?""",
                    (season,),
                )
            teams = c.fetchall()
            conn.commit()

        teams_data = [TeamView(id=row["id"], code=row["code"], name=row["name"], thumbnail=get_th_base64(row["img_name"])) for row in teams]

        return teams_data

    def get_team_roster(self, season, team_id):
        with get_db_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """SELECT DISTINCT p.code AS player_code, p.first_name AS first_name, p.last_name AS last_name, p.yob AS yob
                    FROM players p 
                    JOIN playersTeams pt on p.id = pt.player_id 
                    JOIN teams t on t.id = pt.team_id
                    JOIN seasons s on s.id = pt.season_id 
                    WHERE s."year" = ? and t.id = ?""",
                (season, team_id),
            )
            players = c.fetchall()

        # Create TeamRoster objects, ensuring only expected columns are unpacked
        roster = [
            TeamRoster(
                player_code=row["player_code"],
                player_first_name=row["first_name"],
                player_last_name=row["last_name"],
                player_yob=row["yob"],
            )
            for row in players
        ]

        return roster
    
    def get_team_pic(self, team_id):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute('''SELECT img_name FROM teams WHERE id = ?''', (team_id,))
            res = c.fetchone()
            if res is not None:
                return res[0]
        return None