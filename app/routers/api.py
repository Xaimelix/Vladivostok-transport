"""
API маршруты
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from data.database import get_db
from data import schemas
from services import station_service, route_service


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/stations", response_model=List[schemas.StationOut])
def get_stations(db: Session = Depends(get_db)):
    """Получить список всех станций"""
    return station_service.get_all_stations(db)


@router.post("/route", response_model=schemas.RouteOut)
def find_route(req: schemas.RouteRequest, db: Session = Depends(get_db)):
    """
    Найти кратчайший маршрут между двумя станциями.
    
    Требуемые параметры:
    - start: название начальной станции
    - end: название конечной станции
    """
    try:
        return route_service.find_shortest_route(db, req.start, req.end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска маршрута: {str(e)}")
