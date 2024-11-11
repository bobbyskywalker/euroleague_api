from fastapi import FastAPI, Request
from log.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers.player_routers import players_get, players_insert, players_update, players_delete
from app.routers.team_routers import teams_get, teams_insert, teams_update, teams_delete
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/view/static"), name="static")

templates = Jinja2Templates(directory="app/view/static")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
