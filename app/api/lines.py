"""API маршруты для линий."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.data.database import get_db
from app.models.line import Line


router = APIRouter(prefix="/lines", tags=["lines"])


@router.get("", response_model=List[dict])
def list_lines(db: Session = Depends(get_db)):
    """Получить список всех линий"""
    lines = db.query(Line).all()
    return [{"id": line.id, "name": line.name, "points": line.points} for line in lines]
