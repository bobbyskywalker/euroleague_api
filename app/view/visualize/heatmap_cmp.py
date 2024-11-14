import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from app.dal.get_id import get_id


def get_players_json(names: list, season: int):
    ids = []
    data = []
    
    for first_name, last_name in names:
        ids.append(get_id(first_name, last_name))
    
    for player_id in ids: 
        response = requests.get(f'http://0.0.0.0:8000/players/{player_id}')
        player_data = response.json()
        
        season_data = [
            player for player in player_data["player"] 
            if player["year"] == season
        ]
        
        if season_data:
            data.extend(season_data)
    
    return data

# Function to generate a heatmap for comparison
def heatmap_compare(names: list, season: int):
    profiles = get_players_json(names, season)
    
    # Prepare stats for each player
    stats = {
        f"{player['first_name']} {player['last_name']}": [
            player["points_scored"],
            player["offensive_rebounds"] + player["defensive_rebounds"],
            player["assists"],
            player["blocks"],
            player["steals"]
        ]
        for player in profiles
    }

    stats_array = np.array(list(stats.values()))
    players = list(stats.keys())
    categories = ['Points', 'Rebounds', 'Assists', 'Blocks', 'Steals']

    plt.figure(figsize=(8, 6))
    sns.heatmap(stats_array, annot=True, cmap="coolwarm", xticklabels=categories, yticklabels=players)
    plt.title('Player Stats Heatmap')
    plt.xlabel('Statistics')
    plt.ylabel('Players')
    plt.show()
    plt.savefig('app/view/visualize/visuals/heatmap.png')
    plt.close()

# name1 = input()
# name11 = input()
# p1 = (name1, name11)
# name2 = input()
# name22 = input()
# p2 = (name2, name22)
# name3 = input()
# name33 = input()
# p3 = (name3, name33)

# ps = [p1, p2, p3]
# heatmap_compare(ps, 2024)