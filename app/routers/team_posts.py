from fastapi import APIRouter

from app.models.team_model import Team
from app.dal.insert_team import add_team

team_insert = APIRouter()


@team_insert.post("/team/add", response_model=Team)
async def insert_team(team: Team):
    add_team(team)
    return team
