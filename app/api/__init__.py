"""API маршруты для транспортного приложения."""
from .stations import router as stations_router
from .routes import router as routes_router
from .lines import router as lines_router

__all__ = ["stations_router", "routes_router", "lines_router"]
