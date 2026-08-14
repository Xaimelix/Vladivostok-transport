"""Модель линии."""
from sqlalchemy import Column, Integer, String, Text
from app.data.database import Base


class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    points = Column(Text, nullable=True)  # JSON или координаты
