from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from app.dal.fetch_players import get_players_data


def heatmap_compare(names: list, season: int):
    profiles = get_players_data(names, season)
    
    structured_data = []
    for player_list in profiles:
        for player_stats in player_list:
            structured_data.append({
                "first_name": player_stats[0],
                "last_name": player_stats[1],
                "points_scored": player_stats[2],
                "rebounds": player_stats[9] + player_stats[10],
                "assists": player_stats[11],
                "blocks": player_stats[14],
                "steals": player_stats[12],
            })

    stats = {
        f"{player['first_name']} {player['last_name']}": [
            player["points_scored"],
            player["rebounds"],
            player["assists"],
            player["blocks"],
            player["steals"],
        ]
        for player in structured_data
    }

    stats_array = np.array(list(stats.values()))

    players = list(stats.keys())
    categories = ["Points", "Rebounds", "Assists", "Blocks", "Steals"]

    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        stats_array,
        annot=True,
        fmt="g",
        cmap="coolwarm",
        xticklabels=categories,
        yticklabels=players,
    )
    plt.title("Player Stats Heatmap")
    plt.xlabel("Statistics")
    plt.ylabel("Players")
    plt.tight_layout()

    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    return img_stream
