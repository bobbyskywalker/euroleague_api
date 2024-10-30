from fastapi import APIRouter, HTTPException

from app.dal.remove_players import rm_player


player_delete = APIRouter()


@player_delete.delete("/players/{player_code}")
async def delete_player(player_code: str):
    r = rm_player(player_code)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_code