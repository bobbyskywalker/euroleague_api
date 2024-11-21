import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from log.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from db.db_creator.creator import create_database, delete_db
from config.env_loader import get_base_path
from app.routers.player_routers import players_get, players_insert, players_update, players_delete
from app.routers.team_routers import teams_get, teams_insert, teams_update, teams_delete
from app.routers.frontend_handler import front

# cronjob to update database at 2:00 AM
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_db, 'cron', hour=2, minute=0)
    scheduler.add_job(create_database, 'cron', hour=2, minute=5)
    scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(get_base_path()):
        create_database()
        logging.info('Database created')
    start_scheduler()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/view/static"), name="static")

# logging middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

# controllers/routers
app.include_router(players_get)
app.include_router(teams_get)
app.include_router(players_insert)
app.include_router(teams_insert)
app.include_router(players_update)
app.include_router(teams_update)
app.include_router(players_delete)
app.include_router(teams_delete)
app.include_router(front)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
