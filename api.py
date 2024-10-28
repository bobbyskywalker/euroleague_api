from fastapi import FastAPI

from app.routers.player_gets import players_get_router
from app.routers.team_gets import teams_router
from app.routers.player_posts import player_insert
from app.routers.team_posts import team_insert

app = FastAPI()

app.include_router(players_get_router)
app.include_router(teams_router)
app.include_router(player_insert)
app.include_router(team_insert)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
