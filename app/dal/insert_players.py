from fastapi import HTTPException

from app.dal.utils import get_db_conn
from app.models.player_insert_model import Player
from app.models.player_insert_model import PlayerSeason

# The object is responsible for inserting players misc, stat and picture data into db
class PlayerInserter:
    def __init__(self) -> None:
        pass

    def add_player(self, player: Player):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute(
                """INSERT INTO players (code, first_name, last_name, yob) VALUES (?, ?, ?, ?)""",
                (player.code, player.first_name, player.last_name, f"{player.yob}-01-01"),
            )
            conn.commit()


    def insert_stats(self, c, player_season: PlayerSeason, PlayerTeam_code):
        c.execute(
            """ INSERT INTO stats (player_team_id, games_played, points_scored, two_pointers_made, two_pointers_attempted, 
            three_pointers_made, three_pointers_attempted, free_throws_made, free_throws_attempted, offensive_rebounds, defensive_rebounds, 
            assists, steals, turnovers, blocks, fouls)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                PlayerTeam_code,
                player_season.games_played,
                player_season.points_scored,
                player_season.two_pointers_made,
                player_season.two_pointers_attempted,
                player_season.three_pointers_made,
                player_season.three_pointers_attempted,
                player_season.free_throws_made,
                player_season.free_throws_attempted,
                player_season.offensive_rebounds,
                player_season.defensive_rebounds,
                player_season.assists,
                player_season.steals,
                player_season.turnovers,
                player_season.blocks,
                player_season.fouls,
            ),
        )


    def add_player_season(self, player_season: PlayerSeason):
        with get_db_conn() as conn:
            c = conn.cursor()

            # Find team id
            c.execute("""SELECT id FROM teams WHERE code = ?""", (player_season.team_code,))
            team_id_row = c.fetchone()
            if not team_id_row:
                raise HTTPException(status_code=404, detail="Team not found")
            team_id = team_id_row[0]

            # Find player id
            c.execute(
                """SELECT id FROM players WHERE code = ?""", (player_season.player_code,)
            )
            player_id_row = c.fetchone()
            if not player_id_row:
                raise HTTPException(status_code=404, detail="Player not found")
            player_id = player_id_row[0]

            # Find season id
            c.execute(
                """SELECT id FROM seasons WHERE "year" = ?""", (player_season.season_year,)
            )
            season_id_row = c.fetchone()
            if not season_id_row:
                raise HTTPException(status_code=404, detail="Season not found")
            season_id = season_id_row[0]

            # Insert into playersTeams table
            c.execute(
                """INSERT INTO playersTeams (player_id, team_id, season_id) VALUES (?, ?, ?)""",
                (player_id, team_id, season_id),
            )
            conn.commit()

            # Get playerTeam id
            c.execute(
                """SELECT id FROM playersTeams WHERE player_id = ? AND team_id = ? AND season_id = ?""",
                (player_id, team_id, season_id),
            )
            player_team_id_row = c.fetchone()
            if not player_team_id_row:
                raise HTTPException(
                    status_code=500, detail="Failed to retrieve playerTeam ID"
                )
            player_team_id = player_team_id_row[0]

            # Insert stats
            self.insert_stats(c, player_season, player_team_id)
            conn.commit()

    def add_player_picture(self, img_name: str, player_id: int):
        with get_db_conn() as conn:
            c = conn.cursor()
            c.execute(
                """UPDATE players SET img_name = ? WHERE id = ?""",
                (img_name, player_id),
            )
            conn.commit()