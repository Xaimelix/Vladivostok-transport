"""
Бизнес-логика для работы со станциями
"""
from sqlalchemy.orm import Session
from data import models


def get_all_stations(db: Session) -> list[models.Station]:
    """Получить все станции, отсортированные по ID"""
    return db.query(models.Station).order_by(models.Station.id).all()


def get_station_by_name(db: Session, name: str) -> models.Station | None:
    """Получить станцию по названию"""
    return db.query(models.Station).filter(
        models.Station.name == name
    ).first()


def get_station_by_id(db: Session, station_id: int) -> models.Station | None:
    """Получить станцию по ID"""
    return db.query(models.Station).filter(
        models.Station.id == station_id
    ).first()
