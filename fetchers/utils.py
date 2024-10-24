import json


def model_player_json(player_carrer):
    seasons_data = []
    for row in player_carrer:
        player_data = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "yob": row["yob"],
            "team_name": row["team_name"],
            "points_scored": row["points_scored"],
            "two_pointers_made": row["two_pointers_made"],
            "two_pointers_attempted": row["two_pointers_attempted"],
            "three_pointers_made": row["three_pointers_made"],
            "three_pointers_attempted": row["three_pointers_attempted"],
            "free_throws_made": row["free_throws_made"],
            "free_throws_attempted": row["free_throws_attempted"],
            "offensive_rebounds": row["offensive_rebounds"],
            "defensive_rebounds": row["defensive_rebounds"],
            "assists": row["assists"],
            "steals": row["steals"],
            "turnovers": row["turnovers"],
            "blocks": row["blocks"],
            "fouls": row["fouls"],
        }
        seasons_data.append(player_data)
    res_json = json.dumps(seasons_data, indent=4)
    return res_json
