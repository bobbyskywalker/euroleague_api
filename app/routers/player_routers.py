from fastapi import APIRouter, HTTPException

from app.models.player_get_model import PaginatedPlayersResponse
from app.models.player_insert_model import Player, PlayerSeason
from app.models.search_player_class import SearchPlayer
from app.models.player_get_model import PlayerGet
from app.models.player_get_model import PaginatedPlayersResponse
from app.dal.fetch_players import PlayerFetcher
from app.dal.insert_players import add_player, add_player_season
from app.dal.search_player import find_player
from app.dal.put_players import player_put
from app.dal.remove_players import rm_player

player_fetch = PlayerFetcher()

players_get = APIRouter()
players_insert = APIRouter()
players_update = APIRouter()
players_delete = APIRouter()

# GET: all players list from one season
@players_get.get("/players/{season}", response_model=PaginatedPlayersResponse)
async def all_players_data(season: int, page: int, limit: int):
    players = player_fetch.retrieve_all_players(season, page, limit)
    if not players or players == "[]":
        raise HTTPException(status_code=404, detail="Resource not found.")
    return PaginatedPlayersResponse(total=len(players), items=players)


# GET: player carrer grouped by seasons
# TODO: firstname lastname as query parameters, search by id
@players_get.get("/players/{firstname}/{lastname}")
async def single_player_data_and_stats(firstname: str, lastname: str):
    player = player_fetch.retrieve_player(firstname.upper(), lastname.upper())
    if not player or player == "[]":
        raise HTTPException(status_code=404, detail="Player not found.")
    return player

# POST: insert player
@players_insert.post("/players", response_model=Player)
async def insert_player(player: Player):
    add_player(player)
    return player

# POST: insert player's single season performance (stats)
@players_insert.post("/players", response_model=PlayerSeason)
async def insert_player_season(player_season: PlayerSeason):
    add_player_season(player_season)
    return player_season

# POST: search for a specific player
@players_insert.post("/players/search", response_model=PaginatedPlayersResponse)
async def search_player(attributes: SearchPlayer, page: int, limit: int):
    players = find_player(attributes, page, limit)
    players_data = [
        PlayerGet(
            id=row[0],
            code=row[1],
            first_name=row[2],
            last_name=row[3],
            team_name=row[4],
        )
        for row in players
    ]
    return PaginatedPlayersResponse(total=len(players_data), items=players_data)

# PUT: update player info
@players_update.put("/players/{player_code}", response_model=Player)
async def update_player(player_code: str, player: Player):
    r = player_put(player, player_code)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# DELETE: delete player
@players_delete.delete("/players/{player_code}")
async def delete_player(player_code: str):
    r = rm_player(player_code)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_code