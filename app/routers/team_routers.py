from fastapi import APIRouter, HTTPException

from app.models.team_model import Team
from app.models.team_model import Team
from app.dal.fetch_teams import TeamFetcher
from app.dal.put_team import team_put
from app.dal.insert_team import add_team
from app.dal.remove_team import rm_team

team_fetch = TeamFetcher()

teams_get = APIRouter()
teams_update = APIRouter()
teams_insert = APIRouter()
teams_delete = APIRouter()

# GET: all teams that ever played in euroleague
@teams_get.get("/teams")
def team_list():
    teams_json = team_fetch.get_team_list(None)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: teams playing in a specific season
@teams_get.get("/teams/{season}")
def teams_in_season(season):
    teams_json = team_fetch.get_team_list(season)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: team roster
@teams_get.get("/teams/{team_code}/{season}")
def team_roster(team_code, season):
    roster_json = team_fetch.get_team_roster(season, team_code)
    if roster_json == [] or not roster_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return roster_json


# PUT: update team
# r = error check
@teams_update.put("/teams/{team_code}", response_model=Team)
async def update_team(team: Team, team_code: str):
    r = team_put(team, team_code)
    if r:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# DELETE: delete team
@teams_delete.delete("/teams/{team_code}")
async def delete_team(team_code: str):
    r = rm_team(team_code)
    if r:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_code

# POST: insert team
@teams_insert.post("/teams", response_model=Team)
async def insert_team(team: Team):
    add_team(team)
    return team