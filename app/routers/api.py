"""
API маршруты (заглушка для демонстрации)
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/stations")
def get_stations():
    """Получить список всех станций - заглушка"""
    return []


@router.post("/route")
def find_route():
    """
    Найти кратчайший маршрут между двумя станциями - заглушка.
    
    Требуемые параметры:
    - start: название начальной станции
    - end: название конечной станции
    """
    return {"message": "Маршрут будет реализован в будущем"}
