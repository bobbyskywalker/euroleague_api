from fastapi import FastAPI, Request, Form
from log.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers.player_routers import players_get, players_insert, players_update, players_delete
from app.routers.team_routers import teams_get, teams_insert, teams_update, teams_delete
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.view.visualize.heatmap_cmp import heatmap_compare

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/view/static"), name="static")

templates = Jinja2Templates(directory="app/view/static")

# frontend controllers, to put somewhere else later
@app.get("/", response_class=HTMLResponse)
async def read_homepage(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={}
    )

@app.get("/heatmap", response_class=HTMLResponse)
async def heatmap_input(request: Request):
    return templates.TemplateResponse(
        request=request, name="heatmap.html", context={}
    )

@app.post("/heatmap/submit")
async def save_players(
    request: Request,
    player1_first: str = Form(...),
    player1_last: str = Form(...),
    player2_first: str = Form(...),
    player2_last: str = Form(...),
    player3_first: str = Form(...),
    player3_last: str = Form(...),
    season: int = Form(...),
):
    heatmap_compare(
        [(player1_first, player1_last), (player2_first, player2_last), (player3_first, player3_last)],
        season
    )
    image_path = 'app/view/visualize/visuals/heatmap.png'

    return templates.TemplateResponse(
        "heatmap.html", 
        {"request": request, "image_path": image_path}
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
