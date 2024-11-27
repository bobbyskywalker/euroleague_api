from fastapi import HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter

from app.view.visualize.heatmap_cmp import heatmap_compare
from app.view.visualize.shot_radar import shot_percentage_radar
from app.view.visualize.leaders import create_ranking

from app.dal.fetch_players import get_ranking

front = APIRouter()

templates = Jinja2Templates(directory="app/view/static")

@front.get("/", response_class=HTMLResponse)
async def read_homepage(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={}
    )

@front.get("/heatmap", response_class=HTMLResponse)
async def heatmap_input(request: Request):
    return templates.TemplateResponse(
        request=request, name="heatmap.html", context={}
    )

@front.post("/heatmap/submit")
async def save_players(
    request: Request,
    player1_first: str = Form(...),
    player1_last: str = Form(...),
    player2_first: str = Form(...),
    player2_last: str = Form(...),
    player3_first: str = Form(...),
    player3_last: str = Form(...),
    season: str = Form(...),
):
    season_value = int(season[0:4])
    img = heatmap_compare(
        [(player1_first.upper(), player1_last.upper()), (player2_first.upper(), player2_last.upper()), (player3_first.upper(), player3_last.upper())],
        season_value
    )
    if not img:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return Response(content=img.getvalue(), media_type="image/png")

@front.get("/leaders", response_class=HTMLResponse)
async def leaders_input(request: Request):
    return templates.TemplateResponse(
        request=request, name="leaders.html", context={}
    )

@front.post("/leaders/submit")
async def save_leaders(
    request: Request,
    stat_type: str = Form(...),
    season: str = Form(...),
):
    season_value = int(season[0:4])
    ranking = get_ranking(stat_type, season_value)
    img = create_ranking(stat_type, ranking)
    if not img:
        raise HTTPException(status_code=404, detail="Player not found")
    return Response(content=img.getvalue(), media_type="image/png")

@front.get("/shooting-chart", response_class=HTMLResponse)
async def chart_input(request: Request):
    return templates.TemplateResponse(
        request=request, name="sh_chart.html", context={}
    )

@front.post("/shooting-chart/submit")
async def save_chart(
    request: Request,
    player_first: str = Form(...),
    player_last: str = Form(...),
    shot_type: str = Form(...),
):
    if shot_type == '3-pointer':
        shot_type = 3
    elif shot_type == '2-pointer':
        shot_type = 2
    elif shot_type == 'free-throw':
        shot_type = 1

    img = shot_percentage_radar([(player_first.upper(), player_last.upper())], shot_type)

    if not img:
        raise HTTPException(status_code=404, detail="Player not found")

    return Response(content=img.getvalue(), media_type="image/png")