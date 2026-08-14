"""
Бизнес-логика для работы со станциями
"""
from sqlalchemy.orm import Session
from app.models.station import Station


def get_all_stations(db: Session) -> list[Station]:
    """Получить все станции, отсортированные по ID"""
    return db.query(Station).order_by(Station.id).all()


def get_station_by_name(db: Session, name: str) -> Station | None:
    """Получить станцию по названию"""
    return db.query(Station).filter(
        Station.name == name
    ).first()


def get_station_by_id(db: Session, station_id: int) -> Station | None:
    """Получить станцию по ID"""
    return db.query(Station).filter(
        Station.id == station_id
    ).first()
