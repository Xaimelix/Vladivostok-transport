"""Модели маршрутов и рёбер."""
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.data.database import Base


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    station_a_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    station_b_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    weight = Column(Float, nullable=False)


class Route:
    """Класс для представления маршрута (не ORM модель)."""

    def __init__(self, stations: list[int], lines: list[str] = None):
        self.stations = stations
        self.lines = lines or []
