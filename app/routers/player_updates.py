from fastapi import APIRouter, HTTPException

from app.models.player_insert_model import Player
from app.dal.put_players import player_put

player_update = APIRouter()

@player_update.put("/player/{player_code}", response_model=Player)
async def update_player(player_code: str, player: Player):
    r = player_put(player, player_code)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player