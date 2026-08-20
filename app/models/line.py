"""Модель линии."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.data.database import Base


class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=True)
    
    # Связь со станциями (many-to-many)
    stations = relationship("Station", secondary="station_lines", back_populates="lines")
