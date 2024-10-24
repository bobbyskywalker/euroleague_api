import sqlite3
from fetchers.utils import model_player_json


class PlayerFetcher:
    def __init__(self, db_path) -> None:
        self.db_path = db_path

    # retrieves players list for a provided season
    def retrieve_all_players(self, season):
        conn = sqlite3.connect(self.db_path)
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
            return []
        return p_list

    # retrieves player data across all seasons
    def retrieve_player(self, first_name, last_name):
        conn = sqlite3.connect(self.db_path)
        # ret rows as dicts
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            """SELECT DISTINCT p.id, p.first_name, p.last_name, p.yob, t.name AS team_name, s.year, 
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
            return []
        player_json = model_player_json(player_career)
        return player_json
