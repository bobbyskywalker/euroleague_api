from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import uuid
import os

from app.models.player_insert_model import Player, PlayerSeason
from app.models.search_player_class import SearchPlayer
from app.models.player_get_model import PlayerGet, PaginatedPlayersResponse
from app.dal.fetch_players import PlayerFetcher
from app.dal.insert_players import add_player, add_player_season, add_player_picture
from app.dal.search_player import find_player
from app.dal.put_players import player_put
from app.dal.remove_players import rm_player
from app.dal.utils import save_thumbnail, get_th_base64
from config.env_loader import get_images_path

player_fetch = PlayerFetcher()

players_get = APIRouter()
players_insert = APIRouter()
players_update = APIRouter()
players_delete = APIRouter()

IMG_DIR = get_images_path()

#TODO: configure logging
# temp, debug
import logging
logging.basicConfig(filename='API.log', level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# GET: all players list from one season
@players_get.get("/players/season/{season}", response_model=PaginatedPlayersResponse)
async def all_players_data(season: int, page: int, limit: int):
    players = player_fetch.retrieve_all_players(season, page, limit)
    logging.info(f'Players: {players} {type(players)}')
    if not players or players == "[]":
        raise HTTPException(status_code=404, detail="Resource not found.")
    return PaginatedPlayersResponse(total=len(players), items=players)


# GET: player carrer grouped by seasons
@players_get.get("/players/{player_id}")
async def single_player_data_and_stats(player_id: int):
    player, thumbnail = player_fetch.retrieve_player(player_id)
    if not player or player == "[]":
        raise HTTPException(status_code=404, detail="Player not found.")
    return {"thumbnail": thumbnail, "player": player}

# GET: player image
@players_get.get("/players/download/{player_id}", response_class=FileResponse)
async def player_image(player_id: int):
    file_name = player_fetch.get_player_pic(player_id)
    logging.info(f'File name: {file_name} {type(file_name)}')
    if file_name is None:
        raise HTTPException(status_code=404, detail="Player not found")
    image_path = os.path.join(IMG_DIR, file_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)

# POST: insert player
@players_insert.post("/players", response_model=Player)
async def insert_player(player: Player):
    logging.info(f'Player: {player} {type(player)}')
    add_player(player)
    return player

# POST: insert player's single season performance (stats)
@players_insert.post("/players/season", response_model=PlayerSeason)
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
            thumbnail=get_th_base64(row[5])
        )
        for row in players
    ]
    return PaginatedPlayersResponse(total=len(players_data), items=players_data)

# POST: player_image
@players_insert.post("/players/upload/{player_id}")
async def player_image(player_id: int, image: UploadFile = File(...)):
    
    # pngs only
    if image.content_type != "image/png":
        raise HTTPException(status_code=400, detail="Only PNG files are allowed.")
    
    image.filename = f'{uuid.uuid4()}.png'
    content = await image.read()
    img_path = f'{IMG_DIR}{image.filename}'
    # save
    with open(img_path, "wb") as f:
        f.write(content)
    # save thumbnail
    save_thumbnail(img_path, image.filename)
    # save name to db
    add_player_picture(image.filename, player_id)

    return {"filename": image.filename}


# PUT: update player info
@players_update.put("/players/{player_id}", response_model=Player)
async def update_player(player_id: int, player: Player):
    r = player_put(player, player_id)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# DELETE: delete player
@players_delete.delete("/players/{player_id}")
async def delete_player(player_id : int):
    r = rm_player(player_id)
    if r:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_id