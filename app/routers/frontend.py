from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter

from app.view.visualize.heatmap_cmp import heatmap_compare


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
    season: int = Form(...),
):
    img = heatmap_compare(
        [(player1_first.upper(), player1_last.upper()), (player2_first.upper(), player2_last.upper()), (player3_first.upper(), player3_last.upper())],
        season
    )
    return Response(content=img.getvalue(), media_type="image/png")