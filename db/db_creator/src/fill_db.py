import sqlite3

from datetime import datetime

from db.db_creator.src.player import Player, Stats
from db.db_creator.src.scrape_data import get_player_data, get_teams_data
from db.db_creator.src.db_utils import get_ids
from config.env_loader import get_base_path

db_path = get_base_path()

# sql fun, data was aggregated inside of the classes;
# seasons table didnt require any particular parsing as it contains
# pretty straightforward records
def fill_seasons_table() -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    season = 2000
    while season <= datetime.now().year:
        cursor.execute("INSERT INTO seasons (year) VALUES (?)", (season,))
        season += 1

    connection.commit()
    connection.close()


def fill_players_table(player, season) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    [lastname, firstname] = player.name.split(", ")

    cursor.execute(
        """INSERT INTO players (code, first_name, last_name, yob) 
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(code) DO NOTHING""",
        (str(player.code), firstname, lastname, f"{season - player.age}-01-01"),
    )
    connection.commit()
    connection.close()


def fill_teams_table(team) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO teams (code, name)
                   VALUES (?, ?)
                   ON CONFLICT(code) DO NOTHING""",
        (str(team.code), team.name),
    )
    connection.commit()
    connection.close()


# get_ids defined in utils; used due to redundancy fix
def fill_players_teams_table(players_list, season) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for player in players_list:

        player_id, team_id, season_id = get_ids(cursor, player, season)

        cursor.execute(
            """INSERT INTO playersTeams (player_id, team_id, season_id)
                       VALUES (?, ?, ?)""",
            (player_id, team_id, season_id),
        )

    connection.commit()
    connection.close()


def fill_stats(players_list, season) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for player in players_list:

        player_id, team_id, season_id = get_ids(cursor, player, season)
        if player_id is None or team_id is None or season_id is None:
            connection.close()
            return False

        # get players_teams id
        cursor.execute(
            "SELECT id FROM playersTeams WHERE player_id = ? AND team_id = ? AND season_id = ?",
            (player_id, team_id, season_id),
        )
        player_team_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO stats (player_team_id, games_played, points_scored, two_pointers_made, two_pointers_attempted, three_pointers_made, three_pointers_attempted, free_throws_made, free_throws_attempted, offensive_rebounds, defensive_rebounds, assists, steals, turnovers, blocks, fouls) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                player_team_id,
                player.stats.games_played,
                player.stats.points_scored,
                player.stats.two_pointers_made,
                player.stats.two_pointers_attempted,
                player.stats.three_pointers_made,
                player.stats.three_pointers_attempted,
                player.stats.free_throws_made,
                player.stats.free_throws_attempted,
                player.stats.offensive_rebounds,
                player.stats.defensive_rebounds,
                player.stats.assists,
                player.stats.steals,
                player.stats.turnovers,
                player.stats.blocks,
                player.stats.fouls,
            ),
        )
    connection.commit()
    connection.close()
    return True

def fill_database() -> bool:
    db_status = True
    fill_seasons_table()
    season = datetime.now().year
    while season >= 2000:
        teams_data = get_teams_data(season)
        players_data = get_player_data(season)

        for team in teams_data:
            fill_teams_table(team)
        for player in players_data:
            fill_players_table(player, season)

        fill_players_teams_table(players_data, season)
        stats_status = fill_stats(players_data, season)
        if stats_status == False:
            db_status = False
            break
        season -= 1
    return db_status
