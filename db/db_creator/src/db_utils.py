def get_ids(cursor, player, season):
    # get player id
    cursor.execute("SELECT id FROM players WHERE code = ?", (player.code,))
    player_row = cursor.fetchone()
    if player_row is None:
        print(f"Error: Player with code {player.code} not found.")
        return False, False, False
    player_id = player_row[0]

    # get team id
    cursor.execute("SELECT id FROM teams WHERE code = ?", (player.team_code,))
    team_row = cursor.fetchone()
    if team_row is None:
        print(f"Error: Team {player.team} not found.")
        return False, False, False
    team_id = team_row[0]

    # get season id
    cursor.execute("SELECT id from seasons WHERE year = ?", (season,))
    season_row = cursor.fetchone()
    if season_row is None:
        print(f"Error: Season {season} not found.")
        return False, False, False
    season_id = season_row[0]

    return player_id, team_id, season_id
