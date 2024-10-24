from fastapi import APIRouter, HTTPException

from fetchers.get_players import PlayerFetcher


db_path = "../euroleague.db"

player_fetch = PlayerFetcher(db_path)
players_router = APIRouter()


# GET: all players list from one season
@players_router.get("/players/{season}")
async def all_players_data(season: int):
    players = player_fetch.retrieve_all_players(season)
    if not players or players == "[]":
        raise HTTPException(status_code=404, detail="Resource not found.")
    return players


# GET: player carrer grouped by seasons
@players_router.get("/player/{firstname}/{lastname}")
async def single_player_data(firstname: str, lastname: str):
    player = player_fetch.retrieve_player(firstname.upper(), lastname.upper())
    if not player or player == "[]":
        raise HTTPException(status_code=404, detail="Player not found.")
    return player
