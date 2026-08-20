"""Модель станции."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.data.database import Base


# Таблица связи многие-ко-многим для станций и линий
station_lines = Table(
    "station_lines",
    Base.metadata,
    Column("station_id", Integer, ForeignKey("stations.id"), primary_key=True),
    Column("line_id", Integer, ForeignKey("lines.id"), primary_key=True),
)


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_transfer = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    svg_id = Column(String, nullable=True)
    
    # Связь с линиями (many-to-many)
    lines = relationship("Line", secondary=station_lines, back_populates="stations")
    
    # Связь с соединениями (как начальная и конечная станция)
    outgoing_connections = relationship(
        "Connection",
        foreign_keys="Connection.from_station_id",
        back_populates="from_station"
    )
    incoming_connections = relationship(
        "Connection",
        foreign_keys="Connection.to_station_id",
        back_populates="to_station"
    )
