from fastapi import APIRouter, HTTPException

from app.dal.remove_team import rm_team


team_delete = APIRouter()

@team_delete.delete("/team/delete/{team_code}")
async def delete_team(team_code: str):
    r = rm_team(team_code)
    if r:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_code