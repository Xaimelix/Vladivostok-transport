from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

from app.data.database import init_db
from app.routers.pages import router as pages_router
from app.routers.api import router as api_router


BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


def create_app() -> FastAPI:
    """Создание и настройка приложения FastAPI."""
    app = FastAPI(title="Vladivostok Transport API")

    # Инициализация БД (создание таблиц)
    init_db()

    # Подключение статики
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Подключение роутеров
    app.include_router(pages_router)
    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
