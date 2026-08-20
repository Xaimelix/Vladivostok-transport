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
from app.models.station import Station, station_lines
from app.models.line import Line
from app.models.route import Connection


def load_json_data() -> dict:
    """Загрузка данных из stations.json."""
    json_path = ROOT_DIR / "app" / "static" / "map" / "stations.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_db(session: Session):
    """Очистка всех таблиц."""
    session.query(Connection).delete()
    # Очищаем ассоциативную таблицу station_lines
    session.execute(station_lines.delete())
    session.query(Station).delete()
    session.query(Line).delete()
    session.commit()
    print("✓ База данных очищена")


def seed_lines(session: Session, lines_data: list) -> dict:
    """Добавление линий. Возвращает мапу {name: Line}."""
    lines_map = {}
    for line_data in lines_data:
        line = Line(
            name=line_data["name"],
            color=line_data.get("color", "")
        )
        session.add(line)
        lines_map[line.name] = line
    session.commit()
    print(f"✓ Добавлено {len(lines_data)} линий")
    return lines_map


def seed_stations(session: Session, stations_data: list, lines_map: dict) -> dict:
    """Добавление станций. Возвращает мапу {name: Station}."""
    stations_map = {}
    
    for station_data in stations_data:
        # Определяем, является ли станция пересадочной
        station_lines_list = station_data.get("lines", [])
        is_transfer = len(station_lines_list) > 1 or station_data.get("transfer_to") is not None
        
        station = Station(
            id=station_data["id"],
            name=station_data["name"],
            is_transfer=is_transfer,
            # Используем x, y как latitude, longitude (в JSON это координаты SVG)
            latitude=station_data.get("y"),
            longitude=station_data.get("x"),
            svg_id=f"station_{station_data['id']}"
        )
        
        # Связываем станции с линиями
        for line_name in station_lines_list:
            if line_name in lines_map:
                station.lines.append(lines_map[line_name])
        
        session.add(station)
        stations_map[station.name] = station
    
    session.commit()
    print(f"✓ Добавлено {len(stations_data)} станций")
    return stations_map


def seed_connections(session: Session, connections_data: list, stations_map: dict, lines_map: dict):
    """Добавление соединений между станциями."""
    edges_count = 0
    
    for conn in connections_data:
        from_station = stations_map.get(conn["from"])
        to_station = stations_map.get(conn["to"])
        
        if from_station and to_station:
            # Определяем линию для соединения
            line_id = None
            from_lines = [l.name for l in from_station.lines]
            to_lines = [l.name for l in to_station.lines]
            common_lines = set(from_lines) & set(to_lines)
            
            if common_lines:
                line_name = list(common_lines)[0]
                line_id = lines_map[line_name].id
            
            # Добавляем соединение
            connection = Connection(
                from_station_id=from_station.id,
                to_station_id=to_station.id,
                line_id=line_id,
                travel_time=conn.get("weight", 1.0)
            )
            session.add(connection)
            edges_count += 1
    
    session.commit()
    print(f"✓ Добавлено {edges_count} соединений")


def verify_graph(stations_map: dict, connections_data: list):
    """Проверка целостности графа."""
    print("\n🔍 Проверка графа...")
    
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
    transfer_stations = [s for s in stations_map.values() if s.is_transfer]
    if transfer_stations:
        print(f"  ✓ Пересадочных узлов: {len(transfer_stations)}")
        for ts in transfer_stations[:5]:
            line_names = ", ".join([l.name for l in ts.lines])
            print(f"    - {ts.name} (линии: {line_names})")


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
        lines_map = seed_lines(db, data["lines"])
        
        # Seed станций
        stations_map = seed_stations(db, data["stations"], lines_map)
        
        # Seed соединений
        seed_connections(db, data["connections"], stations_map, lines_map)
        
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
