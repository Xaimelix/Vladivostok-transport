from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Line(Base):
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    points = Column(Text)  # опционально храните JSON или координаты

    # relation to stations через association table можно добавить при необходимости

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
    lines = Column(String, nullable=True)  # или relation

class Edge(Base):
    __tablename__ = "edges"
    id = Column(Integer, primary_key=True, index=True)
    station_a_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    station_b_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    weight = Column(Float, nullable=False)
    # Дополнительно можно добавить индекс уникальности для пары (a,b)