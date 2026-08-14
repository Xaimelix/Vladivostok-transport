"""Модель станции."""
from sqlalchemy import Column, Integer, String
from app.data.database import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    time = Column(String, nullable=True)
    transfer = Column(String, nullable=True)
    transfer_to = Column(String, nullable=True)
    lines = Column(String, nullable=True)
