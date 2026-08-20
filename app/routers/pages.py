"""
Маршруты для страниц
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Главная страница с картой транспорта"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Карта транспорта Владивостока"
    })
