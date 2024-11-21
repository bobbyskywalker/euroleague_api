import json
import subprocess
from datetime import datetime
from typing import List

import requests

from db.db_creator.src.player import Player, Stats
from db.db_creator.src.team import Team


# request json scraping from euroleague page
def get_player_jsons() -> None:
    season = datetime.now().year
    subprocess.run(["mkdir players_data"], shell=True)
    while season > 1999:
        req = requests.get(
            f"https://feeds.incrowdsports.com/provider/euroleague-feeds/v3/competitions/E/statistics/players/traditional?seasonMode=Single&statistic=score&limit=1000&sortDirection=descending&seasonCode=E{season}&statisticMode=perGame&statisticSortMode=perGame"
        )
        with open(f"players_data/players{season}.json", "w") as f:
            f.write(req.text)
        season -= 1


def get_teams_jsons() -> None:
    season = datetime.now().year
    subprocess.run(["mkdir teams_data"], shell=True)
    while season > 1999:
        req = requests.get(
            f"https://feeds.incrowdsports.com/provider/euroleague-feeds/v2/competitions/E/seasons/E{season}/clubs"
        )
        with open(f"teams_data/teams{season}.json", "w") as f:
            f.write(req.text)
        season -= 1


# parsing json data into classes
def get_player_data(season) -> List[Player]:
    player_list = []
    with open(f"players_data/players{season}.json", "r") as f:
        data = json.load(f)
    for player_data in data["players"]:

        # if a player changed teams mid-season, the LATEST one is stored
        player_info = player_data["player"]
        stats = Stats(
            player_data["gamesPlayed"],
            player_data["gamesStarted"],
            player_data["minutesPlayed"],
            player_data["pointsScored"],
            player_data["twoPointersMade"],
            player_data["twoPointersAttempted"],
            player_data["threePointersMade"],
            player_data["threePointersAttempted"],
            player_data["freeThrowsMade"],
            player_data["freeThrowsAttempted"],
            player_data["offensiveRebounds"],
            player_data["defensiveRebounds"],
            player_data["assists"],
            player_data["steals"],
            player_data["turnovers"],
            player_data["blocks"],
            player_data["blocksAgainst"],
            player_data["foulsCommited"],
            player_data["foulsDrawn"],
            player_data["pir"],
        )
        player = Player(
            player_info["code"],
            player_info["name"],
            player_info["age"],
            player_info["team"]["name"].split(";")[0],
            stats,
            player_info["team"]["code"].split(";")[0],
        )

        player.stats = stats

        player_list.append(player)
    return player_list


def get_teams_data(season) -> List[Team]:
    team_list = []
    with open(f"teams_data/teams{season}.json", "r") as f:
        data = json.load(f)
    for team_data in data["data"]:
        team = Team(team_data["code"], team_data["name"])
        team_list.append(team)
    return team_list
