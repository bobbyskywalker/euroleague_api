from fastapi import APIRouter

from app.models.player_insert_model import Player, PlayerSeason
from app.dal.insert_players import add_player, add_player_season

player_insert = APIRouter()


@player_insert.post("/player/add", response_model=Player)
async def insert_player(player: Player):
    add_player(player)
    return player


@player_insert.post("/player/add-season", response_model=PlayerSeason)
async def insert_player_season(player_season: PlayerSeason):
    add_player_season(player_season)
    return player_season
