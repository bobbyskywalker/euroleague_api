from fastapi import FastAPI

from routers.player_requests import players_router
from routers.team_requests import teams_router

db_path = "../euroleague.db"

app = FastAPI()

app.include_router(players_router)
app.include_router(teams_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
