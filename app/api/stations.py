"""API маршруты для станций."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.data.database import get_db
from app.models.schemas import StationOut
from app.services.transport import get_all_stations, get_station_by_name


router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=List[StationOut])
def list_stations(db: Session = Depends(get_db)):
    """Получить список всех станций"""
    return get_all_stations(db)


@router.get("/{station_name}", response_model=StationOut)
def get_station(station_name: str, db: Session = Depends(get_db)):
    """Получить информацию о станции по названию"""
    station = get_station_by_name(db, station_name)
    if station is None:
        raise HTTPException(status_code=404, detail="Станция не найдена")
    return station
