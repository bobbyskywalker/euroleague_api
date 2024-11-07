from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.responses import FileResponse

import uuid
import os

from config.env_loader import get_images_path
from app.dal.utils import save_thumbnail
from app.models.team_model import Team
from app.dal.fetch_teams import TeamFetcher
from app.dal.put_team import team_put
from app.dal.insert_team import TeamInserter
from app.dal.remove_team import rm_team
from app.auth.authenticate import verify

team_fetch = TeamFetcher()
team_add = TeamInserter()

teams_get = APIRouter()
teams_update = APIRouter()
teams_insert = APIRouter()
teams_delete = APIRouter()

IMG_DIR = get_images_path()


# GET: all teams that ever played in euroleague
@teams_get.get("/teams")
def team_list():
    teams_json = team_fetch.get_team_list(None)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: teams playing in a specific season
@teams_get.get("/teams/season/{season}")
def teams_in_season(season):
    teams_json = team_fetch.get_team_list(season)
    if teams_json == [] or not teams_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return teams_json


# GET: team roster
@teams_get.get("/teams/roster/{team_id}/{season}")
def team_roster(team_id, season):
    roster_json = team_fetch.get_team_roster(season, team_id)
    if roster_json == [] or not roster_json:
        raise HTTPException(status_code=404, detail="Resource not found.")
    return roster_json


# GET: team picture
@teams_get.get("/teams/download/{team_id}")
def team_picture(team_id: int):
    file_name = team_fetch.get_team_pic(team_id)
    if file_name is None:
        raise HTTPException(status_code=404, detail="Team not found")
    image_path = os.path.join(IMG_DIR, file_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


# PUT: update team
# r = error check
@teams_update.put("/teams/update/{team_id}", response_model=Team)
async def update_team(team: Team, team_id: int, Verification: bool = Depends(verify)):
    if Verification:
        r = team_put(team, team_id)
        if r:
            raise HTTPException(status_code=404, detail="Team not found")
        return team
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# DELETE: delete team
@teams_delete.delete("/teams/delete{team_id}")
async def delete_team(team_id=int, Verification: bool = Depends(verify)):
    if Verification:
        r = rm_team(team_id)
        if r:
            raise HTTPException(status_code=404, detail="Team not found")
        return team_id
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# POST: insert team
@teams_insert.post("/teams", response_model=Team)
async def insert_team(team: Team, Verification: bool = Depends(verify)):
    if Verification:
        team_add.add_team(team)
        return team
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# POST: team picture
@teams_insert.post("/teams/upload/{team_id}")
async def team_image(
    team_id: int, image: UploadFile = File(...), Verification: bool = Depends(verify)
):
    if Verification:
        # pngs only
        if image.content_type != "image/png":
            raise HTTPException(status_code=400, detail="Only PNG files are allowed.")
        image.filename = f"{uuid.uuid4()}.png"
        content = await image.read()
        img_path = f"{IMG_DIR}{image.filename}"
        # save
        with open(img_path, "wb") as f:
            f.write(content)
        # save thumbnail
        save_thumbnail(img_path, image.filename)
        # save name to db
        team_add.add_team_picture(image.filename, team_id)

        return {"filename": image.filename}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
