from fastapi import APIRouter, HTTPException

from app.dal.fetch_players import PlayerFetcher
from app.models.player_get_model import PaginatedPlayersResponse

player_fetch = PlayerFetcher()
players_get_router = APIRouter()


# GET: all players list from one season
@players_get_router.get("/players/{season}", response_model=PaginatedPlayersResponse)
async def all_players_data(season: int, page: int, limit: int):
    players = player_fetch.retrieve_all_players(season, page, limit)
    if not players or players == "[]":
        raise HTTPException(status_code=404, detail="Resource not found.")
    return PaginatedPlayersResponse(total=len(players), items=players)


# GET: player carrer grouped by seasons
# TODO: firstname lastname as query parameters, search by id
@players_get_router.get("/players/{firstname}/{lastname}")
async def single_player_data_and_stats(firstname: str, lastname: str):
    player = player_fetch.retrieve_player(firstname.upper(), lastname.upper())
    if not player or player == "[]":
        raise HTTPException(status_code=404, detail="Player not found.")
    return player

    
