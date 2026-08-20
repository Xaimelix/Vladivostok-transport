#!/usr/bin/env python3
"""Seed скрипт для заполнения БД данными о транспорте."""

import json
import sys
from pathlib import Path

# Добавляем корень проекта в path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy.orm import Session
from app.data.database import engine, Base, SessionLocal
from app.models.station import Station
from app.models.line import Line
from app.models.route import Edge


def load_json_data() -> dict:
    """Загрузка данных из stations.json."""
    json_path = ROOT_DIR / "app" / "static" / "map" / "stations.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_db(session: Session):
    """Очистка всех таблиц."""
    session.query(Edge).delete()
    session.query(Station).delete()
    session.query(Line).delete()
    session.commit()
    print("✓ База данных очищена")


def seed_lines(session: Session, lines_data: list):
    """Добавление линий."""
    for line_data in lines_data:
        line = Line(
            name=line_data["name"],
            color=line_data.get("color", ""),
            points=json.dumps(line_data.get("points", []))
        )
        session.add(line)
    session.commit()
    print(f"✓ Добавлено {len(lines_data)} линий")


def seed_stations(session: Session, stations_data: list):
    """Добавление станций."""
    for station_data in stations_data:
        station = Station(
            id=station_data["id"],
            name=station_data["name"],
            x=station_data.get("x"),
            y=station_data.get("y"),
            lines=",".join(station_data.get("lines", [])),
            transfer_to=station_data.get("transfer_to"),
            status=station_data.get("status", "active"),
            time=station_data.get("time", "0")
        )
        session.add(station)
    session.commit()
    print(f"✓ Добавлено {len(stations_data)} станций")


def seed_connections(session: Session, connections_data: list, stations_map: dict):
    """Добавление соединений между станциями."""
    edges_count = 0
    for conn in connections_data:
        from_station = stations_map.get(conn["from"])
        to_station = stations_map.get(conn["to"])
        
        if from_station and to_station:
            # Добавляем двунаправленное соединение
            edge_ab = Edge(
                station_a_id=from_station.id,
                station_b_id=to_station.id,
                weight=conn.get("weight", 1.0)
            )
            edge_ba = Edge(
                station_a_id=to_station.id,
                station_b_id=from_station.id,
                weight=conn.get("weight", 1.0)
            )
            session.add(edge_ab)
            session.add(edge_ba)
            edges_count += 2
    
    session.commit()
    print(f"✓ Добавлено {edges_count} соединений (рёбер)")


def verify_graph(stations_map: dict, connections_data: list):
    """Проверка целостности графа."""
    print("\n🔍 Проверка графа...")
    
    # Построение adjacency list
    from collections import defaultdict, deque
    
    graph = defaultdict(set)
    for conn in connections_data:
        graph[conn["from"]].add(conn["to"])
        graph[conn["to"]].add(conn["from"])
    
    # Поиск конечных станций (степень 1)
    terminal_stations = [
        name for name, neighbors in graph.items() 
        if len(neighbors) == 1
    ]
    print(f"  Конечные станции: {', '.join(terminal_stations)}")
    
    # Проверка связности через BFS
    if graph:
        start = next(iter(graph.keys()))
        visited = set()
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            queue.extend(graph[node] - visited)
        
        all_stations = set(graph.keys())
        unreachable = all_stations - visited
        
        if unreachable:
            print(f"  ⚠️  Найдены изолированные станции: {unreachable}")
        else:
            print(f"  ✓ Граф связный ({len(visited)} станций в компоненте)")
    
    # Проверка пересадок
    transfer_stations = [
        s for s in stations_map.values() 
        if s.transfer_to
    ]
    if transfer_stations:
        print(f"  ✓ Пересадочных узлов: {len(transfer_stations)}")
        for ts in transfer_stations[:5]:  # Показать первые 5
            print(f"    - {ts.name} ↔ {ts.transfer_to}")


def main():
    """Основная функция seed."""
    print("🚇 Запуск seed транспорта...\n")
    
    # Создание таблиц
    Base.metadata.create_all(bind=engine)
    print("✓ Таблицы созданы/проверены\n")
    
    # Загрузка данных
    data = load_json_data()
    
    # Создание сессии
    db = SessionLocal()
    
    try:
        # Очистка БД
        clear_db(db)
        
        # Seed линий
        seed_lines(db, data["lines"])
        
        # Seed станций
        seed_stations(db, data["stations"])
        
        # Построение мапы станций
        stations_map = {s.name: s for s in db.query(Station).all()}
        
        # Seed соединений
        seed_connections(db, data["connections"], stations_map)
        
        # Верификация
        verify_graph(stations_map, data["connections"])
        
        print("\n✅ Seed завершен успешно!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка при seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
