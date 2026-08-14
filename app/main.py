from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
from data.database import init_db

from routers.pages import router as pages_router
from routers.api import router as api_router

# Получить абсолютный путь к директории static
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Train-project API")

# Инициализация ORM (create tables если нужно)
init_db()

def create_app() -> FastAPI:
    app = FastAPI(title="Vladivostok Transport API")

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.include_router(pages_router)
    app.include_router(api_router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
