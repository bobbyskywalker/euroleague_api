import sqlite3

from app.dal.utils import get_db_conn, get_th_base64
from app.models.player_get_model import PlayerGet, PlayerGetCarrer

# the object is responsible for fetching players data from db and returning it in a predefined model format
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
                """SELECT p.id AS id, p.code AS code, p.first_name AS first_name, p.last_name AS last_name, p.img_name AS img_name, t.name AS team_name
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
                thumbnail=get_th_base64(row["img_name"])
            )
            for row in players
        ]

        return players_data

    # retrieves player data across all seasons
    def retrieve_player(self, player_id):
        with get_db_conn() as conn:
            # ret rows as dicts
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """SELECT DISTINCT p.id, p.code, p.first_name, p.last_name, p.yob, p.img_name AS img_name, t.name AS team_name, s.year, 
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
                    WHERE p.id = ?""",
                (player_id, ),
            )
            player_career = c.fetchall()
            conn.commit()

        if not player_career:
            return None, None
        
        #th to appear just once in json response
        thumbnail = get_th_base64(player_career[0]["img_name"])

        player_data = [
            PlayerGetCarrer(
                id=row["id"],
                code=row["code"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                yob=row["yob"],
                team_name=row["team_name"],
                thumbnail=get_th_base64(row["img_name"]),
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
        return player_data, thumbnail
    
    def get_player_pic(self, player_id):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute('''SELECT img_name FROM players WHERE id = ?''', (player_id,))
            res = c.fetchone()
            if res is not None:
                return res[0]
        return None


#### SECTION: UTILS ####
 
# used in heatmap comparison
def get_players_data(names: list, season: int):
    data = []
    with get_db_conn() as conn:
        for full_name in names:
            first_name = full_name[0]
            last_name = full_name[1]
            c = conn.cursor()
            c.execute(
                    """SELECT DISTINCT p.first_name, p.last_name, st.points_scored, st.two_pointers_made, st.two_pointers_attempted, 
                                st.three_pointers_made, st.three_pointers_attempted, 
                                st.free_throws_made, st.free_throws_attempted, 
                                st.offensive_rebounds, st.defensive_rebounds, 
                                st.assists, st.steals, st.turnovers, st.blocks, st.fouls 
                        FROM players p 
                        JOIN playersTeams pt ON p.id = pt.player_id
                        JOIN stats st ON pt.id = st.player_team_id 
                        JOIN teams t ON pt.team_id  = t.id 
                        JOIN seasons s ON pt.season_id = s.id
                        WHERE p.first_name = ? AND p.last_name = ? AND s.year = ?""", (first_name, last_name, season))
            player_data = c.fetchall()
            data.append(player_data)
    return data

# used in shooting chart
def get_player_shooting(name: list):
    with get_db_conn() as conn:
        c = conn.cursor()
        c.execute(
                """SELECT DISTINCT s.year, st.two_pointers_made, st.two_pointers_attempted, st.three_pointers_made,
                  st.three_pointers_attempted, st.free_throws_made, st.free_throws_attempted
                  FROM players p
                  JOIN playersTeams pt ON p.id = pt.player_id
                  JOIN seasons s ON pt.season_id = s.id
                  JOIN stats st ON pt.id = st.player_team_id 
                  WHERE p.first_name = ? AND p.last_name = ?""", (name[0][0], name[0][1]))
        player_shooting = c.fetchall()
    return player_shooting