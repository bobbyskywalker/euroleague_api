from fastapi import APIRouter, HTTPException

from fetchers.get_teams import TeamFetcher


db_path = "../euroleague.db"

team_fetch = TeamFetcher(db_path)
teams_router = APIRouter()


# GET: all teams that ever played in euroleague
@teams_router.get("/teams")
def team_list():
    teams_json = team_fetch.get_team_list(None)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: teams playing in a specific season
@teams_router.get("/teams/{season}")
def teams_in_season(season):
    teams_json = team_fetch.get_team_list(season)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: team roster
@teams_router.get("/teams/{team_code}/{season}")
def team_roster(team_code, season):
    roster_json = team_fetch.get_team_roster(season, team_code)
    if roster_json == [] or not roster_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return roster_json
