"""API маршруты для маршрутов."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.data.database import get_db
from app.models.schemas import RouteOut, RouteRequest
from app.services.routing import find_shortest_route


router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/find", response_model=RouteOut)
def find_route(req: RouteRequest, db: Session = Depends(get_db)):
    """
    Найти кратчайший маршрут между двумя станциями.
    
    Требуемые параметры:
    - start: название начальной станции
    - end: название конечной станции
    """
    try:
        return find_shortest_route(db, req.start, req.end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска маршрута: {str(e)}")
