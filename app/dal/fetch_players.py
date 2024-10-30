import sqlite3

from app.dal.utils import get_db_conn
from app.models.player_get_model import PlayerGet, PlayerGetCarrer


class PlayerFetcher:
    def __init__(self) -> None:
        pass

    # retrieves players list for a provided season
    def retrieve_all_players(self, season, page, limit):
        offset = (page - 1) * limit
        with get_db_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """SELECT p.id AS id, p.code AS code, p.first_name AS first_name, p.last_name AS last_name, t.name AS team_name
                    FROM players p 
                    JOIN playersTeams pt ON p.id = pt.player_id 
                    JOIN teams t ON pt.team_id  = t.id 
                    JOIN seasons s ON pt.season_id = s.id
                    WHERE s."year" = ?
                    LIMIT ? OFFSET ?""",
                (season, limit, offset),
            )
            players = c.fetchall()
            conn.commit()

        players_data = [
            PlayerGet(
                id=row["id"],
                code=row["code"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                team_name=row["team_name"],
            )
            for row in players
        ]

        return players_data

    # retrieves player data across all seasons
    def retrieve_player(self, first_name: str, last_name: str):
        with get_db_conn() as conn:
            # ret rows as dicts
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """SELECT DISTINCT p.id, p.code, p.first_name, p.last_name, p.yob, t.name AS team_name, s.year, 
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
            conn.commit()

        player_data = [
            PlayerGetCarrer(
                id=row["id"],
                code=row["code"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                yob=row["yob"],
                team_name=row["team_name"],
                year=row["year"],
                points_scored=row["points_scored"],
                two_pointers_made=row["two_pointers_made"],
                two_pointers_attempted=row["two_pointers_attempted"],
                three_pointers_made=row["three_pointers_made"],
                three_pointers_attempted=row["three_pointers_attempted"],
                free_throws_made=row["free_throws_made"],
                free_throws_attempted=row["free_throws_attempted"],
                offensive_rebounds=row["offensive_rebounds"],
                defensive_rebounds=row["defensive_rebounds"],
                assists=row["assists"],
                steals=row["steals"],
                turnovers=row["turnovers"],
                blocks=row["blocks"],
                fouls=row["fouls"],
            )
            for row in player_career
        ]
        return player_data
