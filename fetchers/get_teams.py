import sqlite3


class TeamFetcher:
    def __init__(self, db_path) -> None:
        self.db_path = db_path

    # season parameter is optional- makes func generic both for 
    # all-time list and specific season lists
    def get_team_list(self, season):
        conn = sqlite3.connect(self.db_path)
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

        return res

    def get_team_roster(self, season, team_code):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        conn.row_factory = sqlite3.Row
        c.execute(
            """SELECT DISTINCT p.code, p.first_name, p.last_name, p.yob
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
        return res
