from fastapi import FastAPI

#TODO: add functional pagination to the search engine

from app.routers.player_routers import players_get, players_insert, players_update, players_delete
from app.routers.team_routers import teams_get, teams_insert, teams_update, teams_delete

app = FastAPI()

app.include_router(players_get)
app.include_router(teams_get)
app.include_router(players_insert)
app.include_router(teams_insert)
app.include_router(players_update)
app.include_router(teams_update)
app.include_router(players_delete)
app.include_router(teams_delete)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
