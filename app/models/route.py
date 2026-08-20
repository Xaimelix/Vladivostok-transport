"""Модели маршрутов и соединений."""
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.data.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    from_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    to_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)
    travel_time = Column(Float, nullable=False)
    
    # Связи со станциями
    from_station = relationship(
        "Station",
        foreign_keys=[from_station_id],
        back_populates="outgoing_connections"
    )
    to_station = relationship(
        "Station",
        foreign_keys=[to_station_id],
        back_populates="incoming_connections"
    )
    
    # Связь с линией
    line = relationship("Line", back_populates="connections")


# Добавляем обратную связь в Line для connections
# Это нужно сделать после импорта Connection
from app.models.line import Line
Line.connections = relationship("Connection", back_populates="line")
