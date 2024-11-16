import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from app.dal.utils import get_db_conn

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

    output_path = "app/view/visualize/visuals/heatmap.png"
    plt.savefig(output_path)
    plt.show()
    plt.close()
    return
