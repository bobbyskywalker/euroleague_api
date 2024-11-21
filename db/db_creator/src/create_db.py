import sqlite3
from config.env_loader import get_base_path

db_path = get_base_path()

# empty db creator
def create_tables():
    connection = sqlite3.connect(db_path)

    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute(
        """CREATE TABLE IF NOT EXISTS players
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT UNIQUE, 
                        first_name TEXT, 
                        last_name TEXT, 
                        yob DATE,
                        img_name TEXT)"""
    )

    connection.execute(
        """CREATE TABLE IF NOT EXISTS teams
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code TEXT UNIQUE, 
                        name TEXT,
                        img_name TEXT)"""
    )

    connection.execute(
        """CREATE TABLE IF NOT EXISTS seasons
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        year INTEGER)"""
    )

    connection.execute(
        """CREATE TABLE IF NOT EXISTS playersTeams
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_id INTEGER,
                        team_id INTEGER,
                        season_id INTEGER,
                        FOREIGN KEY(player_id) REFERENCES players(id),
                        FOREIGN KEY(team_id) REFERENCES teams(id),
                        FOREIGN KEY(season_id) REFERENCES seasons(id))"""
    )

    connection.execute(
        """CREATE TABLE IF NOT EXISTS stats
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_team_id INTEGER,
                        games_played INTEGER,
                        points_scored INTEGER,
                        two_pointers_made INTEGER,
                        two_pointers_attempted INTEGER,
                        three_pointers_made INTEGER,
                        three_pointers_attempted INTEGER,
                        free_throws_made INTEGER,
                        free_throws_attempted INTEGER,
                        offensive_rebounds INTEGER,
                        defensive_rebounds INTEGER,
                        assists INTEGER,
                        steals INTEGER,
                        turnovers INTEGER,
                        blocks INTEGER,
                        fouls INTEGER,
                        FOREIGN KEY(player_team_id) REFERENCES playersTeams(id))"""
    )
    connection.commit()
    connection.close()
