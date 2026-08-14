"""
Бизнес-логика для поиска маршрутов
"""
from sqlalchemy.orm import Session
from app.data import models, schemas
from app.modules import path as path_module
from .station_service import get_station_by_name


def build_graph_from_edges(db: Session) -> dict[int, list[tuple[float, int]]]:
    """
    Построить граф станций из рёбер в БД.
    
    Возвращает:
        dict: {station_id: [(weight, neighbor_station_id), ...], ...}
    """
    graph = {}
    edges = db.query(models.Edge).all()
    for e in edges:
        graph.setdefault(e.station_a_id, []).append((e.weight, e.station_b_id))
        graph.setdefault(e.station_b_id, []).append((e.weight, e.station_a_id))
    return graph


def find_shortest_route(
    db: Session, 
    start_name: str, 
    end_name: str
) -> schemas.RouteOut:
    """
    Найти кратчайший маршрут между двумя станциями.
    
    Args:
        db: Сессия БД
        start_name: Название начальной станции
        end_name: Название конечной станции
    
    Returns:
        RouteOut: Объект с маршрутом (список ID станций)
    
    Raises:
        ValueError: Если станция не найдена
    """
    # Получить станции по названиям
    s_start = get_station_by_name(db, start_name)
    s_end = get_station_by_name(db, end_name)
    
    if s_start is None:
        raise ValueError(f"Начальная станция '{start_name}' не найдена")
    if s_end is None:
        raise ValueError(f"Конечная станция '{end_name}' не найдена")
    
    # Построить граф
    graph = build_graph_from_edges(db)
    
    # Проверить, что обе станции в графе
    if s_start.id not in graph:
        raise ValueError(f"Станция '{start_name}' не подключена к сети")
    if s_end.id not in graph:
        raise ValueError(f"Станция '{end_name}' не подключена к сети")
    
    # Найти кратчайший путь методом Dijkstra
    visited = path_module.dijkstra(s_start.id, s_end.id, graph)
    
    # Восстановить маршрут
    route = []
    cur = s_end.id
    while cur is not None:
        route.append(cur)
        cur = visited.get(cur)
    
    route.reverse()
    
    return schemas.RouteOut(route=route, lines=[])
