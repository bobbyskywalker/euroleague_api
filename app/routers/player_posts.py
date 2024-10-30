from fastapi import APIRouter

from app.models.player_insert_model import Player, PlayerSeason
from app.dal.insert_players import add_player, add_player_season
from app.dal.search_player import find_player
from app.models.search_player_class import SearchPlayer
from app.models.player_get_model import PlayerGet
from app.models.player_get_model import PaginatedPlayersResponse

player_insert = APIRouter()


@player_insert.post("/players", response_model=Player)
async def insert_player(player: Player):
    add_player(player)
    return player


@player_insert.post("/players", response_model=PlayerSeason)
async def insert_player_season(player_season: PlayerSeason):
    add_player_season(player_season)
    return player_season

@player_insert.post("/players/search", response_model=PaginatedPlayersResponse)
async def search_player(attributes: SearchPlayer):
    players = find_player(attributes)
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