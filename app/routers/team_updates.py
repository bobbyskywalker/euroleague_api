from fastapi import APIRouter, HTTPException

from app.models.team_model import Team
from app.dal.put_team import team_put


team_update = APIRouter()

# r = return value
@team_update.put("/teams/{team_code}", response_model=Team)
async def update_team(team: Team, team_code: str):
    r = team_put(team, team_code)
    if r:
        raise HTTPException(status_code=404, detail="Team not found")
    return team